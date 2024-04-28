from config.api_keys import NAME


PREVIEW_WATER_MARK = f'Theme created in {NAME}'
START_COMMAND_DESCRIPTION = 'Начать работу с ботом.'
MESSAGE_ON_START_COMMAND = 'Привет '
MESSAGE_ON_CREATE_THEME = 'Отправьте мне картинку и я сделаю из нее тему для Telegram'
MESSAGE_ON_ADD_TO_CHAT = 'Нажмите кнопку добавить бота в группу, выберите группу в которую нужно добавить бота и нажмите Сохранить'
MESSAGE_ON_FAQ = """
Возникли вопросы?

<a href="https://telegra.ph/Test-title-12-14-6">Тебе сюда</a>

По другим вопросам к <a href="https://t.me/mrlucker">администратору</a>.
"""

MESSAGE_ON_START_IN_GROUP = 'Отправь в чат картинку с подписью "/bg" и я сделаю из нее фон для твоего Telegram или переходи в бот, там много интересного😉'
BUTTON_GO_TO_BOT = 'Бот с темками👉'
MESSAGE_WITH_CHAT = 'Чат: '
MESSAGE_CHECK_SUBSCRIBE = 'Проверить подписку'
MESSAGE_YOU_NOT_SUBSCRIBE = 'Вы не подписаны на наши чаты🧐, для пользования ботом подпишитесь на наши чаты😊:'
MESSAGE_YOU_NOT_SUBSCRIBE_GROUP = ' ты не подписаны на наши чаты и бот🧐, перейди в бот и зарегистрируйся для начала😊'

SUBSCRIBE_CHECKED = 'Бот готов к работе, отправьте ему картинку.'
WAIT_MESSAGE = 'Провожу анализ изображения ⏳'
NOT_IMAGE = 'ОЙ, кажется это не картинка 🤨🧐\nПроверьте файл, который вы отправили!'

BUTTON_CREATE_THEME = 'Создать тему'
BUTTON_ADD_TO_CHAT = '💭Добавить бота в чат'
BUTTON_THEME_CATALOG = '🌄Каталог тем'
BUTTON_FONTS_CATALOG = '🈸Изменить шрифт'
BUTTON_FAQ = '❓ F.A.Q'
BUTTON_ADMIN = 'Админка'
MESSAGE_ON_ADMIN = 'Права админа подтверждены!'

BUTTON_ADD_THEME = 'Добавить тему'
BUTTON_ADD_LANGUAGE = 'Добавить язык'
BUTTON_BACK_TO_USER_KB = 'Клавиатура пользователя'
MESSAGE_ON_BACK_TO_USER_KB = 'Клавиатура пользователя!'
BUTTON_NEXT_THEMES = 'Следующие 5 тем'

MESSAGE_CHOICE_DEVICE_FOR_LANGUAGE = 'Выберите девайсы на которых доступен язык:'
DEVICE_FOR_LANGUAGE = ['android', 'ios', 'computer']
MESSAGE_CHOICE_CATEGORY_FOR_LANGUAGE = 'Выберите категорию для языка'
MESAGE_SEND_ME_PREVIEW_AND_TEXT = 'Отправьте мне изображения (три изображения❗️) для превью, и описание для языка со ссылкой.'
BUTTON_SAVE_LANGUAGE = 'Сохранить язык'
MESSAGE_LANGUAGE_IS_SAVE = 'Язык сохранен в базе'
MESSAGE_NO_DATA_TO_SAVE_LANGUAGE = 'Нет данных для сохранения'

MESSAGE_CHOICE_DEVICE_FOR_LANG = 'Для какого девайса язык?'
BUTTON_LANGUAGE_CATALOG = '🌆Каталог языков'
BUTTON_NEXT_LANGUAGES = 'Следующие 5 языков'
BUTTON_BACK_FROM_LANG_CAT = '👈 Главное меню'
MESSAGE_OUR_LANGUAGES = 'Вот языки что у меня есть'
MESSAGE_NO_LANGUAGES_IN_CATALOG = 'Ой! кажется языков по таким параметрам у нас нет!'
MESSAGE_NO_MORE_LANGUAGES = 'Ой! кажется языки закончились!'

BUTTON_ADD_BOT_TO_CHAT = 'Добавить бота в группу'

