#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char *flag;

void set(){
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	// FILE *f = fopen("flag.txt", "r");
	// if (!f){
	// 	puts("err opening flag");
	// 	return;
	// }
	// flag = malloc(64);
	// fgets(flag, 64, f);
	// fclose(f);
    flag = malloc(64);

    char obf[] = {
    0x66, 0x6c, 0x61, 0x6d, 0x65, 0x7b,
    0x35, 0x20,
    0x52, 0x69, 0x64, 0x67, 0x65, 0x77, 0x61, 0x74, 0x65, 0x72,
    0x73, 0x74, 0x72, 0x65, 0x61, 0x6d, 0x76, 0x69, 0x65, 0x77,
    0x20,
    0x4c, 0x6e,
    0x7d,
    0x00
    };

    memcpy(flag, obf, sizeof(obf));
	return;
}

int main(){
	set();
	char buf[64];
	puts("please, oh please, let me know the address!:");
	read(0, buf, 48);
	buf[47] = '\0';
	printf(buf,flag);
	puts("bye");
	return 0;
}