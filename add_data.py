from database import create_database, add_question


create_database()


add_question(
    "chemistry",
    "পানির রাসায়নিক সংকেত কী?",
    "What is the chemical formula of water?",
    "পানির রাসায়নিক সংকেত H₂O।",
    "The chemical formula of water is H₂O."
)


add_question(
    "physics",
    "আলোর বেগ কত?",
    "What is the speed of light?",
    "শূন্যস্থানে আলোর বেগ প্রায় ৩ × ১০⁸ মিটার/সেকেন্ড।",
    "The speed of light in vacuum is approximately 3 × 10⁸ meters per second."
)


add_question(
    "biology",
    "সালোকসংশ্লেষণ কী?",
    "What is photosynthesis?",
    "সালোকসংশ্লেষণ হলো এমন একটি প্রক্রিয়া যার মাধ্যমে সবুজ উদ্ভিদ সূর্যের আলোর সাহায্যে খাদ্য তৈরি করে।",
    "Photosynthesis is the process by which green plants make food using sunlight."
)


add_question(
    "math",
    "৫ × ৮ কত?",
    "What is 5 × 8?",
    "৫ × ৮ = ৪০",
    "5 × 8 = 40"
)


print("✅ Sample questions added!")