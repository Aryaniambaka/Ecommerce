FROM python:3.12-slim
WORKDIR /usr/src/app
COPY requirement.txt ./
RUN pip install -r requirement.txt
COPY . .
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]