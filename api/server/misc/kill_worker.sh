kill_celery_worker () {
   ps -ux | grep celery| awk '{print $2}' | xargs kill -9
}

kill_celery_worker
exit 0
