from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import io

BOT_TOKEN = "8138672735:AAGuPqZQLOgvopPb5mgdxbiNhDemaUKkB2w"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    
    # Rasmni o‘qish
    image = Image.open(io.BytesIO(photo_bytes))

    # 1. Rasmni qora va oq rangga aylantirish
    image = image.convert("L")

    # 2. Rasmga chizilgan effekt qo‘shish
    image = image.filter(ImageFilter.CONTOUR)  # Kontur effektini qo‘shish

    # 3. Yana bir o‘zgartirish: kontrastni oshirish (qalin chizgilarga o‘xshash ko‘rinish uchun)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # 4. Rasmni o‘zgartirish, qora ranglarni yanada aniqlashtirish
    image = image.filter(ImageFilter.SHARPEN)

    # 5. PNG formatida saqlash
    output = io.BytesIO()
    image.save(output, format='PNG')
    output.seek(0)

    # Chizilgan rasmni foydalanuvchiga yuborish
    await update.message.reply_photo(photo=InputFile(output, filename="drawing.png"))

# Botni ishga tushirish
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()