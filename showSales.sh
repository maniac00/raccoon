#!/bin/bash

sudo ps -ef | grep rpi | awk '{print $2}' | xargs kill -15
result=$(python3 /root/raccoon/getSales.py)
sudo /root/rpi-rgb-led-matrix/utils/text-scroller -f /root/raccoon/Arial.bdf -C255,255,255 -s0 -x3 -y13 --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-brightness=70 "$result"

