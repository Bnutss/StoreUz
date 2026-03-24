from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def open_webapp_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🛍 Перейти в магазин', web_app={'url': webapp_url})],
        ]
    )


def order_detail_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='📋 Детали заказа', callback_data=f'order:{order_id}')],
        ]
    )
