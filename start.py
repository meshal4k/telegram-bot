from keep_alive import keep_alive
import asyncio
from bot import main  # لو اسم ملف البوت شيء آخر غير bot.py غيره هنا

keep_alive()
asyncio.run(main())
