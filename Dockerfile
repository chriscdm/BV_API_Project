FROM python:3.7.2
COPY . /Users/christophermarker/Documents/BV_API_Project
WORKDIR /Users/christophermarker/Documents/BV_API_Project/api
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["api_script.py"]