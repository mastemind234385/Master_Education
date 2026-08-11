from database import (
    create_database,
    add_question
)


create_database()


add_question(
    "chemistry",

    "পানির রাসায়নিক সংকেত কী?",

    "What is the chemical formula of water?",

    "পানির রাসায়নিক সংকেত H₂O।",

    "The chemical formula of water is H₂O."
)


add_question(
    "math",

    "৫ × ৮ কত?",

    "What is 5 × 8?",

    "৫ × ৮ = ৪০",

    "5 × 8 = 40"
)


add_question(
    "biology",

    "সালোকসংশ্লেষণ কী?",

    "What is photosynthesis?",

    "সালোকসংশ্লেষণ হলো এমন একটি প্রক্রিয়া যার মাধ্যমে সবুজ উদ্ভিদ সূর্যের আলোর সাহায্যে খাদ্য তৈরি করে।",

    "Photosynthesis is the process by which green plants make food using sunlight."
)


print("Sample data added successfully!")
