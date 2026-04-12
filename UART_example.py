#!/usr/bin/python3
import time
import serial

print("UART Demonstration Program")
print("NVIDIA Jetson Nano Developer Kit")


msg_buffer = ""
time_last_sent_command = time.time()
time_last_recv_command = time.time()
prev_ack_index = 0
command_period = 0.02
end_of_packet = 0
commanded_vel = 1
pico_id = -1
pairing_cooldown_s = 1
time_last_pair_attempted = time.time()
id_file = "UART_pico_id.txt"


serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=38400,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)
serial_port.reset_input_buffer()


def write_number(number: int) -> None:
    with open(id_file, 'w') as f:
        f.write(str(number))

def read_number() -> int:
    with open(id_file, 'r') as f:
        return int(f.read().strip())

def increment_number() -> int:
    number = read_number() + 1
    write_number(number)
    return number


def send_command():
    global end_of_packet, commanded_vel
    for i in range(8):
        serial_port.write(commanded_vel.to_bytes(1, byteorder='big'))
    serial_port.write(end_of_packet.to_bytes(1, byteorder='big'))

    commanded_vel += 1
    if (commanded_vel > 255): 
        commanded_vel = 1


def send_paring_ack():
    global time_last_pair_attempted, pairing_cooldown_s, pico_id
    if (time.time() - time_last_pair_attempted > pairing_cooldown_s):
        pico_id = increment_number()
        serial_port.write(b'ACK:ID')
        serial_port.write(end_of_packet.to_bytes(1, byteorder='big'))
        print("Pico Reboot Detected, assigning new ID")
        time_last_pair_attempted = time.time()


def process_msg():
    global msg_buffer, pico_id, time_last_recv_command, prev_ack_index
    while (serial_port.in_waiting > 0):
        data = serial_port.read()
        if(data == b'\x00'):
            if (len(msg_buffer) > 0): print(str(pico_id) + '>' + msg_buffer)
            msg_buffer = ""
            time_last_recv_command = time.time()
        else:
            if "ACK:" in msg_buffer:
                index = int.from_bytes(data, "big")
                if (index != prev_ack_index+1 and prev_ack_index != 255): print("SELF>NONSEQUENTIAL_ACK")
                prev_ack_index = index
                msg_buffer += str(index)
            else:
                msg_buffer += data.decode("utf-8", errors="replace")

            if "REQ:ID" in msg_buffer:
                send_paring_ack()


try:
    pico_id = read_number()
    while True:
        if (time.time() - time_last_sent_command >= command_period):
            send_command() #Test
            time_last_sent_command = time.time()    

        process_msg()

        if (time.time() - time_last_recv_command > command_period*3):
            time_last_recv_command = time.time()
            print("SELF>DID_NOT_RECV_PACKET")
      
except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass


