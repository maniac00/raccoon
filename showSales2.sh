#!/bin/bash
sleep 3
sudo /root/rpi-rgb-led-matrix/utils/text-scroller -f /root/raccoon/BMJUA.bdf -C255,255,153 -s0 -x3 --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-brightness=50 "65만원"

