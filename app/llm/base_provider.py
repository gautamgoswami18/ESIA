from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        json_mode: bool = False
    ) -> str:
        """
        Generate response from LLM.

        Args:
            prompt: User/System prompt
            json_mode: True -> Return JSON response

        Returns:
            String response from LLM
        """
        pass