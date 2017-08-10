FROM python:3.6

RUN mkdir /root/tldr

ADD start.py requirements.txt /root/tldr/
ADD server /root/tldr/server
ADD middlewares /root/tldr/middlewares
ADD utils /root/tldr/utils
ADD endpoints /root/tldr/endpoints
ADD context /root/tldr/context
ADD assets /root/tldr/assets

RUN mkdir /root/tldr/cache

RUN pip install -r /root/tldr/requirements.txt

EXPOSE 3001
ENTRYPOINT cd /root/tldr && \
           export PYTHONPATH=/root/tldr && \
           python /root/tldr/start.py
