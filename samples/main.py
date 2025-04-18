import sys
from utime import sleep
from random import randint

# If your device needs wifi before running uncomment and adapt the code below as necessary
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "password")
while not wlan.isconnected():
    pass
print('Network config:', wlan.ipconfig('addr4'))

try:
    import iotc
except:
    import mip
    mip.install('github:jcaldeira-iot/iot-central-micropython-client/package.json')
    import iotc
    
from iotc import IoTCClient, IoTCConnectType, IoTCLogLevel, IoTCEvents

scope_id = 'scope-id'
device_id = 'device-id'
key = 'device or symmetric key'
conn_type = IoTCConnectType.DEVICE_KEY#SYMM_KEY

client = IoTCClient(scope_id, device_id, conn_type, key)
client.set_log_level(IoTCLogLevel.ALL)

def on_properties(name, value):
    print('Received property {} with value {}'.format(name, value))
    return value


def on_commands(command, ack):
    print('Command {}.'.format(command.name))
    ack(command, command.payload)

def on_enqueued(command):
    print('Enqueued Command {}.'.format(command.name))


client.on(IoTCEvents.PROPERTIES, on_properties)
client.on(IoTCEvents.COMMANDS, on_commands)
client.connect()

client.send_property({'readOnlyProp':40})

while client.is_connected():
    client.listen()
    json_msg = {'temperature':randint(0,20),'pressure':randint(0,20),'acceleration':{'x':randint(0,20),'y':randint(0,20)}}
    print('Sending telemetry:', json_msg)
    client.send_telemetry(json_msg)
    sleep(2)
