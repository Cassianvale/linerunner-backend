#!/bin/bash
PkgName='linerunner-backend'
Dockerfile='./Dockerfile'
DockerContext=../
LogFile='build.log'

echo "$(date '+%Y-%m-%d %H:%M:%S') - Start build image..." >> $LogFile
docker build -f $Dockerfile -t $PkgName $DockerContext >> $LogFile 2>&1
if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅✅✅ Build docker image success !" >> $LogFile
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅✅✅ exit 0" >> $LogFile
    exit 0
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌❌❌ Build docker image failed !" >> $LogFile
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌❌❌ exit 1" >> $LogFile
    exit 1
fi