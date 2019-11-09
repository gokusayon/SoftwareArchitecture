docker stop app
docker rm app
export cid=$(docker run -d -p 8080:8080 --name=app app)
echo $cid
exit 1
