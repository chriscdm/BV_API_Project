# BV_API_Project
The purpose of this project is to create an API which will deliver song data in JSON format. My initial plan was to create a flask app and host it using Heroku or another similar service but after discussing the prompt with Scott Wagner I decided to create a Docker image to run the app with.

# Set up instructions:
To run the Docker file you will need to install[Docker](https://docs.docker.com/install/) and [Docker Compose]https://docs.docker.com/compose/install/on your system.

Once Docker and Docker Compose are installed, you can clone this repository (assuming you have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).

Initial commit containing some preliminary work. I set up a virtual python 3 environment and installed the libraries I will need. Created the sqlite db from the script provided in the BV prompt and began working on the script for the app - in its current preliminary stage the app can only deliver the entire songs table in json format. 

Thurs ~ 6:20 - The api now can answer basic get requests involving artist, genre, and song name