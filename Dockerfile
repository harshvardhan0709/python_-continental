FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . . 
# WORKDIR src
# RUN ls
# RUN python manage.py makemigrations

