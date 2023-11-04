# 
FROM python:3.11.6-slim

# 
WORKDIR /server

# 
COPY requirements.txt ./

# 
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# 
COPY . .

# 
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

# Build image: docker build -t threads-server .
# Run container: docker run -d --name threads-server-container -p 8000:8000 threads-server