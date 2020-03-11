FROM navikt/python:3.8
COPY . /app
WORKDIR /app
RUN pip3 install poetry && \
    poetry install

RUN cd src/data_catalog_api
RUN uvicorn --version
#ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
CMD ["uvicorn", "main:app"]