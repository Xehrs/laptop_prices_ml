# Get base image from Docker site
FROM python 

# WORKDIR /project_app
WORKDIR . 

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
