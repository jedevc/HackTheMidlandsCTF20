CFLAGS = -g -O0 -Wall -Wextra
LDFLAGS =

.PHONY: all build clean

all: build

build: sh

clean:
	rm -f sh

sh: sh.c
	gcc $(CFLAGS) $(LDFLAGS) sh.c -o sh
