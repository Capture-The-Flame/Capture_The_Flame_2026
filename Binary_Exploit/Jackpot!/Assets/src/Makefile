OPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0 -g
SETOPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0


all: Jackpot!

Jackpot!: main.o
	gcc $^ -o $@ $(OPTS)

main.o: Jackpot.c
	gcc $< -c -o $@ $(OPTS)

clean:
	rm -f *.o Jackpot!