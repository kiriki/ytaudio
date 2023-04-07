#FROM app/app_api AS api
#RUN mkdir /app/api/files /app/api/static
#RUN python manage.py collectstatic --noinput

FROM nginx:alpine
RUN mkdir /var/www /var/www/frontend
COPY --from=app/app_front /app/dist/ /var/www/frontend/
