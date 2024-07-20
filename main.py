from aiogram import Bot, Dispatcher, types, filters, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from pytube import YouTube
import ssl
from aiogram.types import FSInputFile

ssl._create_default_https_context = ssl._create_unverified_context

bot = Bot(token='7310794716:AAH1m1jVzQoxa9NcWj90gVsMBf3GvC5lRGw')
dp = Dispatcher(bot=bot)


url = None


resolutions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 1080p", callback_data="1080"), InlineKeyboardButton(text="⚡ 720p", callback_data="720")],
    [InlineKeyboardButton(text="👾 360p", callback_data="360")]


])


@dp.message(filters.Command("start"))
async def start_function(message: types.Message):
    await message.answer("Xush kelibsiz youtube botiga. Link jo'natsez man sizga video qilib yozib beraman")


@dp.message()
async def tex_message(message: types.Message):
    # chat_id = message.chat.id
    global url
    url = message.text
    yt = YouTube(url=url)

    if message.text.startswith("http"):
        yt = YouTube(url=url)

        await message.answer(f"📹 Video title: {yt.title}\n"
                                        f"🙍‍♂️ Author: {yt.author}\n"
                                        f"{yt.thumbnail_url}", reply_markup=resolutions)


@dp.callback_query(F.data == "1080")
async def download_video(callback: types.CallbackQuery):
    global url

    if url:
        yt = YouTube(url=url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4")
        video = yt.streams.get_highest_resolution().download()
        result = FSInputFile(video)
        await callback.message.answer_video(video=result, caption=f"📹: {yt.title}")
    else:
        await callback.message.answer("❌ No URL")


@dp.callback_query(F.data == "720")
async def download3_video(callback: types.CallbackQuery):
    global url

    if url:
        yt = YouTube(url=url)
        video = yt.streams.get_highest_resolution().download()
        result = FSInputFile(video)
        await callback.message.answer_video(video=result, caption=f"📹: {yt.title}")
    else:
        await callback.message.answer("❌ No URL")


@dp.callback_query(F.data == "360")
async def download2_video(callback: types.CallbackQuery):
    global url


    if url:
        yt = YouTube(url=url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4", resolution="360p").first()

        if stream:
            video_file = stream.download(filename=f"{yt.title}.mp4")

            video_input_file = FSInputFile(video_file)

            await callback.message.answer_video(video=video_input_file, caption=f"📹: {yt.title}")
        else:
            await callback.message.answer("❌ No 360p video stream available. ❌")
    else:
        await callback.message.answer("❌ No URL")


@dp.callback_query(F.data == "360")
async def download3_video(callback: types.CallbackQuery):
    global url

    if url:
        yt = YouTube(url=url)
        video = yt.streams.get_lowest_resolution().download()
        result = FSInputFile(video)
        await callback.message.answer_video(video=result, caption=f"{yt.title}")
    else:
        await callback.message.answer("No URL")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
