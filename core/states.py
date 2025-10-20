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


class AddLanguageCat(StatesGroup):
    category = State()


class ThemesCatalogState(StatesGroup):
    device = State()
    category = State()
    catalog = State()
    page = State()
    pages = State()
 
 
class LanguagesCatalogState(StatesGroup):
    catalog = State()
    start = State()
    end = State()


class RandomThemeState(StatesGroup):
    device = State()


class RandomLanguageState(StatesGroup):
    device = State()


class SetWallpaperState(StatesGroup):
    theme_path = State()
    image_path = State()


class WallpState(StatesGroup):
    message = State()
    photo = State()


class GetImageIdState(StatesGroup):
    image = State()


class OPKanal(StatesGroup):
    chanel_id = State()
    invate_url = State()


class OPDelKanal(StatesGroup):
    chanel_id = State()
