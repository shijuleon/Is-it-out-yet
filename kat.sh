#!/usr/bin/env bash
echo "Starting up KAT at `date`" 
filename="/home/shiju/Dev/Python/kat/latest"
while read -r line
do
	name="$line"
	echo "Latest torrents for Silicon Valley $name"
	/home/shiju/Dev/Python/kat/kat.py -s silicon valley | grep $name
	if [ $? -ne 0 ]
		then echo "No torrents found"
	else 
		echo "Torrent(s) found for Silicon Valley $name"
		echo "Getting links"
		/home/shiju/Dev/Python/kat/kat.py -s 'silicon valley' -n 5
	fi
done < "$filename"
