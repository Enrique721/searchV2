from typing import Match
import re
from src.data_normalization.login_normalization import AccessCredentialNormalizationInterface


class EmailNormalization(AccessCredentialNormalizationInterface):

    EMAIL_REGEX: re.Pattern = re.compile(
                 r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\b'
             )

    PROVIDER_BASE: dict = {
        "gmail": "gmail.com",
        "outlook": "outlook.com",
        "hotmail": "hotmail.com",
        "yahoo": "yahoo.com",
        "icloud": "icloud.com",
        "proton": "proton.me",
    }


    @staticmethod
    def normalization(raw: str):

        matched: Match[str] = EmailNormalization.EMAIL_REGEX.match(raw)

        if matched is None:
            return raw, False

        detected: str = matched.group(0)

        identifier, domain = detected.split('@')
        pure_domain = domain.split('.')[0]

        if pure_domain in EmailNormalization.PROVIDER_BASE:
            return "@".join([
                        identifier,
                        EmailNormalization.PROVIDER_BASE[pure_domain]
                    ]), True

        return raw, False
