#based on https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html
FROM node:lts-alpine as front
#RUN yarn global add http-server
WORKDIR /app
COPY package*.json ./
RUN yarn
COPY . .
RUN yarn build-only

#EXPOSE 8080
#CMD [ "http-server", "dist", "-p", "8080" ]

#FROM nginx:alpine
#RUN mkdir /var/www /var/www/frontend
#COPY --from=front /app/dist/ /var/www/frontend/
