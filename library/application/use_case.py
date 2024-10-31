from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol


class IUseCase[InputDTO, OutputDTO](Protocol):
    @abstractmethod
    async def execute(self, *, input_dto: InputDTO) -> OutputDTO:
        raise NotImplementedError


@dataclass(frozen=True)
class ICommand[InputDTO, OutputDTO](IUseCase, Protocol): ...


@dataclass(frozen=True)
class IQuery[InputDTO, OutputDTO](IUseCase, Protocol): ...
