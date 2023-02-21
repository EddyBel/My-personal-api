# Use python in the alpine distribution to be lighter in weight.
FROM python:3.9.16-alpine3.17

# The work area will be the internal app folder.
WORKDIR /app

# Environment variables to be used
ARG PORT=3000
ARG DEBUG=False
ARG SECRET_KEY=encryption_key
ARG ROOT_USERNAME=username
ARG ROOT_PASSWORD=123456
ARG EMAIL_SENDER=example@gmail.com
ARG PASSWORD_SENDER=123456
ARG EMAILS_ADDRESSEE=example@gmail.com
ARG USER_GITHUB=username
ARG TOKEN_GITHUB=user_token
ARG REPO_NOTES=name_repository

# Copy the requirements for the app to work correctly.
COPY ./requeriments.txt /app/requeriments.txt

# Install the necessary requirements from the copied file.
RUN pip install -r requeriments.txt

# Time copy all project files to the work area.
COPY . /app

# Specifies the port to expose.
EXPOSE 3000

# Execute the command to initialize the project.
CMD ["python3", "app.py"]
