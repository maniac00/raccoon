#!/bin/bash

sudo ps -ef | grep rpi | awk '{print $2}' | xargs kill -15

