# Use a base image with Python installed
FROM python:3.11-slim

# Install required packages (including build tools and OpenGL libraries)
RUN apt-get update && \
    apt-get install -y gcc g++ patchelf libgl1-mesa-glx libglib2.0-0 libglib2.0-dev && \
    python3 -m pip install --upgrade pip

# Upgrade pip, setuptools, and wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Nuitka
RUN python3 -m pip install nuitka

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project folder into the container
COPY . /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Compile the Python script using Nuitka for Linux
RUN python3 -m nuitka main.py --onefile --output-filename=linuxpackager

# Run the generated Linux binary
CMD ["./linuxpackager"]