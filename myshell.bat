@echo off
cd /d "C:\Users\priti\OneDrive\Documents\Shell"
docker run -it --env-file .env -v "%cd%:/app" geekdecode/my-ai-shell
