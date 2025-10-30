#include <stdlib.h>
#include <stdio.h>

#include "Peasants.h"

int main(){
    printBeginning();

    printf("\n");
    
    void* dam = makeDam();
    void* cow = makeFarm();
    void* wife = makeWife();
    void* kid = makeKid();

    DamStory();
    closeDam(dam);
    goBerserk(cow,kid,wife);

    return 0;
}