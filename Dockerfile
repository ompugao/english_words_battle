FROM python:3.6.3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

RUN mkdir -p /ewb/src
COPY src/ /ewb/src
