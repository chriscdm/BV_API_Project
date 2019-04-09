# BV_API_Project
The purpose of this project is to create an API which will deliver song data in JSON format. My initial plan was to create a flask app and host it using Heroku or another similar service but after discussing the prompt with Scott Wagner I decided to create a Docker image to run the app with.

# Set up instructions:
To run the Docker file you will need to install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on your system.

Once Docker and Docker Compose are installed, you can clone this repository (assuming you have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)), navigate to the BV_API_Project in your terminal, and run  the following (may require root privileges):

```
docker-compose build

docker-compose up
```

This command will create a  container with all necessary dependencies and run the API inside of it. The app will run on localhost port 5000.

At this point the API can be called using any language or utility that can issue HTTP GET requests, in the ```test_notebook.ipynb``` file I show several examples of this using the requests library in Python.  Additionally, you can open ```http://127.0.0.1:5000/``` in a web browser to display some basic information about the API.

The API has several functions:
1. It can return a list of all songs in the library, a request would look like:
```
http://127.0.0.1:5000/all_songs
```
The response will include a JSON object with songs, artist, genre name, and duration data.

2. It can return information regarding available genres in the database, a request would look like this:
```
http://127.0.0.1:5000/genres
```
The response will include a JSON object with data on all 9 genres. The data will include the aggregated duration of all songs in that genre, the total number of all songs in that genre, the genre name, and the genre database ID.

3. It can search the database based on artist, song, genre, minimum song length, or maximum song length. The api can accept song length in either seconds (ex. 195) or a time string (ex. 00:03:15 or 03:15). Some requests might looks like:
```
http://127.0.0.1:5000/songs?artist=Bobby+Darin
http://127.0.0.1:5000/songs?artist=Beatles&genre=Classic+Rock
http://127.0.0.1:5000/songs?min_length=194&max_length=196
```
The response will include a JSON object with songs, artist, genre name, and duration data.

# Additional Questions
## 1. Are there any suggestions you could make about the structure of our data?
For the purposes of this project, merging the songs and genres table could reduce some overhead by eliminating the need for joins. Additionally, the length of the varchar could be reduced for the artist and song fields.
## 2. What fields would you index in these tables?
I would index the fields being queried in the API - songs.artist, songs.songs, songs.duration, and genres.name. Indexing these fields would decrease the time needed to perform the queries.