# У цьому повідомлені допускається не більше 200 символів !!!
MESSAGE_IS_NOT_YOUR_THEME = f'''
Не вы создаете тему, не вам и щелкать кнопки😁
Начните создавать свою тему для взаимодействия с ботом здесь, отправьте ему картинку с подписью /theme.
Или переходи к боту: {NAME}
'''
CHOOSE_DEVICE_TEXT = '1️⃣ Выберите устройство: 📱'
ANDROID = 'Android'
IPHONE = 'IPhone'
PC = "Компьютер [Windows/Linux]"
FOR_PC = "Компьютера [Windows/Linux]"
ABORT = 'Отменить'

CHOOSE_BACKGROUND_COLOR_TEXT = '2️⃣ Выберите цвет для фона:'
BUTTON_1 = '1'
BUTTON_2 = '2'
BUTTON_3 = '3'
BUTTON_4 = '4'
BUTTON_5 = '5'
BUTTON_WHITE = 'Белый'
BUTTON_BLACK = 'Черный'
BUTTON_AUTO = 'Авто'
BUTTON_BACK = '⬅️ Главное меню'
BUTTON_BACK_IKB = '⬅️ Назад'

CHOOSE_PRIMARY_COLOR_TEXT = '3️⃣ Выберите цвет для основного текста:'
CHOOSE_SECONDARY_COLOR_TEXT = '4️⃣ Выберите цвет для второстепенного текста:'
CHOOSE_ALFA = '5️⃣ Выберите прозрачность для сообщений:'
BUTTON_ALFA_10 = '10%'
BUTTON_ALFA_20 = '20%'
BUTTON_ALFA_30 = '30%'
BUTTON_ALFA_40 = '40%'
BUTTON_ALFA_50 = '50%'
BUTTON_ALFA_60 = '60%'
BUTTON_ALFA_70 = '70%'
BUTTON_ALFA_80 = '80%'
BUTTON_ALFA_90 = '90%'
BUTTON_ALFA_0 = 'Без прозрачности'

MESSAGE_EQUAL_COLOR_1 = 'Цвет фона не должен быть одинаковым с цветом основного текста!'
MESSAGE_EQUAL_COLOR_2 = 'Цвет фона не должен быть одинаковым с второстепенным цветом текста!'

MESSAGE_CREATING_THEME = 'Создаю тему ⏳'
MESSAGE_THEME_DONE = f'Тема создана в <a href="https://t.me/{NAME[1:]}?start=from_theme">{NAME}</a> 😉 '

MESSAGE_ADDED_TO_DB = 'Тема добавлена в каталог'

MESSAGE_SEND_PREVIEW_THEME = 'Сбросьте мне превью для темы (1 изображение)'
MESSAGE_SEND_THEME_FILE = 'Сбросьте мне файл темы'
MESSAGE_CHOICE_CATEGORY = 'Выберите категорию'
MESSAGE_CHOICE_DEVICE = 'Для какого девайса тема?'
MESSAGE_IS_NOT_THEME = 'Это не файл темы!'
MESSAGE_NO_PREVIEW_IN_THEME = 'У темы нет превью! Сбросьте превью на тему!'

MESSAGE_OUR_THEMES = 'Вот темы, что у нас есть'
CAPTION_TO_THEME_IN_CATALOG = f'Нажми для установки!\n\nТема создана в <a href="https://t.me/{NAME[1:]}?start=from_theme">{NAME}</a> 😉 '
MESSAGE_ON_BACK = 'Главное меню'

