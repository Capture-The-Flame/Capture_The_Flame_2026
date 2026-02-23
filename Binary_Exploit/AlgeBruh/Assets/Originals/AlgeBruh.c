#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void printFlag(){
    printf("\nNICE JOB!\nHere's your reward:");
    int ascii[] = {
        102, 108, 97, 109, 101, 123,
        64, 108, 98, 51, 114, 116, 95,
        51, 33, 110, 36, 116, 33, 51, 110,
        125
    };

    int length = sizeof(ascii) / sizeof(ascii[0]);

    for (int i = 0; i < length; i++) {
        printf("%c", ascii[i]);
    }

    printf("\n");
}

int main(){
    int x;

    printf("Are you good at math?? Let's find out >:) \n Enter:");
    scanf("%d",&x);

    x=x+13;
    x= x+20;
    x=x*5;
    x = x+7;

    if(x==357){
        printFlag();
    }
    else{
        printf("\nBetter luck next time! : (\n");
    }
    return 0;
}