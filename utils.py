import re

def extract_code(text: str) -> str:
    code_blocks = text.split("```")[1:-1:2]
    code_blocks = ["\n".join(x.splitlines()[1:]) for x in code_blocks]
    return "\n\n".join(code_blocks)

def detect_table(text: str) -> bool:
    return re.search(r"\|.*\|.*\|", text) is not None

def detect_code(text: str) -> bool:
    return '```' in text