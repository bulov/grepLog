#!/usr/bin/python
import os ,sys

DEST='/usr/local/bin'
Prog=os.path.basename(sys.argv[0])
Job='worker-tasks'
LogName=Job
LogFile=os.environ.get('LogFile',f"""/var/log/{LogName}.log""")
StrSearch=os.environ.get('StrSearch',"ERROR/MainProcess")
Timer='5min'
#for test
User='backend'
User='admin'
########################################################################
def help():
   Usage=f"""
    Usage: {Prog} [-h] [-i ] [ -l /var/log/grepLog ] [ -s ERROR/MainProcess ] [ -c ./grepLog.cfg ]
      -h|--help      - help
      -l|--LogFile   - log file
      -s|--StrSearch - string search
      -i|--install   - install in /usr/local/bin /etc/systemd/system
      -c - config file
      -d - delete and disable
    Example
      {Prog} --LogFile /tmp/grepLog --StrSearch \"ERROR xxx\"
   """
   print(Usage)
   exit(0)
######################################################################
def install():
#   os.system(f'sudo cp {Prog} {DEST}')
#   os.system(f'sudo chmod +x {DEST}/{Prog}')

   file1=f"""
[Unit]
Description={Prog}
After=syslog.target
[Service]
Type=forking
WorkingDirectory=/tmp
User={User}
Group=wheel
Environment=LogFile={LogFile}
Environment=StrSearch="{StrSearch}"
ExecStart={DEST}/{Prog}
[Install]
WantedBy=multi-user.target
WantedBy=timers.target
"""
   file2=f"""
[Timer]
OnBootSec=1min
OnUnitActiveSec={Timer}
"""
   ProgServ=Prog.removesuffix('.py')
   with open(f"/tmp/{ProgServ}.service","w") as f:
     f.write(file1)
     f.close()
   os.system(f'sudo mv /tmp/{ProgServ}.service /etc/systemd/system/{ProgServ}.service')
   with open(f"/tmp/{ProgServ}.timer","w") as f:
       f.write(file2)
       f.close()
   os.system(f'sudo mv /tmp/{ProgServ}.timer   /etc/systemd/system/{ProgServ}.timer'  )
   os.system(f'sudo systemctl daemon-reload')
   os.system(f'sudo systemctl enable {ProgServ}.service')
   os.system(f'sudo systemctl start  {ProgServ}.service')
   os.system(f'sudo systemctl start  {ProgServ}.timer'  )
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
   os.system(f"""sudo bash -c 'echo $(date) ===restart {Job}=== >> {LogFile}'""")
######################################################################
#
# main
#
for i ,arg in enumerate(sys.argv[1:]):
   print(i ,arg)
   match arg:
       case "-h"|"--help":         help()
       case "-i"|"--install":      install()
       case "-l"|"--Logfile":      LogFile=sys.argv[i+2]
       case "-s"|"--StrSearch":    StrSearch=sys.argv[i+2]
       case "-c":                  ConfigFile=sys.argv[i+2]
       case "-d":                  delete()
       case "-t":                  testCreateLogFile()
       case "-u":                  testCreateUserAndJob()
       case "-j":                  testRestartJob()