MESSAGE_NO_MORE_THEMES = 'Ой! кажется темы закончились!'
MESSAGE_NO_THEMES_IN_CATALOG = 'Ой! кажется тем по таким параметрам у нас нет!'
MESSAGE_GIVE_ME_POST = """
Сбросьте мне пост для рассылки.
Если пост содержит несколько медиа файлов, то после их загрузки нажмите кнопку "Показать пост"
"""
BUTTON_CREATE_MAILING = 'Создать пост'
BUTTON_CREATE_LIMITED_POST = 'Отправить только активным пользователям'
MESSAGE_SEND_USERS_COUNT = 'Отправьте число соответствующее количеству пользователей, которые увидят этот пост.'
MESSAGE_IS_NOT_NUMBER = 'Вы отправили не число!'
MESSAGE_USERS_COUNT_INSERT = 'Количество пользователей для рассылки установлено на: '
MESSAGE_SEND_ME_POST_FOR_LIMIT_SENDS = 'Отправьте мне пост для рассылки этим пользователям.'
BUTTON_SEND_LIMITED_POST = 'Отправить пост пользователям!'
MESSAGE_LIMITED_POST_SEND = 'Пост для активных пользователей отправлен на рассылку!'
MESSAGE_POST_IS_SEND = 'Пост отправлен на рассылку!'
MESSAGE_POST_SEND_COMPLITE = 'Рассылка окончена! Пост доставлен пользователям.'
MESSAGE_LIMITED_POST_NOT_SEND = 'Нет поста для рассылки!'
MESSAGE_PREV_POST_NOT_SENDED = 'Предыдущий пост еще не разослан до конца, осталось еще разослать: '
MESSAGE_SENDING_IS_STOP = 'Рассылка прекращена!\nСоздать пост для рассылки заново!'
BUTTON_VIEW_MAILING = 'Показать пост'
MESSAGE_IS_YOUR_POST = 'Это пост, который вы хотите отправить.\nЧто мне следует с ним сделать?'
BUTTON_DELETE_POST = 'Удалить пост'
BUTTON_SEND_TO_ALL = 'Отправить всем'
BUTTON_SEND_TO_PRIVATE = 'Отправить в приватные'
BUTTON_SEND_TO_GROUP = 'Отправить в групповые'
MESSAGE_NO_POST = 'Нет постов для отправки!'
MESSAGE_DELETE_POST = 'Пост удалён'
BUTTON_ABORT_CREATE_POST = 'Отменить создание поста'
BUTTON_STOP_SENDING_POST = 'Остановить рассылку поста'
BUTTON_ABORT_ADD_THEME = 'Отменить добавление темы'
FONTS_BUTTONS = {
    'Пⷫрⷬuͧмⷨеⷷрⷬ / Eͤxͯaͣрⷬmͫleͤ': 'font_1',
    'Пᵖиᴹᵉᵖ / Exapmle': 'font_2',
    'П𝕡и𝕄𝕖𝕡 / 𝔼𝕩𝕒𝕡𝕞𝕝𝕖': 'font_3',
    'П̶р̶и̶м̶е̶р̶ /̶ E̶x̶a̶p̶m̶l̶e̶': 'font_4',
    'П̝̪р̝͖и̡̻͔м͍͍͕е̡͉̫р̝͖ /̪̝͖ E͇͖͜x̻̼a̟͇͜p̡͉̺m̢͕͇l͉͓̙e̟͍': 'font_5',
    'П̒͐͑р́͆͝и͊͘͝м͆͛͆е̾͌̽р́͆͝ /̔͐̓ E͑͒̐x͛͑̓ä́̈́͝p͋̾͘m͐̾̿l̽̒̈́e͆͒͠': 'font_6',
    'П̸̻͐̓̕͜р̴͙͙͍͆̓͠и̴̢͖͙̒͒̈́м̵̦͓͇͛͝͠е̴̫̪̞͋̈́р̴͙͙͍͆̓͠ /̵̢̟͍̐͊͠ E̸̦͖͙͌͒͝x̵͇̦̪͒̈́̿a̸͓͇̟̽͌̓p̵̞͙͇͐͛͆m̵͍͉͔̕͝l̵̘͌̀̈́͜e̸̘͓͉͌̓͝': 'font_7',
    'П̷р̷и̷м̷е̷р̷ /̷ E̷x̷a̷p̷m̷l̷e̷': 'font_8',
    'П̲р̲и̲м̲е̲р̲ /̲ E̲x̲a̲p̲m̲l̲e̲': 'font_9',
    'П̅р̅и̅м̅е̅р̅ /̅ E̅x̅a̅p̅m̅l̅e̅': 'font_10',
    'П𝘱и𝘔𝘦𝘱 / 𝘌𝘹𝘢𝘱𝘮𝘭𝘦': 'font_11',
    'П𝑝и𝑀𝑒𝑝 / 𝐸𝑥𝑎𝑝𝑚𝑙𝑒': 'font_12',
    'Пример / 𝐄𝐱𝐚𝐩𝐦𝐥𝐞': 'font_13',
    'П𝚙и𝙼𝚎𝚙 / 𝙴𝚡𝚊𝚙𝚖𝚕𝚎': 'font_14',
    'П𝓅иℳℯ𝓅 / ℰ𝓍𝒶𝓅𝓂𝓁ℯ': 'font_15',
    'П🄿и🄼🄴🄿 / 🄴🅇🄰🄿🄼🄻🄴': 'font_16',
    'П🅿и🅼🅴🅿 / 🅴🆇🅰🅿🅼🅻🅴': 'font_17',
    'П🅟и🅜🅔🅟 / 🅔🅧🅐🅟🅜🅛🅔': 'font_18',
    'ПⓟиⓂⓔⓟ / Ⓔⓧⓐⓟⓜⓛⓔ': 'font_19',
}
MESSAGE_SEND_ME_TEXT = 'Отправьте мне текст и я изменю его шрифт.'
MESSAGE_CHOICE_FONT = 'Выберите шрифт'

