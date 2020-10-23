FROM python:3.8-alpine

WORKDIR /usr/src/app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./templates/* ./templates/
COPY ./app.py ./flag.txt ./password.txt ./code.zip ./

EXPOSE 4000

CMD ["python", "app.py"]
