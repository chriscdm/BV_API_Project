FROM python:3.7.2
MAINTAINER Chris Marker "chris.d.marker@gmail.com"
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY ./ /src 
WORKDIR /src/api
ENTRYPOINT ["python"]
CMD ["api_script.py"]