#! /bin/bash

while true; do
	python3 bot.py &>> log.log
	echo "\nbot stopped working at: `date`\n" >> log.log
done &
