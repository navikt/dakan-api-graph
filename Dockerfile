FROM sondresimage
COPY . /app
WORKDIR /app
RUN pip3 install poetry && \
    poetry install

RUN cd src/data_catalog_api
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
CMD ["uvicorn", "main:app"]