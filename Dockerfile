FROM navikt/python:3.8
COPY . /app
WORKDIR /app

USER root

RUN pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

USER apprunner

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
CMD ["uvicorn", "dakan_api_graph.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "warning"]
