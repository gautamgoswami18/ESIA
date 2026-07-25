from datetime import datetime


class ProcessManager:

    _cache = {}

    @classmethod
    def save(
        cls,
        process_id: str,
        data: dict
    ):

        cls._cache[process_id] = {

            "created_at": datetime.now(),

            "data": data

        }

    @classmethod
    def get(
        cls,
        process_id: str
    ):

        process = cls._cache.get(process_id)

        if process is None:

            raise ValueError("Invalid Process Id.")

        return process["data"]

    @classmethod
    def remove(
        cls,
        process_id: str
    ):

        cls._cache.pop(
            process_id,
            None
        )