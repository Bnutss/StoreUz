from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.config import WEBAPP_URL
from bot.keyboards.reply import main_menu_keyboard

router = Router()

STATUS_LABELS = {
    'new': '🆕 Новый',
    'confirmed': '✅ Подтверждён',
    'paid': '💳 Оплачен',
    'shipped': '🚚 Отправлен',
    'delivered': '📦 Доставлен',
    'cancelled': '❌ Отменён',
}


@router.message(F.text == '📦 Мои заказы')
async def my_orders(message: Message, db_user):
    if not db_user or not db_user.phone_number:
        await message.answer('⚠️ Сначала пройдите регистрацию. Введите /start')
        return

    from telegrambot.models import Order
    orders = await Order.objects.filter(user=db_user).aorder_by('-created_at').ato_list()

    if not orders:
        await message.answer(
            '📭 У вас пока нет заказов.\n\nОткройте магазин и сделайте первый заказ! 🛍',
            reply_markup=main_menu_keyboard(WEBAPP_URL),
        )
        return

    text = '📦 <b>Ваши заказы:</b>\n\n'
    for order in orders[:10]:
        status = STATUS_LABELS.get(order.status, order.status)
        text += (
            f'<b>Заказ #{order.pk}</b>\n'
            f'Статус: {status}\n'
            f'Сумма: {int(order.total_price):,} сум\n'
            f'Дата: {order.created_at.strftime("%d.%m.%Y %H:%M")}\n'
            '━━━━━━━━━━━━━━━\n'
        )

    await message.answer(text, parse_mode='HTML', reply_markup=main_menu_keyboard(WEBAPP_URL))


@router.message(F.text == '👤 Профиль')
async def profile(message: Message, db_user):
    if not db_user or not db_user.phone_number:
        await message.answer('⚠️ Сначала пройдите регистрацию. Введите /start')
        return

    from telegrambot.models import Order
    orders_count = await Order.objects.filter(user=db_user).acount()

    name = f'{db_user.first_name or ""} {db_user.last_name or ""}'.strip() or 'Не указано'
    phone = db_user.phone_number or 'Не указан'
    username = f'@{db_user.username}' if db_user.username else 'Не указан'

    text = (
        '👤 <b>Ваш профиль</b>\n\n'
        f'👤 Имя: <b>{name}</b>\n'
        f'📱 Телефон: <b>{phone}</b>\n'
        f'🔗 Username: <b>{username}</b>\n'
        f'📦 Заказов: <b>{orders_count}</b>\n'
        f'📅 Дата регистрации: <b>{db_user.created_at.strftime("%d.%m.%Y")}</b>\n'
    )

    await message.answer(text, parse_mode='HTML', reply_markup=main_menu_keyboard(WEBAPP_URL))


@router.message(F.text == '📞 Поддержка')
async def support(message: Message):
    text = (
        '📞 <b>Поддержка TIMODA</b>\n\n'
        '🕐 Мы работаем: 9:00 — 21:00\n\n'
        '📩 Напишите нам:\n'
        '• Telegram: @storeuzsupport\n'
        '• Телефон: +998 71 123-45-67\n\n'
        'Мы ответим в течение 30 минут!'
    )
    await message.answer(text, parse_mode='HTML')
