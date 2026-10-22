FROM node:24-alpine3.24

WORKDIR /app
ENV TEXTLINT_PORT=3000
COPY package.json ./
RUN apk update
RUN apk add git
RUN npm install -g npm
RUN npm install --allow-git all

COPY server.js ./
COPY textlint /app/textlint

EXPOSE $TEXTLINT_PORT
CMD ["node", "server.js"]
