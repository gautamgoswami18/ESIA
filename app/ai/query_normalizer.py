import re


class QueryNormalizer:

    ROLE_WORDS = [
        "developer",
        "developers",
        "engineer",
        "engineers",
        "software engineer",
        "software engineers",
        "architect",
        "consultant",
        "lead",
        "manager",
        "expert",
        "specialist",
        "programmer",
        "coder"
    ]

    SEARCH_WORDS = [
        "find",
        "search",
        "need",
        "looking for",
        "show",
        "list",
        "give me"
    ]

    @classmethod
    def normalize(cls, query: str):

        query = query.lower()

        for word in cls.SEARCH_WORDS:
            query = query.replace(word, "")

        for word in cls.ROLE_WORDS:
            query = query.replace(word, "")

        query = re.sub(r"\s+", " ", query)

        return query.strip()