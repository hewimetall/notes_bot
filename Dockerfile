FROM python:3.10-rc-buster
WORKDIR /app
COPY . .
RUN  pip install -r requirements.txt
CMD python main.py