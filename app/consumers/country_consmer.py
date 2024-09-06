import json

import MySQLdb

from .base_consumer import BaseConsumer


class CountryConsumer(BaseConsumer):
    def process(self, msg):
        """
        Processes the message from the Kafka topic, creating or updating countries in the database.
        And adding the country_id to the message. Sends the message to the team consumer.
        """
        message = msg.value()
        try:
            message = json.loads(message)
        except Exception as err:
            self.logger.error(err)
            return

        sql = (
            "INSERT INTO country (name) "
            "VALUES (%(name)s) "
            "ON DUPLICATE KEY UPDATE name = %(name)s;"
        )
        params = {"name": message["country"]}

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, params)

        sql = "SELECT country_id FROM country where name = %(name)s"
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        message["country_id"] = rows[0]["country_id"]

        self.producer.produce(
            "team",
            json.dumps(message),
            message["team"],
            callback=self.delivery_callback,
        )

        self.producer.poll(1000)
        self.producer.flush()
