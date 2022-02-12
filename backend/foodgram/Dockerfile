FROM python:3.8
COPY ./ /app
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt
WORKDIR /app/
CMD python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    gunicorn foodgram.wsgi:application --bind 0:8000
