FROM node:24

WORKDIR /app
ENV TEXTLINT_PORT=3000
COPY package.json ./
RUN npm install

COPY server.js ./
COPY textlint /app/textlint

EXPOSE $TEXTLINT_PORT
CMD ["node", "server.js"]
