#include "helper.h"
#include <stdlib.h>
#include <stdio.h>

int main(){
    char attack[20];
    printf("\n You've entered the lair of the elf king...Dare speak the phrase that the mage promised would break his spell: ");
    scanf("%19s",attack);
    printf("\n\n");
    direct_soldiers(attack);
    return 0;
}