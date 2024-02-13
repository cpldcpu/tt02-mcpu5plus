# RP2040 upython program to execute a program on the Zinnia 89 bit MCU on the TinyTapeOut with RP2040 attached
# https://www.tinytapeout.com/runs/tt02/078/

from machine import Pin
import utime
import sys

# Filename of the program as a smal object file. The file needs to be uploaded to the RPico filesystem
program_filename = "primes.o"

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

OUT_PINS = [28, 27, 26, 22, 6, 7, 8, 9]  # List of out pin numbers, inverse order
IN_PINS = [21, 20, 19, 18, 17, 16, 15, 14]  # List of in pin numbers
IN_CLK = 14 # In clock on GPIO9
IN_RES = 15 # In clock on GPIO9

# Instruction encoding

BCC = const(0b000000)  # Branch if carry clear
LDI = const(0b010000)  # Load simm4
ADD = const(0b100000)  # Add reg8
STA = const(0b101000)  # Store reg8
LDA = const(0b110000)  # Load reg8
NOT = const(0b111000)  # Not accu
NEG = const(0b111001)  # Negate accu
OUT = const(0b111011)  # Output accu

def initialize_gpio():
    # Initialize in pins  GPIO as input
    for pin in IN_PINS:
        Pin(pin, Pin.IN)

    # Initialize out pins GPIO as input
    for pin in OUT_PINS:
        Pin(pin, Pin.IN)

def set_clk(clk):
    # Set the clock to high or low
    Pin(IN_CLK, Pin.OUT).value(clk)

def set_res(res):
    # Set the clock to high or low
    Pin(IN_RES, Pin.OUT).value(res)

# write instruction to in2-in7
def write_inst(inst):
    for i in IN_PINS[:6]:
        Pin(i, Pin.OUT).value(inst & 0b00100000)
        inst <<= 1

def tic():
    utime.sleep_us(500)    # about 1kHz clock seems to work with slow_clk set to maximum

def reset():
    set_res(0)
    set_clk(0)
    tic()
    set_clk(1)
    tic()
    set_res(1)
    set_clk(0)
    tic()
    set_clk(1)
    tic()
    set_res(0)
    set_clk(0)
    tic()

def execonecycle():
    set_clk(1)
    tic()
    out_pc = read_out_pins() # memory is directly updated upon PC change, assuming async SRAM
    write_inst(Memory[out_pc])    
    set_clk(0)
    tic()
    out_accu = read_out_pins()
    return out_pc, out_accu

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

# read program binary file

Memory  = [-1 for _ in range(0,256)]
PC      = 0
#   Read program (SMAL Output)

with open(program_filename, 'r') as file:
    for currentline in file.readlines():
        number = currentline.strip().rpartition('#')[2]
        cmd = currentline.strip()[0]
        if cmd == '.':
            try:
                PC = int(number, 16)
            except:
                pass
        elif cmd == 'B':        
            Memory[PC] = int(number, 16)
            # print(hex(PC), hex(Memory[PC]))
            PC = PC + 1

# Reset Zinnia MCU
PC=0
Cycles=0
write_inst(Memory[0])    
reset()

# Test program
while True:
    PCnext,accu=execonecycle()

    if Memory[PC] == OUT:
        print("Output: ", hex(accu), str(accu), " @PC:", hex(PC), " Cycles:", Cycles)

    # print("PC: ", hex(PC), "ACC: ", hex(accu), "PCnext")  # debug every instruction
    PC=PCnext
    Cycles+=1
