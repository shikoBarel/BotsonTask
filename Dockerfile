FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash"]