import io
import re
import time
import datetime
import serial
import socketio

# Just in case something isn't working as expected.
debug = True
# Determines whether we record solar panel voltage locally.
# Can be started/stopped remotely via the socketio
# "Pause Local Data" and "Start Local Data" events. 
run_local_data = True
# Determines whether we emit solar panel voltage events.
# Can be started/stopped remotely via the socketio
# "Pause Socketio Data" and "Start Socketio Data" events. 
run_socketio_data = True
# Breaks the main reader loop when false.
# Can be turned to false remotely via the socketio "Stop" event.
run_reader = True
# When starting the script, determines whether we should append new data
# to the existing local voltage or overwrite the existing data.
# (False means we overwrite existing data)
append_local_data_to_existing = False

# Which port on your computer the arduino is connected to.
# See https://support.arduino.cc/hc/en-us/articles/4406856349970-Select-board-and-port-in-Arduino-IDE
# for more information on where to find the arduino's connected port.
arduino_port = 'COM3'

# Socketio setup
socketio_server = "http://127.0.0.1"
socketio_port = "9000"

sio = socketio.Client(ssl_verify=False)
@sio.event
def connect():
    print("Connected to socketio server")

@sio.event
def connect_error(data):
    print("Socketio connection failed")
    global run_reader 
    run_reader = False
    time.sleep(2)
    exit()

@sio.event
def disconnect():
    print("Socketio disconnected")
    global run_reader 
    run_reader = False
    time.sleep(2)
    exit()

@sio.on("shutdown")
def shutdown(data):
    print("Shutting down")
    global run_reader 
    run_reader = False
    time.sleep(2)
    exit()

@sio.on("error")
def shutdown(data):
    print("Received error, shutting down")
    global run_reader 
    run_reader = False
    time.sleep(2)
    exit()

@sio.on("stop")
def stop(data):
    print("Stopping processes, shutting down")
    global run_reader 
    run_reader = False
    time.sleep(2)
    exit()

@sio.on("pause_local_data")
def pause_local_data(data):
    print("Pausing the recording of local data")
    global run_local_data
    run_local_data = False

@sio.on("start_local_data")
def start_local_data(data):
    print("Starting the recording of local data") 
    global run_local_data
    run_local_data = True

@sio.on("pause_socketio_data")
def pause_socketio_data(data):
    print("Pausing the emission of socketio data")
    global run_socketio_data
    run_socketio_data = False

@sio.on("start_socketio_data")
def start_socketio_data(data):
    print("Starting the emission of socketio data") 
    global run_socketio_data
    run_socketio_data = True


# In a loop, run_voltage_reader collects voltage information from the `arduino` (by reading its standard output),
# then emits a "voltage" event via the `sio` client and records the same data locally through the `file`.
def run_voltage_reader(arduino: serial.Serial, sio: socketio.Client, file: io.TextIOWrapper):
    while run_reader:
        # This value will become the digital representation of voltage
        # as an integer from 0 to 1023 (10 bit resolution),
        # where `value == 1023` means the panel is generating 5 volts of electricity.
        value = str(arduino.readline())
        timestamp = datetime.datetime.now()
        value = re.findall(r'\d+', value)
        # Only send if we have a value. We dont want to read in non-numeric entries from the arduino.
        if value != []:
            # Need to scale value by the highest readable voltage (5 volts on arduino)
            # divided by the digital resolution of the signal
            # (1024 possible numbers can be read by the arduino's analog input, where 1023 is equivalent to 5 volts)
            voltage = int(value[0]) * 5 / 1023
            # When testing with my actual solar panel, the reported voltage here
            # was about 5 times lower than the voltmeter's reading, so scale by 5.
            # (This may need to change depending on what solar panel you use)
            voltage *= 5

            if run_socketio_data:
                sio.emit("voltage", {"voltage": voltage, "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")})
            if run_local_data:
                file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S") + ", " + str(voltage) + "\n")
            if debug:
                print("Time:", timestamp.strftime("%Y-%m-%d %H:%M:%S") + ", " + str(voltage), "- Received voltage:", voltage)
    file.close()

if __name__ == "__main__":
    # The baudrate must be the same as the argument for Serial.begin() in solar_panel_logger.ino.
    arduino = serial.Serial(port=arduino_port, baudrate=9600, timeout=.1)
    # If the program does not get past this point with an exception from the `serial` package,
    # check the value of arduino_port.
    if debug:
        print("Connected to arduino.")
    sio.connect(socketio_server + ":" + socketio_port, auth = {}, wait_timeout=10)
    sio.emit("test", {"foo":"bar"})
    if debug:
        print("Sent test event.")

    if append_local_data_to_existing:
        file = open("voltage_log.csv", "a")
    else:
        file = open("voltage_log.csv", "w")
        file.write("Time, Voltage")

    run_voltage_reader(arduino, sio, file)