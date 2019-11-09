docker rm app
docker build --tag=app .
docker run --name=app app
docker run -p 8080:8080 app