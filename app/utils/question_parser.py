import re


class QuestionParser:

    @staticmethod
    def employee(question: str) -> int:
        """
        Extract a single employee ID from the question.

        Example:
            "Give summary of employee 1001"
            -> 1001
        """

        ids = re.findall(r"\d+", question)

        if not ids:
            raise Exception("Employee ID not found in the question.")

        return int(ids[0])

    @staticmethod
    def employees(question: str) -> tuple[int, int]:
        """
        Extract two employee IDs from the question.

        Example:
            "Compare employee 1001 and 1005"
            -> (1001, 1005)
        """

        ids = re.findall(r"\d+", question)

        if len(ids) < 2:
            raise Exception("Two employee IDs are required.")

        return int(ids[0]), int(ids[1])