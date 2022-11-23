# Zinnia+ (MCPU5+)

An 8 bit RISC CPU for [TinyTapeout02](www.tinytapeout.com). Tinytapeout combines a high number of tiny designs on a single IC to be taped out with the Open MPW-7. This offers the opportunity to actually get a design made on a real IC, but also comes with some constraints:

- Maximum allowed area is 150 x 170 µm² in Skywater 130nm CMOS technology. The actual number of useable gates depends on cell size and routing limitations.
- Only eight digital inputs and eight digital outputs are allowed.
- I/O will be provided via the scanchain (a long shift register) and is hence rather slow.

This is a slightly upgraded version of MCPU5 that was submitted for tinytapeout01. See MCPU repository [here](https://github.com/cpldcpu/tinytapeout_mcpu5).
# Content of repository

  - [src/](src/) Cleaned up source, Testbench, Assembler and code examples
  - See below for design description
# Design Description

## Top level

The strict limitations on I/O do not allow implementing a normal interface with bidirectional data bus and separate address bus. One way of addressing this would be to reduce the data width of the CPU to 4 bit, but this was deemed to limiting. Another option, implementing a serial interface, appeared too slow and too complex.

Instead the I/Os were allocated as shown below.

<p align="center">
  <img width=400 src='https://user-images.githubusercontent.com/4086406/188716014-33053217-c1a6-4cac-afc2-257b7203d407.png'>
</p>

The CPU is based on the Harvard Architecture with separate data and program memories. The data memory is completely internal to the CPU. The program memory is external and is accessed through the I/O. All data has to be loaded as constants through machine code instructions.

Two of the input pins are used for clock and reset, the remaining ones are reserved for instructions and are six bit in length. The output is multiplexed between the program counter (when clk is '1') and the content of the main register, the Accumulator. Accessing the Accumulator allows reading the program output.

## Programmers Model

<p align="center">
  <img src='https://user-images.githubusercontent.com/4086406/188716065-a4d7755b-9020-4291-94e4-f22cf04bb168.png'>
</p>

Besides simplifying the external interface, the Harvard Architecture implementation also removes the requirement to interleave code and data access on the bus. Every instruction can be executed in a single clock cycle. Due to this, no state machine for micro-sequencing is required and instructions can be decoded directly from the inst[5:0] input.

All data operations are performed on the accumulator. In addition, there are eight data registers. The data registers are implemented as a single port memory based on latches, which significantly reduced are usage compared to a two port implementation. The Accu is complemented by a single carry flag, which can be used for conditional branches.

Handling of constants is supported by the integer flag („I-Flag“), which enables loading an eight bit constant with two consecutive 6 bit opcodes.

## Instruction Set Architecture

The list of instructions and their encoding is shown below. One challenge in the instruction set design was to encode the target address for branches. The limited opcode size only allows for a four bit immediate to be encoded as a maximum. Initially, I considered introducing an additional segment register for long jumps, but ultimately decided to introduce relative addressing for conditional branches and a long jmp instruction that is fed from the accumulator. 

Having both NOT and NEG may seems excessive, but the implementation was cheap on resources and some instruction sequences could be simplified.

No boolean logic instructions (AND/OR/NOT/NOR/XOR) are supported since they were not needed in any of my typical test programs.

![grafik](https://user-images.githubusercontent.com/4086406/188716202-d0681200-9578-414f-8c06-417b6ae8950d.png)

The table below shows common instruction sequences that can be realized with macros.

![grafik](https://user-images.githubusercontent.com/4086406/188716303-d0428667-788e-4f98-bd4b-40d5c7e23e4d.png)

## Design after placement and routing

The total cell count after synthesis is 489. Adding any additional features did not allow to complete the routing pass.The summary and floorplan below shows the synthesis result for 115x115µm² area, however the design fits perfectly into 100x100µm² as well.

![grafik](https://user-images.githubusercontent.com/4086406/188730917-91d6c818-d903-449f-bae3-42abefd206a6.png)

![grafik](https://user-images.githubusercontent.com/4086406/188715948-98719648-8b37-4218-b3ca-6674cf783abc.png)

## Summary

Zinnia+ (MCPU5+) is a successful 8 bit processor implementation considering the TinyTapeout contraints. Both Fibonacci and prime search algorithms were successfully ported and run in the testbench.
## Original TinyTapeout Readme
-----

![](../../workflows/wokwi/badge.svg)

Go to https://tinytapeout.com for instructions!
