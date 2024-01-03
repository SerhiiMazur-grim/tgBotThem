from aiogram.fsm.state import State, StatesGroup


class AddThemeState(StatesGroup):
    device = State()
    preview = State()
    file = State()
    category = State()


class AddLanguageState(StatesGroup):
    device = State()
    category = State()
    preview = State()
    caption = State()


class GetThemesCatalogState(StatesGroup):
    device = State()
    category = State()


class GetLanguageCatalogState(StatesGroup):
    device = State()
    category = State()


class GetFontTextState(StatesGroup):
    text = State()
