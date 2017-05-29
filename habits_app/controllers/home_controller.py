import pyramid_handlers
from habits_app.controllers.base_controller import BaseController


class HomeController(BaseController):

    @pyramid_handlers.action(renderer='templates/home/index.pt')
    def index(self):
        return {"value": 'INDEX'}

    @pyramid_handlers.action(renderer='templates/home/memory.pt')
    def memory(self):
        return {"value": 'MEMORY'}

    @pyramid_handlers.action(renderer='templates/home/books.pt')
    def books(self):
        return {"value": 'BOOKS'}
