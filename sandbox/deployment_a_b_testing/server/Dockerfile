FROM python:latest
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY server.py server.py
EXPOSE 5000
CMD python server.py
