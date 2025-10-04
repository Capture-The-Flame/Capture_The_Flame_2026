#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void print_banner() {
    printf("\n");
    printf("THE BLACKSMITH'S CIPHER\n");
    printf("\n");
    printf("The blacksmith guards the ancient forge.\n");
    printf("Speak the secret word to gain entry.\n");
    printf("\n");
}

int check_password(char *input) {
    char *secret = "flame{f0rg3d_1n_f1r3}";
    
    if (strcmp(input, secret) == 0) {
        return 1;
    }
    return 0;
}

int main() {
    char input[100];
    
    print_banner();
    
    printf("Enter the password: ");
    fgets(input, sizeof(input), stdin);
    
    // Remove newline
    input[strcspn(input, "\n")] = 0;
    
    if (check_password(input)) {
        printf("\n");
        printf("The forge roars to life. The flames reveals your flag:\n");
        printf("%s\n", input);
        printf("\nWell done, apprentice.\n");
    } else {
        printf("\nThe blacksmith shakes his head. That is not the word.\n");
    }
    
    return 0;
}