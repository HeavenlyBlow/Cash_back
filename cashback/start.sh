#!/bin/bash

cd /usr/cashback
screen -S server python3 Bot.py
screen -S sync python3 Sync.py
