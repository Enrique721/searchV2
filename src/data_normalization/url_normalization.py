from typing import Tuple
from src.data_normalization.login_normalization import AccessCredentialNormalizationInterface
from urllib.parse import urlparse

class UrlNormalization(AccessCredentialNormalizationInterface):

    @staticmethod
    def normalization(raw: str) -> Tuple[str, bool]:
        url = raw.strip()

        try:
            if "://" not in url:
                parsed = urlparse("http://" + url)
                scheme = ""
            else:
                parsed = urlparse(url)
                scheme = parsed.scheme.lower()

            netloc = parsed.netloc.lower()

            if not netloc:
                netloc = parsed.path.split("/")[0].lower()

            if scheme:
                return f"{scheme}://{netloc}", True
            else:
                return netloc, True
        except:
            return url, False;
