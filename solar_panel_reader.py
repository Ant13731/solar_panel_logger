# import serial

# Importing Libraries
import io
import serial
import time
import datetime
import re
import socketio

run_local_log = True
run_reader = True

port = '/dev/cu.usbmodem14201'
port = 'COM3'

# socketio_server = "http://localhost:5000"
socketio_server = "http://127.0.0.1"
socketio_port = "9000"

sio = socketio.Client(ssl_verify=False)
@sio.event
def connect():
    print("Connected")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on("SHUTDOWN")
def shutdown(data):
    print("Shutting down")
    exit()

@sio.on("Stop")
def shutdown(data):
    print("Stopping processes, shutting down")
    global run_reader 
    run_reader = False
    time.sleep(2)
    exit()

@sio.on("Pause Local Data")
def shutdown(data):
    print("Pausing the recording of local data")

@sio.on("Start Local Data")
def shutdown(data):
    print("Starting the recording of local data") 


@sio.on("ERROR")
def shutdown(data):
    print("Received error, shutting down")
    exit()


def run_voltage_reader(arduino: serial.Serial, sio: socketio.Client, file: io.TextIOWrapper):
    while run_reader:
        # digital representation of voltage as an integer from 0 to 1023 (10 bit resolution), where value == 1023 means the panel is giving 5 volts
        value = str(arduino.readline())
        timestamp = datetime.datetime.now()
        value = re.findall(r'\d+', value)
        if value != []:
            #value seems to be lower by a factor of 5 (according to voltmeter)
            voltage = int(value[0]) * 5 / 1023
            print(voltage)
            sio.emit("analytics", {"voltage": voltage, "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")})
            if run_local_log:
                file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S") + ", " + str(voltage) + "\n")
    file.close()

if __name__ == "__main__":
    arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    sio.connect(socketio_server + ":" + socketio_port, auth = {}, wait_timeout=10)
    sio.emit("test", {"foo":"bar"})

    if run_local_log:
        file = open("voltage_log.csv", "w")
        file.write("Time, Voltage")

    run_voltage_reader(arduino, sio, file)

    



# # arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)
# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data
# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(value) # printing the value