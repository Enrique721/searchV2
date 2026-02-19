from typing import Match
import re

EMAIL_REGEX: re.Pattern = re.compile(
    r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\b'
)

PROVIDER_BASE = {
    "gmail": "gmail.com",
    "outlook": "outlook.com",
    "hotmail": "hotmail.com",
    "yahoo": "yahoo.com",
    "icloud": "icloud.com",
    "proton": "proton.me",
}


def normalize_email(login):

    matched: Match[str] = EMAIL_REGEX.match(login)

    if matched is None:
        return login, False

    detected: str = matched.group(0)

    identifier, domain = detected.split('@')
    pure_domain = domain.split('.')[0]

    if pure_domain in PROVIDER_BASE:
        return "@".join([identifier, PROVIDER_BASE[pure_domain]]), True

    return login, False
   


test = [
    'aaasdkjalsdk@lkasdjflas.c',
    'aaasdkjalsdk@lkasdjflas.com',
    'sajksdfhj@asjdks.com(lksdfjlsfk)',
    'sajksdfhj@asjdks.c(lksdfjlsfk)',

    'sajksdfhj@gmail.c(lksdfjlsfk)',
    'sajksdfhj@gmail.(lksdfjlsfk)',
    'lkasklsdfs@gmail.com',
    'lkasklsdfs@gmail.c',
    'lkasklsdfs@gmail.',
]

for email in test:
    print(email, normalize_email(email))
