#include "Magic.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void print_outro(){
    printf("Fool...you cannot break my spell! Stay out!\n");
}

int test_matching(char string[]){
    char* character = string;

    char correct[] = "y\\f";

    for(int i =0; i<3; i++){
        if(*character != correct[i])
            return 0;
        character++;
    }

    return 1;
}

void print_flag(){
    printf("Though has broken my spell...here is your flag..:");
   printf("\n\t\t~i[z8$\n");
}

unsigned char* generate_key(int length){
    int true_length = length*8;
    unsigned char string[] = "011011000001000001101100011010001011101000001010";


    //0011 0110 0000 1000 0011 0110 0001 0110 0101 1101 0101 0000 -- original
    //1100 0110 0000 0001 1100 0110 1000 0110 1010 1011 1010 0000 -- inverted
    // 0110 1100 0001 0000 0110 1100 0110 1000 1011 1010 0000 1010 -- swapped -- use this one
    //strcpy(string,"000011000000000000010110");

    unsigned char *key = malloc(true_length);

    for (int i = 0; i < (true_length); i++) {
        if(i<48)
            key[i] = string[i] - '0';
        else
            key[i] = rand() % 2;

    }
    return key;
}

void xor(const unsigned char *msg, unsigned char *out, const unsigned char *key, int length) {
    int key_it=0;
    for (int i = 0; i < length; ++i) {
        unsigned char in_byte = msg[i];
        unsigned char out_byte = 0;
        for (int b = 0; b < 8; b++) {
            //isolate bit from message
            unsigned char bit = (in_byte >> b) & 1;
            //isolate bit from key
            unsigned char k = (key[key_it]) & 1;

            //compute xor
            unsigned char res = bit ^ k;
            // printf("XOR: %x ^ %x = %x\n", bit,k,res);

            //return bit into byte
            out_byte |= (res << b);
            key_it++;
        }
        out[i] = out_byte;
        // printf("DOING: %c,%02x ()-> %c,%02x\n", in_byte,in_byte,out_byte,out_byte);
    }
}

void Abracadabra(char string[]){

    size_t length = strlen(string);

    //check string before doing encryption, if they sent the proper string then
    //no need to do all the computation
    if(length==3){
        if(test_matching(string)){
            print_flag();
            return;
        }
    }

    size_t bit_count = length * 8;
    unsigned char *key = generate_key(length);

    unsigned char *plaintext = (unsigned char*)malloc(length);
    unsigned char *ciphertext = (unsigned char*)malloc(length);

    memcpy(plaintext, string, length);

    //Encrypt
    xor(plaintext, ciphertext, key, length);

    for (size_t i = 0; i < length; i++) {
        printf("%c", ciphertext[i]);
    }
    printf("\n");

    print_outro();

    free(key);
    free(plaintext);
    free(ciphertext);
}


