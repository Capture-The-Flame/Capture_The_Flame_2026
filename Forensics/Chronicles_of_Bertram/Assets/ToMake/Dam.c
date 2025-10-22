#include <stdlib.h>
#include <stdio.h>

#include "Peasants.h"

int main(){
    printBeginning();

    printf("\n");
    
    void* dam = makeDam();
    DamStory();
    closeDam(dam);
    return 0;
}