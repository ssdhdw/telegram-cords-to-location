import telebot
import os

API_TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Coordinates to venue bot greeting you
Send me coordinates and i send you same venue, For examlpe:
`55.983403 37.208097`
Better use with inline:
`@coords2venueBot 55.983403 37.208097`
or
`@coords2venueBot 55.983403 37.208097 МИЭТ Начало пар в 9:00`
Underscore in title will be replaced with space
`@coords2venueBot 55.983403 37.208097 МИЭТ_Университет Начало пар в 9:00`\
""", parse_mode="MarkdownV2")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    text = message.text.replace(",", "")
    text = text.split()
    if len(text) != 2:
        bot.reply_to(message, "Worng usage")
        return
    try:
        latitude = float(text[0])
        longitude = float(text[1])
        bot.send_location(message.chat.id,
                          latitude,
                          longitude,
                          reply_to_message_id=message.id)
    except Exception:
        bot.reply_to(message, "Error")

@bot.inline_handler(func=lambda message: True)
def inline_handler(query: telebot.types.InlineQuery):
    text = query.query
    text = text.split()
    results = []
    if len(text) < 2:
        bot.answer_inline_query(query.id, results)
        return
    elif len(text) == 2:
        try:
            latitude = float(text[0].replace(",", ""))
            longitude = float(text[1].replace(",", ""))
            title = f"{latitude} {longitude}"
            results.append(telebot.types.InlineQueryResultLocation(title, title, latitude, longitude, 0))
            bot.answer_inline_query(query.id, results)
        except Exception:
            bot.answer_inline_query(query.id, results)
            return
    elif len(text) > 2:
        try:
            latitude = float(text[0].replace(",", ""))
            longitude = float(text[1].replace(",", ""))
            title = text[2].replace("_", " ")
            address = " "
            if len(text) > 3:
                address = " ".join(text[3:])
            results.append(telebot.types.InlineQueryResultVenue(f"{latitude} {longitude}", title, latitude, longitude, address))
            bot.answer_inline_query(query.id, results)
        except Exception:
            bot.answer_inline_query(query.id, results)
            return
    
bot.infinity_polling()