FROM node:8

COPY json_server /tmp/json_server

RUN npm install -g json-server

EXPOSE 3000

CMD json-server --watch /tmp/json_server/index.js --port 3000 --host 127.0.0.1

