FROM python:3.10

# Copy requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Install necessary libraries
RUN python3 -m pip install -r /app/requirements.txt

# Copy python scripts and db
COPY ./flaskr /app/flaskr

WORKDIR /app/flaskr

# Expose port 5000
EXPOSE 5000

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "hello:create_app()"]
