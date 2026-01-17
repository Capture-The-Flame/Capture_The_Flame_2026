#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define BUFFER_SIZE 24
#define POOR "You live your life with no money ever..."
#define DEAD "You pass in a tragic accident on the way to a farm..."
#define NO_JOB "You find no job in the village and live your life on the streets to fade away.."

int get_buf(){
    char buff[BUFFER_SIZE];
    gets(buff);
    return 1;
}

void printIT(){
    int flag[14]= {102,108,97,109,101,123,114,105,99,104,51,36,33,125};
    int i;
    for(i=0;i<14;i++){
        printf("%c",(char)flag[i]);
    }
    printf("\n");
}

void test(){
    int val;
    val = get_buf();
    printf(POOR);
}

void call_tester(){
    test();
}

void overflowing_riches(){
    printf("CONGRATS!!! You have unlimited ");
    printIT();
}
