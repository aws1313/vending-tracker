#!/bin/bash
log=/home/temp_log.txt

temp_target_hi=60000 # turn on at this temperature
temp_target_lo=47000 # turn off at this temperature

gpio_control_pin=12 ## 14 is serial, so we use a more general GPIO 23 (pinout.xyz)

temp_current=$(cat /sys/class/thermal/thermal_zone0/temp)

## Can't read the value directly, because it toggles the state so we skip this
#fan_on=$(gpioget gpiochip0 $gpio_control_pin) # 0 - off, 1 - on

#echo -n "$(date) : [fan-state=$fan_state,$temp_target_lo < $temp_current < $temp_target_hi] " >> $log
echo -n "$(date) : [$temp_target_lo < $temp_current < $temp_target_hi] " >> $log

if [ $temp_current -gt $temp_target_hi ]; then
#if [ $fan_state != 1 ]; then
echo -n ": fan on" >> $log
#fi
gpioset gpiochip0 $gpio_control_pin=1

elif [ $temp_current -lt $temp_target_lo ]; then
#if [ $fan_state != 0 ]; then
echo -n ": fan off" >> $log
#fi
gpioset gpiochip0 $gpio_control_pin=0
else
echo -n ": maintain fan state" >> $log
fi

echo "" >> $log