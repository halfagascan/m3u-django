FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/code/code/entrypoint.sh"]

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh


COPY . /code/
