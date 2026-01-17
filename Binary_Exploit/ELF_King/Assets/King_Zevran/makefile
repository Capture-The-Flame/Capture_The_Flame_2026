OPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -Wpedantic -O0 -g3
SETOPTS=-Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -Wpedantic -O0

all: Zevran

Zevran: main.o helper.o
	gcc $^ -o $@ $(OPTS)

main.o: main.c helper.h
	gcc $< -c -o $@ $(OPTS)

helper.o: helper.c helper.h
	gcc $< -c -o $@ $(OPTS)

clean:
	rm -f *.o Zevran