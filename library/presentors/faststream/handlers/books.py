from dishka import FromDishka
from faststream.nats import NatsRouter

from library.adapters.nats.stream import STREAM
from library.domains.entities.book import UploadBooks
from library.domains.use_cases.commands.book.upload_books import UploadBooksCommand
from library.presentors.faststream.events.upload_books import UploadBooksEvent
from library.presentors.faststream.subjects import BooksSubjects

router = NatsRouter(include_in_schema=True)


@router.subscriber(BooksSubjects.UPLOAD_OPEN_LIBRARY, stream=STREAM)
async def upload_open_library_books(
    event: UploadBooksEvent,
    upload_books_command: FromDishka[UploadBooksCommand],
) -> None:
    await upload_books_command.execute(
        input_dto=UploadBooks(queries=event.queries),
    )
