python -m venv venv
venv\Scripts\activate
pip install --trusted-host pypi.python.org -r requirements.txt


49154
https://hub.docker.com/r/splasher2000/find-the-client

1.
docker images,
docker tag find-the-client:latest splasher2000/find-the-client:latest
docker push splasher2000/find-the-client:latest





# Build the container
docker build -t find-the-client .

# login
docker login

# tag the image
docker tag find-the-client splasher2000/find-the-client:0.0.2

# image pushen
docker push splasher2000/find-the-client:latest