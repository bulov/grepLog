# grepLog

git clone -b main https://github.com/bulov/grepLog
cd grepLog
./grepLog -i   # install

if need for test Create
./grepLog -u   # add user backend and worker-tasks.service

./grepLog -t   # write ERROR in LogFile
sudo systemctl status backend@worker-tasks.service

result after 5min

sudo systemctl status grepLog.service

TEST
sudo systemctl restart backend@worker-tasks.service

cat /var/log/grepLog.log
Ср 02 фев 2022 01:20:27 MSK restart <<< worker-tasks >>>

./grepLog -t
cat /var/log/grepLog.log
Ср 02 фев 2022 01:20:27 MSK restart <<< worker-tasks >>>
Dec 27 00:01:30 ip-10-0-5-224 worker-tasks: [2019-12-27 00:01:30,710: ERROR/MainProcess] Error in timer: TimeoutError('Timeout reading from socket',)\nTraceback (most recent call last):\n

�� grepLog.service - grepLog
     Loaded: loaded (/etc/systemd/system/grepLog.service; enabled; vendor preset: disabled)
     Active: inactive (dead) since Wed 2022-02-02 01:25:54 MSK; 33s ago
TriggeredBy: �� grepLog.timer
    Process: 1395870 ExecStart=/usr/local/bin/grepLog (code=exited, status=0/SUCCESS)
	CPU: 161ms

фев 02 01:25:50 kvmHome.bvg.msk.ru systemd[1]: Starting grepLog...
фев 02 01:25:50 kvmHome.bvg.msk.ru sudo[1395904]:  backend : PWD=/tmp ; USER=root ; COMMAND=/usr/bin/mv /var/log/grepLog.log /var/log/grepLog.log.2022-02-02_01:25:50
фев 02 01:25:53 kvmHome.bvg.msk.ru sudo[1396170]:  backend : PWD=/tmp ; USER=root ; COMMAND=/usr/bin/systemctl restart backend@worker-tasks.service
фев 02 01:25:54 kvmHome.bvg.msk.ru systemd[1]: grepLog.service: Deactivated successfully.
фев 02 01:25:54 kvmHome.bvg.msk.ru systemd[1]: Started grepLog.


cat /var/log/grepLog.log
Ср 02 фев 2022 01:25:54 MSK restart <<< worker-tasks >>>
