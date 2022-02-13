FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    gunicorn foodgram.wsgi:application --bind 0:8000
