# Library Web Service

Example REST web service for library

## Routes

List of routes:

### Books

```api
GET     /api/v1/books/            Fetch Books
POST    /api/v1/books/            Create Book
GET     /api/v1/books/{book_id}/  Fetch Book by ID
PATCH   /api/v1/books/{book_id}/  Update Book by ID
DELETE  /api/v1/books/{book_id}/  Delete Book by ID
```

### Users

```api
GET     /api/v1/users/             Fetch Users
POST    /api/v1/users/             Create Book
GET     /api/v1/users/{user_id}/   Fetch User by ID
PATCH   /api/v1/users/{user_id}/   Update User by ID
DELETE  /api/v1/users/{user_id}/   Delete User by ID
```

### User Books

```api
GET     /api/v1/users/{user_id}/books/                   Get user books
POST    /api/v1/users/{user_id}/books/{book_id}/issue/   Issue Book to User
POST    /api/v1/users/{user_id}/books/{book_id}/return/  Return Book from User
```
