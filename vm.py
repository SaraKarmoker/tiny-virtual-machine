from instructions import Instruction


class VMError(Exception):
    pass


class TinyVirtualMachine:
    def __init__(self, instructions, labels, trace=False):
        self.instructions = instructions
        self.labels = labels
        self.trace = trace

        self.stack = []
        self.memory = {}
        self.pc = 0
        self.running = True

    def run(self) -> None:
        while self.running:
            if self.pc < 0 or self.pc >= len(self.instructions):
                raise VMError(
                    f"Program counter out of range: {self.pc}. "
                    "Use HALT to end the program."
                )

            instruction = self.instructions[self.pc]

            if self.trace:
                self.print_trace_before(instruction)

            self.execute(instruction)

            if self.trace:
                self.print_trace_after()

    def execute(self, instruction: Instruction) -> None:
        opcode = instruction.opcode
        operand = instruction.operand

        if opcode == "LOADI":
            self.require_operand(instruction)
            self.stack.append(self.to_integer(operand, instruction))
            self.pc += 1

        elif opcode == "LOAD":
            self.require_operand(instruction)
            if operand not in self.memory:
                raise VMError(
                    f"Variable '{operand}' is not defined "
                    f"(line {instruction.line_number})."
                )
            self.stack.append(self.memory[operand])
            self.pc += 1

        elif opcode == "STORE":
            self.require_operand(instruction)
            self.memory[operand] = self.pop_stack(instruction)
            self.pc += 1

        elif opcode == "ADD":
            self.binary_operation(instruction, lambda a, b: a + b)

        elif opcode == "SUB":
            self.binary_operation(instruction, lambda a, b: a - b)

        elif opcode == "MUL":
            self.binary_operation(instruction, lambda a, b: a * b)

        elif opcode == "DIV":
            b = self.pop_stack(instruction)
            a = self.pop_stack(instruction)
            if b == 0:
                raise VMError(f"Division by zero at line {instruction.line_number}.")
            self.stack.append(a // b)
            self.pc += 1

        elif opcode == "MOD":
            b = self.pop_stack(instruction)
            a = self.pop_stack(instruction)
            if b == 0:
                raise VMError(f"Modulo by zero at line {instruction.line_number}.")
            self.stack.append(a % b)
            self.pc += 1

        elif opcode == "DUP":
            self.stack.append(self.peek_stack(instruction))
            self.pc += 1

        elif opcode == "POP":
            self.pop_stack(instruction)
            self.pc += 1

        elif opcode == "EQ":
            self.binary_operation(instruction, lambda a, b: 1 if a == b else 0)

        elif opcode == "LT":
            self.binary_operation(instruction, lambda a, b: 1 if a < b else 0)

        elif opcode == "GT":
            self.binary_operation(instruction, lambda a, b: 1 if a > b else 0)

        elif opcode == "JMP":
            self.jump_to_label(instruction)

        elif opcode == "JZ":
            self.require_operand(instruction)
            condition = self.pop_stack(instruction)
            if condition == 0:
                self.jump_to_label(instruction)
            else:
                self.pc += 1

        elif opcode == "PRINT":
            value = self.pop_stack(instruction)
            print(f"OUTPUT: {value}")
            self.pc += 1

        elif opcode == "HALT":
            self.running = False

        else:
            raise VMError(
                f"Unsupported instruction '{opcode}' at line {instruction.line_number}."
            )

    def binary_operation(self, instruction, operation) -> None:
        b = self.pop_stack(instruction)
        a = self.pop_stack(instruction)
        self.stack.append(operation(a, b))
        self.pc += 1

    def jump_to_label(self, instruction) -> None:
        self.require_operand(instruction)
        if instruction.operand not in self.labels:
            raise VMError(
                f"Label '{instruction.operand}' does not exist "
                f"(line {instruction.line_number})."
            )
        self.pc = self.labels[instruction.operand]

    def pop_stack(self, instruction):
        if not self.stack:
            raise VMError(
                f"Stack underflow at line {instruction.line_number}: "
                f"'{instruction.opcode}' needs a value."
            )
        return self.stack.pop()

    def peek_stack(self, instruction):
        if not self.stack:
            raise VMError(
                f"Stack is empty at line {instruction.line_number}: "
                f"'{instruction.opcode}' needs a value."
            )
        return self.stack[-1]

    def require_operand(self, instruction) -> None:
        if instruction.operand is None:
            raise VMError(
                f"Instruction '{instruction.opcode}' needs an operand "
                f"(line {instruction.line_number})."
            )

    def to_integer(self, value, instruction) -> int:
        try:
            return int(value)
        except ValueError as error:
            raise VMError(
                f"Expected an integer after LOADI at line "
                f"{instruction.line_number}, got '{value}'."
            ) from error

    def print_trace_before(self, instruction) -> None:
        print("\n" + "=" * 58)
        print(f"PC          : {self.pc}")
        print(f"Instruction : {instruction}")
        print(f"Stack before: {self.stack}")
        print(f"Memory      : {self.memory}")

    def print_trace_after(self) -> None:
        print(f"Stack after : {self.stack}")
        print(f"Next PC     : {self.pc}")