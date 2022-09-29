FROM python:3.10

# Copy requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Install necessary libraries
RUN python3 -m pip install -r /app/requirements.txt

# Copy python scripts
COPY ./flaskr /app/flaskr

WORKDIR /app/flaskr

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:80", "hello:create_app()"]
