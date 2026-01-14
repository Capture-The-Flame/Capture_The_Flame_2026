#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char input[32];
    int val1, val2;
    
    printf("\n=== SOFTWARE ACTIVATION PORTAL ===\n");
    printf("Enter Product Key: ");
    
    if (fgets(input, sizeof(input), stdin) == NULL) return 1;
    input[strcspn(input, "\n")] = 0;

    if (strlen(input) != 16) {
        printf("Invalid Key Format (Error 101)\n");
        return 1;
    }

    if (strncmp(input, "flame{", 6) != 0) {
        printf("Invalid Vendor ID (Error 102)\n");
        return 1;
    }

    if (input[6] + input[7] != 215) {
        printf("Checksum Failed (Error 103)\n");
        return 1;
    }
    
    if (input[6] != 'r') {
        printf("Checksum Failed (Error 103-B)\n");
        return 1;
    }

    if ((input[8] ^ 0x55) != 0x0A) {
        printf("Bitmask Integrity Violation (Error 104)\n");
        return 1;
    }

    if (input[9] != 'w' || input[10] != '1' || input[11] != 'z') {
        printf("Invalid Product Series (Error 105)\n");
        return 1;
    }

    int magic = (input[12] - 48) * 100;
    if (magic != 400) { 
        printf("Numeric Constraint Error (Error 106)\n");
        return 1;
    }

    if (input[13] != 'r') return 1;
    
    if (input[15] != '}') return 1;

    if (input[14] % 2 != 0 || input[14] != 100) { 
         printf("Parity Check Failed (Error 107)\n");
         return 1;
    }

    printf("PRODUCT ACTIVATED SUCCESSFULLY.\n");
    return 0;
}