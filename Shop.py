import telebot, buttons as bt, database as db
from geopy import Nominatim
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot('YOUR_TOKEN_HERE')
# Использование карт
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')


# Обработка команды старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    check = db.checker(user_id)
    if check:
        bot.send_message(user_id, f'Добро Пожаловать {message.from_user.first_name}!')
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию☺️!'
                                  '\nВведите свое имя:')
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Отлично! Пожалуйста поделитесь контактом☎️:', reply_markup=bt.num_bt())
    # Этап получения номера
    bot.register_next_step_handler(message, get_number, name)


# Этап получения номера
def get_number(message, name):
    user_id = message.from_user.id
    # Если юзер отправил номер по кнопке
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Принято! И последнее поделитесь локацией🗺:', reply_markup=bt.loc_bt())
        # Этап получения локации
        bot.register_next_step_handler(message, get_location, name, number)
    # Если юзер отправил не по кнопке
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь контактом☎️!', reply_markup=bt.num_bt())
        # Этап получения номера
        bot.register_next_step_handler(message, get_number, name)


# Этап получения локации
def get_location(message, name, number):
    user_id = message.from_user.id
    # Если юзер отправил локацию по кнопке
    if message.location:
        location = str(geolocator.reverse(f'{message.location.latitude}, '
                                          f'{message.location.longitude}'))
        db.registration(user_id, name, number, location)
        products = db.get_pr_but()
        bot.send_message(user_id, 'Все готово! Регистрация прошла успешно✅',
                         reply_markup=bt.main_menu_buttons(products))
    # Если юзер отправил не по кнопке
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь локацией🗺!', reply_markup=bt.loc_bt())
        # Этап получения локации
        bot.register_next_step_handler(message, get_location, name, number)


# Обработка команды admin
@bot.message_handler(commands=['admin'])
def act(message):
    admin_id = 692440883
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Выберите действие:', reply_markup=bt.admin_menu())
        # Переход на этап выбора
        bot.register_next_step_handler(message, admin_choose)
    else:
        bot.send_message(message.from_user.id, 'Вы не админ!')


# Выбор действия админом
def admin_choose(message):
    admin_id = 692440883
    if message.text == 'Добавить продукт':
        bot.send_message(admin_id, 'Напишите название продукта!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_name)
    elif message.text == 'Удалить продукт':
        bot.send_message(admin_id, 'Напишите id продукта!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_id)
    elif message.text == 'Изменить продукт':
        bot.send_message(admin_id, 'Напишите id продукта!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_change)
    elif message.text == 'Перейти в меню':
        products = db.get_pr_but()
        bot.send_message(admin_id, 'Добро пожаловать в меню!',
                         reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(admin_id, 'Неизвестная операция', reply_markup=bt.admin_menu())
        # Возврат на этап выбора
        bot.register_next_step_handler(message, admin_choose)

# def maintainnig(message, name, number):
#     user_id = message.from_user.id
#     bot.send_message(user_id, 'Пока что бот на тех. обслуживании👷🏾‍♂️')
#
#
# @bot.message_handler(commands=['негр'])
# def negr(message):
#     user_id = message.from_user.id
#     bot.send_message(user_id, 'Как сказал создатель этого бота:\n"Это всего лишь слово для идентификации Акмаля"')


bot.polling(none_stop=True)
