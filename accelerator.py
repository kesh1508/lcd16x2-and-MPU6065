import RPi_I2C_driver
import smbus
from time import sleep

# Initialize the LCD
mylcd = RPi_I2C_driver.lcd()

# Initialize the MPU6050
bus = smbus.SMBus(1)
Device_Address = 0x68

# MPU6050 Registers
ACCEL_XOUT_H = 0x3B

# Function to initialize MPU6050
def MPU_Init():
    bus.write_byte_data(Device_Address, 0x6B, 0x00)

# Function to read raw accelerometer data
def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

# Function to determine movement direction
def get_movement_direction(acc_x):
    if acc_x > 0:
        return "Forward"
    elif acc_x < 0:
        return "Backwrd"
    else:
        return "Stationary"

# Initialize MPU6050
MPU_Init()

print("Reading Data of Gyroscope and Accelerometer")

while True:
    # Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H) / 16384.0
    
    # Determine movement direction
    movement_direction = get_movement_direction(acc_x)

    # Display on LCD
    mylcd.lcd_clear()
    mylcd.lcd_display_string(f"Movement:{movement_direction}", 1)

    sleep(0.1)
