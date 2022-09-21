#!/bin/bash


#cd songs_txt_Queen/
cd songs_txt_The-Rolling-Stones

rename 's/\[/_/' *\[*.txt
rename 's/\]/_/'g *\]*.txt
rename 's/__/_/'g *__*.txt
rename 's/\(/_/'g *\(*.txt
rename -f 's/\)/_/'g *\)*.txt
rename -f  "s/\'//" *\'*.txt
rename -f  "s/^_//" _*.txt

