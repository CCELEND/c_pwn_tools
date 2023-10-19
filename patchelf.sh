#!/bin/bash

#判断libcbase目录是否存在，不存在就新建
ls -d ~/libcbase > /dev/null 2>&1
if [ $? -eq 0 ]; then
	echo -e "\033[32m\033[1m[+] The libcbase directory exists.(~/libcbase)\033[0m"
else
	mkdir ~/libcbase
fi

#判断glibc-all-in-one目录是否存在，不存在就拉取git
ls -d ~/libcbase/glibc-all-in-one > /dev/null 2>&1
if [ $? -eq 0 ]; then
	echo -e "\033[32m\033[1m[+] The glibc-all-in-one directory exists.(~/libcbase/glibc-all-in-one)\033[0m"
else
	git clone https://github.com/matrix1001/glibc-all-in-one.git ~/libcbase/glibc-all-in-one
fi

function patch_arch()
{
	num=`ls $patchlibs | grep $1 | wc -l`
	echo -e "\033[32m\033[1m[+] There are ${num} candidates for patch.\033[0m"
	echo -e "\033[32m\033[1m----------------------------------------\033[0m"
	for (( i=1;i<=$num;i=i+1))
	do 
	declare -A libs
	libs[$i]=`ls $patchlibs | grep $1 | tail -n +$i | head -n 1`
	echo -e "\033[32m\033[1m${i}\033[0m		\033[31m\033[1m${libs[$i]}\033[0m"
	done
	echo -e "\033[32m\033[1m----------------------------------------\033[0m"
	echo -n -e "\033[34m\033[1m[*] Select the glibc to patch >> \033[0m"
	read Select

	expr $Select + 1 &>/dev/null
	if [ $? -eq 0 ]; then
		if [ $Select -ge 1 ] && [ $Select -le $num ]; then
			patchelf --set-interpreter $patchlibs/${libs[$Select]}/$2 ./$filename
			patchelf --replace-needed libc.so.6 $patchlibs/${libs[$Select]}/libc.so.6 ./$filename
			echo -e "\033[32m\033[1m[+] Successful patch.\033[0m"
			ldd ./$filename
			echo -e "\033[32m\033[1m----------------------------------------\033[0m"
		else
			echo -e "\033[31m\033[1m[-] Out of range.\033[0m"
		fi
	else
		echo -e "\033[31m\033[1m[-] Not a positive integer.\033[0m"
	fi
}

#判断glibc-all-in-one/libs目录是否存在，不存在就退出
ls -d ~/libcbase/glibc-all-in-one/libs > /dev/null 2>&1
if [ $? -eq 0 ]; then
	echo -e "\033[32m\033[1m[+] The libs directory exists.(~/libcbase/glibc-all-in-one/libs)\033[0m"
	patchlibs=~/libcbase/glibc-all-in-one/libs
	echo -n -e "\033[34m\033[1m[*] Enter file name: \033[0m"
	read filename

	if [ -f $filename ];then
		cp $filename ./$filename.old
		readelf -h $filename | grep 'ELF64' > /dev/null 2>&1
		if [ $? -eq 0 ]; then
			patch_arch amd64 ld-linux-x86-64.so.2
		else
			patch_arch i386 ld-linux.so.2
		fi

	else
		echo -e "\033[31m\033[1m[-] $filename: No such file.\033[0m"
	fi

else
	echo -e "\033[33m\033[1m[!] Please download glibc.\033[0m"
fi
