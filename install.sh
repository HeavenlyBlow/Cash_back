#!/bin/bash

cp /root/cashback /usr
sudo apt-get update
sudo apt-get install python3
sudo apt-get install pip3
sudo apt-get install screen
sudo pip3 install --upgrade pip
sudo pip3 install CherryPy
sudo pip3 install pyTelegramBotAPI
sudo apt-get install openssl
cd /usr/cashback
openssl genrsa -out webhook_pke.pem 2048
openssl req -new -x509 -days 3650 -key webhook_pke.pem -out webhook_cer.pem
sudo add-apt-repository ppa:nilarimogard/webupd8
sudo apt-get update
sudo apt-get install grive
cd /usr/cashback/Sync
grive -a 
grive
cd /usr/cashback
cp -f start.sh /root
cp -f stop.sh /root
rm /usr/cashback/start.sh
rm /usr/cashback/stop.sh
cd /root
chmod +x start.sh
chmod +x stop.sh
sudo python3 start.sh