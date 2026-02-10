import re
from typing import Literal, TypedDict

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


class AccessCredentialNormalizationInterface:

    @staticmethod
    def normalization(login: str):
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
        access_method_candidate_factory(
            re.compile(
                r'^[A-Z0-9][A-Z0-9.\-\/]{4,29}$',
                re.IGNORECASE
            ),
            "document"
        ),
        access_method_candidate_factory(
            re.compile(
                r'^\d{4,20}$'
            ),
            "id_number"
        ),
        access_method_candidate_factory(
            re.compile(
                r'^[A-Z][A-Z0-9._-]{2,29}$',
                re.IGNORECASE
            ),
            "nickname"
        )
    ]
    
    @staticmethod
    def __access_credential_detect(login: str) ->  crendential_type:

        for access_login in LoginTypeIdentificationAndNormalization.access_login_candidates:
            if m:= access_login["pattern"].match(login):
                return access_login["type"]
        
        return 'unknown'

    @staticmethod
    def credential_normalization(login: str):

        credential_type = LoginTypeIdentificationAndNormalization.credential_normalization(login)

        match credential_type:
            case 'email':
                pass

            case 'document':
                pass

            case 'id_number':
                pass

            case 'phone':
                pass

            case _:
                pass
        
        return

