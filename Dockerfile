FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

# Expose
EXPOSE  5000

# Run
CMD ["python", "./app.py"]