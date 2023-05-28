# YouTube audio downloader
App to extract and download audio track from a YouTube video.

1. Create and fill `api/config/.env` file using the provided template `api/config/.env.template`. You can make a copy of it and specify the values of the environment variables. At least, you will need to specify values for the `DJANGO_SECRET_KEY` and `DOMAIN_NAME` variables, which are used for Django application.

2. Build containers
  ```
  docker-compose -f docker-compose.local-staging.yml build
  ```
2. Run
  ```
  docker-compose -f docker-compose.local-staging.yml up -d
  ```
3. Login as Admin
- username: `admin`
- pass: `admin`

## services
- api: [django](https://www.djangoproject.com/), [django rest framework](https://www.django-rest-framework.org/) - main app logic
- db-pg: [postgres](https://www.postgresql.org/) - main data storage
- celery_worker: [celery](https://docs.celeryq.dev/en/stable/) - distributed task queue
- front: [Vue.js](https://vuejs.org/), [Element Plus](https://element-plus.org/) - GUI
- nginx: [nginx](https://nginx.org/ru/)
- redis: [redis](https://redis.io/)

## Features
A simple SPA application that provides the ability to extract and download the audio track from a YouTube video. For this purpose, [yt-dlp](https://github.com/yt-dlp/yt-dlp) is used in conjunction with the capabilities of the ffmpeg library.
