"""
AMOUS TECH Ultimate Downloader Bot
Powered by Pyrogram + yt-dlp
"""

import os
import asyncio
import logging
import re
import time
from pathlib import Path

import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, FloodWait

# ─── Credentials ──────────────────────────────────────────────────────────────
BOT_TOKEN  = "8544673152:AAEcPOVSG9tx3kCp3hulN2BJfDhM9mQEU_0"
API_ID     = 23976867
API_HASH   = "81523366cc9924823a0780f2d590e8a7"
ADMIN_ID   = 6363654522

CHANNEL_USERNAME = "AmousTechnology"
GROUP_USERNAME   = "IAmousTechnologychat"

CHANNEL_LINK = "https://t.me/AmousTechnology"
GROUP_LINK   = "https://t.me/IAmousTechnologychat"

BRAND_TAG = "📢 @AmousTechnology"

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)

# ─── Language Strings ─────────────────────────────────────────────────────────
STRINGS = {
    "en": {
        "welcome": (
            "👋 <b>Welcome to AMOUS TECH Downloader!</b>\n\n"
            "Send me any video link from:\n"
            "• TikTok • Instagram • YouTube • Facebook • Twitter\n\n"
            "I will download it in high quality — <b>watermark-free</b>! 🚀"
        ),
        "choose_lang": "🌐 Please choose your language:",
        "lang_set": "✅ Language set to <b>English</b>.",
        "join_required": (
            "🔒 <b>Access Restricted!</b>\n\n"
            "To use this bot you must join <b>both</b>:\n\n"
            "📢 Channel: {channel}\n"
            "💬 Group: {group}\n\n"
            "After joining, tap <b>✅ I Joined</b> below."
        ),
        "join_channel_btn": "📢 Join Channel",
        "join_group_btn":   "💬 Join Group",
        "verify_btn":       "✅ I Joined",
        "still_not_joined": (
            "❌ You haven't joined yet!\n\n"
            "Please join <b>both</b> the channel and the group first."
        ),
        "verified": "✅ Verified! You can now send me video links.",
        "downloading": "⬇️ Downloading your video, please wait…",
        "uploading":   "📤 Uploading… almost done!",
        "done": "✅ Done!",
        "error": "❌ Error: {err}\n\nMake sure the link is valid and publicly accessible.",
        "unsupported": "⚠️ Unsupported link. Send a TikTok, Instagram, YouTube, Facebook, or Twitter URL.",
        "premium_btn":  "⭐ Upgrade to Premium",
        "meta_caption": (
            "{brand}\n\n"
            "🎬 <b>{title}</b>\n"
            "👤 Creator: <code>{creator}</code>\n"
            "👁 Views: <code>{views}</code>\n"
            "❤️ Likes: <code>{likes}</code>\n"
            "⏱ Duration: <code>{duration}</code>"
        ),
    },
    "ar": {
        "welcome": (
            "👋 <b>مرحباً بك في AMOUS TECH Downloader!</b>\n\n"
            "أرسل لي أي رابط فيديو من:\n"
            "• TikTok • Instagram • YouTube • Facebook • Twitter\n\n"
            "سأقوم بتحميله بجودة عالية — <b>بدون علامة مائية</b>! 🚀"
        ),
        "choose_lang": "🌐 يرجى اختيار لغتك:",
        "lang_set": "✅ تم ضبط اللغة على <b>العربية</b>.",
        "join_required": (
            "🔒 <b>الوصول مقيد!</b>\n\n"
            "لاستخدام البوت يجب الانضمام إلى <b>كليهما</b>:\n\n"
            "📢 القناة: {channel}\n"
            "💬 المجموعة: {group}\n\n"
            "بعد الانضمام اضغط على <b>✅ انضممت</b> أدناه."
        ),
        "join_channel_btn": "📢 انضم للقناة",
        "join_group_btn":   "💬 انضم للمجموعة",
        "verify_btn":       "✅ انضممت",
        "still_not_joined": "❌ لم تنضم بعد!\n\nيرجى الانضمام إلى القناة والمجموعة أولاً.",
        "verified": "✅ تم التحقق! يمكنك الآن إرسال روابط الفيديو.",
        "downloading": "⬇️ جارٍ تحميل الفيديو، يرجى الانتظار…",
        "uploading":   "📤 جارٍ الرفع… لحظات!",
        "done": "✅ تم!",
        "error": "❌ خطأ: {err}\n\nتأكد من أن الرابط صحيح وعام.",
        "unsupported": "⚠️ رابط غير مدعوم. أرسل رابط TikTok أو Instagram أو YouTube أو Facebook أو Twitter.",
        "premium_btn":  "⭐ الترقية إلى Premium",
        "meta_caption": (
            "{brand}\n\n"
            "🎬 <b>{title}</b>\n"
            "👤 المنشئ: <code>{creator}</code>\n"
            "👁 المشاهدات: <code>{views}</code>\n"
            "❤️ الإعجابات: <code>{likes}</code>\n"
            "⏱ المدة: <code>{duration}</code>"
        ),
    },
    "ru": {
        "welcome": (
            "👋 <b>Добро пожаловать в AMOUS TECH Downloader!</b>\n\n"
            "Отправь мне ссылку на видео из:\n"
            "• TikTok • Instagram • YouTube • Facebook • Twitter\n\n"
            "Скачаю в высоком качестве — <b>без водяного знака</b>! 🚀"
        ),
        "choose_lang": "🌐 Выберите язык:",
        "lang_set": "✅ Язык установлен: <b>Русский</b>.",
        "join_required": (
            "🔒 <b>Доступ ограничен!</b>\n\n"
            "Для использования бота вступи в <b>оба</b>:\n\n"
            "📢 Канал: {channel}\n"
            "💬 Группа: {group}\n\n"
            "После вступления нажми <b>✅ Я вступил</b>."
        ),
        "join_channel_btn": "📢 Вступить в канал",
        "join_group_btn":   "💬 Вступить в группу",
        "verify_btn":       "✅ Я вступил",
        "still_not_joined": "❌ Ты ещё не вступил!\n\nПожалуйста, вступи в канал и группу.",
        "verified": "✅ Проверено! Теперь можешь отправлять ссылки на видео.",
        "downloading": "⬇️ Скачиваю видео, подожди…",
        "uploading":   "📤 Загружаю… почти готово!",
        "done": "✅ Готово!",
        "error": "❌ Ошибка: {err}\n\nУбедись, что ссылка правильная и публичная.",
        "unsupported": "⚠️ Неподдерживаемая ссылка. Отправь ссылку TikTok, Instagram, YouTube, Facebook или Twitter.",
        "premium_btn":  "⭐ Улучшить до Premium",
        "meta_caption": (
            "{brand}\n\n"
            "🎬 <b>{title}</b>\n"
            "👤 Автор: <code>{creator}</code>\n"
            "👁 Просмотры: <code>{views}</code>\n"
            "❤️ Лайки: <code>{likes}</code>\n"
            "⏱ Длительность: <code>{duration}</code>"
        ),
    },
    "am": {
        "welcome": (
            "👋 <b>ወደ AMOUS TECH Downloader እንኳን ደህና መጡ!</b>\n\n"
            "ከዚህ ቪዲዮ ሊንክ ይላኩ:\n"
            "• TikTok • Instagram • YouTube • Facebook • Twitter\n\n"
            "በከፍተኛ ጥራት — <b>ያለ ዎተርማርክ</b> አወርዳለሁ! 🚀"
        ),
        "choose_lang": "🌐 ቋንቋዎን ይምረጡ:",
        "lang_set": "✅ ቋንቋ ወደ <b>አማርኛ</b> ተቀናብሯል።",
        "join_required": (
            "🔒 <b>መዳረሻ ተገድቧል!</b>\n\n"
            "ቦቱን ለመጠቀም <b>ሁለቱንም</b> መቀላቀል አለብዎ:\n\n"
            "📢 ቻናል: {channel}\n"
            "💬 ቡድን: {group}\n\n"
            "ከተቀላቀሉ በኋላ <b>✅ ተቀላቅያለሁ</b> ይጫኑ።"
        ),
        "join_channel_btn": "📢 ቻናሉን ይቀላቀሉ",
        "join_group_btn":   "💬 ቡድኑን ይቀላቀሉ",
        "verify_btn":       "✅ ተቀላቅያለሁ",
        "still_not_joined": "❌ እስካሁን አልተቀላቀሉም!\n\nእባክዎ ቻናሉን እና ቡድኑን ይቀላቀሉ።",
        "verified": "✅ ተረጋግጧል! አሁን የቪዲዮ ሊንኮችን መላክ ይችላሉ።",
        "downloading": "⬇️ ቪዲዮ በማውረድ ላይ፣ እባክዎ ይጠብቁ…",
        "uploading":   "📤 በመጫን ላይ… ትንሽ ቆይ!",
        "done": "✅ ተጠናቀቀ!",
        "error": "❌ ስህተት: {err}\n\nሊንኩ ትክክለኛ እና ይፋዊ መሆኑን ያረጋግጡ።",
        "unsupported": "⚠️ ያልተደገፈ ሊንክ። TikTok፣ Instagram፣ YouTube፣ Facebook ወይም Twitter ሊንክ ይላኩ።",
        "premium_btn":  "⭐ ወደ Premium ያሻሽሉ",
        "meta_caption": (
            "{brand}\n\n"
            "🎬 <b>{title}</b>\n"
            "👤 ፈጣሪ: <code>{creator}</code>\n"
            "👁 እይታዎች: <code>{views}</code>\n"
            "❤️ ወደዱ: <code>{likes}</code>\n"
            "⏱ ቆይታ: <code>{duration}</code>"
        ),
    },
}

