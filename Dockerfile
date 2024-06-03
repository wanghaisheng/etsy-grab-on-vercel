FROM python:3.9

WORKDIR /app

RUN curl -sS https://dl.google.com/linux/linux_signing_key.pub | apt-key add - &&
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >/etc/apt/sources.list.d/google.list &&
    apt-get update &&
    apt-get install xvfb libjpeg-dev ffmpeg google-chrome-stable -y --no-install-recommends --fix-missing

COPY requirements.txt .
RUN pip install --upgrade pip &&
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
