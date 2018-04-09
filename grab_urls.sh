#!/bin/bash

END=465

url="https://www.traceinternational2.org/compendium/view.asp?id="

for (( i = 1; i <= END; i++ )); do
	content="$(curl -s "$url$i" | w3m -dump -T text)"
	echo "$content" >> files/id$i.txt
done