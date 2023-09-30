# Use the official Python image
FROM python:3.8-slim

# Define the working directory
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that the app will run on
EXPOSE 8050

# Command to run the application
CMD ["python3", "dashInvestiments.py"]
