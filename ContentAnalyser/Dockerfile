FROM python:3.9

 

ENV PYTHONUNBUFFERED 1

ENV FLASK_APP=manage.py

COPY . /app

 

WORKDIR /app

 



 

RUN pip3 install -r requirements.txt



COPY utils/fields.py /usr/local/lib/python3.9/site-packages/flask_restplus/fields.py



COPY utils/api.py /usr/local/lib/python3.9/site-packages/flask_restplus/api.py



RUN pip3 install Flask-Cors

 

ENTRYPOINT flask run --host=0.0.0.0 --port=5005
