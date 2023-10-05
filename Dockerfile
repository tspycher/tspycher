#
FROM python:3.11
ENV PIP_ROOT_USER_ACTION=ignore

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./tspycher /code/tspycher

#
CMD ["uvicorn", "tspycher.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
