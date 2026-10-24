from dataclasses import dataclass
from typing import Optional


@dataclass
class Instruction:
    opcode: str
    operand: Optional[str] = None
    line_number: int = 0

    def __str__(self) -> str:
        if self.operand is None:
            return self.opcode
        return f"{self.opcode} {self.operand}"