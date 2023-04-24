import asyncio
import random
from azure.iot.device import (
    IoTHubSession,
    MQTTError,
    MQTTConnectionFailedError,
)


CONNECTION_STRING = "HostName=MikeFirstIotHub.azure-devices.net;DeviceId=MyDesktop;SharedAccessKey=dYiBxRV+D0LE8qajhQs2VX329/fEvlrnyqVYvszfHvU="
TOTAL_MESSAGES_SEND = 0
SWITCH = True


async def send_telemetry(session):
    global TOTAL_MESSAGES_SEND
    global SWITCH
    while True:
        if SWITCH:
            TOTAL_MESSAGES_SEND+=1
            FakeData = "{id:"+str(TOTAL_MESSAGES_SEND)+", temperature:"+str(random.randint(1,50))+" , humidity:"+str(random.randint(1,100))+"}"

            print("Sending Message:"+FakeData)
            await session.send_message(FakeData)
            print("Send complete")
        await asyncio.sleep(5)
        


async def receive_c2d_messages(session):
    global SWITCH
    async with session.messages() as messages:
        print("Waiting to receive messages...")
        async for message in messages:
            print("Message received: {}".format(message.payload))
            if message.payload == "OPEN":
                SWITCH = True
            elif message.payload == "CLOSE":
                SWITCH = False

async def main():
    print("Press Ctrl-C to exit")
    while True:
        try:
            print("Connecting to IoT Hub...")
            async with IoTHubSession.from_connection_string(CONNECTION_STRING) as session:
                print("Connected to IoT Hub")
                await asyncio.gather(
                    send_telemetry(session),
                    receive_c2d_messages(session)
                )

        except MQTTError:
            print("Dropped connection. Reconnecting in 1 second")
            await asyncio.sleep(1)
        except MQTTConnectionFailedError:
            print("Could not connect. Retrying in 10 seconds")
            await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Exit application because user indicated they wish to exit.
        # This will have cancelled `main()` implicitly.
        print("User initiated exit. Exiting.")
    finally:
        print("End Message Send")