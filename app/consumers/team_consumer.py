import json

import MySQLdb

from .base_consumer import BaseConsumer


class TeamConsumer(BaseConsumer):
    def process(self, msg):
        """
        Processes the message from the Kafka topic, creating or updating teams in the database.
        And adding the team_id to the message. Sends the message to the rider consumer.
        """
        message = msg.value()
        try:
            message = json.loads(message)
        except Exception as err:
            self.logger.error(err)
            return

        sql = (
            "INSERT INTO team (name) "
            "VALUES (%(name)s) "
            "ON DUPLICATE KEY UPDATE name = %(name)s;"
        )
        params = {"name": message["team"]}

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, params)

        sql = "SELECT team_id FROM team where name = %(name)s"
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        message["team_id"] = rows[0]["team_id"]

        self.producer.produce(
            "rider",
            json.dumps(message),
            message["rider"],
            callback=self.delivery_callback,
        )

        self.producer.poll(1000)
        self.producer.flush()
