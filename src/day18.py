from typing import List


class Stack:
    """
    A classical LIFO data structure.
    """

    def __init__(self):
        """
        Creates an empty stack.
        """

        self.elements = []

    def push(self, element):
        """
        Pushes the given element onto the stack.
        """

        self.elements.append(element)

    def pop(self):
        """
        Removes and returns the most-recently pushed element from the stack.
        """

        if self.is_empty():
            raise RuntimeError("stack is empty")

        return self.elements.pop()

    def __len__(self):
        """
        Returns the number of elements in the stack.
        """

        return len(self.elements)

    def peek(self):
        """
        Returns but does not remove the most-recently pushed element in the stack.
        """

        if self.is_empty():
            raise RuntimeError("stack is empty")

        return self.elements[-1]

    def is_empty(self):
        """
        Returns True if the stack contains no elements. Returns False otherwise.
        """

        return len(self.elements) == 0


def evaluate(expr: str, equal_precedence: bool) -> int:
    """
    Evaluates the given arithmetic expression consisting of only "+", "*", nonnegative integers,
    parentheses, and spaces. Assumes the expression is well-formed and is written in infix notation.
    If equal_precedence is True, then the "+" and "*" operators have equal precedence. Otherwise,
    "+" has higher precedence than "*".
    """

    def tokenize(expr: str) -> List[str]:
        """
        Returns a list of the tokens in the given arithmetic expression in order of appearance
        from left to right. A token is either a number, "+", "*", "(", or ")".
        """

        result = []
        i = 0

        while i < len(expr):
            if expr[i] == "+" or expr[i] == "*" or expr[i] == "(" or expr[i] == ")":
                result.append(expr[i])
                i += 1
            else:
                start = i

                while i < len(expr) and expr[i].isdigit():
                    i += 1

                if start != i:
                    result.append(expr[start:i])
                else:
                    i += 1

        return result

    def postfix_notation(tokens: List[str], equal_precedence: bool) -> List[str]:
        """
        Given an arithmetic expression written in infix notation using the given tokens, returns the
        postfix notation representation of the expression as a list of tokens. If equal_precedence is True,
        then the "+" and "*" operators have equal precedence. Otherwise, "+" has higher precedence than "*".
        """

        if equal_precedence:
            precedence_map = {"+": 1, "*": 1}
        else:
            precedence_map = {"+": 2, "*": 1}

        operator_stack = Stack()
        result = []

        for token in tokens:
            if token == "(":
                # A left parenthesis signifies the beginning of a subexpression.
                operator_stack.push(token)
            elif token == "+" or token == "*":
                precedence = precedence_map.get(token)

                # Pop off all operators on the stack whose precedence is at least as high
                # as the current token's precedence. Append these operators to result.
                while not operator_stack.is_empty() and precedence <= precedence_map.get(operator_stack.peek(), 0):
                    # By design, this preserves the left-to-right order of the operators.
                    result.append(operator_stack.pop())

                operator_stack.push(token)
            elif token == ")":
                # Append all operators to result
                while not operator_stack.is_empty() and operator_stack.peek() != "(":
                    result.append(operator_stack.pop())

                # Pop the left parenthesis off the stack
                operator_stack.pop()
            else:  # token is a number
                result.append(token)

        # Append all remaining operators to result
        while not operator_stack.is_empty():
            result.append(operator_stack.pop())

        return result

    postfix_tokens = postfix_notation(tokenize(expr), equal_precedence)
    operand_stack = Stack()

    for token in postfix_tokens:
        if token == "+":
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            operand_stack.push(left_operand + right_operand)
        elif token == "*":
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            operand_stack.push(left_operand * right_operand)
        else:  # token is a number
            operand_stack.push(int(token))

    return operand_stack.pop()


with open("day18.txt", "r") as f:
    contents = f.read().splitlines()

print(sum(evaluate(line, True) for line in contents))   # Part 1 answer
print(sum(evaluate(line, False) for line in contents))  # Part 2 answer
