FROM python:3.9

WORKDIR /geolocation-api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./meta ./meta
COPY ./model ./model
COPY ./route ./route
COPY ./util ./util
COPY app.py .

CMD ["python", "app.py", "-t", "API_KEY", "-i", "0.0.0.0", "-p", "5000"]