# ─── In-memory user state ──────────────────────────────────────────────────────
# { user_id: { "lang": "en" } }
user_data: dict[int, dict] = {}

def get_lang(user_id: int) -> str:
    return user_data.get(user_id, {}).get("lang", "en")

def t(user_id: int, key: str, **kwargs) -> str:
    lang = get_lang(user_id)
    text = STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text

# ─── Supported URL patterns ───────────────────────────────────────────────────
SUPPORTED_RE = re.compile(
    r"(https?://)?"
    r"(www\.)?"
    r"(tiktok\.com|vm\.tiktok\.com|"
    r"instagram\.com|"
    r"youtube\.com|youtu\.be|"
    r"facebook\.com|fb\.watch|"
    r"twitter\.com|x\.com|t\.co)",
    re.I,
)

def is_supported_url(text: str) -> bool:
    return bool(SUPPORTED_RE.search(text))

# ─── Membership check ─────────────────────────────────────────────────────────
async def is_member(client: Client, user_id: int) -> bool:
    """Returns True only if user is in BOTH channel and group."""
    if user_id == ADMIN_ID:
        return True
    try:
        ch = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        gp = await client.get_chat_member(GROUP_USERNAME,   user_id)
        ok_statuses = {"member", "administrator", "creator"}
        return (ch.status.name.lower() in ok_statuses and
                gp.status.name.lower() in ok_statuses)
    except (UserNotParticipant, ChatAdminRequired, Exception):
        return False

