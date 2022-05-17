import os
import re
import pytz
from source.work_flow.workflow import WorkFlow
from source.configs import init_environment
from source.data_classes.data_package import DataPackage
from source.data_classes.errors import TimeFormatError
from telegram import Update
import datetime
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)


class Bot:
    def __init__(self):
        init_environment()
        self.work_flow = WorkFlow()
        self.updater: Updater
        self.update = Update
        self.updater = Updater(os.getenv("TELEGRAM_TOKEN"))
        self.dispatcher = self.updater.dispatcher

    @staticmethod
    def remove_job_if_exists(name, context: CallbackContext):
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    @staticmethod
    def _get_data_package(chat_id, ids_list, from_date, to_date, filter_status):
        # TODO create method to get ids list and data
        return DataPackage.create(chat_id, ids_list, from_date, to_date, filter_status)

    @staticmethod
    def _get_time(time_data):
        if re.match(r"^(2[0-3]|[0-1]?[0-9])(\.)([0-5]?[0-9])$", time_data):
            hours, minutes = time_data.split(".")
            return datetime.time(hour=int(hours), minute=int(minutes), second=00, tzinfo=pytz.timezone("Europe/Moscow"))
        else:
            raise TimeFormatError()

    def get_today(self, update: Update, context: CallbackContext):
        data_package = self._get_data_package(update.message.chat_id, [312, 313, 311, 314], "2022-04-29", None, True)
        self.work_flow.set_task(data_package)

    def run_daily(self, update: Update, context: CallbackContext):
        try:
            self.remove_job_if_exists(str(update.effective_chat.id), context)
            time = self._get_time(context.args[0])
            data_package = self._get_data_package(update.effective_chat.id, [312, 313, 311, 314], "2022-04-29", None,
                                                  True)
            context.job_queue.run_daily(
                self.work_flow.set_task,
                time=time,
                context=data_package,
                name=str(update.message.chat_id))
        except TimeFormatError:
            update.message.reply_text(f"Time format is invalid")
        else:
            update.message.reply_text(f"Notifications set to {time}!")

    def unset(self, update, context):
        chat_id = update.message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id), context)
        text = 'Notifications have been canceled.' if job_removed else 'No active notifications.'
        update.message.reply_text(text)

    def start(self):
        timer_handler = CommandHandler('notify', self.run_daily, run_async=True)
        timer_deleter = CommandHandler('unset', self.unset, run_async=True)
        get_today = CommandHandler('get_today', self.get_today, run_async=True)
        self.dispatcher.add_handler(timer_handler)
        self.dispatcher.add_handler(timer_deleter)
        self.dispatcher.add_handler(get_today)
        self.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        self.updater.idle()


def main():
    bot = Bot()
    bot.start()


if __name__ == '__main__':
    main()
