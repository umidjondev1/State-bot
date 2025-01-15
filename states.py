from aiogram.fsm.state import State, StatesGroup


class UserList(StatesGroup):
    name = State()
    interesting = State()
    code = State()
    finish = State()
    admin = State()
