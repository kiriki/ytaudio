#based on https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html
FROM node:lts-alpine as base
#RUN yarn global add http-server
WORKDIR /app
COPY package*.json yarn.* ./
RUN yarn install
COPY . .

FROM base as prod
RUN yarn build-only

FROM base as dev
CMD [ "yarn", "dev" ]

#FROM nginx:alpine
#RUN mkdir /var/www /var/www/frontend
#COPY --from=front /app/dist/ /var/www/frontend/
