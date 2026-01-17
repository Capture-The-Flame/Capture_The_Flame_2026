# OPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -Wpedantic -O0 -g3
# SETOPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -Wpedantic -O0
OPTS = -fno-stack-protector -O0 -g

all: Crystal_Ball

Crystal_Ball: main.o helper.o
	gcc -std=gnu89 $^ -o $@ $(OPTS)

main.o: main.c helper.h
	gcc -std=gnu89 $< -c -o $@ $(OPTS)

helper.o: helper.c helper.h
	gcc -std=gnu89 $< -c -o $@ $(OPTS)

clean:
	rm -f *.o Crystal_Ball