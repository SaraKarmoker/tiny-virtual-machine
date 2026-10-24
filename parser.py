from pathlib import Path
from instructions import Instruction


VALID_OPCODES = {
    "LOADI", "LOAD", "STORE", "ADD", "SUB", "MUL", "DIV", "MOD",
    "DUP", "POP", "EQ", "LT", "GT", "JMP", "JZ", "PRINT", "HALT",
}


class ParserError(Exception):
    pass


def remove_comment(line: str) -> str:
    return line.split("#", 1)[0].strip()


def parse_program(file_path: str) -> tuple[list[Instruction], dict[str, int]]:
    path = Path(file_path)

    if not path.exists():
        raise ParserError(f"Program file not found: {file_path}")

    raw_lines = path.read_text(encoding="utf-8").splitlines()

    instructions = []
    labels = {}

    for line_number, raw_line in enumerate(raw_lines, start=1):
        line = remove_comment(raw_line)

        if not line:
            continue

        if ":" in line:
            label, remaining = line.split(":", 1)
            label = label.strip()
            remaining = remaining.strip()

            if not label:
                raise ParserError(f"Empty label at line {line_number}")

            if label in labels:
                raise ParserError(f"Duplicate label '{label}' at line {line_number}")

            labels[label] = len(instructions)
            line = remaining

            if not line:
                continue

        parts = line.split()
        opcode = parts[0].upper()
        operand = " ".join(parts[1:]) if len(parts) > 1 else None

        if opcode not in VALID_OPCODES:
            raise ParserError(f"Unknown instruction '{opcode}' at line {line_number}")

        instructions.append(
            Instruction(opcode=opcode, operand=operand, line_number=line_number)
        )

    if not instructions:
        raise ParserError("The program contains no instructions.")

    return instructions, labels