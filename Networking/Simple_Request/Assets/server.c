#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/epoll.h>
#include <assert.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <limits.h> 
#include <unistd.h>

// red squiggly lines on windows machine, shouldnt appear on WSL or Linux machines

#define RMAX 4096
#define HMAX 1024
#define BMAX 1024

static char request[RMAX+1];

static int HSIZE = 0;
static char header[HMAX];

static int BSIZE = 0;
static char body[BMAX];

// requests
static const char greet_request[] = "GET /hello HTTP/1.1\r\n\r\n";
static const char headers_request[] = "GET /headers HTTP/1.1\r\n";
static const char post_req[] = "POST /data HTTP/1.1\r\n";
static const char read_req[] = "GET /stored HTTP/1.1\r\n";
static const char welcome_req[] = "GET /welcome HTTP/1.1\r\n";
static const char help_req[] = "GET /need_help HTTP/1.1\r\n";
static const char sdoc_req[] = "GET /documentation.txt HTTP\1.1\r\n";
// responses
static const char OK200[] = "HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n";
static const char greet_body[] = "greetings";
static const char welcome_msg[] = "Welcome to the CHANGE_NAME 2.0 Capture the Flame challenge, you may begin whenever you like, best of luck!\n";
static const char help_msg[] = "HTTP request structure: method /resource(s) HTTP/1.1\\r\\n\n.Method could be:\n\t1)GET\n\t2)POST\nResource(s) could be:\n\t1)a filename, eg: requirements.txt\n\t2)a number of bytes, eg: bytes=32\n\t3)user permissions, eg: user=allen\n\t4)a mix of 2 and 3 where 2 comes before 3\nIf you want further assistance, please refer to the challenge description, documentation.txt or ask a board member for help. Best of luck!\n";
// error responses
static char BR400[] = "HTTP/1.1 400 Bad Request\r\n\r\n";
static char TL413[] = "HTTP/1.1 413 Request Entity Too Large\r\n\r\n"; 
static char NF404[] = "HTTP/1.1 404 Not Found\r\n\r\n";
static char UAUTH[] = "HTTP/1.1 400 Access Denied\r\n\r\n";
static char WHORU[] = "HTTP/1.1 400 No User Found, Who Are You?\r\n\r\n";

static int BUFSIZE = 6;
static char buffer[BMAX] = "(NULL)";


static void send_error(int clientfd, char* error);

#define FDMAX 1024
#define EMAX 16
static int epfd = -1;
static int client2file[1024];
static int num_reqs = 0;

// LONG MAX = 9223372036854775807
// INT MAX = 2147483647

// test behaviors
// 1) GET /files, 404 if file DNE
// 2) GET /need_help
// 3) GET /welcome
// 4) GET /bytes=N user=S if (N < 0 || N > INT_MAX) && S == admin -> give flag
// 5) GET /bytes=N user=S if (N < 0 || N > INT_MAX) && S != admin -> junk data
// 6) GET /bytes=N user=S if (N >= 0 || N <= INT_MAX) && S != admin -> auth error
// 7) GET /bytes=N user=S if (N >= 0 || N <= INT_MAX) && S == admin -> access history
// 8) GET /bytes=N || GET /bytes=N user= -> WHO ARE YOU
// 9) order in GET must be bytes=N first then user=S else error
// 10) No segfaults due to bad input
// 11) one server per player or one server for multiple players
// 12) GET /flag.txt || GET /server.c -> fails

static int open_listenfd(int port) {
	
	int listenfd = socket(AF_INET, SOCK_STREAM, 0);
	int optval = 1;
	setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
	
	struct sockaddr_in server;
	server.sin_family = AF_INET;
	server.sin_port = htons(port);
	inet_pton(AF_INET, "127.0.0.1", &server.sin_addr);

	bind(listenfd, (struct sockaddr*)&server, sizeof(server));
	listen(listenfd, 10);
	return listenfd;

}

