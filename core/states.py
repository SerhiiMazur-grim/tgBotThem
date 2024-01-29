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


class AddPostState(StatesGroup):
    post = State()
    post_type = State()
    users_count = State()


class AddThemeCat(StatesGroup):
    category = State()


class ThemesCatalogState(StatesGroup):
    catalog = State()
    start = State()
    end = State()
 