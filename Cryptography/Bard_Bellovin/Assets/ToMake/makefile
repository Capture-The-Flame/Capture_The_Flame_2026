OPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0 -g3
SETOPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0


all: Cursed_Scribe

Cursed_Scribe: main.o Magic.o
	gcc $^ -o $@ $(OPTS)

main.o: main.c Magic.h
	gcc $< -c -o $@ $(OPTS)

Magic.o: Magic.c Magic.h
	gcc $< -c -o $@ $(SETOPTS)

clean:
	rm -f *.o Cursed_Scribe