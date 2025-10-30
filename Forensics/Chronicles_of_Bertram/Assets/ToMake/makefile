OPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0 -g3
SETOPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0


all: MorningRoutine

MorningRoutine: Dam.o Peasants.o 
	gcc $^ -o $@ $(OPTS)

Dam.o: Dam.c Peasants.h
	gcc $< -c -o $@ $(OPTS)

Peasants.o: Peasants.c Peasants.h
	gcc $< -c -o $@ $(SETOPTS)

clean:
	rm -f *.o MorningRoutine