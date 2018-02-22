#!/bin/bash

pushd `dirname ${BASH_SOURCE[0]}`
img=`docker build . | grep -Po '(?<=Successfully built )[0-9a-f]+'`
if [ $? -ne 0 ]; then
    echo "Could not build docker image"
    exit 1
fi
container=`docker run -d ${img} tail -f /dev/null`
if [ $? -ne 0 ]; then
    echo "Could not build docker container"
    exit 1
fi

echo ${img}
echo ${container}
docker exec -it ${container} bash
popd
