from argparse import ArgumentParser

from app.consumers.base_consumer import BaseConsumer
from app.utils.factory import Factory


class AppLauncher:
    def launch(self):
        """
        Launch the application.
        """
        parser = ArgumentParser(description="Kafka Consumer Launcher")
        parser.add_argument(
            "-t",
            "--topic",
            required=True,
            help="The topic name that will be consumed.",
        )
        args = parser.parse_args()

        consumer = Factory.create_subclass(
            base=BaseConsumer, prefix=args.topic, use_base=False, topic=args.topic
        )
        consumer.parse()


class AppLauncherException(Exception):
    """
    Root exception for any error while attempting to queue tasks.
    """

    pass


if __name__ == "__main__":
    app = AppLauncher()
    app.launch()
