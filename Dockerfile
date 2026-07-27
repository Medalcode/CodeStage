FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

# Install system dependencies
RUN apt-get update && apt-get install -y git ffmpeg wget unzip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone SadTalker
RUN git clone https://github.com/OpenTalker/SadTalker.git /app/SadTalker

WORKDIR /app/SadTalker

# Replace numpy version restriction to avoid build errors on Python 3.10
RUN sed -i 's/numpy==1.23.4/numpy/g' requirements.txt

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir edge-tts

# Download models
RUN bash scripts/download_models.sh

WORKDIR /app

# CMD will keep the container running so we can execute scripts inside it, or just run the scripts directly
CMD ["tail", "-f", "/dev/null"]
