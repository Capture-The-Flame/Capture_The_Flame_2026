#include <stdio.h>
#include <ctype.h>

#define WORD_SIZE 8   // 4 bytes = 32-bit (change to 8 for 64-bit)

int main(void) {
    int c;
    int high = -1;
    unsigned char buf[WORD_SIZE];
    int idx = 0;

    while ((c = getchar()) != EOF) {
        if (isspace(c))
            continue;

        if (!isxdigit(c))
            continue;

        int value;
        if (c >= '0' && c <= '9') value = c - '0';
        else if (c >= 'a' && c <= 'f') value = c - 'a' + 10;
        else value = c - 'A' + 10;

        if (high < 0) {
            high = value;
        } else {
            buf[idx++] = (high << 4) | value;
            high = -1;

            if (idx == WORD_SIZE) {
                // emit little-endian
                for (int i = WORD_SIZE - 1; i >= 0; i--) {
                    putchar(buf[i]);
                }
                idx = 0;
            }
        }
    }

    /* Flush remaining bytes (if input not multiple of WORD_SIZE) */
    if (idx > 0) {
        for (int i = idx - 1; i >= 0; i--) {
            putchar(buf[i]);
        }
    }

    return 0;
}
