FROM python:3.9
WORKDIR /app
COPY app/ /app/
COPY templates/ /app/templates/
RUN pip install -r requirements.txt
CMD ["python", "app.py"]