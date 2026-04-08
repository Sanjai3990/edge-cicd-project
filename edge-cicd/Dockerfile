# ─────────────────────────────────────────────────────────────────
#  Dockerfile — Edge Sensor Node
#  Packages the Flask app into a lightweight Docker container
#  that can run on any edge device (Raspberry Pi, server, cloud VM)
# ─────────────────────────────────────────────────────────────────

# Step 1: Use a lightweight Python base image
FROM python:3.11-slim

# Step 2: Set working directory inside the container
WORKDIR /app

# Step 3: Copy dependency list first (helps Docker cache layers)
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the application source code
COPY app.py .

# Step 6: Expose port 5000 (Flask default)
EXPOSE 5000

# Step 7: Health check — Docker will ping this to verify container health
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Step 8: Run the Flask application
CMD ["python", "app.py"]
