# MIPS Implementation

## Introduction

This project is for the course CSEN 601 Computer System Architecture.
We implemented pipelined version MIPS using Python 3.7.

## Running the code
1. Input the instructions you want to run in the [Instructions](./Instructions.txt) text file
2. Run the [Main](./main.py) python script where it compiles the code in the Instructions file and prints the output.
###### In the Instructions file there is a sample program written that demos the code.
###### Sample output for that program can be found [here](./SampleOutput.txt)

## Supported Instructions
1. and
2. or
3. add
4. sub
5. slt
6. nor
7. nop
8. lw
9. sw
10. addi
11. beq
12. j
13. jal
14. jra

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
        addi $t0 $0 `0000000000001010`
        ````
* You can add labels to lines of code to jump and branch to example:
    * ```` 
      main: # This is the main
      j exit
      # 'Functions'
      exit:
      ````  
    
    
    
    
    
    
    
    
    
    
    
    
    
    