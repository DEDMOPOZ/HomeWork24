# Run Project using Docker
docker-compose up -d --build
docker-compose exec backend python manage.py migrate --noinput
docker-compose exec backend python manage.py collectstatic --no-input --clear
docker-compose up
