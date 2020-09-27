FROM node:14

RUN npm install uglify-js --global
COPY src/main.js main.js
RUN uglifyjs main.js > main.min.js

FROM nginx

COPY src/ /usr/share/nginx/html/
COPY --from=0 main.min.js /usr/share/nginx/html/main.js
COPY flag.txt /usr/share/nginx/html/flag/01337133713371337

EXPOSE 80
