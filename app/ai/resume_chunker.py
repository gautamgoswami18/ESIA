from langchain_text_splitters import RecursiveCharacterTextSplitter


class ResumeChunker:

    _text_splitter = None
    _boilerplate_chunks = {
        "employee profile",
        "employee profile:",
        "resume text",
        "resume text:",
    }

    @classmethod
    def get_splitter(cls):

        if cls._text_splitter is None:

            cls._text_splitter = RecursiveCharacterTextSplitter(

                chunk_size=1000,

                chunk_overlap=200,

                separators=[

                    "\n\n",

                    "\n",

                    ". ",

                    " ",

                    ""

                ]

            )

        return cls._text_splitter

    @classmethod
    def chunk(
        cls,
        text: str
    ) -> list[str]:

        if not text:

            return []

        splitter = cls.get_splitter()

        return [
            chunk.strip()
            for chunk in splitter.split_text(text)
            if cls._is_indexable(chunk)
        ]

    @classmethod
    def _is_indexable(cls, chunk: str) -> bool:
        normalized = " ".join((chunk or "").split()).casefold()
        return bool(normalized) and normalized not in cls._boilerplate_chunks
