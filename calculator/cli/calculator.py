#!/usr/bin/env python3
"""
CLI Calculator - Simple Command Line Calculator
==============================================

Features:
- Basic math operations (+, -, *, /, **)
- Continuous calculation (use previous result)
- Clean and user-friendly interface
- Improved error handling
- Logging for debugging and monitoring
"""

import sys
import operator
import logging
from typing import Union, Optional


# Configure logging
logging.basicConfig(
    filename="calculator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Calculator:
    """Simple calculator class"""

    def __init__(self):
        self.memory: Optional[float] = None
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '%': operator.mod
        }

    def calculate(self, expression: str) -> Union[float, str]:
        """
        Calculates the given expression
        """

        expression = expression.strip().replace(' ', '')

        if not expression:
            logging.warning("User entered empty expression")
            return "Please enter an expression"

        # Check special commands
        if expression.lower() in ['quit', 'exit', 'q']:
            logging.info("User requested program exit")
            return 'quit'

        if expression.lower() in ['clear', 'c']:
            self.memory = None
            logging.info("Memory cleared by user")
            return "Memory cleared"

        if expression.lower() in ['memory', 'm']:
            logging.info("User checked memory value")
            return f"Memory: {self.memory if self.memory is not None else 'Empty'}"

        # Replace 'ans' with previous result if exists
        if 'ans' in expression.lower() and self.memory is not None:
            expression = expression.lower().replace('ans', str(self.memory))

        try:
            result = self._safe_eval(expression)
            self.memory = result

            logging.info(f"Calculation successful: {expression} = {result}")

            return result

        except ZeroDivisionError:
            logging.error(f"Division by zero attempted in expression: {expression}")
            return "Error: Division by zero!"

        except ValueError as e:
            logging.error(f"Invalid value in expression {expression}: {str(e)}")
            return f"Error: Invalid value - {str(e)}"

        except Exception as e:
            logging.error(f"Unexpected error for expression {expression}: {str(e)}")
            return f"Error: {str(e)}"

    def _safe_eval(self, expression: str) -> float:
        """
        Safe mathematical expression evaluation
        """

        allowed_chars = set('0123456789+-*/.()% ')

        if not all(c in allowed_chars for c in expression):
            logging.warning(f"Invalid character detected in expression: {expression}")
            raise ValueError("Invalid character")

        allowed_names = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "pow": pow,
            "max": max,
            "min": min
        }

        return eval(expression, allowed_names)


def print_banner():
    """Prints the startup banner"""

    print("=" * 50)
    print("🧮  CLI CALCULATOR  🧮")
    print("=" * 50)
    print("Commands:")
    print("  • Math operations: +, -, *, /, **, %")
    print("  • Previous result: 'ans' or 'memory'")
    print("  • Clear memory: 'clear' or 'c'")
    print("  • Exit: 'quit', 'exit' or 'q'")
    print("=" * 50)
    print("Examples:")
    print("  > 2 + 3")
    print("  > ans * 4")
    print("  > (5 + 3) ** 2")
    print("=" * 50)


def main():
    """Main program loop"""

    calc = Calculator()

    logging.info("Calculator program started")

    print_banner()

    while True:
        try:
            expression = input("\n📱 Calculator > ").strip()

            if not expression:
                continue

            result = calc.calculate(expression)

            if result == 'quit':
                print("\n👋 Goodbye!")
                logging.info("Calculator program terminated by user")
                break

            if isinstance(result, (int, float)):
                print(f"📊 Result: {result}")

                if result != int(result):
                    print(f"📊 Rounded: {round(result, 6)}")

            else:
                print(f"💬 {result}")

        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
            logging.info("Program interrupted by keyboard (Ctrl+C)")
            break

        except EOFError:
            print("\n\n👋 Exiting...")
            logging.info("Program terminated by EOF")
            break


if __name__ == "__main__":
    main()
