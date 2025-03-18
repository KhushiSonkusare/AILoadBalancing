FROM python:3.9-slim

WORKDIR /app

# Copy your packages folder and requirements file into the container
COPY packages/ ./packages
COPY requirements.txt .

# Install using packages
RUN pip install -r requirements.txt


# Copy the rest of your application files
COPY . .

CMD ["python", "app.py"]
