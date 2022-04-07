# Zenjob Platform Challenge
## How To?

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This repo contains code to create a Docker image which will create a file on AWS S3 and it will also delete files from S3 bucket which are older than 24 hours. 
To test the functionality, you need to provide the AWS Access_KEY & SECRET_KEY while running the container.

```sh
docker run -e ENV=<qa || staging> -e ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID> -e SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY> -itd <IMAGE_ID>
```
This repo also contains the terraform code to create a K8s cluste, namespaces and S3 buckets on AWS.

## TODOS:
- Docker Registry Secret creation is still manual
- Cron Job creation on K8s to schedule our pod to run in 5 mins is in progress
