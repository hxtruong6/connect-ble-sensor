import logging
import asyncio

from bleak import BleakClient
from bleak import _logger as logger

CHARACTERISTIC_UUID = "f000aa65-0451-4000-b000-000000000000"  # <--- Change to the characteristic you want to enable notifications from.
ADDRESS = "24:71:89:cc:09:05"  # <--- Change to your device's address here if you are using Windows or Linux

SLEEP_TIME = 2
TIME_OUT = 20


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("---> Notification handler:\t {0}: {1}".format(sender, data))


def disconnect_callback(client: BleakClient):
    print("xxxxx Client with address {} got disconnected!".format(client.address))


async def connect_to_device(address: str, debug=True):
    if debug:
        import sys
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    while True:
        print("Waiting connect to sensor....")
        try:
            async with BleakClient(address, timeout=TIME_OUT, disconnected_callback=disconnect_callback) as client:
                # await client.connect();
                is_connected = await client.is_connected()
                if is_connected:
                    print("Connected to Device")

                    await client.start_notify(
                        CHARACTERISTIC_UUID, notification_handler,
                    )
                    while True:
                        if not is_connected:
                            print("Device disconnected!!!")
                            break
                        await asyncio.sleep(SLEEP_TIME)
                        print("=========")

                    # await client.stop_notify(CHARACTERISTIC_UUID)
                else:
                    print(f"Failed to connect to Device")
        except Exception as e:
            print(f"Exception when connect: {e}")

        print(f"\n---Reconnect! Sleep {SLEEP_TIME} seconds!")
        await asyncio.sleep(SLEEP_TIME)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    task = asyncio.ensure_future(connect_to_device(ADDRESS, debug=True))
    loop.run_until_complete(task)
