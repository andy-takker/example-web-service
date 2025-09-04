from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True, slots=True)
class OpenLibraryConfig:
    url: str = field(default_factory=lambda: "https://openlibrary.org")
