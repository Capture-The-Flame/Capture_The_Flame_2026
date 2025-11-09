#include <stdio.h>
#include <string.h>
#include <unistd.h>


int check1(char *input_string) {
    return (
        input_string[0] == 'f' &&
        input_string[1] == 'l' &&
        input_string[2] == 'a' &&
        input_string[3] == 'm' &&
        input_string[4] == 'e' &&
        input_string[5] == '{' &&
        input_string[15] == '}'
    );
}

int check2(char *input_string) {
    return (
        input_string[12] == '1' &&
        input_string[8] == 'v' &&
        input_string[11] == 's' &&
        input_string[13] == 'n' &&
        input_string[7] == '3' &&
        input_string[9] == '3' &&
        input_string[10] == 'r' &&
        input_string[14] == 'g' &&
        input_string[6] == 'r' 
    );
}

int check_flag(char *input_string) {
    if(check1(input_string) == 0) {
        printf("You don't even know the format of the flag!\n");
        return 0;
    }
    return check2(input_string);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: ./chall <flag>\n");
        return 1;
    }

    char *user_input = argv[1];
    int input_len = strlen(user_input);

    printf("Checking flag...\n");
    sleep(1);

    
    if (input_len != 16) {
        printf("Incorrect.\n");
        return 1;
    }
    
    if (check_flag(user_input) == 0) {
        printf("Incorrect.\n");
        return 1;
    }

    
    printf("Correct! You found the flag.\n");
    return 0; 
}
