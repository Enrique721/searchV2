import re

def normalize_phone(raw: str):
    if not raw:
        return raw, False

    raw = raw.strip()

    has_plus = raw.startswith("+")

    digits = re.sub(r"\D", "", raw)

    if not digits:
        return raw, False

    if not (8 <= len(digits) <= 15):
        return raw, False

    if has_plus:
        return f"+{digits}", True

    return digits, True

test = [
    "+32490820938402",
    "+92348 (23) 02948 234098",
    "9283 409 2832",
    "39284-39248",
    "+1 (1) 0000-0000",
    "+1 (1) 0000 0000",
    "+1 (1) 00000000"
]

for numbers in test:
    print(normalize_phone(numbers))
