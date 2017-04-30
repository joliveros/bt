FROM codequants/notebook:latest

USER root

COPY . ./bt

WORKDIR ./bt

RUN pip install -e .

RUN python ./setup.py nosetests
