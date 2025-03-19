# Use a lightweight Python image
FROM python:3.12-slim AS builder

# Install required dependencies
RUN apt-get update && apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only the requirements file first (for caching efficiency)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the correct port (8501 for Streamlit)
EXPOSE 8503

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8503", "--server.address=0.0.0.0"]