def join_markup(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t(user_id, "join_channel_btn"), url=CHANNEL_LINK),
            InlineKeyboardButton(t(user_id, "join_group_btn"),   url=GROUP_LINK),
        ],
        [InlineKeyboardButton(t(user_id, "verify_btn"), callback_data="verify")],
    ])

def premium_markup(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(t(user_id, "premium_btn"), url=CHANNEL_LINK)
    ]])

# ─── yt-dlp helpers ───────────────────────────────────────────────────────────
def fmt_duration(secs) -> str:
    try:
        secs = int(secs)
        return f"{secs // 60}:{secs % 60:02d}"
    except Exception:
        return "N/A"

def fmt_count(n) -> str:
    try:
        n = int(n)
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        if n >= 1_000:
            return f"{n/1_000:.1f}K"
        return str(n)
    except Exception:
        return "N/A"

def build_ydl_opts(out_path: str, platform: str) -> dict:
    """Build yt-dlp options tailored per platform."""
    common = {
        "outtmpl": out_path,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "noplaylist": True,
    }
    if platform == "tiktok":
        common.update({
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "extractor_args": {"tiktok": {"embed_metadata": True}},
        })
    elif platform == "instagram":
        common.update({"format": "best[ext=mp4]/best"})
    elif platform == "youtube":
        common.update({
            "format": (
                "bestvideo[height<=1080][ext=mp4]"
                "+bestaudio[ext=m4a]"
                "/bestvideo[height<=1080]+bestaudio"
                "/best[height<=1080]/best"
            ),
        })
    else:
        common.update({"format": "best[ext=mp4]/best"})
    return common

def detect_platform(url: str) -> str:
    url_l = url.lower()
    if "tiktok.com" in url_l or "vm.tiktok.com" in url_l:
        return "tiktok"
    if "instagram.com" in url_l:
        return "instagram"
    if "youtube.com" in url_l or "youtu.be" in url_l:
        return "youtube"
    if "facebook.com" in url_l or "fb.watch" in url_l:
        return "facebook"
    if "twitter.com" in url_l or "x.com" in url_l or "t.co" in url_l:
        return "twitter"
    return "generic"

async def download_video(url: str) -> tuple[str | None, dict]:
    """
    Download the video to /tmp and return (file_path, info_dict).
    Returns (None, {}) on failure.
    """
    ts = int(time.time())
    platform = detect_platform(url)
    out_tmpl = f"/tmp/amoustech_{ts}.%(ext)s"
    opts = build_ydl_opts(out_tmpl, platform)

    loop = asyncio.get_event_loop()

    def _dl():
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info

    try:
        info = await loop.run_in_executor(None, _dl)
    except Exception as e:
        log.error("yt-dlp error: %s", e)
        return None, {"error": str(e)}

    # Find the downloaded file
    ext = info.get("ext", "mp4")
    file_path = f"/tmp/amoustech_{ts}.{ext}"
    if not os.path.exists(file_path):
        # Try mp4 fallback
        file_path = f"/tmp/amoustech_{ts}.mp4"
    if not os.path.exists(file_path):
        # Search /tmp for any matching file
        matches = list(Path("/tmp").glob(f"amoustech_{ts}.*"))
        file_path = str(matches[0]) if matches else None

    return file_path, info

