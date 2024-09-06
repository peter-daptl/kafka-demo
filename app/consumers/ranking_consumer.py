import json

import MySQLdb

from .base_consumer import BaseConsumer


class RankingConsumer(BaseConsumer):
    def process(self, msg):
        """
        Processes the message from the Kafka topic, creating or updating rankings in the database.
        """
        message = msg.value()
        try:
            message = json.loads(message)
        except Exception as err:
            self.logger.error(err)
            return

        sql = (
            "INSERT INTO `rank` (rider_id, ranking, season, week, points) "
            "VALUES (%(rider_id)s, %(ranking)s, %(season)s, %(week)s, %(points)s) "
            "ON DUPLICATE KEY UPDATE rider_id = %(rider_id)s, "
            "ranking = %(ranking)s, season = %(season)s, "
            "week = %(week)s, points = %(points)s;"
        )
        params = {
            "rider_id": message["rider_id"],
            "ranking": message["ranking"],
            "season": message["season"],
            "week": message["week"],
            "points": message["points"],
        }

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, params)
        self.logger.info(f"INSERTED/UPDATED {message['rider']} for week {message['week']}")
