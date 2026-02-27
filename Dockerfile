# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
# Note: Excluding visual libraries not needed for backend to keep image light if desired,
# but keeping them simple for now.
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ backend/
COPY models/ models/

# Expose port
EXPOSE 8000

# Run the application
# We assume the app is in backend/app.py, so module is backend.app
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
