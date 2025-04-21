import code

code_string = """
def greet(name):
    print("Hello", name)

greet("Alice")
for i in range(3):
    print("Count", i)
"""

interpreter = code.InteractiveInterpreter()
buffer = ""

for line in code_string.splitlines():
    buffer += line + "\n"
    if interpreter.runsource(buffer, symbol="exec"):
        # Incomplete block, keep buffering
        continue
    else:
        # Block is complete, reset buffer
        buffer = ""