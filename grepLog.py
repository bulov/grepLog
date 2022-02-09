#!/usr/bin/python
import os ,sys
DEST='/usr/local/bin'
Help=0
Prog=os.path.basename(sys.argv[0])
ProgServ=Prog.removesuffix('.py')
Job='worker-tasks'
LogName=Job
LogFile=os.environ.get('LogFile',f"""/var/log/{LogName}.log""")
StrSearch=os.environ.get('StrSearch',"ERROR/MainProcess")
Timer='5min'
User='backend'
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
      systemctl status {User}@{Job}.service
      systemctl status {User}@{ProgServ}.service
      python -m trace -t {Prog} -i
   """
   print(Usage)
######################################################################
def install():
   global Help ; Help=1
   file1=f"""
[Unit]
Description={User}@{Prog}
After=syslog.target
[Service]
Type=forking
WorkingDirectory=/tmp
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
   os.system(f'sudo cp {Prog} {DEST}')
   os.system(f'sudo chmod +x {DEST}/{Prog}')
   with open(f"/tmp/{ProgServ}.service","w") as f:
     f.write(file1)
     f.close()
   os.system(f'sudo mv /tmp/{ProgServ}.service /etc/systemd/system/{User}@{ProgServ}.service')
   with open(f"/tmp/{ProgServ}.timer","w") as f:
       f.write(file2)
       f.close()
   os.system(f'sudo mv /tmp/{ProgServ}.timer   /etc/systemd/system/{User}@{ProgServ}.timer'  )
   os.system(f'sudo systemctl daemon-reload')
   os.system(f'sudo systemctl enable {User}@{ProgServ}.service')
   os.system(f'sudo systemctl start  {User}@{ProgServ}.service')
   os.system(f'sudo systemctl start  {User}@{ProgServ}.timer'  )
######################################################################
def testCreateLogFile():
   logFileAdd=f"""Dec 27 00:01:30 ip-10-0-5-224 worker-tasks: [2019-12-27 00:01:30,710: ERROR/MainProcess] Error in timer: TimeoutError('Timeout reading from socket',)\nTraceback (most recent call last):\n
"""
   with open(f"/tmp/LogFile","w") as f:
     f.write(logFileAdd)
     f.close()
   os.system(f"sudo bash -c 'cat /tmp/LogFile >>{LogFile}'")
#######################################################################
def testCreateUserAndJob():
   file4=f"""
[Unit]
Description={Job}
After=syslog.target
[Service]
Type=forking
#WorkingDirectory=/tmp
User={User}
Group=wheel
ExecStart=/usr/local/bin/{Prog} -j
[Install]
WantedBy=multi-user.target
"""
   os.system(f"sudo adduser {User}")
   os.system(f"sudo usermod -aG wheel  {User}")
   os.system(f"""sudo bash -c 'echo \"{User} ALL=(ALL)  NOPASSWD: ALL\"  > /etc/sudoers.d/{User}'""")
   os.system(f"""sudo bash -c 'echo "{file4}" >/etc/systemd/system/{User}@{Job}.service'""")
   os.system(f'sudo systemctl daemon-reload')
   os.system(f'sudo systemctl enable {User}@{Job}.service')
   os.system(f'sudo systemctl start  {User}@{Job}.service')
######################################################################
def testRestartJob():
   global Help ; Help=1
   os.system(f"""sudo bash -c 'echo $(date) ===restart {Job}=== >> {LogFile}'""")
######################################################################
def lf(LogFile):
   if os.path.isfile(LogFile):
       return (LogFile)
   print(f"No {LogFile=}")
   exit(-1)
######################################################################
def grepLog():
   cmd=f'grep "{StrSearch}" {LogFile}'+" | awk -F: '{print $3 }' | awk -F' ' '{print $3 }'"
   job=os.popen(cmd).read().strip()
   if '' != job:
       os.system(f"sudo mv {LogFile} {LogFile}.$(date +%Y-%m-%d_%H:%M:%S)")
       os.system(f"sudo systemctl restart {User}@{job}.service")
######################################################################
#
# main
#
args=sys.argv[1:]
while args:
   argv=args[0] ; args.pop(0) #; print(argv)
   match argv:
       case "-g"|"--grepLog":      grepLog()               ; exit(0)
       case "-h"|"--help":         help()                  ; exit(0)
       case "-i"|"--install":      install()
       case "-l"|"--Logfile":      LogFile=lf(args[0])     ; args.pop(0)
       case "-s"|"--StrSearch":    StrSearch=args[0]       ; args.pop(0)
       case "-c":                  ConfigFile=args[0]      ; args.pop(0)
       case "-t":                  testCreateLogFile()     ; exit(0)
       case "-u":                  testCreateUserAndJob()
       case "-j":                  testRestartJob()
       case "-d":                  delete()
       case    _:                  print(f"usage -h for help ; Do not know {argv=}")
if 0 == Help:
   help()

#./grepLog.py --install -u -t
