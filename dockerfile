FROM python:latest

# Install the docker module
RUN pip install docker

WORKDIR /app

#COPY the remote file at working directory in container
COPY app.py ./
# Now the structure looks like this '/app/app.py'

CMD [ "python", "./app.py"]