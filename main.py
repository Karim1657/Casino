import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ⚙️ কনফিগারেশন (আপনার তথ্য এখানে বসান)
TOKEN = "YOUR_BOT_TOKEN_HERE"          # BotFather থেকে পাওয়া টোকেন
ADMIN_CHAT_ID = 123456789              # এডমিনের টেলিগ্রাম ইউজার আইডি (সংখ্যায়)

# 🎰 ক্যাসিনো সাইটসমূহের সম্পূর্ণ তালিকা
CASINO_SITES = [
    "JeeWin", "Baazi365", "MegaPari", "Melbet", 
    "1xBet", "Babu88", "Krikya", "Bet365", 
    "Casino88", "T20win", "Bwin", "JeetBuzz", 
    "Mostbet", "Pin-Up Casino", "MarvelBet", 
    "Crickex", "Betfair", "Betway"
]

# 🏠 /start কমান্ড ও মূল ড্যাশবোর্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⭐ BD P2P ড্যাশবোর্ড ⭐", callback_data="dashboard")],
        [InlineKeyboardButton("📥 ডিপোজিট করুন", callback_data="deposit_menu")],
        [InlineKeyboardButton("📤 উত্তোলন করুন", callback_data="withdraw_menu")],
        [InlineKeyboardButton("💾 প্লেয়ার আইডি সেভ করুন", callback_data="save_id_menu")],
        [InlineKeyboardButton("🤝 কাস্টমার সাপোর্ট", url="https://t.me/your_support_username")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "⭐ **BD P2P** ⭐\n"
        "📱 ইউজার ড্যাশবোর্ড\n"
        "------------------------------------\n"
        "💰 মূল ব্যালেন্স: ৳ 0.00\n\n"
        "💬 আপনার লেনদেন নিরাপদে সম্পন্ন করতে নিচের অপশনগুলো ব্যবহার করুন:"
    )
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# 📥 ডিপোজিট সাইট সিলেক্ট মেনু
async def deposit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for site in CASINO_SITES:
        keyboard.append([InlineKeyboardButton(f"🌐 {site}", callback_data=f"dep_site_{site}")])
    keyboard.append([InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "📥 **ডিপোজিট সেকশন**\n\nদয়া করে নিচের তালিকা থেকে আপনার ক্যাসিনো সাইটটি সিলেক্ট করুন:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 🌐 ডিপোজিট সাইট সিলেক্ট করার পর তথ্য চাওয়া
async def handle_deposit_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    site_name = query.data.split("_")[2]
    
    context.user_data['deposit_site'] = site_name
    context.user_data['waiting_for_deposit_info'] = True
    
    keyboard = [[InlineKeyboardButton("🔙 বাতিল করুন", callback_data="deposit_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"✅ আপনি সিলেক্ট করেছেন: **{site_name}**\n\n"
        f"✍️ এখন আপনার **প্লেয়ার আইডি**, **নাম** এবং **ব্যালেন্স/পরিমাণ** লিখে পাঠান\n"
        f"(উদাহরণ: `ID: 12345, Name: রহিম, Amount: 1000`)",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 📤 উত্তোলন সাইট সিলেক্ট মেনু
async def withdraw_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for site in CASINO_SITES:
        keyboard.append([InlineKeyboardButton(f"🌐 {site}", callback_data=f"wd_site_{site}")])
    keyboard.append([InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "📤 **উত্তোলন সেকশন**\n\nকোন সাইট থেকে উত্তোলন করতে চান? তালিকা থেকে সিলেক্ট করুন:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 📤 উত্তোলন সাইট সিলেক্ট করার পর তথ্য চাওয়া
async def handle_withdraw_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    site_name = query.data.split("_")[2]
    
    context.user_data['withdraw_site'] = site_name
    context.user_data['waiting_for_withdraw_info'] = True
    
    keyboard = [[InlineKeyboardButton("🔙 বাতিল করুন", callback_data="withdraw_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"✅ আপনি সিলেক্ট করেছেন: **{site_name}**\n\n"
        f"✍️ উত্তোলনের জন্য আপনার **প্লেয়ার আইডি**, **নাম** এবং **টাকার পরিমাণ** লিখে পাঠান:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 💾 প্লেয়ার আইডি সেভ মেনু
async def save_id_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for site in CASINO_SITES:
        keyboard.append([InlineKeyboardButton(f"🌐 {site}", callback_data=f"save_site_{site}")])
    keyboard.append([InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "💾 **প্লেয়ার আইডি সেভ সেকশন**\n\nযে সাইটের আইডি সেভ করতে চান তা সিলেক্ট করুন:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_save_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    site_name = query.data.split("_")[2]
    
    context.user_data['save_site'] = site_name
    context.user_data['waiting_for_save_id'] = True
    
    await query.edit_message_text(
        f"✅ সাইট: **{site_name}**\n\n✍️ এখন আপনার প্লেয়ার আইডি বা ইউজারনেম লিখে পাঠান:",
        parse_mode="Markdown"
    )

# 📨 ইউজারের মেসেজ হ্যান্ডেল করা
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user = update.effective_user
    
    if context.user_data.get('waiting_for_deposit_info'):
        site = context.user_data.get('deposit_site')
        keyboard = [
            [
                InlineKeyboardButton("✅ এপ্রুভ", callback_data=f"approve_dep_{user.id}"),
                InlineKeyboardButton("❌ রিজেক্ট", callback_data=f"reject_dep_{user.id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        admin_msg = (
            f"🔔 **নতুন ডিপোজিট রিকোয়েস্ট!**\n\n"
            f"🌐 **সাইট:** {site}\n"
            f"👤 **ইউজার:** {user.full_name} (@{user.username or 'N/A'})\n"
            f"🆔 **ডিটেইলস:** {user_text}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, reply_markup=reply_markup, parse_mode="Markdown")
        await update.message.reply_text("✅ আপনার ডিপোজিট রিকোয়েস্টটি এডমিনের কাছে পাঠানো হয়েছে। ⏳")
        context.user_data['waiting_for_deposit_info'] = False

    elif context.user_data.get('waiting_for_withdraw_info'):
        site = context.user_data.get('withdraw_site')
        keyboard = [
            [
                InlineKeyboardButton("✅ এপ্রুভ", callback_data=f"approve_wd_{user.id}"),
                InlineKeyboardButton("❌ রিজেক্ট", callback_data=f"reject_wd_{user.id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        admin_msg = (
            f"🔔 **নতুন উত্তোলন রিকোয়েস্ট!**\n\n"
            f"🌐 **সাইট:** {site}\n"
            f"👤 **ইউজার:** {user.full_name} (@{user.username or 'N/A'})\n"
            f"🆔 **ডিটেইলস:** {user_text}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, reply_markup=reply_markup, parse_mode="Markdown")
        await update.message.reply_text("✅ আপনার উত্তোলনের রিকোয়েস্টটি এডমিনের কাছে পাঠানো হয়েছে। ⏳")
        context.user_data['waiting_for_withdraw_info'] = False

    elif context.user_data.get('waiting_for_save_id'):
        site = context.user_data.get('save_site')
        await update.message.reply_text(f"💾 সফলভাবে সংরক্ষিত হয়েছে!\n🌐 সাইট: {site}\n🆔 আইডি: {user_text}")
        context.user_data['waiting_for_save_id'] = False

# 🛠️ এডমিন অ্যাকশন হ্যান্ডলার (এপ্রুভ / রিজেক্ট ও মেসেজ ডিলিট)
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    parts = data.split("_")
    action = parts[0]
    target_user_id = int(parts[2])
    
    if action == "approve":
        await context.bot.send_message(
            chat_id=target_user_id,
            text="🎉 অভিনন্দন! আপনার রিকোয়েস্টটি এডমিন কর্তৃক সফলভাবে **এপ্রুভ** করা হয়েছে। ✅"
        )
        await query.message.delete()
        
    elif action == "reject":
        await context.bot.send_message(
            chat_id=target_user_id,
            text="❌ দুঃখিত! আপনার রিকোয়েস্টটি এডমিন কর্তৃক **রিজেক্ট** করা হয়েছে।\n\n📌 কারণ: সঠিক তথ্য পাওয়া যায়নি। অনুগ্রহ করে সঠিক তথ্য দিয়ে পুনরায় চেষ্টা করুন।"
        )
        await query.message.delete()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(deposit_menu, pattern="^deposit_menu$"))
    app.add_handler(CallbackQueryHandler(withdraw_menu, pattern="^withdraw_menu$"))
    app.add_handler(CallbackQueryHandler(save_id_menu, pattern="^save_id_menu$"))
    
    app.add_handler(CallbackQueryHandler(handle_deposit_site, pattern="^dep_site_"))
    app.add_handler(CallbackQueryHandler(handle_withdraw_site, pattern="^wd_site_"))
    app.add_handler(CallbackQueryHandler(handle_save_site, pattern="^save_site_"))
    
    app.add_handler(CallbackQueryHandler(admin_action, pattern="^(approve|reject)_"))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_user_message))
    
    print("🤖 BD P2P বট সফলভাবে চালু হয়েছে এবং রান করছে...")
    app.run_polling()
