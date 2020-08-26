# MIPS Implementation

## Introduction

This project is for the course CSEN 601 Computer System Architecture.
I implemented pipelined version MIPS using Python 3.7.
Datapath diagram is the Logisim implementation of the project and documentation on the Instructions is in this file.

## Running the code
1. Input the instructions you want to run in the [Instructions](./Instructions.txt) text file
2. Run the [Main](./main.py) python script where it compiles the code in the Instructions file and prints the output.
###### In the Instructions file there is a sample program written that demos the code.
###### Sample output for that program can be found [here](./SampleOutput.txt)

## Supported Instructions
1. and
    * Bit-wise and on rs and and rt and stores result in rd
    *   |000000|rs|rt|rd|00000|100100|
        |---|---|---|---|---|---|
        |6|5|5|5|5|6|
2. or
    * Bit-wise or on rs and and rt and stores result in rd
    *   |000000|rs|rt|rd|00000|100101|
        |---|---|---|---|---|---|
        |6|5|5|5|5|6|
3. add
    * Addition of rs and and rt and stores result in rd
    *   |000000|rs|rt|rd|00000|100000|
        |---|---|---|---|---|---|
        |6|5|5|5|5|6|
4. sub
    * Subtraction of rs and and rt and stores result in rd
    *   |000000|rs|rt|rd|00000|100010|
        |---|---|---|---|---|---|
        |6|5|5|5|5|6|
5. slt
    * If rt is less than rs put 1 in rd else 0
    *   |000000|rs|rt|rd|00000|101010|
        |---|---|---|---|---|---|
        |6|5|5|5|5|6|
6. nor
    * Bit-wise nor on rs and and rt and stores result in rd
    *   |000000|rs|rt|rd|00000|100111|
        |---|---|---|---|---|---|
        |6|5|5|5|5|6|
7. nop
    * no operation by shifting reg 0 0 bits to the left
    *   |000000|00000|00000|00000|00000|000000|
        |---|---|---|---|---|---|
        |6|5|5|5|5|6|
8. lw
    * Loads word at base address + offset from memory into register rt
    *   |100011|base|rt|offset|
        |---|---|---|---|
        |6|5|5|16|
9. sw
    * Stores word in register rt into memory at address base + offset
    *   |101011|base|rt|offset|
        |---|---|---|---|
        |6|5|5|16|
10. addi
    * Adds the immediate value to rs and stores it into rt
    *   |001000|rs|rt|immediate|
        |---|---|---|---|
        |6|5|5|16|
11. beq
    * If rs and rt are equal branch to label
    *   |000100|rs|rt|offset|
        |---|---|---|---|
        |6|5|5|16|
12. j
    * unconditional jump to label
    *   |000010|instr_index|
        |---|---|
        |6|26|
13. jal
    * unconditional jump to label and saves return address in register ra
    *   |000011|instr_index|
        |---|---|
        |6|26|
14. jra
    * unconditional jump to address inside register ra
    *   |000111|00000000000000000000000000|
        |---|---|
        |6|26|

## Syntax

### Instruction syntax
1. `and rd rs rt`
2. `or rd rs rt`
3. `add rd rs rt`
4. `sub rd rs rt`
5. `slt rd rs rt`
6. `nor rd rs rt`
7. `nop`
8. `lw rt offset(base)`
9. `sw rt offset(base)`
10. `addi rt rs immediate`
11. `beq rs rt offset`
12. `j label`
13. `jal label`
14. `jra`

### Code syntax
* You can add comments using a pound `#` in the start of the line example:
    *   ````
        # This is a comment
        ````
* You can add white space in between lines of code or in the middle of the instruction and it will be ignored example:
    *    ```` 
         addi $t0, $0, 1 
        
         addi $t1  $0  10
         ````
* You can either use commas `,` between registers and commands or not example:
    *   ````
        and, $t0, $t1, $t2
        and  $t0  $t1  $t2
        ```` 
* You can insert machine code in the middle of the program using back-ticks `` ` `` example:
    *   ````
        `00000000000000000000000000000000`
        ````
* You can replace part of the instruction using machine code with back-ticks `` ` `` example:
    *   ````
        addi $t0 `00000` `0000000000001010`
        ````
* You can add labels to lines of code to jump and branch to example:
    * ```` 
      main: # This is the main
      j exit
      # 'Functions'
      exit:
      ````  
