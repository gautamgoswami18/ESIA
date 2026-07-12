from abc import ABC, abstractmethod


class BaseRAG(ABC):

    @abstractmethod
    def ask(self, question: str):
        pass

    @abstractmethod
    def summarize_resume(self, resume_text: str):
        pass

    @abstractmethod
    def compare_candidates(
        self,
        employee1: int,
        employee2: int
    ):
        pass