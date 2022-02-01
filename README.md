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
