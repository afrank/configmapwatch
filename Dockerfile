FROM python:3

COPY watch.py /

RUN pip3 install watchdog

CMD python3 /watch.py /opt/config
