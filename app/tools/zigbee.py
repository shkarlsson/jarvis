from paho.mqtt import client as mqtt_client
import logging
import time

from app.helpers.env_vars import (
    HIVEMQ_PASSWORD,
    MACHINE_NAME,
    MQTT_BROKER_IP,
    MQTT_BROKER_PORT,
)


# Copied from JiaNao
def connect_to_mqtt(
    topic,
    on_message=None,
    try_no=1,
):
    try:
        client = mqtt_client.Client(
            # mqtt_client.CallbackAPIVersion.VERSION1,
            client_id="",
            userdata=None,
            protocol=mqtt_client.MQTTv5,
        )

        result = client.connect(MQTT_BRIDGE_IP, MQTT_BRIDGE_PORT)
        if result > 0:
            logging.warning(
                {
                    0: "Connection successful",
                    1: "Connection refused - incorrect protocol version",
                    2: "Connection refused - invalid client identifier",
                    3: "Connection refused - server unavailable",
                    4: "Connection refused - bad username or password",
                    5: "Connection refused - not authorised",
                }[result]
            )

        if topic is not None:
            client.subscribe(topic, qos=1)

            if on_message is not None:
                client.on_message = on_message

            # TODO: Make sure all functions that use this start the loop themselves.
            # client.loop_start()

        return client

    #  Dealing with OSError: [Errno 113] No route to host

    except OSError as e:
        logging.warning(
            f"Could not connect to {MQTT_BROKER_IP}:{MQTT_BROKER_PORT} with topic {topic}. Error: {e}"
        )
        if try_no > 5:
            raise e

        logging.warning("Trying again in 5 seconds.")
        time.sleep(5)
        return connect_to_mqtt(
            topic,
            on_message,
            try_no=try_no + 1,
        )


client = connect_to_mqtt("zigbee2mqtt/#")


def get_devices():
    result = client.publish("zigbee2mqtt/bridge/config/devices/get", qos=1)

    return result


client.publish(topic, payload)
