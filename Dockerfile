FROM python:3.7.2
MAINTAINER Chris Marker "chris.d.marker@gmail.com"
COPY . /Users/christophermarker/Documents/BV_API_Project
WORKDIR /Users/christophermarker/Documents/BV_API_Project/api
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["api_script.py"]