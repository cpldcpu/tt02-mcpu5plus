# RP2040 upython program
# Read inputs from TT02 board
from machine import Pin
import utime

# Pins mapping
# Pin   Label  Function
# 19    in0    GPIO14
# 20    in1    GPIO15
# 21    in2    GPIO16
# 22    in3    GPIO17
# 24    in4    GPIO18
# 25    in5    GPIO19
# 26    in6    GPIO20
# 27    in7    GPIO21

# 12    out0   GPIO9
# 11    out1   GPIO8
# 10    out2   GPIO7
# 9     out3   GPIO6
# 29    out4   GPIO22
# 31    out5   GPIO26
# 32    out6   GPIO27
# 34    out7   GPIO28

OUT_PINS = [28, 27, 26, 22, 6, 7, 8, 9]  # List of out pin numbers
IN_PINS = [21, 20, 19, 18, 17, 16, 15, 14]  # List of in pin numbers

def initialize_gpio():
    # Initialize in pins  GPIO as input
    for pin in IN_PINS:
        Pin(pin, Pin.IN)

    # Initialize out pins GPIO as input
    for pin in OUT_PINS:
        Pin(pin, Pin.IN)

def read_in_pins():
    # Read in pins and combine into a byte
    byte = 0
    for pin in IN_PINS:
        value = Pin(pin, Pin.IN).value()
        byte = (byte << 1) | value

    return byte

def read_out_pins():
    # Read out pins and combine into a byte
    byte = 0
    for pin in OUT_PINS:
        value = Pin(pin, Pin.IN).value()
        byte = (byte << 1) | value

    return byte

initialize_gpio()

while True:
    in_byte = read_in_pins()
    out_byte = read_out_pins()
    print("IN: ", hex(in_byte), "OUT: ", hex(out_byte), "CLK: ", clk)
    utime.sleep_ms(100)
    