#!/bin/bash

echo -e "\033[36m\033[1mlocal GNU C Library=========================================\033[0m"
strings /lib/x86_64-linux-gnu/libc.so.6 | grep "GNU C Library"
echo -e "\033[36m\033[1m============================================================\033[0m"

read -p "Enter file name: " filename
read -p "Enter libc name: " libcname

if [ -f $filename ];then

	echo -e "\033[32m\033[1mchecksec====================================================\033[0m"
	checksec $filename

	echo -e "\033[32m\033[1msandbox check===============================================\033[0m"
	objdump -d -j .plt.sec $filename > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		objdump -d -j .plt.sec $filename | grep prctl > /dev/null 2>&1
		if [ $? -eq 0 ]; then
			seccomp-tools dump ./$filename
		fi
	else
		objdump -d -j .plt $filename | grep prctl > /dev/null 2>&1
		if [ $? -eq 0 ]; then
			seccomp-tools dump ./$filename
		fi
	fi
	echo -e "\033[32m\033[1m============================================================\033[0m"

	echo -e "\033[34mfile gadget:\033[0m"
	echo -e "\033[32m\033[1mleave|ret===================================================\033[0m"
	ROPgadget --binary $filename --only "leave|ret" | grep ": leave ; ret$"

	echo -e "\033[32m\033[1mmov|pop|ret|xor|xchg========================================\033[0m"
	ROPgadget --binary $filename --depth 20 --only "pop|ret|xor|xchg" | grep "ret$"

	echo -e "\033[32m\033[1mmov rdx,r14;mov rsi,r13;mov edi,r12d;call [r15+rbx*8]=======\033[0m"
	ROPgadget --binary $filename --opcode 4c89f2 | tail -n +3 | head -n 1

	echo -e "\033[32m\033[1mmov rdx,r15;mov rsi,r14;mov edi,r13d;call [r12+rbx*8]=======\033[0m"
	ROPgadget --binary $filename --opcode 4c89fa | tail -n +3 | head -n 1

	echo -e "\033[32m\033[1madd DWORD PTR [rbp-0x3d],ebx(magic_gadget)==================\033[0m"
	ROPgadget --binary $filename --opcode 015dc3 | tail -n +3 | head -n 1

	echo -e "\033[32m\033[1msyscall_ret=================================================\033[0m"
	ropper -f $filename --search "syscall; ret;"

	echo -e "\033[32m\033[1m_start======================================================\033[0m"
	objdump -d -j .text $filename | grep "<_start>:"
	echo -e "\033[32m\033[1mmain========================================================\033[0m"
	objdump -d -j .text $filename | grep "<main>:"

	echo -e "\033[32m\033[1msystem======================================================\033[0m"
	objdump -d -j .text $filename | grep "<system>:"

	echo -e "\033[32m\033[1m/bin/sh=====================================================\033[0m"
	ROPgadget --binary $filename --string "/bin/sh" | tail -n +3 | head -n 1

	objdump -d -j .plt.sec $filename > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		echo -e "\033[32m\033[1msystem_plt==================================================\033[0m"
		objdump -d -j .plt.sec $filename | grep system

		echo -e "\033[32m\033[1mfree_plt====================================================\033[0m"
		objdump -d -j .plt.sec $filename | grep free

		echo -e "\033[32m\033[1mputs_plt====================================================\033[0m"
		objdump -d -j .plt.sec $filename | grep puts
	
		echo -e "\033[32m\033[1mgets_plt====================================================\033[0m"
		objdump -d -j .plt.sec $filename | grep gets

		echo -e "\033[32m\033[1mread_plt====================================================\033[0m"
		objdump -d -j .plt.sec $filename | grep read
	else
		echo -e "\033[32m\033[1msystem_plt==================================================\033[0m"
		objdump -d -j .plt $filename | grep system

		echo -e "\033[32m\033[1mfree_plt====================================================\033[0m"
		objdump -d -j .plt $filename | grep free

		echo -e "\033[32m\033[1mputs_plt====================================================\033[0m"
		objdump -d -j .plt $filename | grep puts

		echo -e "\033[32m\033[1mgets_plt====================================================\033[0m"
		objdump -d -j .plt $filename | grep gets

		echo -e "\033[32m\033[1mread_plt====================================================\033[0m"
		objdump -d -j .plt $filename | grep read
	fi

	ldd $filename > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		echo -e "\033[32m\033[1msystem_got==================================================\033[0m"
		objdump -R $filename | grep system

		echo -e "\033[32m\033[1mfree_got====================================================\033[0m"
		objdump -R $filename | grep free

		echo -e "\033[32m\033[1mputs_got====================================================\033[0m"
		objdump -R $filename | grep puts
	
		echo -e "\033[32m\033[1mgets_got====================================================\033[0m"
		objdump -R $filename | grep gets

		echo -e "\033[32m\033[1mread_got====================================================\033[0m"
		objdump -R $filename | grep read
	else
		:
	fi

	echo -e "\033[32m\033[1mstdin=======================================================\033[0m"
	readelf --symbols $filename | grep "stdin" | head -n 1
	echo -e "\033[32m\033[1mstdout======================================================\033[0m"
	readelf --symbols $filename | grep "stdout"
	echo -e "\033[32m\033[1mstderr======================================================\033[0m"
	readelf --symbols $filename | grep "stderr"
	echo -e "\033[32m\033[1m============================================================\033[0m"