static int accept_connection(int listenfd) {

        static struct sockaddr_in client;
        static socklen_t csize;
        memset(&client, 0x00, sizeof(client));
        memset(&csize, 0x00, sizeof(csize));

        int clientfd = accept(listenfd, (struct sockaddr*)&client, &csize);
        return clientfd;

} 

static void send_data(int clientfd, char buf[], int size) {

	ssize_t amt, total = 0;
	do {
		amt = send(clientfd, buf + total, size - total, 0);
		total += amt;
	
	} while(total < size);

}

static void send_response(int clientfd) {
	
	send_data(clientfd, header, HSIZE);
	send_data(clientfd, body, BSIZE);
}

static void handle_greet(int clientfd) {

	BSIZE = strlen(greet_body);
	memcpy(body, greet_body, BSIZE);
	HSIZE = snprintf(header, HMAX, OK200, BSIZE);
	send_response(clientfd);
	close(clientfd);
}

static void handle_help(int clientfd) {
	BSIZE = strlen(help_msg);
	memcpy(body, help_msg, BSIZE);
	HSIZE = snprintf(header, HMAX, OK200, BSIZE);
	send_response(clientfd);
	close(clientfd);
}

static void handle_welcome(int clientfd) {
	BSIZE = strlen(welcome_msg);
	memcpy(body, welcome_msg, BSIZE);
	HSIZE = snprintf(header, HMAX, OK200, BSIZE);
	send_response(clientfd);
	close(clientfd);
}

static void handle_headers(int clientfd) {

	char* start = strstr(request, "\r\n") + 2;
	char* end = strstr(request, "\r\n\r\n") ;
	if (end == NULL) { send_error(clientfd, BR400); return; }
	*end = '\0';
	BSIZE = strlen(start);
	if(BSIZE > BMAX) { send_error(clientfd, TL413); return; }
	memcpy(body, start, BSIZE);
	HSIZE = snprintf(header, HMAX, OK200, BSIZE);
        send_response(clientfd);
        close(clientfd);

}

static void send_error(int clientfd, char* error) {
	
	send_data(clientfd, error, strlen(error));
	close(clientfd);
}

static void handle_read(int clientfd) {
	
	HSIZE = snprintf(header, HMAX, OK200, BUFSIZE);
	BSIZE = BUFSIZE;
	memcpy(body, buffer, BUFSIZE);
	send_response(clientfd);
	close(clientfd);
}

static void handle_post(int clientfd) {
	
	char* body_start = strstr(request, "\r\n\r\n");
	assert(body_start != NULL);
	body_start += 4;

	char* start = strstr(request, "Content-Length: ");
	start += 16;
	char* end = strstr(request, "\r\n");
	*end = '\0';

	int size = atoi(start);
	if (size > BMAX) { send_error(clientfd, TL413); return; }
	BUFSIZE = size;
	memcpy(buffer, body_start, BUFSIZE);

	handle_read(clientfd);

}

static void handle_file(int clientfd) {
	
	char* filename = strstr(request, "/") + 1;
	filename = strtok(filename, " \r\n");
	if (!strncmp(filename, "flag.txt", 8)) { send_error(clientfd, NF404); return; }
	if (!strncmp(filename, "server.c", 8)) { send_error(clientfd, NF404); return; }
	int fd = open(filename, O_RDONLY);
	if (fd < 0) { send_error(clientfd, NF404); return; }
	static struct stat file;
	fstat(fd, &file);
	if (!S_ISREG(file.st_mode)) { send_error(clientfd, NF404); close(fd); return; }
	int size = file.st_size;
	HSIZE = snprintf(header, HMAX, OK200, size);
	send_data(clientfd, header, HSIZE);

	static struct epoll_event Event;
	memset(&Event, 0x00, sizeof(Event));
	Event.events = EPOLLOUT;
	Event.data.fd = clientfd;
	epoll_ctl(epfd, EPOLL_CTL_ADD, clientfd, &Event);
	client2file[clientfd] = fd;

	/*while( (BSIZE = read(fd, body, BMAX)) > 0) {
		send_data(clientfd, body, BSIZE);
	}
	close(fd);
	close(clientfd);*/
}

