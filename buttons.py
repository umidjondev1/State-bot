from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

Tasdiqlash = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="ha"), InlineKeyboardButton(text="Bekor qilish ❌", callback_data="yoq")]
    ]
)