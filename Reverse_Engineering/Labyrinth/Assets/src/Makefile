OPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0 -g
SETOPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0 -g


all: Labyrinth

Labyrinth: main.o Lists.o
	gcc $^ -o $@ $(OPTS)

main.o: main.c Labyrinth.h
	gcc $< -c -o $@ $(OPTS)

Lists.o: Labyrinth.c Labyrinth.h
	gcc $< -c -o $@ $(SETOPTS)

clean:
	rm -f *.o Labyrinth