#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "Magic.h"

int main(){
    srand(1919);
    char input[200];

    printf("State your spell: ");
    fgets(input, sizeof(input), stdin);

    input[strcspn(input, "\n")] = '\0';

    size_t length = strlen(input);
    if (length == 0) {
        printf("Thou hath entered a non existent spell. Good riddance\n");
        return 0;
    }

    Abracadabra(input);

    return 0;
}
