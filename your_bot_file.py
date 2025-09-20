import logging
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Задание 1: Простое меню с кнопками
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем клавиатуру с кнопками
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Привет"))
    builder.add(types.KeyboardButton(text="Пока"))
    builder.adjust(2)  # Располагаем кнопки в 2 колонки

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


# Обработка нажатий на кнопки
@dp.message(F.text.in_(["Привет", "Пока"]))
async def handle_buttons(message: types.Message):
    user_name = message.from_user.first_name

    if message.text == "Привет":
        await message.answer(f"Привет, {user_name}!")
    else:
        await message.answer(f"До свидания, {user_name}!")


# Задание 2: Кнопки с URL-ссылками
@dp.message(Command("links"))
async def cmd_links(message: types.Message):
    # Создаем инлайн-клавиатуру с URL-кнопками
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Новости 📰",
        url="https://news.google.com"
    ))
    builder.add(types.InlineKeyboardButton(
        text="Музыка 🎵",
        url="https://www.youtube.com"
    ))
    builder.add(types.InlineKeyboardButton(
        text="Видео 🎥",
        url="https://vimeo.com"
    ))
    builder.adjust(1)  # По одной кнопке в строке

    await message.answer(
        "Выберите категорию:",
        reply_markup=builder.as_markup()
    )


# Задание 3: Динамическое изменение клавиатуры
@dp.message(Command("dynamic"))
async def cmd_dynamic(message: types.Message):
    # Создаем инлайн-кнопку "Показать больше"
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Показать больше ➕",
        callback_data="show_more"
    ))

    await message.answer(
        "Нажмите кнопку чтобы увидеть больше опций:",
        reply_markup=builder.as_markup()
    )


# Обработчик нажатия на кнопку "Показать больше"
@dp.callback_query(F.data == "show_more")
async def show_more_options(callback: types.CallbackQuery):
    # Создаем новые кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Опция 1 ✅",
        callback_data="option_1"
    ))
    builder.add(types.InlineKeyboardButton(
        text="Опция 2 ✅",
        callback_data="option_2"
    ))
    builder.adjust(2)  # Две кнопки в строке

    # Редактируем сообщение с новыми кнопками
    await callback.message.edit_text(
        "Выберите опцию:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


# Обработчики для опций
@dp.callback_query(F.data == "option_1")
async def handle_option_1(callback: types.CallbackQuery):
    await callback.message.edit_text("Вы выбрали Опцию 1")
    await callback.answer()


@dp.callback_query(F.data == "option_2")
async def handle_option_2(callback: types.CallbackQuery):
    await callback.message.edit_text("Вы выбрали Опцию 2")
    await callback.answer()


# Основная функция запуска
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())