BUTTON_BACKUP = 'BACKUP DB'
MESSAGE_BACKUP = f'Ваш архив с бекапом за: '
MESSAGE_SOME_ERROR = 'Хмм...🧐 Что-то пошло не так, попробуй создать тему сначала 🥹 или попробуй позже'
MESSAGE_WALLPAPER_SOME_ERROR = 'Хмм...🧐 Что-то пошло не так, попробуй создать обои сначала 🥹 или попробуй позже'

BUTTON_ADMIN_THEME_CATALOG = 'Каталог тем Admin'
MESSAGE_ADMIN_THEME_CATALOG = 'Редактирование каталога тем.'
BUTTON_ADMIN_THEME_CATEGORY = 'Категории тем'
IKB_BUTTON_ADMIN_ADD_THEME_CATEGORY = 'Добавить категорию'
MESSAGE_ADMIN_INPUT_THEME_CATEGORY = 'Введите название категории для темы:'
MESSAGE_ADMIN_INPUT_THEME_CATEGORY_ERR = 'Это не подходит для названия категории темы!\nВведите корректное название категории:'
MESSAGE_ADMIN_INPUT_THEME_CATEGORY_DONE = 'Категорию добавлено в список категорий для тем!'
MESSAGE_ADMIN_ADD_THEME_CATEGORY_ERR = 'Такая категория уже существует в каталоге тем !!!'
IKB_BUTTON_ADMIN_DEL_THEME_CATEGORY = 'Удалить категорию'
MESSAGE_CHOICE_THEME_CAT_TO_DELETE = 'Выберите категорию для удаления! ВНИМАНИЕ! все темы которые относятся к данной категории тоже буду удалены!'
MESSAGE_THEME_CAT_IS_DELETE = 'Категория и все темы связанные с ней удалены!'
MESSAGE_THEME_CAT_DELETE_ERR = 'Ошибка при удалении категории темы! Детали смотрите в логах!'
MESSAGE_ADD_THEME_TO_CATALOG_ERR = 'Ошибка при добавлении темы в каталог! Детали смотрите в логах!'

BUTTON_ADMIN_LANGUAGE_CATALOG = 'Каталог языков Admin'
MESSAGE_ADMIN_LANGUAGE_CATALOG = 'Редактирование каталога языков.'
BUTTON_ADMIN_LANGUAGE_CATEGORY = 'Категории языков'
IKB_BUTTON_ADMIN_ADD_LANGUAGE_CATEGORY = 'Добавить категорию'
IKB_BUTTON_ADMIN_DEL_LANGUAGE_CATEGORY = 'Удалить категорию'
MESSAGE_ADMIN_INPUT_LANGUAGE_CATEGORY = 'Введите название категории для языка:'
MESSAGE_ADMIN_INPUT_LANGUAGE_CATEGORY_DONE = 'Категорию добавлено в список категорий для языков!'
MESSAGE_ADMIN_ADD_LANGUAGE_CATEGORY_ERR = 'Такая категория уже существует в каталоге языков !!!'
MESSAGE_ADMIN_INPUT_LANGUAGE_CATEGORY_ERR = 'Это не подходит для названия категории языка!\nВведите корректное название категории:'
MESSAGE_CHOICE_LANGUAGE_CAT_TO_DELETE = 'Выберите категорию для удаления! ВНИМАНИЕ! все языки которые относятся к данной категории тоже буду удалены!'
MESSAGE_LANGUAGE_CAT_IS_DELETE = 'Категория и все языки связанные с ней удалены!'
MESSAGE_LANGUAGE_CAT_DELETE_ERR = 'Ошибка при удалении категории языка! Детали смотрите в логах!'
MESSAGE_ADD_LANGUAGE_TO_CATALOG_ERR = 'Ошибка при добавлении языка в каталог! Детали смотрите в логах!'

