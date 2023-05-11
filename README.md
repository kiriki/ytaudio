1. Build containers
  ```
  docker-compose -f docker-compose.local-staging.yml build
  ```
2. Run
  ```
  docker-compose -f docker-compose.local-staging.yml up -d
  ```
3. Login
- username: `admin`
- pass: `admin`

## services
- api: [django](https://www.djangoproject.com/), [django rest framework](https://www.django-rest-framework.org/) - main app logic
- db-pg: [postgres](https://www.postgresql.org/) - main data storage
- celery_worker: [celery](https://docs.celeryq.dev/en/stable/) - distributed task queue
- front: [Vue.js](https://vuejs.org/), [Element Plus](https://element-plus.org/) - GUI
- nginx: [nginx](https://nginx.org/ru/)
- redis: [redis](https://redis.io/)

## Feathures
...
