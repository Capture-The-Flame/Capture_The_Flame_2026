OPTS=-fno-pie -no-pie -fno-builtin -Wall -Wextra -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Werror -std=c17 -Wpedantic -O0 -g


all: server

server: server.o
	gcc $^ -o $@ $(OPTS)

server.o: server.c
	gcc $< -c -o $@ $(OPTS)

clean:
	rm -f *.o server
