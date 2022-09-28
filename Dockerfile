FROM python:3.10

# Copy requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Install necessary libraries
RUN python3 -m pip install -r /app/requirements.txt

# Copy python scripts and db
COPY ./database /app/database
COPY ./flaskr /app/flaskr

WORKDIR /app/flaskr

# If the database does not exist, create it
RUN if test -f ../database/birthday.db; then echo "Database created, skipping creation process.."; else python3 init-db.py; fi

# Expose port 5000
EXPOSE 5000

# Run server
CMD ["python3", "hello.py"]