else
	echo -e "\033[31m\033[1m[-] $filename: No such file.\033[0m"
fi

if [ -f $libcname ];then

	echo -e "\033[35mlibc gadget:\033[0m"
	echo -e "\033[36m\033[1mGNU C Library===============================================\033[0m"
	strings ./$libcname | grep "GNU C Library"
	
	echo -e "\033[36m\033[1mone_gadget==================================================\033[0m"
	one_gadget $libcname

	echo -e "\033[36m\033[1mpop rax=====================================================\033[0m"
	ROPgadget --binary $libcname --only "pop|ret" | grep "rax" | grep "ret$"

	echo -e "\033[36m\033[1mpop rdx=====================================================\033[0m"
	ROPgadget --binary $libcname --only "pop|ret" | grep "rdx" | grep "ret$"

	echo -e "\033[36m\033[1mpop rdi=====================================================\033[0m"
	ROPgadget --binary $libcname --only "pop|ret" | grep "rdi" | grep "ret$"

	echo -e "\033[36m\033[1mpop rsi=====================================================\033[0m"
	ROPgadget --binary $libcname --only "pop|ret" | grep "rsi" | grep "ret$"

	echo -e "\033[36m\033[1mpop rbx=====================================================\033[0m"
	ROPgadget --binary $libcname --only "pop|ret" | grep "rbx" | grep "ret$"

	echo -e "\033[36m\033[1msyscall_ret=================================================\033[0m"
	ropper -f $libcname --search "syscall; ret;"

	echo -e "\033[36m\033[1msystem======================================================\033[0m"
	objdump -d -j .text $libcname | grep "<__libc_system@@GLIBC_PRIVATE>:"
	echo -e "\033[36m\033[1m/bin/sh=====================================================\033[0m"
	ROPgadget --binary $libcname --string "/bin/sh" | tail -n +3 | head -n 1

	echo -e "\033[36m\033[1mstdin=======================================================\033[0m"
	objdump -d -j .data $libcname | grep stdin
	echo -e "\033[36m\033[1mstdout======================================================\033[0m"
	objdump -d -j .data $libcname | grep stdout
	echo -e "\033[36m\033[1mstderr======================================================\033[0m"
	objdump -d -j .data $libcname | grep stderr

	echo -e "\033[36m\033[1mmprotect====================================================\033[0m"
	readelf --symbols $libcname | grep "mprotect"

	echo -e "\033[36m\033[1msetcontext==================================================\033[0m"
	objdump -d -j .text $libcname | grep "<setcontext@@GLIBC_2.2.5>:"

	echo -e "\033[36m\033[1m__free_hook=================================================\033[0m"
	objdump -d -j .bss $libcname | grep "__free_hook"

	echo -e "\033[36m\033[1mmain_arena==================================================\033[0m"
	objdump -d -j .data $libcname | grep main_arena
	echo "unsortdbin = main_arena + 0x60"
	echo -e "\033[36m\033[1m============================================================\033[0m"

else
	echo -e "\033[31m\033[1m[-] $libcname: No such file.\033[0m"
fi
