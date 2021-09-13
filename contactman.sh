#!/bin/sh

name=$(echo -e "`cat ~/.rolo/contacts.vcf |
	grep '^FN:' |
	sed -r 's/^FN://g' |
	sed -r 's/[^a-zA-Z0-9]*$//g'`" |
	dmenu)

category=$(cat ~/.rolo/contacts.vcf |
	tr '\r\n' '§' |
	grep -oP "BEGIN:VCARD.*$name.*?END:VCARD" |
	grep -oP 'BEGIN:VCARD.*?END:VCARD' |
	tail -1 |
	grep -oP '§.*?:' |
	tr -d '§:'|
	grep -v 'END' |
	grep -v 'VERSION' |
	dmenu)

val=$(cat ~/.rolo/contacts.vcf | 
	tr '\r\n' '§' |
	grep -oP "BEGIN:VCARD.*$name.*?END:VCARD" |
	grep -oP 'BEGIN:VCARD.*?END:VCARD' |
	tail -1 |
	grep -oP "§$category:.*?§" |
	tr -d '§' |
	sed "s|$category:||g"
	)

echo "$val"
notify-send --urgency low "contactman" "$val"
echo "$val" | xclip -sel clip
echo "$val" | xclip -sel primary
echo "$val" | xclip -sel secondary
