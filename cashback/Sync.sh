#!/bin/bash

cd /usr/cashback
cp -f Message_1.db Sync
cd Sync
cp -f Recent/Message_1.db Old
cp -f New/Message_1.db Recent
cp -f Message_1.db New
rm /usr/cashback/Sync/Message_1.db
grive