# base image  
FROM python:3.9
   
# setup environment variable  
#ENV DockerHOME=/root  

# set work directory  

# where your code lives  
WORKDIR /app

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
  
# copy whole project to your docker home directory. 
COPY . .
RUN pip3 --version  
COPY manage.py .
RUN ls -a

# run this command to install all dependencies  
RUN pip3 install -r requirements.txt
  
# port where the Django app runs  
#EXPOSE 8000
  
# start server
CMD python3 manage.py makemigrations
CMD python3 manage.py migrate  
CMD python3 manage.py runserver 0.0.0.0:8080  
