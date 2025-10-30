#ifndef MAGIC
#define MAGIC

void print_intro();
unsigned char* generate_key(int length);
void Abracadabra(char string[]);
void xor(const unsigned char *msg, unsigned char *out, const unsigned char *key, int length);
int test_matching(char string[]);
void print_flag();
void print_outro();
#endif