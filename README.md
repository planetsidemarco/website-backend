# Website Backend

FastAPI python server allowing access to specific AWS EC2 server files and the ability to upload files to AWS S3 bucket.

## Docker

Building docker container with command: ```docker build --no-cache -t backend .```

Running detached docker container with command: ```docker run -it --rm -p 8000:8000 -v $(pwd):/usr/src/app -d backend```
