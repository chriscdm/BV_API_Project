# BV_API_Project
The purpose of this project is to create an API which will deliver song data in JSON format. My initial plan was to create a flask app and host it using Heroku or another similar service but after discussing the prompt with Scott Wagner I decided to create a Docker image to run the app with.

# Set up instructions:
To run the Docker file you will need to install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on your system.

Once Docker and Docker Compose are installed, you can clone this repository (assuming you have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)) and change several directory paths.

Open ```Dockerfile``` and you should see this:

```
FROM python:3.7.2
MAINTAINER Chris Marker "chris.d.marker@gmail.com"
COPY . /Users/christophermarker/Documents/BV_API_Project
WORKDIR /Users/christophermarker/Documents/BV_API_Project/api
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["api_script.py"]
```
Change the paths for COPY and WORKDIR to the correct path for where you cloned the repository.

Next, open ```docker-compose.yml``` and you should see the following:

```
version: '2'
services:
    web:
        build: .
        ports:
            - "5000:5000"
        volumes:
            - .:/Users/christophermarker/Documents/BV_API_Project
        environment:
            - PORT:5000
```

Again, change the path under volumes: to match where you have the repository saved.

Once these changes have been made, navigate to the BV_API_Project in your terminal and run and:

```
docker-compose up
```

This command will create a  container with all necessary dependencies and run the API inside of it. The app will run on local host port 5000.

At this point the API can be called using a method of your choosing, in the ```test_notebook.ipynb``` file I show several example of this using the Requests Library in Python.

The API has several functions:
1. It can return a list of all songs in the library, a request would look like:
```
http://127.0.0.1:5000/all_songs
```
The response will include a JSON with songs, artist, genre name, and duration data.

2. It can return information regarding available genres in the database, a request would look like this:
```
http://127.0.0.1:5000/genres
```
The response will include a JSON with data on all 9 genres. The data will include the aggregated duration of all songs in that genre, the total number of all songs in that genre, the genre name, and the genre database ID.

3. It can search the database based on artist, song, genre, minimum song length, or maximum song length. The api can accept song length in either seconds (ex. 195) or a time string (ex. 00:03:15 or 03:15). some requests might looks like:
```
http://127.0.0.1:5000/songs?artist=Bobby+Darin
http://127.0.0.1:5000/songs?artist=Beatles&genre=Classic+Rock
http://127.0.0.1:5000/songs?min_length=194&max_length=196
```
The response will include a JSON with songs, artist, genre name, and duration data.




Initial commit containing some preliminary work. I set up a virtual python 3 environment and installed the libraries I will need. Created the sqlite db from the script provided in the BV prompt and began working on the script for the app - in its current preliminary stage the app can only deliver the entire songs table in json format. 

Thurs ~ 6:20 - The api now can answer basic get requests involving artist, genre, and song name