#!nawk -f

#**CFile***********************************************************************
#
# FileName    [ioBlifToMv.nawk]
#
# PackageName [io]
#
# Synopsis    [A nawk script to convert a blif file into a blif-mv file.]
#
# Description [A nawk script to convert a blif file into a blif-mv file.
# The blif file should be free of errors. The script ignores synthesis related
# information.]
#
# SeeAlso     []
#
# Author      [Rajeev K. Ranjan, Yuji Kukimoto]
#
# Copyright   [Copyright (c) 1994-1996 The Regents of the Univ. of California.
# All rights reserved.
#
# Permission is hereby granted, without written agreement and without license
# or royalty fees, to use, copy, modify, and distribute this software and its
# documentation for any purpose, provided that the above copyright notice and
# the following two paragraphs appear in all copies of this software.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT
# OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF
# CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS ON AN
# "AS IS" BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.]
#
#*****************************************************************************/

BEGIN {
	while (my_getline()){
		main()
	}
	print ".end"
}

function main(){
	while (1) {
		if (match($1,"\\.latch|\\.model|\\.inputs|\\.outputs")){
			while (last_char("\\") == 1){
				getline
			}	
			break
		}
		if ($1 == ".names"){
			print
			while (last_char("\\")==1){
				getline
				print
			}	
			if (my_getline() == 0) break
			if (row_of_table()){
				if (last_char("0"))
					print ".def 1"
				else
					print ".def 0"
				while (1){
					gsub("1","1 ")
					gsub("0","0 ")
					gsub("-","- ")
					for(i = 1; i< NF; i++)
						printf("%s ",$i)
					printf("%s",$NF)
					printf("\n")
					if (my_getline() == 0) break
					if (row_of_table()) 
						continue
					else 
						break
				}
				continue
			}
			else {
				print ".def 0"
				continue
			}
		}
	 	if ($1 == ".subckt"){
			fieldCounter = 0;
			do{
				last_char_back_slash = last_char("\\")
				gsub("\\\\","")
				for (i=1; i<=NF; i++){
					fieldArray[fieldCounter] = $i;
					fieldCounter++;
				}
				if (last_char_back_slash) getline
			} while (last_char_back_slash)

			printf("%s %s %d ", fieldArray[0], fieldArray[1], subckt_counter)
			subckt_counter++;
			for (i=2; i<fieldCounter-1; i++){
				printf("%s ", fieldArray[i])
			}
			printf("%s\n", fieldArray[fieldCounter-1]);
		}
       	if ($1 == ".exdc"){ # ignore the rest of the file
       		while (getline){
         	}
           	break
       	}
		while (last_char("\\")==1)
			getline
		break
	}
}

function last_char(char,  linelength, lastchar){
	linelength = length
	lastchar = substr($0, linelength)
	if (lastchar == char)
		return 1
	else
		return 0
}

function first_char(char, firstchar){
	firstchar = substr($1,1,1)
	if (firstchar == char)
		return 1
	else 
		return 0
}

function row_of_table(){
	if (first_char("1") || first_char("0") || first_char("-"))
		return 1
	else 
		return 0
}


function my_getline(){
	while (getline){
		if ((NF == 0) || first_char("#"))
			continue
		return 1
	}
	return 0
}
