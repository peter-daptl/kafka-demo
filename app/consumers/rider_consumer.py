import json

import MySQLdb

from .base_consumer import BaseConsumer


class RiderConsumer(BaseConsumer):
    def process(self, msg):
        """
        Processes the message from the Kafka topic, creating or updating riders in the database.
        And adding the rider_id to the message. Sends the message to the ranking consumer.
        """
        message = msg.value()
        try:
            message = json.loads(message)
        except Exception as err:
            self.logger.error(err)
            return

        sql = (
            "INSERT INTO rider (name, country_id, team_id) "
            "VALUES (%(name)s, %(country_id)s, %(team_id)s) "
            "ON DUPLICATE KEY UPDATE name = %(name)s, "
            "country_id = %(country_id)s, team_id = %(team_id)s;"
        )
        params = {
            "name": message["rider"],
            "country_id": message["country_id"],
            "team_id": message["team_id"],
        }

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, params)

        sql = "SELECT rider_id FROM rider where name = %(name)s"
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        message["rider_id"] = rows[0]["rider_id"]

        self.producer.produce(
            "ranking",
            json.dumps(message),
            message["ranking"],
            callback=self.delivery_callback,
        )

        self.producer.poll(1000)
        self.producer.flush()
