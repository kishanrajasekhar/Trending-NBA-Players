FROM python:alpine3.6
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "my_nba_flask_test.py" ]
