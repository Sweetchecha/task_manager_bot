from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Список задач (в реальном проекте стоит использовать базу данных)
tasks = {}


# Функции для обработки команд
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я бот для управления задачами. Используйте /help для получения списка команд.')


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/start - Приветственное сообщение\n"
        "/addtask <задача> - Добавить задачу\n"
        "/listtasks - Показать все задачи\n"
        "/removetask <номер> - Удалить задачу\n"
        "/cleartasks - Очистить все задачи\n"
    )


def add_task(update: Update, context: CallbackContext):
    if context.args:
        task = " ".join(context.args)
        task_id = len(tasks) + 1
        tasks[task_id] = task
        update.message.reply_text(f'Задача "{task}" добавлена с номером {task_id}.')
    else:
        update.message.reply_text('Пожалуйста, укажите задачу после команды /addtask.')


def list_tasks(update: Update, context: CallbackContext):
    if tasks:
        task_list = "\n".join([f"{key}. {value}" for key, value in tasks.items()])
        update.message.reply_text(f"Список задач:\n{task_list}")
    else:
        update.message.reply_text("Список задач пуст.")


def remove_task(update: Update, context: CallbackContext):
    if context.args and context.args[0].isdigit():
        task_id = int(context.args[0])
        if task_id in tasks:
            removed_task = tasks.pop(task_id)
            update.message.reply_text(f'Задача "{removed_task}" удалена.')
        else:
            update.message.reply_text("Задача с таким номером не найдена.")
    else:
        update.message.reply_text("Пожалуйста, укажите номер задачи для удаления.")


def clear_tasks(update: Update, context: CallbackContext):
    tasks.clear()
    update.message.reply_text("Все задачи удалены.")


# Функция для автоматического выполнения задач (например, напоминания)
def scheduled_task():
    print("Это пример автоматической задачи!")


# Основная функция для запуска бота
def main():
    # Создаем объект Updater
    updater = Updater("YOUR_API_KEY", use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Добавляем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("addtask", add_task))
    dispatcher.add_handler(CommandHandler("listtasks", list_tasks))
    dispatcher.add_handler(CommandHandler("removetask", remove_task))
    dispatcher.add_handler(CommandHandler("cleartasks", clear_tasks))

    # Создаем планировщик для автоматических задач
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', minutes=5)  # Пример задачи, которая выполняется каждые 5 минут
    scheduler.start()

    # Запускаем бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()