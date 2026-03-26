OPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0 -g
SETOPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0 -g


all: Scissors

Scissors: main.o
	gcc $^ -o $@ $(OPTS)

main.o: main.c
	gcc $< -c -o $@ $(OPTS)

clean:
	rm -f *.o Scissors