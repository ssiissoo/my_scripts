#!/bin/sh

screenie_folder="$HOME/screenshot"
opt=`echo -e "entire screen\nselect\nselect and copy\nselect and ocr" | dmenu -p "screenie"`
case "$opt" in
	"entire screen")
		scrot $screenie_folder/$(date +'\%Y-\%m-\%d_\%H_\%M_\%S').png &&
		notify-send -u low "screenie" "took screenshot of entire screen"
		;;
	"select")
		scrot --select $screenie_folder/$(date +'\%Y-\%m-\%d_\%H_\%M_\%S').png &&
		notify-send -u low "screenie" "took screenshot of selection"
		;;
	"select and copy")
		scrot --select $screenie_folder/$(date +'\%Y-\%m-\%d_\%H_\%M_\%S').png &&
		xclip -sel clip -t image/png $screenie_folder/`ls /home/s/screenshot | tail -n 1` &&
		xclip -sel primary -t image/png $screenie_folder/`ls /home/s/screenshot | tail -n 1` &&
		xclip -sel secondary -t image/png $screenie_folder/`ls /home/s/screenshot | tail -n 1` &&
		notify-send -u low "screenie" "took screenshot of selection and copied it"
		;;
	"select and ocr")
		lang=`tesseract --list-langs | tail -n +2 | dmenu -p "select ocr language"`
		scrot --select $screenie_folder/$(date +'\%Y-\%m-\%d_\%H_\%M_\%S').png &&
		notify-send -u low "screenie" "starting OCR" &&
		sleep 1 &&
		echo "$(tesseract -l $lang $screenie_folder/`ls $screenie_folder | tail -n 1` -)" | xclip -sel clip &&
		xclip -o -sel clip | xclip -sel primary &&
		xclip -o -sel clip | xclip -sel secondary &&
		notify-send -u low "screenie" "done"
		;;
esac
