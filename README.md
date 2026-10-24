# Tiny Virtual Machine for Intermediate Code Execution

## Objective
A stack-based virtual machine that executes a small intermediate-code language, like the target machine after the intermediate code generation stage of a compiler.

## Architecture
.tvm file -> Parser -> Instruction list + Label table -> VM execution loop -> Output

## Components
- Parser: removes comments, finds labels, validates opcodes
- VM: program counter, stack, memory (dictionary), label table
- Cycle: fetch -> decode -> execute -> update PC, repeat until HALT

## Instruction Set
LOADI n  : push integer n
LOAD x   : push value of variable x
STORE x  : pop and save into variable x
ADD, SUB, MUL, DIV, MOD : pop two values, push result
DUP, POP : duplicate / remove top value
EQ, LT, GT : push 1 if true, else 0
JMP label : jump to label
JZ label  : jump if popped value is 0
PRINT : pop and display
HALT  : stop

## How to Run
python main.py programs/addition.tvm
python main.py programs/loop_demo.tvm
python main.py programs/factorial.tvm --show-code --trace

## Viva Line
The VM acts as a target machine for intermediate code. It repeatedly fetches an instruction using the program counter, decodes it, executes it, and updates the stack, memory, and program counter.