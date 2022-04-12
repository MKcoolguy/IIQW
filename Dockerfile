FROM python:3.8

# install all dependencies here
#RUN conda install -c conda-forge flask
#RUN conda install -c conda-forge flask-bootstrap
#RUN npm install -g firebase-tools
RUN pip install Flask gunicorn
#RUN pip install Flask
#RUN pip install flask-bootstrap
#RUN pip install pyrebase

COPY . Website/
WORKDIR /Website

ENV PORT 8080

CMD exec gunicorn -- bind :$PORT --workers 1 -- threads 8 app:app