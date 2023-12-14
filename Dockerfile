FROM python:3.11.7-slim
# FROM python:3.10.12-slim

# Maintainer info
LABEL maintainer="neko.liyuu@gmail.com"

# Make working directories
RUN  mkdir -p /myocr-backend-api
WORKDIR  /myocr-backend-api

# Install Pytesseract
ENV PYHTONUNBUFFERED=1
RUN apt-get update\
  && apt-get -y install tesseract-ocr tesseract-ocr-ind

# Upgrade pip with no cache
RUN python -m pip install --no-cache-dir -U pip

# Copy application requirements file to the created working directory
COPY requirements.txt .

# Install application dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy every file in the source folder to the created working directory
COPY  . .

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

# Run the python application
CMD ["./start.sh"]