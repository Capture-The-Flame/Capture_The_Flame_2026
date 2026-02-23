#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char printFlag_winner(){
    int bytes[] = {102,108,97,109,51,95,110,101,118,101,114,95,98,117,114,110,95,48,117,116};
    printf("\n");
    for (int i = 0; i < (int)(sizeof(bytes)/sizeof(bytes[0])); i++) {
        printf("%c",(char)bytes[i]);
    }
    printf("\n");
    return 'a';
}

void printFlag2(){
    int bytes[] = {102, 108, 97, 109, 101, 123,109, 33, 76, 76, 33, 48, 110, 64, 33, 114, 51,125};
    printf("\n");
    for (int i = 0; i < (int)(sizeof(bytes)/sizeof(bytes[0])); i++) {
        printf("%c",(char)bytes[i]);
    }
    printf("\n");
}

char* printFlag_correct(){
    int bytes[] = {102,108,97,109,101,123,101,120,97,108,45,104,97,104,97,95,85,45,116,104,111,117,103,104,116};
    printf("\n");
    for (int i = 0; i < (int)(sizeof(bytes)/sizeof(bytes[0])); i++) {
        printf("%c",(char)bytes[i]);
    }
    printf("\n");
    return (char*)"98";
}

int printFlag4(){
    return 97;
}

void* printFlag(){
    int bytes[] = {102,108,97,109,101,115,95,64,114,51,95,104,48,116};
    printf("\n");
    for (int i = 0; i < (int)(sizeof(bytes)/sizeof(bytes[0])); i++) {
        printf("%c",(char)bytes[i]);
    }
    printf("\n");
    return (void*)0;
}

double printFlag1(){
    int bytes[] = {102, 108, 97, 109, 101,95,104, 97, 104, 97,95,108, 111, 108};
    printf("\n");
    for (int i = 0; i < (int)(sizeof(bytes)/sizeof(bytes[0])); i++) {
        printf("%c",(char)bytes[i]);
    }
    printf("\n");
    return 0.0;
}

int main(){
    int a,b,c,d;
    printf("\nEnter your lotto numbers (Each seperated by a dash -> x-x-x-x):");
    scanf("%d-%d-%d-%d", &a,&b,&c,&d);

    if((char)a!='u'){
        printf("\nYou've won: $%d",printFlag4());
        printf("\nBetter luck next time!\n");
        return 0;
    }
    if((char)b!='i'){
        printf("\nYou've won: $%f",printFlag1());
        printf("\nBetter luck next time!\n");
        return 0;
    }
    if((char)c!='c'){
        printf("\nYou've won: $%c",*printFlag_correct());
        printf("\nBetter luck next time!\n");
        return 0;
    }
    if((char)d!='!'){
        printf("\nYou've won: $%c", printFlag_winner());
        printf("\nBetter luck next time!\n");
        return 0;
    }
    printf("\nYou've won: $%p", printFlag());
    printFlag2();
    printf("\nBetter luck next time!\n");
    return 0;
}