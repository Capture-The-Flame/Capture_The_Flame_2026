#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "Peasants.h"

void wait(int delay){
    for(int i=0; i<delay; i++){
        ;
    }
}

void printout(char* x, int times){
    
    int length = strlen(x);
    for(int j = 0; j<times; j++){
        for(int i=0;i<length;i++){
            printf("%c",x[i]);
            fflush(stdout);
            wait(10000000);
        }
        printf("\n");
    }
}

void printDam(){
    for(int i=0;i<25;i++){
        printf("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓");
        printf("\n");
    }
}

void printBeginning(){
    printf("\n");
    printf("\n");
    printf("-----------------------------------------------------------------------------------------------------------------------------------------");
    printf("\n");
    printf("\t\t\t\t\t\t            .--------.               .--------.\n");
    printf("\t\t\t\t\t\t           /          \\             /          \\\n");
    printf("\t\t\t\t\t\t          /            \\           /            \\\n");
    printf("\t\t\t\t\t\t   ------{      ()      }---------{      ()      }------\n");
    printf("\t\t\t\t\t\t          \\            /           \\            /\n");
    printf("\t\t\t\t\t\t           \\          /             \\          /\n");
    printf("\t\t\t\t\t\t            '--------'               '--------'\n");
    printf("\n");


    char monologue_1[168];
    strcpy(monologue_1,"And so it starts again...another monotonous day. I have so much to do. I start everyday with brushing my teeth, feeding the youngins some eggs, and plowing the field.");
    printout(monologue_1,1);

    char monologue_2[200];
    strcpy(monologue_2, "Then I have to go take care of my farm animals. I clean up after them....feed them...Its all the same. I can never escape. I feel like I'm going crazy.");
    printout(monologue_2,1);

    char tmp[5];
    strcpy(tmp,"....");
    printout(tmp,3);

    char monologue_3[200];
    strcpy(monologue_3,"I've had enough...I'm going to skip this. The kids can skip a meal.. I'm going to take a stroll to the dam they just built for the nearby kingdom!");
    printout(monologue_3,1);

    printout(tmp,3);

    char monologue_4[4];
    strcpy(monologue_4,"wow");
    printout(monologue_4,1);

    printout(tmp,3);
    
}

void DamStory(){
    printDam();

    char tmp[5];
    strcpy(tmp,"....");
    printout(tmp,3);

    char comment[50];
    strcpy(comment, "its beautiful");
    printout(comment,1);

    char monologue[211];
    strcpy(monologue, "Its many intricacies are nothing to scoff at. I remember it took so long for them to build this..... I wonder how many perished. I wonder if there were any LEAKS..\n\nWell thats enough for now.. Time to go home.");
    printout(monologue,1);

    printout(tmp,3);
    char goodbye[10];
    strcpy(goodbye, "Goodnight");
    printout(goodbye,1);
}

void* makeDam(){

    Peasant* pipe2 = malloc(sizeof(Peasant));
    pipe2->x = 17;
    strcpy(pipe2->value,"vpsuffX");

    return (void*)pipe2;
}

void closeDam(void* tmp){
    
}

void* makeFarm(){
    void* Farm = (void*)malloc(sizeof(Peasant));
    return Farm;
}

void* makeWife(){
    void* Wife = (void*)malloc(sizeof(Peasant));
    return Wife;
}

void* makeKid(){
    void* Kid = (void*)malloc(sizeof(Peasant));
    return Kid;
}

void goBerserk(void* cow, void* kid, void*wife){
    free(wife);
    free(kid);
    free(cow);
}