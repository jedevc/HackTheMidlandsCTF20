FROM python:3

WORKDIR /usr/src/app/
RUN pip install twisted --no-cache-dir
COPY src/ /usr/src/app/

EXPOSE 10053/tcp
EXPOSE 10053/udp

CMD ["python", "dns.py"]
