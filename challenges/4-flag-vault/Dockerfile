FROM node:14

WORKDIR /source

COPY package.json yarn.lock ./
RUN yarn install

COPY public/ public/
COPY src/ src/
RUN ls && yarn build

FROM nginx

COPY demo.mp4 /usr/share/nginx/html
COPY --from=0 /source/build /usr/share/nginx/html
