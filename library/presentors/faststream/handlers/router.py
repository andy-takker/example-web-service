from faststream.nats import NatsRouter

from library.presentors.faststream.handlers.books import router as books_router

router = NatsRouter(include_in_schema=True)
router.include_router(books_router)
