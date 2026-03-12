FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies without cache
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]