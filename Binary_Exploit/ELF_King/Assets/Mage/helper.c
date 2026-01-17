#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void direct_soldiers(char* attack){
    printf("YOU FOOL! YOU HAVE BEEN DEFEATED\n");
    return;
}

int count_elves(){
    printf("I am the mage!");
    return 0;
}

char get_flag(){
    return 'a';
}

double ha(){
    printf("I love pie!");
    return 5.5;
}

int count_money(){
    int moolah=20;
    for(int i=0;i<20;i++){
        moolah++;
    }
    return moolah;
}

void defend(){
    int flag[4]= {73,100,97};
    int i;
    for(i=0;i<4;i++){
        printf("%c",(char)flag[i]);
    }
    printf("\n\n");
}

void attack_king(char *attack){
    char passphrase[5]={'3','.','1','4','\0'};
    
    for(int i=0;i<5;i++){
        if(attack[i]!=passphrase[i]){
            printf("HAHA");
        }
    }
    printf("Here you pitiful fool...speak this unto the king and you shall defeat him..");
    defend();
}