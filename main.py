import os
import logging
import coloredlogs
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import inspect


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s --- %(message)s')

load_dotenv('creds/.env')

class Mif:
    '''
    Main class for bot

    REQUIREMENTS:
    - API_KEY environment variable must be set in .env file

    Functions that start with _ are not added as commands
    '''
    def __init__(self):
        token = os.getenv('API_KEY')
        assert token is not None, 'API_KEY is not set in .env file'
        self.app = ApplicationBuilder().token(token).build()

        for command in inspect.getmembers(self, predicate=inspect.ismethod):
            if not command[0].startswith('_'):
                self.app.add_handler(CommandHandler(command[0], command[1]))
                logger.info(f'Added command {command[0]}')

        logger.info('Bot ready')
    
    def _run(self):
        logger.info('Running bot')
        self.app.run_polling()
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Boo, Mif is here')

if __name__ == '__main__':
    bot = Mif()
    bot._run()