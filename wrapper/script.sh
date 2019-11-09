docker rm wrapper
docker build --tag=wrapper .
docker run --name=wrapper wrapper
docker run -p 80:80 wrapper