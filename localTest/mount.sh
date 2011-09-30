#!/bin/bash
let i=0
while [ $i -lt '1000' ]
do
	let temp=i+1
	echo liyong$i > name.txt
	echo liyonh$temp >> name.txt
	python test.py < name.txt >> person.txt
	let i=i+1
done
