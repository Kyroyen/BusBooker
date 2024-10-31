FROM node:18-alpine

WORKDIR /app

COPY rctfrontend/busbook/package.json rctfrontend/busbook/package-lock.json /app/
RUN npm install

COPY rctfrontend/busbook/ /app/

RUN npm run build

CMD ["npx", "serve", "-s", "dist"]
