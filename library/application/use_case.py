from abc import abstractmethod
from typing import Protocol


class IUseCase[InputDTO, OutputDTO](Protocol):
    @abstractmethod
    async def execute(self, *, input_dto: InputDTO) -> OutputDTO:
        raise NotImplementedError
