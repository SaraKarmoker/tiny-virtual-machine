# Tiny Virtual Machine for Intermediate Code Execution

A stack-based virtual machine that executes a simple intermediate code language, built for the Compiler Design project (Project-Based Learning).

## About the Project

A compiler first converts source code into intermediate code. This project builds a small virtual machine (VM) that reads that intermediate code and runs it one instruction at a time.

Source Code -> Intermediate Code -> Tiny VM -> Output

The `.tvm` file is the intermediate code. The Tiny VM acts as the target machine.

## System Architecture

.tvm file -> Parser -> Instruction list + Label table -> VM -> Output

## Working Cycle

Fetch -> Decode -> Execute -> Update -> Repeat until HALT

1. Fetch: take the instruction the Program Counter (PC) points to
2. Decode: identify the instruction and its operand
3. Execute: do the work using the stack and memory
4. Update: change the stack, memory, and PC
5. Repeat until HALT

## Main Parts

- Parser: reads and checks the .tvm file
- Stack: keeps numbers while calculating
- Memory: keeps variables and their values
- Label table: remembers where each label is
- Program Counter (PC): shows which instruction runs now

## Instruction Set

| Instruction | Meaning |
|---|---|
| LOADI n | Put the number n on the stack |
| LOAD x | Put the value of variable x on the stack |
| STORE x | Save the top value into variable x |
| ADD, SUB, MUL, DIV, MOD | Calculations on the top two values |
| EQ, LT, GT | Compare two values (1 = true, 0 = false) |
| JMP label | Always jump to the label |
| JZ label | Jump to the label if the top value is 0 |
| DUP | Copy the top value |
| POP | Remove the top value |
| PRINT | Show the top value as output |
| HALT | Stop the program |

## Project Structure

tiny-virtual-machine/
- main.py : starts the program and reads command-line options
- parser.py : reads and checks the .tvm file
- instructions.py : stores each instruction
- vm.py : runs the instructions
- programs/ : addition.tvm, loop_demo.tvm, factorial.tvm
- outputs/ : saved outputs of the programs
- README.md

## Requirements

- Python 3.11 or newer
- No extra libraries needed

## How to Run

Run the addition program:

    python main.py programs/addition.tvm

Run the loop program:

    python main.py programs/loop_demo.tvm

Run the factorial program:

    python main.py programs/factorial.tvm

Show the parsed code and label table:

    python main.py programs/factorial.tvm --show-code

Show step-by-step execution (trace mode):

    python main.py programs/addition.tvm --trace

## Example Program (addition.tvm)

    LOADI 10
    LOADI 20
    ADD
    PRINT
    HALT

Output:

    OUTPUT: 30

## Error Handling

The VM shows a clear message for:
- Division by zero
- Stack underflow (empty stack)
- Unknown instruction
- Undefined variable
- Missing label

Screenshots
Addition Program
Addition Output
Loop Program
Loop Output
Factorial Program
Factorial Output
Trace Mode (Addition Program)
Trace Start
Trace End

## Author

Susmita Karmoker Saraboni
B.Tech CSE, Brainware University