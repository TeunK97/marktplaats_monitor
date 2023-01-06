import telegram
import asyncio

class telegramNotifications:
    def __init__(self, token_id, chat_id):
        self.token_id = token_id
        self.chat_id = chat_id
        self.bot = telegram.Bot(token_id)

    async def notif(self, title, message, link, link_title):
        try:
            keyboard = [[telegram.InlineKeyboardButton(link_title, url=link)]]
            markup = telegram.InlineKeyboardMarkup(keyboard)
            await self.bot.send_message(
                text=f"""
                \U00002714 *{title}*\n{message}""",
                parse_mode="MarkdownV2",
                chat_id=self.chat_id,
                reply_markup=markup
                )
        except Exception as e:
            print(f"Error message: {e}")