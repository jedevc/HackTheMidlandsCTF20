FROM alpine:latest AS build

RUN apk add --no-cache build-base

WORKDIR /build
COPY Makefile sh.c ./
RUN make

FROM alpine:latest

COPY --from=build /build/sh /bin/sh
