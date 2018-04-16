FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install grpcio
RUN pip install grpcio-tools

# Expose
EXPOSE  5000

# Run
CMD ["python", "./app.py"]