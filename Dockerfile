FROM python:3.6.3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
COPY main.py ./
CMD ["python", "main.py"]

