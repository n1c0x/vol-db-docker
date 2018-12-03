# vol-db-docker

To compile the container, execute `sudo docker-compose build`. 
To launch the docker, execute `sudo docker-compose up`

To compile the container WITH A PROXY, run `sudo docker-compose build --build-arg HTTP_PROXY=http://xx.xx.xx.xx:xx --build-arg HTTPS_PROXY=http://xx.xx.xx.xx:xx`

Configuration source : https://docs.docker.com/compose/django/ and https://www.supinfo.com/articles/single/5779-bien-debuter-avec-django-docker
