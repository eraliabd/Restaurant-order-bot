from database import Database
import globals
import methods
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
db = Database("db-evos.db")

def carts1(update, context):
    query = update.callback_query
    db_user = db.get_user_by_chat_id(query.message.chat_id)
    categories = db.get_categories_by_parent()
    buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])
    if context.user_data.get("carts", {}):
        carts = context.user_data.get("carts")
        text = "\n"
        lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]
        total_price = 0
        for cart, val in carts.items():
            product = db.get_product_for_cart(int(cart))
            text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
            total_price += product['price'] * val
        text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price} {globals.SUM[db_user['lang_id']]}"
        buttons.append([InlineKeyboardButton(text=globals.BTN_KORZINKA[db_user['lang_id']], callback_data="cart")])

    else:
        text = globals.TEXT_ORDER[db_user['lang_id']]
    query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons,
        )
    )

def carts2(update, context):
    db_user = db.get_user_by_chat_id(update.message.chat_id)
    categories = db.get_categories_by_parent()
    buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])
    if context.user_data.get("carts", {}):
        carts = context.user_data.get("carts")
        text = f"{globals.AT_KORZINKA[db_user['lang_id']]}:\n\n"
        lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]
        total_price = 0
        for cart, val in carts.items():
            product = db.get_product_for_cart(int(cart))
            text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
            total_price += product['price'] * val

        text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price} {globals.SUM[db_user['lang_id']]}"
        buttons.append([InlineKeyboardButton(text=globals.BTN_KORZINKA[db_user['lang_id']], callback_data="cart")])

    else:
        text = globals.TEXT_ORDER[db_user['lang_id']]
    update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons,
        )
    )

def orders(update, context):
    db_user = db.get_user_by_chat_id(update.message.chat_id)
    if context.user_data.get("carts", {}):
        carts = context.user_data.get("carts")
        text = "\n"
        lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]
        total_price = 0
        for cart, val in carts.items():
            product = db.get_product_for_cart(int(cart))
            text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
            total_price += product['price'] * val
        text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price} {globals.SUM[db_user['lang_id']]}"

        update.message.reply_text(
            text=f"<b>Ma'lumotlarim:</b>\n\n"
                 f"👤 <b>Ism-familiya:</b> {db_user['first_name']} {db_user['last_name']}\n"
                 f"📞 <b>Telefon raqam:</b> {db_user['phone_number']} \n\n"
                 f"📥 <b>Buyurtmalarim:</b> \n"
                 f"{text}",
            parse_mode='HTML'
        )

    else:
        update.message.reply_text(
            text=globals.NO_ZAKAZ[db_user['lang_id']])