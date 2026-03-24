from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import WEBAPP_URL
from bot.keyboards.reply import phone_keyboard, main_menu_keyboard
from bot.keyboards.inline import open_webapp_keyboard

router = Router()


class RegistrationStates(StatesGroup):
    waiting_phone = State()


WELCOME_TEXT = (
    '👋 Добро пожаловать в <b>StoreUz</b> — ваш онлайн-магазин одежды!\n\n'
    '🛍 У нас вы найдёте:\n'
    '• Мужская, женская и детская одежда\n'
    '• Обувь на любой вкус\n'
    '• Аксессуары и сумки\n\n'
    '💳 Удобная оплата и быстрая доставка по всему Узбекистану.\n\n'
)

ALREADY_REGISTERED_TEXT = (
    '👋 С возвращением, <b>{name}</b>!\n\n'
    'Рады снова видеть вас в <b>StoreUz</b>.\n'
    'Нажмите кнопку ниже, чтобы открыть магазин 👇'
)

ASK_PHONE_TEXT = (
    '📱 Для продолжения нам нужен ваш номер телефона.\n\n'
    'Нажмите кнопку <b>«Поделиться номером»</b> ниже 👇'
)

REGISTRATION_SUCCESS_TEXT = (
    '✅ Регистрация прошла успешно!\n\n'
    'Добро пожаловать, <b>{name}</b>!\n\n'
    'Теперь вы можете делать покупки в нашем магазине 🛍'
)


@router.message(CommandStart())
async def cmd_start(message: Message, db_user, state: FSMContext):
    await state.clear()

    if db_user and db_user.phone_number:
        await message.answer(
            ALREADY_REGISTERED_TEXT.format(name=db_user.first_name or message.from_user.first_name),
            parse_mode='HTML',
            reply_markup=main_menu_keyboard(WEBAPP_URL),
        )
        return

    await message.answer(
        WELCOME_TEXT + 'Для начала давайте познакомимся 😊',
        parse_mode='HTML',
    )
    await message.answer(
        ASK_PHONE_TEXT,
        parse_mode='HTML',
        reply_markup=phone_keyboard(),
    )
    await state.set_state(RegistrationStates.waiting_phone)


@router.message(RegistrationStates.waiting_phone, F.contact)
async def handle_contact(message: Message, db_user, state: FSMContext):
    contact = message.contact
    if contact.user_id != message.from_user.id:
        await message.answer('❌ Пожалуйста, отправьте свой собственный номер телефона.')
        return

    db_user.phone_number = contact.phone_number
    if not db_user.first_name:
        db_user.first_name = message.from_user.first_name or ''
    if not db_user.last_name:
        db_user.last_name = message.from_user.last_name or ''
    await db_user.asave()

    await state.clear()

    name = db_user.first_name or message.from_user.first_name
    await message.answer(
        REGISTRATION_SUCCESS_TEXT.format(name=name),
        parse_mode='HTML',
        reply_markup=main_menu_keyboard(WEBAPP_URL),
    )


@router.message(RegistrationStates.waiting_phone)
async def handle_wrong_input(message: Message):
    await message.answer(
        '⚠️ Пожалуйста, воспользуйтесь кнопкой для отправки номера.',
        reply_markup=phone_keyboard(),
    )
