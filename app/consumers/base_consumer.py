from pathlib import Path

import MySQLdb
import yaml
from confluent_kafka import Consumer, Producer

from app import logger


class BaseConsumer:

    def __init__(self, topic):
        self.configure()
        self.topic = topic
        self.logger = logger

    def configure(self):
        """
        Loads the configuration from the config.yaml file.
        """
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        config_path = f"{BASE_DIR}/app/config/config.yaml"

        config_source = {}

        with open(config_path) as f:
            config_source = yaml.safe_load(f.read())

        self.consumer = Consumer(config_source["kafka-broker"])
        self.producer = Producer(config_source["kafka-broker"])
        self.connection = MySQLdb.connect(**config_source["database"])
        self.connection.autocommit(True)

    def delivery_callback(self, err, msg):
        """
        Callback function for the producer.
        """
        if err:
            self.logger.error(f"ERROR: Message failed delivery: {err}")
        else:
            self.logger.info(
                "Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(),
                    key=msg.key().decode("utf-8"),
                    value=msg.value().decode("utf-8"),
                )
            )

    def parse(self):
        """
        Subscribes to the topic and polls for new messages from Kafka.
        """
        self.consumer.subscribe([self.topic])
        # Poll for new messages from Kafka and print them.
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    # Initial message consumption may take up to
                    # `session.timeout.ms` for the consumer group to
                    # rebalance and start consuming
                    # logger.info()
                    self.logger.info("Waiting...")
                elif msg.error():
                    self.logger.error(f"ERROR: {msg.error()}")
                else:
                    self.process(msg)
                    # Extract the (optional) key and value, and print.
                    # reformat message designed for SQL and flatten it for easier kafka development
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            self.consumer.close()
            self.producer.flush()
