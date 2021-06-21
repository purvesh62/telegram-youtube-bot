"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json
# Enable logging
from youtube_api import YoutubeAPI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class TelegramBot(YoutubeAPI):
    def __init__(self):
        YoutubeAPI.__init__(self)
        with open('BOT//credentials.json') as file:
            data = json.loads(file.read())
            self.auth_token = data.get('telegram_auth_token')
            self.playlistId = data.get('playlist_id')

    def main(self) -> None:
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        updater = Updater(self.auth_token)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help_command))

        # on non command i.e message - echo the message on Telegram
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    # Define a few command handlers. These usually take the two arguments update and
    # context.
    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True),
        )

    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def echo(self, update: Update, context: CallbackContext) -> None:
        """Echo the user message."""
        if 'https://www.youtube.com/watch' in update.message.text:
            video_id = update.message.text.split('?v=')[1].split('&')[0]
            response = self.get_video_info(video_id)
            if len(response.get('items')) > 0:
                self.insert_into_playlist(self.playlistId, video_id)
                update.message.text = f'I have added the song to the playlist {update.effective_user.name}'
            else:
                update.message.text = f'Due to some error I couldn\'t perform the operation.'
        elif 'https://youtu.be' in update.message.text:
            video_id = update.message.text.split('/')[-1]
            response = self.get_video_info(video_id)
            if len(response.get('items')) > 0:
                self.insert_into_playlist(self.playlistId, video_id)
                update.message.text = f'I have added the song to the playlist {update.effective_user.name}'
            else:
                update.message.text = f'Due to some error I couldn\'t perform the operation.'
        update.message.reply_text(update.message.text)


if __name__ == '__main__':
    TelegramBot().main()
