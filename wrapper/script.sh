docker stop wrapper
docker rm wrapper
export cid=$(docker run -d -p 80:8080 --name=wrapper wrapper)
echo $cid
exit 1
