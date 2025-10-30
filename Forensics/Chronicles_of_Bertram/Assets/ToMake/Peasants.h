#ifndef PEASANTS_H
#define PEASANTS_H

typedef struct Peasant{
    int x;
    char value[30];
    struct Peasant* to;
} Peasant;

void printBeginning();
void wait(int x);
void printout(char* x, int times);

void DamStory();

void* makeWife();
void* makeFarm();
void* makeKid();

void goBerserk();

void* makeDam();
void closeDam(void* tmp);
#endif