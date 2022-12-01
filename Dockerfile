FROM python:3.10-slim 
# Or any preferred Python version.
ADD src/lambda_function.py .
ADD requirements.txt .
RUN apt-get update
RUN apt install -y libpq-dev python3-dev gcc
RUN pip install -r requirements.txt
CMD ["python3", "./lambda_function.py"] 
# Or enter the name of your unique directory and parameter set.