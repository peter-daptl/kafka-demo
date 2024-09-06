## Demo Kafka Cycling Consumer Launcher: Dynamic Topic Consumption

This application is a flexible Kafka consumer launcher that simplifies starting consumers for specific topics. It dynamically creates and runs a consumer based on the topic you provide.

**Before You Begin:**

**Requirements:**

* Python 3.12
* Pipenv
* Docker

**Setup Steps:**

1. **RedPanda Environment:** Ensure you have started the Kafka environment using the instructions from [https://github.com/peter-daptl/RedPanda-Kafka-Environment](https://github.com/peter-daptl/RedPanda-Kafka-Environment). Remember to use the provided bash script to create the topics you need.
2. **Airflow Demo Setup:** Run `docker compose up` from the root of the [https://github.com/peter-daptl/airflow-demo/tree/kafka](https://github.com/peter-daptl/airflow-demo/tree/kafka) project (ensure you are on the `kafka` branch). Make sure all connections, variables, and database configurations are complete. You might need to trigger the DAG to ensure data is parsed and published to a topic.

**Running the Consumer:**

1. From the root of this project, run `docker compose up` to launch the containers needed for the consumers.


**How it Works:**

1. The application utilizes `argparse` to interpret arguments provided through the command line.
2. Based on the specified topic, it dynamically creates a consumer class using a Factory design pattern.
3. The created consumer then handles processing messages received from the chosen Kafka topic.
4. The docker compose file will run a container for each topic used in this cycling rankings demo, creating parent and child records in the database, and modifying the message for the next step in the process.

**Extending the Application:**

To implement new consumer types for different topics:

1. Create a new consumer class that inherits from the base class `BaseConsumer`.
2. Implement the necessary methods for your unique consumer logic.
3. Name your class following the format `<TopicName>Consumer`.

The Factory mechanism will automatically detect and use your new consumer class whenever the corresponding topic is specified.

**Error Handling:**

This application defines a custom exception named `AppLauncherException` to manage errors specifically related to the launching process.
