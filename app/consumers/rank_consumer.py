import json

from .base_consumer import BaseConsumer


class RankConsumer(BaseConsumer):
    def process(self, msg):
        """
        Processes the message from the Kafka topic, modifying the message from Airflow
        to be less database specific, and flatter for Kafka distributed processing.
        """
        message = msg.value()
        try:
            message = json.loads(message)
        except Exception as err:
            self.logger.error(err)
            return

        reformatted_message = message["values"]
        for fk in message["fks"]:
            reformatted_message[fk["table"]] = fk["values"]["name"]
            for sub_fk in fk["fks"]:
                reformatted_message[sub_fk["table"]] = sub_fk["values"]["name"]
        self.logger.info(reformatted_message)

        self.producer.produce(
            "country",
            json.dumps(reformatted_message),
            reformatted_message["country"],
            callback=self.delivery_callback,
        )

        self.producer.poll(1000)
        self.producer.flush()