static void send_n_bytes(int clientfd) {
    
    // go to where "bytes=" is
    char* eq = strstr(request, "bytes=");
    if (eq == NULL) { 
		send_error(clientfd, BR400);
		return;
	}
	// skip past "bytes="
    eq += 6; 

    // get "number"
    char* num_str = strtok(eq, " \r\n");
    if (num_str == NULL) { 
		send_error(clientfd, BR400);
		return;
	}

    // "number" to number 
    long long raw = atoll(num_str);
	// printf("raw is %ld and INT_MAX is %d or %ld idk\n", raw, INT_MAX, INT_MAX);
    int size = (int)raw;
	printf("size is %d\n", size);

	// skip past the number to go to u of user
	while (*eq != 'u' /* && *eq != '\r' && *eq != '\n'*/ ) { eq++; }
	// skip past user=
	eq += 5;
	// printf("eq is: %s\n", eq);
	int user_chk = strncmp(eq, "admin", 5);

    // exploit condition: (val < 0 || val > LONG_MAX) && user is admin 
    if (size < 0 && user_chk == 0) {
        int fd = open("flag_contents.txt", O_RDONLY);
        if (fd < 0) { 
			send_error(clientfd, NF404);
			return;
		}
        struct stat file;
        fstat(fd, &file);
        int fsize = file.st_size;
        HSIZE = snprintf(header, HMAX, OK200, fsize);
        send_data(clientfd, header, HSIZE);
        while ((BSIZE = read(fd, body, BMAX)) > 0) {
            send_data(clientfd, body, BSIZE);
        }
        close(fd);
        close(clientfd);
        return;
    }

	// exploit failed

	// user check fail && size check fail
	  // send unauthorized access attempt info
	if (user_chk != 0 && size >= 0) {
		printf("user != admin && size = %d >= 0\n", size);
		send_error(clientfd, UAUTH);
		return;
	}

	// user check fail && size check pass
	  // send junk data
    if (user_chk != 0 && size < 0) { 
		printf("user != admin && size (before rand()) = %d\n", size);
		size = rand() % (INT_MAX - 1);
		printf("user != admin && size (after rand()) = %d\n", size);
		
		int remaining = size;
		const char* sources[] = {"random.txt", "test.txt", "random.txt", "test.txt", "random.txt"};
		for (int s = 0; s < 5 && remaining > 0; s++) {
			int fd = open(sources[s], O_RDONLY);
			if (fd < 0) continue;
			struct stat file;
			fstat(fd, &file);

			int to_read = (remaining < (int)file.st_size) ? remaining : (int)file.st_size;
			int total_read = 0;

			HSIZE = snprintf(header, HMAX, OK200, size); // only send header once ideally
			if (s == 0) send_data(clientfd, header, HSIZE);

			while (total_read < to_read) {
				int chunk = (to_read - total_read < BMAX) ? to_read - total_read : BMAX;
				BSIZE = read(fd, body, chunk);
				if (BSIZE <= 0) break;
				send_data(clientfd, body, BSIZE);
				total_read += BSIZE;
				remaining -= BSIZE;
			}

			close(fd);
		}
	}

	// user check pass && size check fail
	  // send server access data
	if (user_chk == 0 && size >= 0) {
		printf("user != admin && size = %d\n", size);
		int fd = open("server_access.txt", O_RDONLY);
        if (fd < 0) { 
			send_error(clientfd, BR400);
			return;
		}
        struct stat file;
        fstat(fd, &file);
        int fsize = file.st_size;
        HSIZE = snprintf(header, HMAX, OK200, fsize);
        send_data(clientfd, header, HSIZE);
        while ((BSIZE = read(fd, body, BMAX)) > 0) {
            send_data(clientfd, body, BSIZE);
        }
        close(fd);
	}
	
    close(clientfd);
}

