FROM python:3.9

COPY src/. /usr/src/metabot/
WORKDIR /usr/src/metabot
COPY requirements.txt .

RUN \
 python3 -m pip install --upgrade pip && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 rm requirements.txt

EXPOSE 8080
CMD ["python", "metabot.py"]