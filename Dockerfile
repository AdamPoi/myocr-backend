FROM python:3.11.7
# FROM python:3.10.12

# Maintainer info
LABEL maintainer="neko.liyuu@gmail.com"

# Make working directories
RUN  mkdir -p  /myocr-backend-api
WORKDIR  /myocr-backend-api

# Upgrade pip with no cache
# RUN pip install --no-cache-dir -U pip

# Copy application requirements file to the created working directory
COPY requirements.txt .

# Install application dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy every file in the source folder to the created working directory
COPY  . .

# Run the python application
CMD ["uvicorn", "main:app"]