FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
WORKDIR /code/venv
RUN pip install git+https://github.com/douwevandermeij/admin-totals.git
WORKDIR /code
ADD . /code/
RUN python manage.py migrate