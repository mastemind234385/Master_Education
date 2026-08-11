import asyncio

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route

import uvicorn

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN, PORT, KOYEB_PUBLIC_DOMAIN

from database import (
    create_database,
    search_question
)


SUBJECTS = {
    "bangla": "📖 বাংলা",
    "english": "🇬🇧 English",
    "math": "➗ গণিত",
    "physics": "⚡ পদার্থবিজ্ঞান",
    "chemistry": "🧪 রসায়ন",
    "biology": "🧬 জীববিজ্ঞান",
    "ict": "💻 ICT",
    "bgs": "🌍 বাংলাদেশ ও বিশ্বপরিচয়",
    "religion": "☪️ ধর্ম",
    "other": "📝 অন্যান্য"
}


def subject_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📖 বাংলা",
                callback_data="subject_bangla"
            ),
            InlineKeyboardButton(
                "🇬🇧 English",
                callback_data="subject_english"
            )
        ],
        [
            InlineKeyboardButton(
                "➗ গণিত",
                callback_data="subject_math"
            ),
            InlineKeyboardButton(
                "⚡ পদার্থবিজ্ঞান",
                callback_data="subject_physics"
            )
        ],
        [
            InlineKeyboardButton(
                "🧪 রসায়ন",
                callback_data="subject_chemistry"
            ),
            InlineKeyboardButton(
                "🧬 জীববিজ্ঞান",
                callback_data="subject_biology"
            )
        ],
        [
            InlineKeyboardButton(
                "💻 ICT",
                callback_data="subject_ict"
            ),
            InlineKeyboardButton(
                "🌍 বাংলাদেশ ও বিশ্বপরিচয়",
                callback_data="subject_bgs"
            )
        ],
        [
            InlineKeyboardButton(
                "☪️ ধর্ম",
                callback_data="subject_religion"
            ),
            InlineKeyboardButton(
                "📝 অন্যান্য",
                callback_data="subject_other"
            )
        ]
    ])


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.pop("subject", None)

    await update.message.reply_text(
        "🎓 *Class 10 Q&A Bot*\n\n"
        "তোমার Subject নির্বাচন করো 👇",
        reply_markup=subject_keyboard(),
        parse_mode="Markdown"
    )


async def subject_selected(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    subject = query.data.replace(
        "subject_",
        ""
    )

    context.user_data["subject"] = subject

    subject_name = SUBJECTS.get(
        subject,
        "Subject"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 Subjects",
                callback_data="back_subjects"
            )
        ]
    ])

    await query.edit_message_text(
        f"{subject_name}\n\n"
        "✍️ এখন তোমার প্রশ্নটি লিখে পাঠাও।\n\n"
        "বাংলা অথবা English—দুইভাবেই প্রশ্ন করতে পারো।",
        reply_markup=keyboard
    )


async def back_subjects(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    context.user_data.pop("subject", None)

    await query.edit_message_text(
        "🎓 *Class 10 Q&A Bot*\n\n"
        "তোমার Subject নির্বাচন করো 👇",
        reply_markup=subject_keyboard(),
        parse_mode="Markdown"
    )


async def question_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_question = update.message.text

    subject = context.user_data.get(
        "subject"
    )

    if not subject:

        await update.message.reply_text(
            "⚠️ আগে একটি Subject নির্বাচন করো।\n\n"
            "/start চাপো।"
        )

        return

    result = search_question(
        subject,
        user_question
    )

    if result:

        answer = (
            result.get("answer_bn")
            or result.get("answer_en")
        )

        await update.message.reply_text(
            f"✅ *Answer*\n\n{answer}",
            parse_mode="Markdown"
        )

    else:

        await update.message.reply_text(
            "❌ এই প্রশ্নটির উত্তর এখনো "
            "আমার database-এ নেই।\n\n"
            "অন্য প্রশ্ন চেষ্টা করো।"
        )


async def telegram_webhook(
    request: Request
):

    data = await request.json()

    update = Update.de_json(
        data=data,
        bot=application.bot
    )

    await application.update_queue.put(
        update
    )

    return Response(status_code=200)


async def healthcheck(
    request: Request
):

    return PlainTextResponse(
        "Class 10 Q&A Bot is running ✅"
    )


async def main():

    global application

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN পাওয়া যায়নি!"
        )

    if not KOYEB_PUBLIC_DOMAIN:

        raise RuntimeError(
            "KOYEB_PUBLIC_DOMAIN পাওয়া যায়নি!"
        )

    create_database()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .updater(None)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            subject_selected,
            pattern=r"^subject_"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            back_subjects,
            pattern=r"^back_subjects$"
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            question_handler
        )
    )

    webhook_url = (
        f"https://{KOYEB_PUBLIC_DOMAIN}"
        f"/telegram"
    )

    await application.bot.set_webhook(
        url=webhook_url,
        allowed_updates=Update.ALL_TYPES
    )

    routes = [
        Route(
            "/telegram",
            telegram_webhook,
            methods=["POST"]
        ),
        Route(
            "/",
            healthcheck,
            methods=["GET"]
        ),
        Route(
            "/healthcheck",
            healthcheck,
            methods=["GET"]
        )
    ]

    web_app = Starlette(
        routes=routes
    )

    server = uvicorn.Server(
        uvicorn.Config(
            web_app,
            host="0.0.0.0",
            port=PORT
        )
    )

    async with application:

        await application.start()

        await server.serve()

        await application.stop()


if __name__ == "__main__":

    asyncio.run(main())