def build_caption(user_id: int, info: dict) -> str:
    title   = info.get("title")   or info.get("fulltitle") or "Unknown"
    creator = (info.get("uploader") or info.get("creator") or
               info.get("channel")  or info.get("uploader_id") or "Unknown")
    views    = fmt_count(info.get("view_count", 0))
    likes    = fmt_count(info.get("like_count", 0))
    duration = fmt_duration(info.get("duration", 0))
    # Truncate long titles
    if len(title) > 80:
        title = title[:77] + "…"
    return t(user_id, "meta_caption",
             brand=BRAND_TAG, title=title, creator=creator,
             views=views, likes=likes, duration=duration)

# ─── Bot setup ────────────────────────────────────────────────────────────────
app = Client(
    "amoustech_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=60,
)

# ─── /start ───────────────────────────────────────────────────────────────────
@app.on_message(filters.command("start") & filters.private)
async def cmd_start(client: Client, message: Message):
    uid = message.from_user.id
    lang_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇬🇧 English",  callback_data="lang_en"),
            InlineKeyboardButton("🇸🇦 العربية",  callback_data="lang_ar"),
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский",  callback_data="lang_ru"),
            InlineKeyboardButton("🇪🇹 አማርኛ",    callback_data="lang_am"),
        ],
    ])
    await message.reply(t(uid, "choose_lang"), reply_markup=lang_kb)

# ─── Language callbacks ───────────────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^lang_(en|ar|ru|am)$"))
async def cb_lang(client: Client, cb: CallbackQuery):
    uid  = cb.from_user.id
    lang = cb.data.split("_")[1]
    user_data.setdefault(uid, {})["lang"] = lang
    await cb.answer()
    await cb.message.edit_text(t(uid, "lang_set"))
    await asyncio.sleep(0.5)
    await cb.message.reply(t(uid, "welcome"))

# ─── Verify membership callback ───────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^verify$"))
async def cb_verify(client: Client, cb: CallbackQuery):
    uid = cb.from_user.id
    await cb.answer()
    if await is_member(client, uid):
        await cb.message.edit_text(t(uid, "verified"))
    else:
        await cb.message.edit_text(
            t(uid, "still_not_joined"),
            reply_markup=join_markup(uid),
        )

# ─── Main download handler ────────────────────────────────────────────────────
@app.on_message(filters.private & filters.text & ~filters.command(["start", "help"]))
async def handle_link(client: Client, message: Message):
    uid  = message.from_user.id
    text = message.text.strip()

    # ── Subscription gate (bypass for admin) ──
    if uid != ADMIN_ID:
        if not await is_member(client, uid):
            await message.reply(
                t(uid, "join_required",
                  channel=CHANNEL_LINK, group=GROUP_LINK),
                reply_markup=join_markup(uid),
                disable_web_page_preview=True,
            )
            return

    # ── URL check ──
    if not is_supported_url(text):
        await message.reply(t(uid, "unsupported"))
        return

    # ── Start downloading ──
    status_msg = await message.reply(t(uid, "downloading"))

    file_path, info = await download_video(text)

    if file_path is None:
        err = info.get("error", "Unknown error")
        await status_msg.edit_text(t(uid, "error", err=err[:300]))
        return

    await status_msg.edit_text(t(uid, "uploading"))

    caption = build_caption(uid, info)
    markup  = premium_markup(uid)

    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption=caption,
            reply_markup=markup,
            supports_streaming=True,
        )
        await status_msg.delete()
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
        await client.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption=caption,
            reply_markup=markup,
            supports_streaming=True,
        )
        await status_msg.delete()
    except Exception as e:
        log.error("Send error: %s", e)
        await status_msg.edit_text(t(uid, "error", err=str(e)[:300]))
    finally:
        # ── Clean up temp file ──
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

# ─── Admin broadcast (bonus) ──────────────────────────────────────────────────
@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def cmd_broadcast(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply("Reply to a message to broadcast it.")
        return
    count = 0
    for uid in list(user_data.keys()):
        try:
            await message.reply_to_message.copy(uid)
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            pass
    await message.reply(f"✅ Broadcast sent to {count} users.")

# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("🚀 AMOUS TECH Bot is starting…")
    app.run()
