import re
from src.data_normalization.login_normalization import AccessCredentialNormalizationInterface

class PhoneNormalization(AccessCredentialNormalizationInterface):

    @staticmethod
    def normalization(raw: str):
        if not raw:
            return raw, False

        login = raw.strip()

        has_plus = login.startswith("+")

        digits = re.sub(r"\D", "", login)

        if not digits:
            return login, False

        if not (8 <= len(digits) <= 15):
            return login, False

        if has_plus:
            return f"+{digits}", True

        return digits, True