MESSAGE_ADMIN_CATEGORY_MENU = 'Меню категории'

BUTTON_STATISTIC_MENU = 'Статистика'
MESSAGE_IS_STATISTIC_MENU = 'Меню статистики'
BUTTON_ACTIVE_STATISTICA = 'Статистика активности'
BUTTON_FULL_STATISTICA = 'Полная статистика'
MESSAGE_PERIOD_OF_ACTIVE_CHOICE = 'Выберите за какой период активности пользователей показать статистику:'
BUTTON_DAY_ACTIVITY = 'Активность за день'
BUTTON_WEEK_ACTIVITY = 'Активность за неделю'
BUTTON_MONTH_ACTIVITY = 'Активность за месяц'

def active_users_per_day_message(users_count, chats_count, total_count, prem_users_count):
    message = f"""
    ⌚️ Активные пользователи за последние 24 часа:
    
    🟢 Всего активных пользователей: {total_count}👤
    
    🟢 Персональные чаты: {users_count}👤
    
    🟢 Груповые чаты: {chats_count}👤
    
    🔮 Пользователи с перм-акаунтом: {prem_users_count}👤
    """
    return message

def active_users_per_week_message(users_count, chats_count, total_count, prem_users_count):
    message = f"""
    ⌚️ Активные пользователи за последние 7 дней:
    
    🟢 Всего активных пользователей: {total_count}👤
    
    🟢 Персональные чаты: {users_count}👤
    
    🟢 Груповые чаты: {chats_count}👤
    
    🔮 Пользователи с перм-акаунтом: {prem_users_count}👤
    """
    return message

def active_users_per_month_message(users_count, chats_count, total_count, prem_users_count):
    message = f"""
    ⌚️ Активные пользователи за последние 30 дней:
    
    🟢 Всего активных пользователей: {total_count}👤
    
    🟢 Персональные чаты: {users_count}👤
    
    🟢 Груповые чаты: {chats_count}👤
    
    🔮 Пользователи с перм-акаунтом: {prem_users_count}👤
    """
    return message

def full_statistica_caption(total_users, refer_users, total_active_users, not_active_users,
                            total_priv_chats, active_priv_chats, not_active_priv_chats,
                            total_group_chats, active_group_chats, not_active_group_chats,
                            total_prem_users, active_prem_users, total_users_in_active_groups):
    message = f"""
    ⌚️ Статистика за всё время работы бота:
    
    🟢 Всего пользователей: {total_users}👤
    🟢 Из них активные: {total_active_users}👤
    🔴 Не активные: {not_active_users}👤
    
    🔗 Пользователи которые пришли по реферальной ссылке: {refer_users}👤
    
    🟢 Всего персональных чатов: {total_priv_chats}👤
    🟢 Из них активные: {active_priv_chats}👤
    🔴 Не активные: {not_active_priv_chats}👤
    
    🟢 Всего груповых чатов: {total_group_chats}👤
    🟢 Из них активные: {active_group_chats}👤
    🔴 Не активные: {not_active_group_chats}👤
    🟢 Пользователей в активных чатах: {total_users_in_active_groups}👤
    
    🔮 Пользователи с перм-акаунтом: {total_prem_users}👤
    🟢 Из них активные: {active_prem_users}👤
       
    """
    return message

BUTTON_REFERAL_STATISTICA = 'Статистика рефералов'
MESSAGE_CHOICE_REFERAL = 'Выберите реферала:'
MESSAGE_NO_REFERALS = 'Список рефералов пустой!'

def referal_detail(ref_id, ref_url, ref_join_date, ref_total_users, ref_active_users,
                   ref_block_users, ref_sub_users, ref_prem_users):
    message = f"""
    Статистика по рефералу:
    
    📎  Ссылка:  {ref_url}  # {ref_id}
    ⌚️ Время создания:  {ref_join_date}

    🚪 Переходы:  {ref_total_users}
    🟢 Активные пользователи:  {ref_active_users}👤
    🔴 Не активные: {ref_block_users}👤
    🤝 Прошли ОП: {ref_sub_users}👤
    🔮 Пользователи с перм-акаунтом: {ref_prem_users}👤
    """
    return message

