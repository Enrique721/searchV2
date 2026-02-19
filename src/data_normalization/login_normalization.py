import re
from typing import Literal, TypedDict, Tuple

crendential_type = Literal['email', 'document', 'id_number', 'phone', 'nickname', 'unknown']

class AccessMethodCandidate(TypedDict):
    pattern: re.Pattern
    type: crendential_type

def access_method_candidate_factory(
    pattern: re.Pattern,
    type: crendential_type) -> AccessMethodCandidate:

    return {
        "pattern": pattern,
        "type": type
    }


# Interface for other normalizers
class AccessCredentialNormalizationInterface:
    @staticmethod
    def normalization(raw: str):
        pass


class LoginTypeIdentificationAndNormalization:

    access_login_candidates = [
        access_method_candidate_factory(
            re.compile(
                r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$',
                re.IGNORECASE
            ),
            "email"
        ),
        access_method_candidate_factory(
            re.compile(
                r'^\+?[0-9][0-9\s().-]{6,20}[0-9]$'
            ),
            "phone"
        ),
    ]
    
    @staticmethod
    def __access_credential_detect(login: str) ->  crendential_type:
        for access_login in LoginTypeIdentificationAndNormalization.access_login_candidates:
            if m:= access_login["pattern"].match(login):
                return access_login["type"]
        
        return 'unknown'

    @staticmethod
    def credential_normalization(login: str) -> Tuple[str, crendential_type]:
        from src.data_normalization.phone_normalization import PhoneNormalization
        from src.data_normalization.email_normalization import EmailNormalization

        credential_type = LoginTypeIdentificationAndNormalization\
                                    .credential_normalization(login)

        match credential_type:
            case 'email':
                normalized, status = EmailNormalization.normalization(login)

                if status:
                    return normalized, credential_type
                else:
                    return login, 'unknown'

            case 'phone':
                normalized, status = PhoneNormalization.normalization(login)
                if status:
                    return normalized, credential_type
                else:
                    return login, 'unknown'

            case _:
                return login, 'unknown'

