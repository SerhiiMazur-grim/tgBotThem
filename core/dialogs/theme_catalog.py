from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models.theme_category import ThemeInCatalog
from core.keyboards.inline_keybords import theme_catalog_ikb
from core.keyboards.reply_keybords import user_keyboard
from config import messages


class ThemeCatalogDialog():
    PREV_STEP = 'prev_page_theme_cat'
    NEXT_STEP = 'next_page_theme_cat'
    SHOW_THEME = 'show_them_'
    CALL_DATA_NONE = 'NONE'
    DEL_THEME = 'del_theme_id_'
    
    DEVICES = {
        'android': 'Android 💚',
        'computer': 'Desktop 🩶',
        'ios': 'iOS 🤍'
    }
    
    def __init__(self,
                 call: CallbackQuery,
                 state: FSMContext,
                 session: AsyncSession) -> None:
        self.call = call
        self.state = state
        self.session = session
    
    
    @property
    def call_data(self):
        data: str = self.call.data
        return data
    
    
    @property
    def theme_index(self):
        if self.call_data.startswith(self.SHOW_THEME):
            id = self.call_data.split('_')[-1]
            id = int(id)
        else:
            id = None
        return id
    
    
    @property
    def theme_id(self):
        if self.call_data.startswith(self.DEL_THEME):
            id = self.call_data.split('_')[-1]
            id = int(id)
        else:
            id = None
        return id
    
    
    @property
    def user_id(self):
        user_id = self.call.from_user.id
        return user_id
    
    
    async def state_data(self):
        data: dict = await self.state.get_data()
        return data
    
    
    async def delete_theme(self, data, page, pages):
        try:
            theme = await self.session.scalar(select(ThemeInCatalog).where(ThemeInCatalog.id==self.theme_id))
            await self.session.delete(theme)
            await self.session.commit()
            
            catalog = data.get('catalog')
            catalog.pop(page-1)
            
            if not catalog:
                await self.call.message.delete()
                await self.state.clear()
                await self.call.answer(text=messages.MESSAGE_THEME_IS_DELETE)
                return await self.call.message.answer(text=messages.MESSAGE_NO_THEMES_IN_CATALOG,
                                                      reply_markup=user_keyboard(self.user_id))
            
            pages = pages-1
            await self.state.update_data({
                'catalog': catalog,
                'pages': pages
            })
            data = await self.state_data()
            await self.call.answer(text=messages.MESSAGE_THEME_IS_DELETE)
            return await self._next_step(data, page-1)
            
        
        except Exception as e:
            print(e)
            await self.call.answer(text=messages.MESSAGE_THEME_IS_DELETE_ERR,
                                   show_alert=True)

    
    
    async def _first_window(self, data, page):
        catalog = data.get('catalog')
        pages = data.get('pages')
        device = data.get('device')
        index = page-1
        theme: ThemeInCatalog = catalog[index]
        
        return await self.call.message.answer_photo(photo=theme.preview,
                                                    caption=f'Тема для {self.DEVICES[device]}',
                                                    parse_mode=ParseMode.HTML,
                                                    reply_markup=theme_catalog_ikb(page, pages, self.user_id, theme.id))
    
    
    async def _next_step(self, data, page):
        next_page = page + 1
        index = page
        catalog = data.get('catalog')
        pages = data.get('pages')
        
        if next_page > pages:
            next_page = 1
            index = 0
            
        theme: ThemeInCatalog = catalog[index]
        await self.state.update_data(page=next_page)
        media = InputMediaPhoto(media=theme.preview,
                                caption=self.call.message.caption,
                                parse_mode=ParseMode.HTML)
        return await self.call.message.edit_media(media=media,
                                                  reply_markup=theme_catalog_ikb(next_page, pages, self.user_id, theme.id))
    
    
    async def _prev_step(self, data, page):
        prev_page = page - 1
        index = page-2
        catalog = data.get('catalog')
        pages = data.get('pages')
        
        if prev_page < 1:
            prev_page = pages
            index = pages-1
            
        theme: ThemeInCatalog = catalog[index]
        await self.state.update_data(page=prev_page)
        media = InputMediaPhoto(media=theme.preview,
                                caption=self.call.message.caption,
                                parse_mode=ParseMode.HTML)
        return await self.call.message.edit_media(media=media,
                                                  reply_markup=theme_catalog_ikb(prev_page, pages, self.user_id, theme.id))
    
    
    async def _show_theme(self, data):
        catalog = data.get('catalog')
        theme: ThemeInCatalog = catalog[self.theme_index]
        await self.state.clear()
        
        await self.call.message.edit_reply_markup(reply_markup=None)
        return await self.call.message.answer_document(document=theme.file,
                                                       caption=messages.CAPTION_TO_THEME_IN_CATALOG,
                                                       parse_mode=ParseMode.HTML,
                                                       reply_markup=user_keyboard(self.user_id))
    
    
    async def dialog_window(self):
        data = await self.state_data()
        page = data.get('page')
        pages = data.get('pages')
        
        if self.theme_index is not None:
            return await self._show_theme(data)
        
        if self.call_data.startswith(self.DEL_THEME):
            return await self.delete_theme(data, page, pages)
        
        if page==1 and self.call_data not in (self.NEXT_STEP, self.PREV_STEP, self.CALL_DATA_NONE):
            return await self._first_window(data, page)
        
        if self.call_data==self.CALL_DATA_NONE or pages==1:
            return await self.call.answer()
        
        if self.call_data==self.NEXT_STEP:
            return await self._next_step(data, page)
            
        if self.call_data==self.PREV_STEP:
            return await self._prev_step(data, page)
