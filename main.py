import json
import dict2xml
import time
from datetime import datetime
from threading import Thread
import paho.mqtt.client as mqtt

FILENAME = "TEST_MQTT_MESSAGES.json"
FILENAME_XML = "TEST_MQTT_MESSAGES.xml"
topics = {
    "/devices/wb-msw-v3_21/controls/CO2", "/devices/wb-msw-v3_21/controls/Sound Level",
    "/devices/wb-ms_11/controls/Illuminance",   "/devices/wb-msw-v3_21/controls/Temperature",
}
names = [
    'CO2', 'Sound Level', 'Illuminance', 'Temperature']
topics = {k: v for k, v in zip(topics, names)}
__DATE_FORMAT__ = "%H:%M:%S %d-%m-%Y"


def now():
    return datetime.now().strftime(__DATE_FORMAT__)


# функция для записи данных в файл
def write_to_file(userdata: dict):
    if (len(userdata['data'])) == 0:
        return
    with open(FILENAME, "w", encoding='utf8') as f:
        f.write(json.dumps(userdata['data']))

def write_to_file_xml(userdata: dict):
    if (len(userdata['data'])) == 0:
        return
    with open(FILENAME_XML, "w", encoding='utf8') as f:
        f.write(dict2xml.dict2xml({"Data": {"Record": userdata['data']}}))


def write_to_file_csv(userdata: dict):
    if (len(userdata['data'])) == 0:
        return
    with open(FILENAME_XML, "w", encoding='utf8') as f:
        f.write(f"{userdata.}")

# функция подписчик на сообщения от топиков
def on_msg(client: mqtt.Client, userdata: dict, msg: mqtt.MQTTMessage):
    key = 'cur_data'
    field = topics[msg.topic]
    userdata[key][field] = msg.payload.decode()
    print(field, msg.payload.decode(), now())
    if sorted(userdata[key].keys() - ['Date', 'Number']) == sorted(names):
        userdata[key]["Date"] = now()
        userdata[key]['Number'] = 26
        userdata['data'].append(dict(userdata[key]))
        print("I live", len(userdata['data']), now())
        # остановка получения на 5с
        time.sleep(5)


def do(client: mqtt.Client):
    client.loop_start()
    while True:
        time.sleep(5)
        if not client.is_connected():
            break

if __name__ == "__main__":
    data = {
    'data': [], 'cur_data': dict()
}

    cli = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=data)
    host = "192.168.2.26"
    cli.connect(host)
    cli.on_message = on_msg
    cli.subscribe([(topic, 0) for topic in topics.keys()])
    thread = Thread(target=lambda: do(cli))
    thread.start()
    thread.join(60)
    cli.disconnect()
    write_to_file(data)
    write_to_file_xml(data)



