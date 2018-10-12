# Project Title

Portcast - Cyclone Crawler

## Description

Portcast - Cyclone Crawler
The cyclone information from  http://rammb.cira.colostate.edu/products/tc_realtime/index.asp will be crawled and stored in postgres db.
Only the new data will be added to the db. We have 2 different docker containers for the python project and postgres db.

### Prerequisites

Docker

Add GPG key
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Add Docker repo.
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"```
```

Update packages.
```
sudo apt-get update
```

Docker repo might be different in differnt version of linux.
```
apt-cache policy docker-ce
```

Install Docker
```
sudo apt-get install -y docker-ce
```

check status
```
sudo systemctl status docker
```

### Installing

Get docker-compose.
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```
Clone the project. to whichever location you may like.

Running the docker-compose.yml to get or env up with 2 containers of postgres and python crawler.

```
sudo docker-compose run web
```

We have 2 containers now.
We need to create database in postgres container.
password : postgres

```
sudo docker exec -it postgres psql -h db -U postgres --password
postgres=# create database portcast;
```

Run again the python container it will do nothing beside executing spider because the containers are already created previously.
```
sudo docker-compose run web

```

## Running the tests

execute this command with the docker python container, to test upper bound and lower bound of request and response. With some tags data.
```
scrapy check -l
```

execute this command with the docker python container, to test fake data with our http response.
```
python3 tests.py
```

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style
```
followed pep-8 and pylint.
```

Explain what these tests test and why

```
Give an example
```

## Author

**Sumit Singh Kanwal**

