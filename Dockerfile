FROM python:3.8


RUN pip install --upgrade pip


EXPOSE 50001


ADD . /app
COPY requirements.txt /app


WORKDIR /app

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt

CMD flask run --host=0.0.0.0 --port=50001