static void handle_requests(int clientfd) {

	ssize_t bytes_received = recv(clientfd, request, RMAX, 0);
	request[bytes_received] = '\0';
	
	// printf("\nrequest is: %s\nlen is %d\n", request, strlen(request));
	if (num_reqs != 0 && num_reqs % 3 == 0) {
		printf("slept\n");
		sleep(10);
		printf("woke\n");
	}
	num_reqs++;
	
	if (bytes_received <= 0) { return; }

	if(!strncmp(request, greet_request, strlen(greet_request))) {
		handle_greet(clientfd);	
	}

	if(!strncmp(request, welcome_req, strlen(welcome_req))) {
		handle_welcome(clientfd);	
	}

	if(!strncmp(request, help_req, strlen(help_req))) {
		handle_help(clientfd);	
	}

	else if (!strncmp(request, headers_request, strlen(headers_request))) {
		handle_headers(clientfd);
	}

	else if (!strncmp(request, post_req, strlen(post_req))) {
		handle_post(clientfd);
	}

	else if (!strncmp(request, read_req, strlen(read_req))) {
		handle_read(clientfd);
	}

	// /bytes=N && no user=
	else if (!strncmp(request, "GET /bytes=", 11) && strstr(request, "user=") == NULL) {
		send_error(clientfd, WHORU);
	}
	
	// /bytes=N && user=(space before HTTP i.e: nothing provided)
	else if (!strncmp(request, "GET /bytes=", 11) && strstr(request, "user= ") != NULL) {
		send_error(clientfd, WHORU);
	}

	// /bytes=N && user=any_char/string_of_chars --> VALID
	else if (!strncmp(request, "GET /bytes=", 11) && strstr(request, "user=") != NULL) {
		send_n_bytes(clientfd);
	}

	else if (!strncmp(request, "GET ", 4)) {
		// printf("1\n");
		handle_file(clientfd);
	}

	else {
		send_error(clientfd, BR400);
	}
} 

static void send_chunk(int clientfd) {
	
	static char buffer[BMAX];
	int fd = client2file[clientfd];
	ssize_t nbytes = read(fd, buffer, BMAX);

	if (nbytes > 0) {
		send_data(clientfd, buffer, nbytes);	
	}
	else {
		epoll_ctl(epfd, EPOLL_CTL_DEL, clientfd, NULL);
		close(clientfd);
		close(fd);
	}

}

static void event_loop(int listenfd) {
	
	epfd = epoll_create1(0);
	static struct epoll_event Event;

	memset(&Event, 0x00, sizeof(Event));
	Event.events = EPOLLIN;
	Event.data.fd = listenfd;
	epoll_ctl(epfd, EPOLL_CTL_ADD, listenfd, &Event);

	static struct epoll_event Events[EMAX];

	while (1) {
		int nfds = epoll_wait(epfd, Events, EMAX, -1);
		for(int i = 0; i < nfds; ++i) {
			int fd = Events[i].data.fd;
			if (Events[i].events == EPOLLIN) {
				if (fd == listenfd) {
					int clientfd = accept_connection(listenfd);
					memset(&Event, 0x00, sizeof(Event));
					Event.events = EPOLLIN;
					Event.data.fd = clientfd;
					epoll_ctl(epfd, EPOLL_CTL_ADD, clientfd, &Event);
				}
				else {
					epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL);
					handle_requests(fd);
				}
			}
			else {
				send_chunk(fd);
			}
		}
	}

}

int main(int argc, char * argv[])
{
    assert(argc == 2);
    int port = atoi(argv[1]);
    int listenfd = open_listenfd(port);
    event_loop(listenfd);
    /*while (1) {
	int clientfd = accept_connection(listenfd);
	handle_requests(clientfd);
	close(clientfd);

    }*/
    return 0;
}
