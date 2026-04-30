FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8278

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8278"]
