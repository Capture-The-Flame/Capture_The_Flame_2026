#include <stdio.h>
#include <string.h>
#include <stdlib.h>

unsigned char secret_data[] = {
    0x39, 0x33, 0x3e, 0x32, 0x3a,
    0x24, 0x27, 0x6f, 0x2d, 0x6c,
    0x3b, 0x00, 0x39, 0x33, 0x6b,
    0x38, 0x22
};

int main() {
    char input[64];
    
    printf("Please enter the super secret password to bypass the firewall: ");
    
    if (fgets(input, sizeof(input), stdin) == NULL) {
        return 1;
    }

    input[strcspn(input, "\n")] = 0;

    if (strlen(input) != sizeof(secret_data)) {
        printf("Error: Size matters. That input was definitely the wrong length.\n");
        return 1;
    }

    for (int i = 0; i < sizeof(secret_data); i++) {
        if ((input[i] ^ 0x5F) != secret_data[i]) {
            printf("ACCESS DENIED. Nice try, script kiddie. Check your math.\n");
            return 1;
        }
    }

    printf("SYSTEM BREACHED! ...Wait, how did you find that? Good job!\n");
    return 0;
}