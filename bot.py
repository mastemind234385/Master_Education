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

from config import BOT_TOKEN
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("📖 বাংলা", callback_data="subject_bangla"),
            InlineKeyboardButton("🇬🇧 English", callback_data="subject_english")
        ],
        [
            InlineKeyboardButton("➗ গণিত", callback_data="subject_math"),
            InlineKeyboardButton("⚡ পদার্থবিজ্ঞান", callback_data="subject_physics")
        ],
        [
            InlineKeyboardButton("🧪 রসায়ন", callback_data="subject_chemistry"),
            InlineKeyboardButton("🧬 জীববিজ্ঞান", callback_data="subject_biology")
        ],
        [
            InlineKeyboardButton("💻 ICT", callback_data="subject_ict"),
            InlineKeyboardButton(
                "🌍 বাংলাদেশ ও বিশ্বপরিচয়",
                callback_data="subject_bgs"
            )
        ],
        [
            InlineKeyboardButton("☪️ ধর্ম", callback_data="subject_religion"),
            InlineKeyboardButton("📝 অন্যান্য", callback_data="subject_other")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎓 *Class 10 Q&A Bot*\n\n"
        "তোমার Subject নির্বাচন করো 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def subject_selected(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    subject = query.data.replace("subject_", "")

    context.user_data["subject"] = subject

    subject_name = SUBJECTS.get(subject, "Subject")

    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 Subjects",
                callback_data="back_subjects"
            )
        ]
    ]

    await query.edit_message_text(
        f"{subject_name}\n\n"
        "✍️ এখন তোমার প্রশ্নটি লিখে পাঠাও।\n\n"
        "বাংলা অথবা English—দুইভাবেই প্রশ্ন করতে পারো।",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def back_subjects(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("📖 বাংলা", callback_data="subject_bangla"),
            InlineKeyboardButton("🇬🇧 English", callback_data="subject_english")
        ],
        [
            InlineKeyboardButton("➗ গণিত", callback_data="subject_math"),
            InlineKeyboardButton("⚡ পদার্থবিজ্ঞান", callback_data="subject_physics")
        ],
        [
            InlineKeyboardButton("🧪 রসায়ন", callback_data="subject_chemistry"),
            InlineKeyboardButton("🧬 জীববিজ্ঞান", callback_data="subject_biology")
        ],
        [
            InlineKeyboardButton("💻 ICT", callback_data="subject_ict"),
            InlineKeyboardButton(
                "🌍 বাংলাদেশ ও বিশ্বপরিচয়",
                callback_data="subject_bgs"
            )
        ],
        [
            InlineKeyboardButton("☪️ ধর্ম", callback_data="subject_religion"),
            InlineKeyboardButton("📝 অন্যান্য", callback_data="subject_other")
        ]
    ]

    await query.edit_message_text(
        "🎓 *Class 10 Q&A Bot*\n\n"
        "তোমার Subject নির্বাচন করো 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def question_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_question = update.message.text

    subject = context.user_data.get("subject")

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

        answer = result["answer_bn"]

        if not answer:
            answer = result["answer_en"]

        await update.message.reply_text(
            f"✅ *Answer*\n\n{answer}",
            parse_mode="Markdown"
        )

    else:

        await update.message.reply_text(
            "❌ এই প্রশ্নটির উত্তর এখনো আমার database-এ নেই।\n\n"
            "অন্য প্রশ্ন চেষ্টা করো।"
        )


def main():

    if not BOT_TOKEN:

        raise ValueError(
            "BOT_TOKEN environment variable পাওয়া যায়নি!"
        )

    create_database()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(
            subject_selected,
            pattern=r"^subject_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            back_subjects,
            pattern=r"^back_subjects$"
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            question_handler
        )
    )

    print("🤖 Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()