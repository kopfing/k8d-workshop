# Use a minimal base image with Python
FROM python:3.12-slim

# Create a working directory
WORKDIR /app

# Add a simple HTML file
RUN echo '<h1>Hello World! Everything is working!</h1>' > index.html

# Expose port
EXPOSE 8080

# Serve the HTML file using Python's built-in HTTP server
CMD ["python", "-m", "http.server", "8080"]
