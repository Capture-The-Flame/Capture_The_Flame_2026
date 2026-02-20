#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void direct_soldiers(){

}
int count_elves(){
    return 0;
}
void throne_room(){
    int flag[14]= {102,108,97,109,101,123,98,108,97,100,118,97,107,125};
    int i;
    for(i=0;i<14;i++){
        printf("%c",(char)flag[i]);
    }
    printf("\n\n");
}
char get_flag(){
    return 'a';
}
double ha(){
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

}
void attack_king(char* attack){
    char array[3]={73,100,97};
    for(int i=0;i<3;i++){
        if(attack[i]==array[i])
            continue;
        else{
            printf("HAHA! I WIN!! LEAVE NOW PITIFUL HUMAN\n");
            return;
        }
    }
    printf("How.....how...no....how could this happen.....");
    throne_room();
    printf("Goodbye cruel world....\n");
}



void Zevran(char* attack){
    attack_king(attack);
}