import pyramid_handlers
from habits_app.controllers.base_controller import BaseController


class BooksController(BaseController):

    @pyramid_handlers.action(renderer='templates/books/index.pt')
    def index(self):
        return {"value": 'INDEX'}
