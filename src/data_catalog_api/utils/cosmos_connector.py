import os
import tornado.iostream
from data_catalog_api.utils.logger import Logger

from dotenv import load_dotenv
from gremlin_python.driver import client, serializer, protocol


class CosmosConnector(Logger):

    def __init__(self):
        super().__init__()
        self._connection = self._get_db_connection()

    def submit(self, query):
        try:
            return self._submit_query(query)
        except (tornado.iostream.StreamClosedError, protocol.GremlinServerError):
            self._logger.warning("Stream closed, reconnecting to database")
            self._connection.close()
            self._connection = self._get_db_connection()
            return self._submit_query(query)

    def _submit_query(self, query):
        data = self._connection.submitAsync(query).result()
        results = []

        if data is not None:
            for result in data:
                results.extend(result)
            return results
        else:
            self._logger.warning(f"No results returned from query: {query}")

    def _get_db_connection(self) -> client.Client:
        try:
            return self._setup_cosmosdb_con()
        except KeyError:
            self._logger.warning("Getting env variables from .env file")
            load_dotenv()
            return self._setup_cosmosdb_con()

    def _setup_cosmosdb_con(self) -> client.Client:
        return client.Client(os.environ["cosmosDBServer"], 'g',
                             username=os.environ["cosmosDBUsername"],
                             password=os.environ["cosmosDBPassword"],
                             message_serializer=serializer.GraphSONSerializersV2d0())
