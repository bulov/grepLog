# grepLog

git clone -b main https://github.com/bulov/grepLog
cd grepLog
./grepLog -i   # install

if need for test Create
./grepLog -u   # add user backend and worker-tasks.service
./grepLog -t   # Create LogFile add user backend
sudo systemctl status grepLog.service

result

sudo systemctl status grepLog.service

�� grepLog.service - grepLog
     Loaded: loaded (/etc/systemd/system/grepLog.service; enabled; vendor preset: disabled)
     Active: inactive (dead) since Tue 2022-02-01 17:16:40 MSK; 58s ago
TriggeredBy: �� grepLog.timer
    Process: 1360528 ExecStart=/usr/local/bin/grepLog (code=exited, status=0/SUCCESS)
	CPU: 178ms

фев 01 17:16:37 kvmHome.bvg.msk.ru systemd[1]: Starting grepLog...
фев 01 17:16:37 kvmHome.bvg.msk.ru sudo[1360540]:  backend : PWD=/tmp ; USER=root ; COMMAND=/usr/bin/mv /var/log/grepLog.log /var/log/grepLog.log.2022-02-01_17:16:37
фев 01 17:16:40 kvmHome.bvg.msk.ru sudo[1360593]:  backend : PWD=/tmp ; USER=root ; COMMAND=/usr/bin/systemctl restart backend@worker-tasks.service
фев 01 17:16:40 kvmHome.bvg.msk.ru systemd[1]: grepLog.service: Deactivated successfully.
фев 01 17:16:40 kvmHome.bvg.msk.ru systemd[1]: Started grepLog.
