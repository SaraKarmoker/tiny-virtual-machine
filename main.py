import argparse
from parser import ParserError, parse_program
from vm import TinyVirtualMachine, VMError


def main() -> None:
    argument_parser = argparse.ArgumentParser(
        description="Tiny Virtual Machine for intermediate code execution."
    )
    argument_parser.add_argument(
        "program_file", help="Path of the .tvm intermediate-code file"
    )
    argument_parser.add_argument(
        "--trace", action="store_true",
        help="Show instruction-by-instruction VM execution",
    )
    argument_parser.add_argument(
        "--show-code", action="store_true",
        help="Display parsed intermediate code before execution",
    )

    args = argument_parser.parse_args()

    try:
        instructions, labels = parse_program(args.program_file)

        if args.show_code:
            print("\n--- PARSED INTERMEDIATE CODE ---")
            for index, instruction in enumerate(instructions):
                print(f"{index:02d}: {instruction}")

            print("\n--- LABEL TABLE ---")
            if labels:
                for label, address in labels.items():
                    print(f"{label} -> {address}")
            else:
                print("No labels found.")

            print("\n--- EXECUTION STARTED ---")

        vm = TinyVirtualMachine(instructions, labels, trace=args.trace)
        vm.run()

        print("\n--- EXECUTION FINISHED SUCCESSFULLY ---")
        print(f"Final stack : {vm.stack}")
        print(f"Final memory: {vm.memory}")

    except (ParserError, VMError) as error:
        print(f"\nVM ERROR: {error}")


if __name__ == "__main__":
    main()