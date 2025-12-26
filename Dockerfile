FROM python:3.11-slim
WORKDIR /app
COPY . .
#AI file used in the project- GROQ
RUN pip install --no-cache-dir groq python-dotenv  
CMD ["python", "main.py"]
