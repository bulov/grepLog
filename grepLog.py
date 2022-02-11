#!/usr/bin/python
import os ,sys ,re
from datetime import datetime
DEST='/usr/local/bin'
Prog=os.path.basename(sys.argv[0])
ProgServ=Prog.removesuffix('.py')
Job='worker-tasks'
LogName=Job
StrSearch=os.environ.get('StrSearch',"ERROR/MainProcess")
LogFile=os.environ.get('LogFile',f"""/var/log/{LogName}.log""")
Timer='5min'
User='backend'
Help=0
########################################################################
def help():
   Usage=f"""
   Usage: {Prog} [-h] [-i ] [ -l {LogFile} ] [ -s ERROR/MainProcess ] [ -c ./grepLog.cfg ]
      -h|--help      - help
      -l|--LogFile   - log file
      -s|--StrSearch - string search
      -i|--install   - install in /usr/local/bin /etc/systemd/system
      -c - config file
      -d - delete and disable
   Example
       {Prog} --LogFile {LogFile} --StrSearch \"ERROR xxx\"
   Install for test
       sudo ./{Prog} --install --testCrUserAndJob
   Display result
       sudo systemctl status {User}@{ProgServ}.service
       sudo systemctl status {User}@{Job}.service
       python -m trace -t {Prog} -i
   """
   print(Usage)
######################################################################
def grepF(str,file):
   if os.path.isfile(file):
       with open(file,"r") as f:
           for line in f.readlines():
               if re.search(str, line):
                   return (line)
   return('')
######################################################################
def wrF(str,file,mode="a"):
   if "r" == mode:
       if true != os.path.isfile(file):
           print (f'File Not Found {file=}')
           return
   with open(file,mode) as f:
       f.write(str)
       f.close()
######################################################################
def install():
   global Help ; Help=1
   file1=f"""
[Unit]
Description={User}@{Prog}
After=syslog.target
[Service]
Type=forking
#WorkingDirectory=/tmp
User={User}
Group=wheel
Environment=LogFile={LogFile}
Environment=StrSearch="{StrSearch}"

ExecStart={DEST}/{Prog} --grepLog
[Install]
WantedBy=multi-user.target
WantedBy=timers.target
"""
   file2=f"""
[Timer]
OnBootSec=1min
OnUnitActiveSec={Timer}
"""
   os.system(f'cp {Prog} {DEST}')
   os.system(f'chmod +x {DEST}/{Prog}')
   wrF(file1,f'/etc/systemd/system/{User}@{ProgServ}.service','w')
   wrF(file2,f'/etc/systemd/system/{User}@{ProgServ}.timer'  ,'w')
   os.system(f'systemctl daemon-reload')
   os.system(f'systemctl enable {User}@{ProgServ}.service')
   os.system(f'systemctl start  {User}@{ProgServ}.service')
   os.system(f'systemctl start  {User}@{ProgServ}.timer'  )
######################################################################
def testRotateLogFile():
   logFileAdd=f"""Dec 27 00:01:30 ip-10-0-5-224 worker-tasks: [2019-12-27 00:01:30,710: ERROR/MainProcess] Error in timer: TimeoutError('Timeout reading from socket',)\nTraceback (most recent call last):\n
"""
   wrF(logFileAdd,LogFile,"a")
######################################################################
def testRestartJob():
   wrF(f'{datetime.now().isoformat(timespec="seconds")} ===restart {Job}===\n',LogFile,'a+')
#######################################################################
def testCrUserAndJob():
   file4=f"""
[Unit]
Description={Job}
After=syslog.target
[Service]
Type=forking
#WorkingDirectory=/tmp
User={User}
Group=wheel
ExecStart=sudo /usr/local/bin/{Prog} --testRestartJob
[Install]
WantedBy=multi-user.target
"""
   if '' == grepF(User,"/etc/passwd"):
       os.system(f"adduser {User}")
   if '' == grepF(f'wheel.*backend.*',"/etc/group"):
       os.system(f"usermod -aG wheel {User}")
   if '' == grepF(f'{User}.*{Prog}.*', f"/etc/sudoers.d/{User}"):
       wrF(f"{User} ALL=(ALL)  NOPASSWD: {DEST}/{Prog}\n",f"/etc/sudoers.d/{User}")
   wrF(file4,f"/etc/systemd/system/{User}@{Job}.service","w")
   os.system(f'systemctl daemon-reload')
   os.system(f'systemctl enable {User}@{Job}.service')
   os.system(f'systemctl start  {User}@{Job}.service')
   testRestartJob()
######################################################################
def lf(LogFile):
   if os.path.isfile(LogFile):
       return (LogFile)
   print(f"No {LogFile=}")
   exit(-1)
######################################################################
def grepLog():
#   cmd=f'grep "{StrSearch}" {LogFile}'+" | awk -F: '{print $3 }' | awk -F' ' '{print $3 }'"
   cmd=f'grep "{StrSearch}" {LogFile}'
   str=os.popen(cmd).read().strip()
   if '' != str:
       str=str.split(': ')
       job=str[0].split(' ')[4]
       if '' != job:
           os.system(f"mv {LogFile} {LogFile}.$(date +%Y-%m-%d_%H:%M:%S)")
           os.system(f"systemctl restart {User}@{job}.service")
######################################################################
if '__main__' == __name__:
   args=sys.argv[1:]
   while args:
      argv=args[0] ; args.pop(0) #; print(argv)
      match argv:
          case "-g"|"--grepLog":           grepLog()               ; exit(0)
          case "-h"|"--help":              help()                  ; exit(0)
          case "-i"|"--install":           install()
          case "-l"|"--Logfile":           LogFile=lf(args[0])     ; args.pop(0)
          case "-s"|"--StrSearch":         StrSearch=args[0]       ; args.pop(0)
          case "-c":                       ConfigFile=args[0]      ; args.pop(0)
          case "-t"|"--testRotateLogFile": testRotateLogFile()     ; exit(0)
          case "-u"|"--testCrUserAndJob":  testCrUserAndJob()      ; exit(0)
          case "-j"|"--testRestartJob":    testRestartJob()        ; exit(0)
          case "-d":                       delete()
          case    _: print(f"usage -h for help ; Do not know {argv=}")
   if 0 == Help:
      help()
