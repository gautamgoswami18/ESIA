import re


class PIIMaskGuard:

    EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE = r"\b\d{10}\b"

    @classmethod
    def sanitize(
        cls,
        text
    ):

        if not isinstance(text, str):

            return text

        text = re.sub(
            cls.EMAIL,
            "[EMAIL]",
            text
        )

        text = re.sub(
            cls.PHONE,
            "[PHONE]",
            text
        )

        return text