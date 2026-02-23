	.file	"Algebruh.c"
	.text
	.globl	printFlag
	.type	printFlag, @function

.LC0:
	.string	"Are you good at math?? Let's find out >:) \n Enter:"
.LC1:
	.string	"%d"
	.text
	.globl	main
	.type	main, @function
main:
	...
	call	__isoc99_scanf@PLT
	movl	-12(%rbp), %eax
	addl	$13, %eax
	movl	%eax, -12(%rbp)
	movl	-12(%rbp), %eax
	addl	$20, %eax
	movl	%eax, -12(%rbp)
	movl	-12(%rbp), %edx
	movl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	movl	%eax, -12(%rbp)
	movl	-12(%rbp), %eax
	addl	$7, %eax
	movl	%eax, -12(%rbp)
	movl	-12(%rbp), %eax
	cmpl	$357, %eax
	jne	.L3
	movl	$0, %eax
	call	printFlag
.L3:
	movl	$0, %eax
	movq	-8(%rbp), %rdx
	subq	%fs:40, %rdx
	call	__stack_chk_fail@PLT