docker rm app
docker build --tag=app .
docker run --name=app app
docker run -d -p 80:8080 app