FROM python:3.12

WORKDIR /workspace

COPY src /workspace/src
COPY requirements.txt /workspace/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt

ENTRYPOINT ["python", "src/main.py"]