MESSAGE_NO_CATEGORIES = 'Категорий нет, кина не будет)))'
MESSAGE_DELETE_LANGUAGE = '⬆️ Удалить язык выше? ⬆️'
BUTTON_DEL = 'DELETE'
MESSAGE_LANGUAGE_IS_DELETE = 'Язык был удален'
MESSAGE_LANGUAGE_IS_DELETE_ERR = 'Ошибка удаления языка! Смотрите логи.'

MESSAGE_DELETE_THEME = '⬆️ Удалить тему выше? ⬆️'
MESSAGE_THEME_IS_DELETE = 'Тема была удалена'
MESSAGE_THEME_IS_DELETE_ERR = 'Ошибка удаления темы! Смотрите логи.'

BUTTON_EXTRACT_USERS = 'Выгрузить пользователей'
MESSAGE_EXTRACT_USERS = 'Каких пользователей вигрузить в файл?'
BUTTON_ALL_USERS = 'Всех пользователей'
BUTTON_ALL_ACTIVE_USERS = 'Только активных'

COMMAND_DESCRIPTION_RANDOM_THEME = '🪄 Рандомная тема'
COMMAND_DESCRIPTION_RANDOM_LANGUAGE = '🪄 Рандомный язык'

def message_what_your_device(user_full_name):
    if user_full_name:
        return f'{user_full_name}, какое у тебя устройство?'
    return 'Какое у тебя устройство?'
MESSAGE_ON_RANDOM_SOME_ERROR = 'Хмм...🧐 Что-то пошло не так, попробуй сначала 🥹 или попытайся позже'
MESSAGE_IS_NOT_YOUR_GET_RANDOM = f'''
Не вы вызвали это меню, не вам и щелкать кнопки😁
Загляните в меню и вызовите команду от своего имени.
Или переходи к боту: {NAME}
'''
COMMAND_DESCRIPTION_SET_WALLPAPER = 'Установить обои в андроид тему'
COMMAND_DESCRIPTION_RESTART_BOT = 'Рестарт бота'
SECON_MESSAGE_ON_START_IN_GROUP = '''
У меня есть команды которые ты можешь использовать здесь 😋

Мои команды:
/randomtheme - 🔖 Рандомная тема
/randomlanguage - 📝 Рандомный язык
'''
def preview_caption_on_theme(devise: str):
    return f'❕ Тема для {devise}\n\nКаталог тем - {NAME}'
BUTTON_INSTALL_THEME = '🔮Установить'
CAPTION_ON_THEME_FILE = f'''
❕Нажми на файл для установки

{NAME} - каталог тем 🪄
'''
MESSAGE_SEND_ANDROID_THEME_FILE = 'Отправьте мне файл с темой для Android устройства чтобы заменить в нем обои⤵️'
MESSAGE_SEND_WALLPAPER = 'Отправьте мне картинку которую нужно вставить в файл темы⤵️'
ERROR_MESSAGE_SEND_ANDROID_THEME_FILE = '❗️Это не файл с темой для Android устройства❗️\n\nОтправьте мне файл с темой для Android устройства⤵️'
ERROR_MESSAGE_SEND_WALLPAPER = '❗️Это не картинка❗️\n\nОтправьте мне картинку⤵️'
ERROR_MESSAGE_INSERT_WALLPAPER = '❗️Что-то пошло не так❗️\n\nПроверьте картинку, может не подходит формат или битый файл темы и попробуйте снова'
ABORT_INSERT_WALLPAPER = 'Вставка обоев отменена❕'

BUTTON_START_CREATE_WALLPAPER = '🏞Создать фон для тг'
MESSAGE_FILLER = 'Ну что ж, давай приступим'
MESSAGE_WALLP_START = 'Отправьте мне картинку и я сделаю из нее фон для Telegram'
def wallpaper_message(wallpaper):
    message = f"""
    Вот твои <a href="https://t.me/bg/{wallpaper}">обои</a> для Telegram
Фон создан в <a href="https://t.me/{NAME[1:]}?start=from_wallpaper">{NAME}</a> 😉
    """
    return message

BUTTON_GET_THEME = '💾Установить'
BUTTON_PREV = '⬅️'
BUTTON_NEXT = '➡️'