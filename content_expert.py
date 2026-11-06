"""
content_expert.py - EXPERT content: complex single-round scenarios, voice scams,
and branching Story Missions.

All organisations, people, numbers and websites are FICTIONAL.
Audio clips live in assets/audio/ and are generated from AUDIO_CLIPS by
generate_audio.py (the transcript shown in the app is the same text).
"""

# --------------------------------------------------------------------------
# AUDIO CLIPS: filename -> voice settings + exact script
# Voices are Microsoft Edge neural voices (free, via the edge-tts package).
# --------------------------------------------------------------------------
AUDIO_CLIPS = {
    # ---- expert single rounds ----
    "x01_courier_robocall_bm.mp3": {
        "voice": "ms-MY-YasminNeural", "rate": "-5%", "pitch": "+0Hz", "phone": True,
        "text": "Ini adalah panggilan automatik daripada KilatPos. Bungkusan atas nama anda yang mengandungi "
                "dua puluh kad pengenalan palsu telah ditahan oleh pihak kastam. Kes ini akan diserahkan kepada "
                "polis dalam masa dua jam. Tekan satu sekarang untuk bercakap dengan pegawai kami."},
    "x02_bank_genuine_call.mp3": {
        "voice": "en-SG-LunaNeural", "rate": "+0%", "pitch": "+0Hz", "phone": True,
        "text": "Hello, this is Nadia from Bank Harmoni card security. I'm calling about an online purchase of "
                "two thousand three hundred and ten ringgit on your card ending four four two one, tonight at nine fifteen. "
                "We've blocked it as a precaution. Please don't share your PIN or any codes with anyone, including me. "
                "If you'd like to confirm this call is genuine, please hang up and call the number on the back of your card. Thank you."},
    "x03_daughter_clone_bm.mp3": {
        "voice": "ms-MY-YasminNeural", "rate": "+12%", "pitch": "+15Hz", "phone": True,
        "text": "Mama, ni Aisyah. Mama, tolong. Saya kena tahan dekat balai. Kawan saya bawa kereta, langgar orang. "
                "Phone saya rosak, ni pinjam phone orang. Saya perlukan seribu lima ratus ringgit sekarang untuk jamin. "
                "Tolong jangan bagitahu Papa dulu, nanti dia marah. Cepat sikit Mama, please."},
    "x04_central_bank_mandarin.mp3": {
        "voice": "zh-CN-YunyangNeural", "rate": "+0%", "pitch": "+0Hz", "phone": True,
        "text": "您好，这里是中央银行反洗钱调查组。我们发现您的身份证被用来开设一个涉及洗钱的账户。"
                "为了证明您的清白，您必须在今天之内把所有存款转入我们指定的安全账户进行核查。"
                "这件事是机密的，请不要告诉任何人，包括您的家人。"},
    "x17_rider_genuine.mp3": {
        "voice": "en-SG-WayneNeural", "rate": "+0%", "pitch": "+0Hz", "phone": True,
        "text": "Hello, KilatPos delivery here. I'm at your condo guardhouse now with your parcel. Nobody answered the intercom. "
                "Can you come down in five minutes, or should I leave it with the guard? No payment needed, it's already paid."},
    # ---- story missions ----
    "s1_n1_robocall.mp3": {
        "voice": "en-SG-LunaNeural", "rate": "-5%", "pitch": "-2Hz", "phone": True,
        "text": "This is an automated message from KilatPos Express. A parcel registered under your identity card number "
                "contains illegal items and has been held by customs. Your case will be transferred to the police within one hour. "
                "Press one now to speak to our customer service officer."},
    "s1_n2_inspector.mp3": {
        "voice": "en-SG-WayneNeural", "rate": "-3%", "pitch": "-6Hz", "phone": True,
        "text": "Good afternoon. I am Inspector Razak from the Commercial Crime Investigation Department. Your identity card "
                "has been used to open a bank account belonging to a money laundering syndicate. There are already twelve victims. "
                "Do not hang up, and do not tell anyone, including your family, because they may be involved. "
                "I will send you the arrest warrant on WhatsApp now. If you cooperate, we can clear your name today."},
    "s1_n4_bank_officer.mp3": {
        "voice": "en-IN-NeerjaNeural", "rate": "+0%", "pitch": "+0Hz", "phone": True,
        "text": "Hello, I am Puan Lim from the central bank audit unit. Inspector Razak has passed me your case. "
                "To prove your money is clean, you must move all your savings into a government safe account for checking. "
                "It will be returned within forty-eight hours. I will also need you to install our secure audit app, "
                "so that we can monitor the account. Please do it now, while I stay on the line."},
    "s2_n1_amir.mp3": {
        "voice": "en-SG-WayneNeural", "rate": "+14%", "pitch": "+8Hz", "phone": True,
        "text": "Kak! Kak, it's me, Amir. I'm in trouble. I was in an accident, the police are here. My phone broke, "
                "I'm using someone else's phone. They say I need to pay three thousand ringgit bail right now or they will "
                "lock me up. Please, Kak, don't tell Mak, she will panic. I'll send you the account number. Please hurry!"},
    "s2_n2_sergeant_bm.mp3": {
        "voice": "ms-MY-OsmanNeural", "rate": "+5%", "pitch": "-4Hz", "phone": True,
        "text": "Hello, saya Sarjan Kamal dari balai polis. Adik awak ada di sini. Kalau tak selesaikan bayaran jaminan "
                "dalam masa tiga puluh minit, dia akan masuk lokap malam ini. Bayar ke akaun yang dia beri. Jangan buang masa."},
    "s2_n3_amir_again.mp3": {
        "voice": "en-SG-WayneNeural", "rate": "+18%", "pitch": "+10Hz", "phone": True,
        "text": "Kak, why did you hang up? Please! The officer is getting angry. Just transfer first, "
                "I'll explain everything later. Please, Kak, I'm scared."},
    "s4_n2_director.mp3": {
        "voice": "en-GB-RyanNeural", "rate": "+6%", "pitch": "+0Hz", "phone": True,
        "text": "Hi, thanks for joining. Sorry the video is a bit choppy, I'm on the road. As I said in my email, we're closing "
                "a confidential acquisition today. The CFO is here with me. We need you to transfer four hundred and eighty "
                "thousand ringgit to the escrow account in the email, within the next thirty minutes. Don't discuss this with "
                "anyone in finance yet, it's market sensitive. I'm counting on you."},
    "s5_n2_card_delivery.mp3": {
        "voice": "en-IN-PrabhatNeural", "rate": "+0%", "pitch": "+0Hz", "phone": True,
        "text": "Good morning, this is Bank Harmoni card delivery. I can see your card was blocked last night after the "
                "suspicious purchase, and your replacement card is ready to be couriered today. For security, I just need to "
                "verify you. We've sent a six-digit code to your phone. Could you read it out to me so I can release the delivery?"},
    # ---- tests ----
    "p05_tax_robocall.mp3": {
        "voice": "en-US-GuyNeural", "rate": "-5%", "pitch": "-4Hz", "phone": True,
        "text": "This is the tax department. Our records show you owe eight thousand four hundred ringgit in unpaid tax. "
                "A warrant for your arrest will be issued today. Press one now to speak with an enforcement officer."},
    "r05_bank_login_bm.mp3": {
        "voice": "ms-MY-YasminNeural", "rate": "-3%", "pitch": "+0Hz", "phone": True,
        "text": "Ini panggilan automatik daripada Bank Seri Nusa. Kami mengesan log masuk ke akaun anda dari peranti baharu. "
                "Untuk membatalkan log masuk ini, tekan satu dan masukkan kata laluan perbankan dalam talian anda sekarang."},
    "q05_fraud_dept_tac.mp3": {
        "voice": "en-IN-PrabhatNeural", "rate": "+4%", "pitch": "+0Hz", "phone": True,
        "text": "Hello, this is Bank Harmoni's fraud department. We've detected suspicious activity and need to protect your money. "
                "We just sent you a six-digit TAC. Please read it out to me now so we can secure your account."},
}


def clip_text(name):
    return AUDIO_CLIPS[name]["text"]


# --------------------------------------------------------------------------
# EXPERT single-round scenarios (17: 13 scam + 4 legit; 5 with real audio)
# --------------------------------------------------------------------------
EXPERT_SCENARIOS = [
    {
        "id": "X01", "channel": "Phone call", "sender": "+603-7728 1904", "context": "",
        "audio": "x01_courier_robocall_bm.mp3",
        "message": clip_text("x01_courier_robocall_bm.mp3") +
                   "\n\n[English] This is an automated call from KilatPos. A parcel in your name containing 20 fake identity "
                   "cards has been held by customs. The case will be handed to police in 2 hours. Press 1 now to speak to our officer.",
        "is_scam": True, "difficulty": "Expert", "tactic": "Impersonating authority",
        "cues": [
            {"text": "A courier calls you about a crime", "is_red_flag": True,
             "why": "Couriers deliver parcels. They don't investigate crimes or threaten police action."},
            {"text": "'Press 1 to speak to an officer'", "is_red_flag": True,
             "why": "Pressing 1 routes you to the scam call centre. It's step one of the Macau-scam chain."},
            {"text": "Two-hour deadline before police", "is_red_flag": True,
             "why": "Fear + deadline stops you from checking."},
            {"text": "Recorded voice sounds professional", "is_red_flag": False,
             "why": "Robocalls are cheap to make sound official. Professional tone proves nothing."},
            {"text": "It's in Bahasa Melayu", "is_red_flag": False,
             "why": "Language is not a warning sign. These calls come in Malay, English, Mandarin and Tamil."},
        ],
        "lesson": "What to do: Hang up. Check parcels only in the courier app you installed. "
                  "This robocall is the opening move of a 'chain' scam that passes you to fake police next.",
    },
    {
        "id": "X02", "channel": "Phone call", "sender": "+603-2050 7700", "context": "You used your card online earlier today, but not for RM2,310.",
        "audio": "x02_bank_genuine_call.mp3",
        "message": clip_text("x02_bank_genuine_call.mp3"),
        "is_scam": False, "difficulty": "Expert", "tactic": "Legit message",
        "cues": [
            {"text": "Says they blocked a purchase you didn't make", "is_red_flag": False,
             "why": "Real banks do call about suspicious transactions. That alone isn't a scam sign."},
            {"text": "Refuses to take your PIN or codes", "is_red_flag": False,
             "why": "A strong sign of a genuine call. Scammers always need a code or a transfer."},
            {"text": "Invites you to hang up and call back yourself", "is_red_flag": False,
             "why": "Scammers try to keep you on the line. This caller encourages you to verify."},
            {"text": "Knows the last 4 digits of your card", "is_red_flag": False,
             "why": "Not proof either way. Here nothing is requested from you, so it's consistent with the real bank."},
        ],
        "lesson": "Legit! It asks for nothing and invites you to verify. Best habit even for real calls: "
                  "hang up and call the number on the back of your card.",
    },
    {
        "id": "X03", "channel": "Phone call", "sender": "Unknown number",
        "context": "You're Aisyah's mother. The voice sounds exactly like your daughter.",
        "audio": "x03_daughter_clone_bm.mp3",
        "message": clip_text("x03_daughter_clone_bm.mp3") +
                   "\n\n[English] Mama, it's Aisyah. Please help, I'm being held at the police station. My friend was driving "
                   "and hit someone. My phone broke, I'm borrowing someone's phone. I need RM1,500 now for bail. "
                   "Please don't tell Papa yet, he'll be angry. Hurry, Mama, please.",
        "is_scam": True, "difficulty": "Expert", "tactic": "Voice / video deepfake",
        "cues": [
            {"text": "Unknown number + 'my phone broke'", "is_red_flag": True,
             "why": "The classic excuse to explain why it's not her usual number."},
            {"text": "'Don't tell Papa'", "is_red_flag": True,
             "why": "Secrecy stops you from checking with the one person who could confirm."},
            {"text": "Urgent bail money by transfer", "is_red_flag": True,
             "why": "Bail in Malaysia isn't paid by instant transfer to a private account over the phone."},
            {"text": "It sounds exactly like Aisyah", "is_red_flag": False,
             "why": "NOT proof. A few seconds of her TikTok or voice notes is enough to clone her voice with AI."},
        ],
        "lesson": "What to do: Hang up and call Aisyah's saved number, or someone who's with her. "
                  "Set a family code word today that a voice clone can't know.",
    },
    {
        "id": "X04", "channel": "Phone call", "sender": "+60 3-9131 2288",
        "context": "", "audio": "x04_central_bank_mandarin.mp3",
        "message": clip_text("x04_central_bank_mandarin.mp3") +
                   "\n\n[English] Hello, this is the central bank's anti-money-laundering unit. Your IC was used to open "
                   "an account involved in money laundering. To prove your innocence you must transfer all your savings "
                   "into our designated safe account today for checking. This is confidential, don't tell anyone, including your family.",
        "is_scam": True, "difficulty": "Expert", "tactic": "Impersonating authority",
        "cues": [
            {"text": "Wants your savings in a 'safe account'", "is_red_flag": True,
             "why": "No 'safe account' exists. No central bank or police unit holds your money for checking."},
            {"text": "Must be done today", "is_red_flag": True,
             "why": "Urgency stops you from thinking and checking."},
            {"text": "Don't tell your family", "is_red_flag": True,
             "why": "Isolation is how they keep control of you."},
            {"text": "Speaks Mandarin", "is_red_flag": False,
             "why": "Scam syndicates target every community in its own language. The language isn't the warning sign."},
        ],
        "lesson": "What to do: Hang up. Central banks don't handle individual accounts or call the public to move money. "
                  "Call NSRC 997 if you're unsure.",
    },
    {
        "id": "X05", "channel": "SMS", "sender": "Bank Harmoni",
        "context": "This SMS appears in the SAME conversation thread as your real Bank Harmoni messages.",
        "message": "Bank Harmoni: Your DuitNow transfer limit was raised to RM50,000. If you did not request this, "
                   "cancel within 2 hours at bankharmoni.com.my-limit-cancel.net",
        "is_scam": True, "difficulty": "Expert", "tactic": "Phishing link",
        "cues": [
            {"text": "Shows up in the real bank's SMS thread", "is_red_flag": False,
             "why": "Careful: NOT proof. Sender IDs can be spoofed so fake SMS land in the real thread."},
            {"text": "Real domain is '…limit-cancel.net'", "is_red_flag": True,
             "why": "Read to the end: 'bankharmoni.com.my' is just the start. The site is actually '…-limit-cancel.net'."},
            {"text": "Scary change you didn't make", "is_red_flag": True,
             "why": "Fear of losing money makes you click fast."},
            {"text": "2-hour deadline", "is_red_flag": True,
             "why": "Urgency stops you from checking in the app."},
        ],
        "lesson": "What to do: Never act on links in SMS, even inside the real thread. Open your banking app and check your limits there.",
    },
    {
        "id": "X06", "channel": "Email", "sender": "Mei Ling <meiling@segarfoods-my.com>",
        "context": "You handle payments for your family's catering business. This is a reply in a REAL email thread with your regular "
                   "supplier, whose address is meiling@segarfood.com.my.",
        "message": "Hi, as discussed, please note our bank account has changed due to our annual audit. Kindly pay invoice "
                   "INV-2291 (RM12,480) to our new account: Bank Seri Nusa 8820 1173 4456. Please don't call the office, "
                   "our phone lines are under maintenance this week. Thanks & regards, Mei Ling",
        "is_scam": True, "difficulty": "Expert", "tactic": "Phishing link",
        "cues": [
            {"text": "It's a reply in a real, ongoing thread", "is_red_flag": False,
             "why": "Not proof. Hackers who break into an email account reply inside real threads."},
            {"text": "Address is segarfoods-my.com, not segarfood.com.my", "is_red_flag": True,
             "why": "A look-alike domain. One extra 's' and a '-my' is all it takes."},
            {"text": "Bank account suddenly changed", "is_red_flag": True,
             "why": "Account changes are the #1 sign of business email compromise."},
            {"text": "Asks you NOT to call the office", "is_red_flag": True,
             "why": "They're blocking the one check that would expose them."},
            {"text": "Mentions a real invoice number", "is_red_flag": False,
             "why": "Hackers read the real emails, so they know real invoice numbers."},
        ],
        "lesson": "What to do: Always confirm bank-account changes by phone using a number you already had, never one in the email.",
    },
    {
        "id": "X07", "channel": "WhatsApp", "sender": "+60 13-447 2091 (profile photo: a bride & groom)", "context": "",
        "message": "Assalamualaikum. Dengan segala hormatnya, dijemput hadir ke majlis perkahwinan anak kami. "
                   "Sila buka kad jemputan digital di bawah 🤍\n📎 Kad_Jemputan_Majlis.apk (2.1 MB)",
        "is_scam": True, "difficulty": "Expert", "tactic": "Phishing link",
        "cues": [
            {"text": "The invitation is an .apk file", "is_red_flag": True,
             "why": "An APK is an Android app, not a card. It can read your SMS (including TAC codes) and drain your bank."},
            {"text": "From a number you don't have saved", "is_red_flag": True,
             "why": "Who is getting married? If you can't tell, don't open anything."},
            {"text": "Polite, warm, cultural greeting", "is_red_flag": False,
             "why": "Scammers copy local customs to blend in. Politeness proves nothing."},
            {"text": "Wedding photo on the profile", "is_red_flag": False,
             "why": "Profile photos are easy to copy from anywhere."},
        ],
        "lesson": "What to do: Never install APK files sent in chats. Real e-invites are images, PDFs or web links from people you know. "
                  "In phone settings, keep 'Install unknown apps' turned OFF.",
    },
    {
        "id": "X08", "channel": "WhatsApp", "sender": "+60 11-5520 3381",
        "context": "Your banking app really does show: 'Received RM980.00 from TAN AH KOW'. You don't know this person.",
        "message": "Hi sorry ah, I accidentally transferred RM980 to your account 🙏 That's my rent money. "
                   "Please return to my wife's account instead, mine is frozen: 1123 0098 7721 (Bank Seri Nusa). Very urgent, thank you!",
        "is_scam": True, "difficulty": "Expert", "tactic": "Money mule",
        "cues": [
            {"text": "The money really is in your account", "is_red_flag": False,
             "why": "Tricky: the money is real, but it's likely stolen. Real money is not proof of an honest sender."},
            {"text": "Asks you to send it to a DIFFERENT account", "is_red_flag": True,
             "why": "Sending it onward makes YOU the link that moves stolen money: a money mule."},
            {"text": "'My account is frozen'", "is_red_flag": True,
             "why": "Frozen accounts are often frozen because of fraud."},
            {"text": "Urgent and apologetic", "is_red_flag": True,
             "why": "Guilt and urgency push you to 'just be kind' quickly."},
        ],
        "lesson": "What to do: Don't send the money anywhere yourself. Contact your bank and let them reverse the transfer properly.",
    },
    {
        "id": "X09", "channel": "Email", "sender": "Cyber Fund Recovery Unit <recovery@cfru-asia.org>",
        "context": "Last year you lost RM20,000 to an investment scam and reported it to the police.",
        "message": "Dear Victim, our legal team has traced your lost funds (RM20,000) to an offshore wallet. We work with international "
                   "law enforcement. To begin recovery, a refundable processing fee of 10% (RM2,000) is required. Success rate 97%. "
                   "Act within 72 hours before the wallet is moved.",
        "is_scam": True, "difficulty": "Expert", "tactic": "Impersonating authority",
        "cues": [
            {"text": "They know about your real loss", "is_red_flag": False,
             "why": "Not proof. Scammers sell 'victim lists' to other scammers."},
            {"text": "Upfront fee to recover money", "is_red_flag": True,
             "why": "Real recovery through police and banks never needs an upfront fee to a private company."},
            {"text": "'97% success rate'", "is_red_flag": True,
             "why": "Unrealistic promises. Recovery is rare and never guaranteed."},
            {"text": "72-hour deadline", "is_red_flag": True,
             "why": "Pressure again."},
        ],
        "lesson": "What to do: This is a 'recovery scam' that targets past victims. Only deal with the police and your bank.",
    },
    {
        "id": "X10", "channel": "Social media", "sender": "Tabung Banjir Prihatin 🤲",
        "context": "Floods are really happening in Kelantan this week and are all over the news.",
        "message": "🚨 BANJIR KELANTAN 🚨 2,000 keluarga terkandas tanpa makanan! Setiap RM20 = 1 pek makanan. "
                   "Derma terus ke akaun peribadi pengasas kami (Bank Harmoni 5521 0019 2283) supaya bantuan sampai lebih cepat. "
                   "Kongsi sekarang! 🙏",
        "is_scam": True, "difficulty": "Expert", "tactic": "Prize & giveaway",
        "cues": [
            {"text": "The flood is real", "is_red_flag": False,
             "why": "Scammers ride on real disasters. A real event doesn't make the collector real."},
            {"text": "Donations go to a founder's personal account", "is_red_flag": True,
             "why": "Registered charities use organisation accounts, not personal ones."},
            {"text": "Emotional urgency + 'share now'", "is_red_flag": True,
             "why": "Strong emotion plus urgency pushes you to give before checking."},
            {"text": "Written in Bahasa Melayu", "is_red_flag": False,
             "why": "Language isn't the warning sign."},
        ],
        "lesson": "What to do: Give through registered charities, official relief funds or your mosque/church/temple. "
                  "Check the account on Semak Mule before donating.",
    },
    {
        "id": "X11", "channel": "Website", "sender": "eWalletKu app (you opened it yourself)",
        "context": "You opened the official eWalletKu app from your home screen. A banner appears inside the app.",
        "message": "Complete your eKYC to keep using transfers above RM1,000/month. Step 1: Scan your MyKad. "
                   "Step 2: Take a selfie. This takes about 2 minutes.",
        "is_scam": False, "difficulty": "Expert", "tactic": "Legit message",
        "cues": [
            {"text": "Asks for your MyKad and a selfie", "is_red_flag": False,
             "why": "Tricky: normally a big warning, but here it's eKYC inside the official app YOU opened. That's how real eKYC works."},
            {"text": "You opened the app yourself", "is_red_flag": False,
             "why": "The key safety factor: you started this, from a trusted app."},
            {"text": "No deadline or threat", "is_red_flag": False,
             "why": "Calm, informational, no pressure."},
            {"text": "Mentions transfer limits", "is_red_flag": False,
             "why": "Normal regulatory requirement for e-wallets."},
        ],
        "lesson": "Legit! Same request, different context: inside the official app you opened = OK. "
                  "Via a link someone sent you = scam. Context is everything.",
    },
    {
        "id": "X12", "channel": "SMS", "sender": "PasarKu",
        "context": "Last week you asked for a refund for a damaged phone case (order #77120).",
        "message": "PasarKu: Your refund of RM89.00 for order #77120 has been credited to your PasarKu Wallet. No action needed.",
        "is_scam": False, "difficulty": "Expert", "tactic": "Legit message",
        "cues": [
            {"text": "Matches a refund you requested", "is_red_flag": False,
             "why": "Context fits what you did."},
            {"text": "Mentions money being credited", "is_red_flag": False,
             "why": "Money going TO you inside the platform, with nothing asked, is normal."},
            {"text": "'No action needed'", "is_red_flag": False,
             "why": "No link, no request, no pressure."},
            {"text": "Uses your real order number", "is_red_flag": False,
             "why": "Fine here because nothing else is suspicious."},
        ],
        "lesson": "Legit! Nothing to click, nothing to give. Not every message about money is a trap.",
    },
    {
        "id": "X13", "channel": "QR code", "sender": "Sticker on a street parking meter",
        "context": "You're parking in town. A sticker is pasted over the meter's screen.",
        "message": "⚠️ METER ROSAK / MACHINE FAULTY ⚠️\nScan QR to pay parking & avoid RM50 saman.\n[QR CODE] → parkir-bayar-segera.site",
        "is_scam": True, "difficulty": "Expert", "tactic": "Phishing link",
        "cues": [
            {"text": "Sticker pasted over the official screen", "is_red_flag": True,
             "why": "Scammers stick fake QR codes on top of real machines ('quishing')."},
            {"text": "QR leads to an unofficial '.site' address", "is_red_flag": True,
             "why": "Councils use their official parking app or website."},
            {"text": "Threat of a RM50 fine", "is_red_flag": True,
             "why": "Fear of a fine makes you scan without thinking."},
            {"text": "It's on a real parking meter", "is_red_flag": False,
             "why": "Being in a real place doesn't make the sticker real."},
        ],
        "lesson": "What to do: Pay parking only in the council's official app. Preview a QR link before opening it, "
                  "and never enter card details on a site you reached by QR on a sticker.",
    },
    {
        "id": "X14", "channel": "Email", "sender": "Bank Harmoni <alerts@bankharrnoni.com.my>", "context": "",
        "message": "Dear Valued Customer, your e-statement for October is now available. "
                   "Log in to view it: bankharrnoni.com.my/estatement\nThank you for banking with us.",
        "is_scam": True, "difficulty": "Expert", "tactic": "Phishing link",
        "cues": [
            {"text": "'harrnoni': 'rn' pretending to be 'm'", "is_red_flag": True,
             "why": "Look closely: r + n looks like m. A look-alike domain."},
            {"text": "Asks you to log in through a link", "is_red_flag": True,
             "why": "The login page is where they steal your password and TAC."},
            {"text": "No urgency or threat at all", "is_red_flag": False,
             "why": "Calm scams exist too. No pressure doesn't mean safe."},
            {"text": "It's about a normal e-statement", "is_red_flag": False,
             "why": "Ordinary topics are used on purpose so you don't suspect anything."},
        ],
        "lesson": "What to do: Always open your bank by typing the address yourself or using the app, never through email links.",
    },
    {
        "id": "X15", "channel": "Website", "sender": "Search result · Sponsored",
        "context": "You searched 'Bank Seri Nusa login' and clicked the FIRST result, which was marked 'Sponsored'.",
        "message": "🔒 Bank Seri Nusa Online Banking\nbankserinusa-online.help\n\nUsername: [        ]\nPassword: [        ]\n"
                   "TAC (sent to your phone): [      ]\n[ LOG IN ]",
        "is_scam": True, "difficulty": "Expert", "tactic": "Phishing link",
        "cues": [
            {"text": "Reached through a 'Sponsored' search ad", "is_red_flag": True,
             "why": "Scammers buy ads that appear above the real bank."},
            {"text": "Domain ends in '.help'", "is_red_flag": True,
             "why": "Not the bank's official domain."},
            {"text": "Asks for username, password AND TAC at once", "is_red_flag": True,
             "why": "With all three, they can log in and approve transfers immediately."},
            {"text": "Shows a padlock 🔒", "is_red_flag": False,
             "why": "A padlock only means the connection is encrypted, even to a scam site."},
        ],
        "lesson": "What to do: Bookmark your bank's real address or use the official app. Never log in via search ads.",
    },
    {
        "id": "X16", "channel": "Social media", "sender": "eWalletKu Support ✔️ (@ewalletku_care_my)",
        "context": "You posted a public complaint that your RM200 transfer failed. This account replied to you within minutes.",
        "message": "Hi! I'm eWalletKu's AI assistant 🤖 Sorry for the trouble! To trace your RM200, please fill in our secure form "
                   "with your phone number, 6-digit eWallet PIN and the verification code we'll send you: ewalletku-care.my-help.app",
        "is_scam": True, "difficulty": "Expert", "tactic": "OTP / TAC theft",
        "cues": [
            {"text": "Replied fast to your public complaint", "is_red_flag": True,
             "why": "Fake 'support' accounts watch for complaints and jump in first."},
            {"text": "Asks for your PIN and verification code", "is_red_flag": True,
             "why": "No real support team ever needs your PIN or OTP."},
            {"text": "Has a ✔️ in its name", "is_red_flag": False,
             "why": "An emoji in a name is not a verified badge."},
            {"text": "Calls itself an 'AI assistant'", "is_red_flag": False,
             "why": "Real companies use AI chat too. The request is what gives it away."},
        ],
        "lesson": "What to do: Contact support only through the help section inside the official app.",
    },
    {
        "id": "X17", "channel": "Phone call", "sender": "+60 17-338 9021",
        "context": "You're expecting a parcel today and you live in a condo with a guardhouse.",
        "audio": "x17_rider_genuine.mp3",
        "message": clip_text("x17_rider_genuine.mp3"),
        "is_scam": False, "difficulty": "Expert", "tactic": "Legit message",
        "cues": [
            {"text": "Unknown mobile number", "is_red_flag": False,
             "why": "Riders call from their own phones. On its own it's not a warning sign."},
            {"text": "Says 'no payment needed'", "is_red_flag": False,
             "why": "Nothing is being asked from you."},
            {"text": "Matches a parcel you're expecting", "is_red_flag": False,
             "why": "Context fits."},
            {"text": "Offers to leave it with the guard", "is_red_flag": False,
             "why": "A normal, low-pressure option."},
        ],
        "lesson": "Legit! No money, no codes, no pressure, and it matches your situation.",
    },
]


# --------------------------------------------------------------------------
# STORY MISSIONS: branching, multi-step situations with consequences
# node: {channel, sender, context, message, audio?, choices:[{text, next, score, note, loss?}]}
# ending node: {ending: "safe"|"close"|"lost", title, text, xp, loss?}
# --------------------------------------------------------------------------
STORIES = [
    {
        "id": "S1", "icon": "⛓️", "title": "The Chain Call", "tactic": "Impersonating authority",
        "subtitle": "Courier → 'Police' → 'Bank officer'. The classic Macau-scam chain, with real voices.",
        "savings": 38000,
        "intro": "It's a quiet weekday afternoon. You have RM38,000 in savings for your wedding next year. Your phone rings.",
        "start": "n1",
        "nodes": {
            "n1": {"channel": "Phone call", "sender": "+603-2716 8840", "context": "", "audio": "s1_n1_robocall.mp3",
                   "message": clip_text("s1_n1_robocall.mp3"),
                   "choices": [
                       {"text": "Press 1 to speak to an officer and sort it out", "next": "n2", "score": 0,
                        "note": "Pressing 1 connects you straight to the scam team. Couriers don't call about crimes."},
                       {"text": "Hang up and check your parcels in the official KilatPos app", "next": "end_best", "score": 3,
                        "note": "Perfect. You verified through a channel YOU control."},
                       {"text": "Call back the number that just called you", "next": "n2", "score": 0,
                        "note": "Calling back a scammer's number just reaches the same scammers."},
                   ]},
            "n2": {"channel": "Phone call", "sender": "'Inspector Razak'", "context": "You're transferred. A man's voice:",
                   "audio": "s1_n2_inspector.mp3", "message": clip_text("s1_n2_inspector.mp3"),
                   "choices": [
                       {"text": "Ask his name and station, hang up, then call that station using a number from an official website",
                        "next": "end_safe", "score": 3, "note": "Excellent. Independent verification breaks the chain."},
                       {"text": "Agree to receive the warrant on WhatsApp so you can check it", "next": "n3", "score": 0,
                        "note": "Real warrants aren't sent on WhatsApp. Accepting keeps you inside their script."},
                       {"text": "Say you need to talk to your family first", "next": "n2b", "score": 1,
                        "note": "Good instinct. Involving others breaks the isolation scammers depend on."},
                   ]},
            "n2b": {"channel": "Phone call", "sender": "'Inspector Razak'", "context": "His tone turns angry.",
                    "message": "\"If you tell anyone, you will be charged with obstructing an investigation. You have ONE hour. "
                               "Your bank account is already being frozen. Do you want to go to prison?\"",
                    "choices": [
                        {"text": "Hang up and tell your family anyway", "next": "end_safe", "score": 3,
                         "note": "Right call. Threats are the scammer's last tool when you start to resist."},
                        {"text": "Apologise and promise to keep it secret", "next": "n3", "score": 0,
                         "note": "Fear worked. Real police don't threaten you for talking to your family."},
                    ]},
            "n3": {"channel": "WhatsApp", "sender": "Insp. Razak (PDRM) ✔️", "context": "",
                   "message": "[Image] 'WARAN TANGKAP / ARREST WARRANT' with a police crest, your full name, IC number and case no. "
                              "CCID/KL/4471/2026.\n\n'This is your warrant. Video call me now so I can verify your face.'\n\n"
                              "[Video call] A man in police uniform sits at what looks like a police station desk.",
                   "choices": [
                       {"text": "The documents and uniform look real, so follow his instructions", "next": "n4", "score": 0,
                        "note": "Crests, uniforms and backgrounds are easy to fake. Looking real isn't proof."},
                       {"text": "End the call and phone NSRC 997 to check", "next": "end_close", "score": 2,
                        "note": "Good escape, late but safe. NSRC can confirm it's a scam."},
                       {"text": "Send a photo of your IC so he can 'verify' you", "next": "n4", "score": -1,
                        "note": "Your IC photo can be used to open mule accounts or loans in your name."},
                   ]},
            "n4": {"channel": "Phone call", "sender": "'Puan Lim, central bank audit unit'",
                   "context": "Razak transfers you again, to a woman:", "audio": "s1_n4_bank_officer.mp3",
                   "message": clip_text("s1_n4_bank_officer.mp3"),
                   "choices": [
                       {"text": "Transfer the RM38,000 to the 'safe account'", "next": "end_lost", "score": -2, "loss": 38000,
                        "note": "There is no safe account. The money goes straight to the syndicate."},
                       {"text": "Don't transfer, but install the 'secure audit app' they send", "next": "end_lost_app", "score": -2, "loss": 38000,
                        "note": "The app is malware. It gives them remote control of your phone and banking."},
                       {"text": "Stop. Hang up and call your bank using the number on your card", "next": "end_close", "score": 2,
                        "note": "Phew. Your bank can freeze anything suspicious and confirm the scam."},
                   ]},
            "end_best": {"ending": "safe", "xp": 160, "title": "🛡️ Textbook escape!",
                         "text": "You never entered the chain. Two minutes in the KilatPos app showed no such parcel."},
            "end_safe": {"ending": "safe", "xp": 130, "title": "🛡️ Safe! You broke the chain.",
                         "text": "The 'inspector' doesn't exist. Calling an official number yourself exposed it."},
            "end_close": {"ending": "close", "xp": 90, "title": "😮‍💨 Close call, but your money is safe",
                          "text": "You went deep into the scam but stopped before losing money. If you shared your IC, tell your bank and watch for accounts opened in your name."},
            "end_lost": {"ending": "lost", "xp": 20, "title": "💸 You lost RM38,000",
                         "text": "The 'safe account' was a mule account. The money moved overseas within minutes. Call NSRC 997 immediately: speed matters."},
            "end_lost_app": {"ending": "lost", "xp": 20, "title": "💸 Your account was drained",
                             "text": "The 'audit app' read your SMS codes and controlled your banking. RM38,000 was gone by night."},
        },
        "debrief": "The chain scam uses three hand-offs (courier → police → bank) to build authority step by step. "
                   "Each step adds fear, secrecy and urgency. The golden rule: **no police, court or central bank will ever ask you "
                   "to move money, install an app, or keep it secret from your family.**",
    },
    {
        "id": "S2", "icon": "🎙️", "title": "\"Kak, It's Me\"", "tactic": "Voice / video deepfake",
        "subtitle": "An AI voice clone of your brother, a fake sergeant, and a voicemail that seems to 'prove' it.",
        "savings": 3000,
        "intro": "It's 9pm. Your younger brother Amir (19) went out with friends. An unknown number calls.",
        "start": "n1",
        "nodes": {
            "n1": {"channel": "Phone call", "sender": "Unknown number", "context": "The voice sounds EXACTLY like Amir.",
                   "audio": "s2_n1_amir.mp3", "message": clip_text("s2_n1_amir.mp3"),
                   "choices": [
                       {"text": "Transfer RM3,000 now, he sounds terrified", "next": "end_lost", "score": -2, "loss": 3000,
                        "note": "Panic is exactly what the clone was designed to create."},
                       {"text": "Ask him something only the real Amir would know", "next": "n2a", "score": 2,
                        "note": "Smart. A clone can copy a voice, not your shared memories."},
                       {"text": "Hang up and call Amir's saved number", "next": "n2b", "score": 3,
                        "note": "The best first move: verify on a channel you trust."},
                   ]},
            "n2a": {"channel": "Phone call", "sender": "Unknown number",
                    "context": "You ask: 'What's our cat's name?' He hesitates: 'Kak, this is NOT the time! The officer wants to talk to you.' A new voice takes the phone:",
                    "audio": "s2_n2_sergeant_bm.mp3",
                    "message": clip_text("s2_n2_sergeant_bm.mp3") +
                               "\n\n[English] Hello, I'm Sergeant Kamal from the police station. Your brother is here. If the bail "
                               "isn't paid within 30 minutes, he goes into lockup tonight. Pay to the account he gave. Don't waste time.",
                    "choices": [
                        {"text": "Transfer. A police officer just confirmed it", "next": "end_lost", "score": -2, "loss": 3000,
                         "note": "The 'sergeant' is part of the same scam. Dodging your question was the giveaway."},
                        {"text": "Hang up and call Amir's saved number", "next": "n2b", "score": 2,
                         "note": "Good. Dodging your question was a huge red flag."},
                        {"text": "Hang up and call Mak to ask where Amir is", "next": "n3", "score": 3,
                         "note": "Excellent. They said 'don't tell Mak', so that's exactly who to call."},
                    ]},
            "n2b": {"channel": "Phone call", "sender": "Unknown number (again)",
                    "context": "You call Amir's saved number. 📵 It goes straight to voicemail. Seconds later, the unknown number calls again:",
                    "audio": "s2_n3_amir_again.mp3", "message": clip_text("s2_n3_amir_again.mp3"),
                    "choices": [
                        {"text": "Voicemail proves his phone is broken, so transfer now", "next": "end_lost", "score": -2, "loss": 3000,
                         "note": "Voicemail only means his phone is off, busy or in a cinema. Scammers count on this moment."},
                        {"text": "Don't answer. Call Mak or Amir's friend to check where he is", "next": "n3", "score": 3,
                         "note": "Exactly right. Use a second trusted person."},
                        {"text": "Call the police station the 'sergeant' named, using an official number", "next": "end_safe", "score": 3,
                         "note": "Great. The station has no record of Amir."},
                    ]},
            "n3": {"channel": "WhatsApp", "sender": "Mak ❤️", "context": "",
                   "message": "\"Amir? He's at Danish's house doing his assignment. I spoke to him 10 minutes ago. Why, what happened?\"",
                   "choices": [
                       {"text": "Tell Mak, then report the number to NSRC 997 and the police", "next": "end_best", "score": 3,
                        "note": "Reporting helps freeze the mule account and protects the next family."},
                       {"text": "Block the number and move on", "next": "end_safe", "score": 1,
                        "note": "Safe, but reporting helps stop the syndicate."},
                   ]},
            "end_best": {"ending": "safe", "xp": 160, "title": "🛡️ You beat the voice clone!",
                         "text": "Amir is fine. You verified through family and reported the scam. Now set up a family code word."},
            "end_safe": {"ending": "safe", "xp": 130, "title": "🛡️ Safe!",
                         "text": "No money lost. Amir was never in trouble. The voice was cloned from his social media videos."},
            "end_lost": {"ending": "lost", "xp": 20, "title": "💸 You lost RM3,000",
                         "text": "Amir was at a friend's house all along. Call your bank and NSRC 997 right now: fast reports can freeze the money."},
        },
        "debrief": "AI can clone a voice from a few seconds of video. **The voice is no longer proof of identity.** "
                   "Defences: (1) hang up and call back on a saved number, (2) check with a second trusted person, "
                   "(3) agree on a family code word today.",
    },
    {
        "id": "S3", "icon": "📈", "title": "The Profitable Group", "tactic": "Investment scam",
        "subtitle": "10 days inside a 'VIP' investment group. The withdrawal really works... at first.",
        "savings": 15000,
        "intro": "Your old school friend Farah adds you to a WhatsApp group: 'AI Quant Malaysia VIP 💎' (214 members). "
                 "People post profit screenshots every day. You have RM15,000 in savings.",
        "start": "n1",
        "nodes": {
            "n1": {"channel": "WhatsApp", "sender": "Dr. Lim (Mentor) · AI Quant Malaysia VIP 💎", "context": "Day 1",
                   "message": "\"Welcome! 🎉 Our AI bot made members 38% this month. Try our trial plan: RM100 only, withdraw any time. "
                              "New members get a RM30 bonus 🎁\"\n\nMember 'Kak Ros': \"Thank you Dr Lim, received RM1,250 today 🙏🙏\"\n"
                              "Member 'Jason T.': \"3rd month in, best decision of my life 🚀\"",
                   "choices": [
                       {"text": "Join with RM100. It's only a small amount", "next": "n2", "score": 0, "loss": 100,
                        "note": "Small 'trial' amounts are designed to start the hook."},
                       {"text": "Check the company and app on the Securities Commission's investor-alert and licensed lists first",
                        "next": "end_best", "score": 3, "note": "Perfect. It's on the investor alert list."},
                       {"text": "Message Farah privately: 'How long have you been in this?'", "next": "n1b", "score": 2,
                        "note": "Smart. Checking with the person outside the group."},
                   ]},
            "n1b": {"channel": "WhatsApp", "sender": "Farah (private chat)", "context": "",
                    "message": "\"Haha what group?? 😅 I'm not in any investment group... OMG my WhatsApp got hacked last week! "
                               "Don't trust anything sent from my number before Tuesday!!\"",
                    "choices": [
                        {"text": "Leave the group and report it", "next": "end_best", "score": 3,
                         "note": "The 'friend' invite was from a hijacked account."},
                        {"text": "Stay anyway. The profits look real", "next": "n2", "score": 0, "loss": 100,
                         "note": "Those 'members' are mostly scammers and bots."},
                    ]},
            "n2": {"channel": "WhatsApp", "sender": "Dr. Lim (Mentor)", "context": "Day 3", "refund": 40,
                   "message": "Your app dashboard shows RM100 → RM146. You request a RM40 withdrawal and **RM40 really arrives in your bank ✅**.\n\n"
                              "Dr. Lim: \"See? 100% real. VIP tier opens tonight: deposit RM5,000 for 40% monthly. Only 10 slots left! 🔥\"",
                   "choices": [
                       {"text": "The withdrawal worked, so it's legit. Deposit RM5,000", "next": "n3", "score": 0, "loss": 5000,
                        "note": "Small real payouts are bait to win your trust for a much bigger deposit."},
                       {"text": "Go all in with RM10,000 before the slots run out", "next": "n3", "score": -1, "loss": 10000,
                        "note": "'Limited slots' is fake scarcity."},
                       {"text": "Withdraw everything that's left and leave", "next": "n2c", "score": 2,
                        "note": "Good instinct. Let's see if they let you."},
                   ]},
            "n2c": {"channel": "WhatsApp", "sender": "AI Quant Support", "context": "Your withdrawal shows 'PENDING'.",
                    "message": "\"To withdraw your full balance, please pay 10% tax (RM10.60) plus a RM300 refundable anti-money-laundering "
                               "deposit. This is required by Bank Negara regulations.\"",
                    "choices": [
                        {"text": "Pay RM310.60 to unlock your money", "next": "end_lost_small", "score": -1, "loss": 311,
                         "note": "Fees to withdraw are the clearest sign the platform is fake. They'll invent another fee next."},
                        {"text": "Stop paying, keep screenshots, report to NSRC 997 and your bank", "next": "end_close", "score": 3,
                         "note": "You lost a little but stopped the bleeding."},
                    ]},
            "n3": {"channel": "WhatsApp", "sender": "Dr. Lim (Mentor)", "context": "Day 10",
                   "message": "Your dashboard shows **RM14,800 profit** 🤑. You try to withdraw.\n\n"
                              "\"Congratulations! Before withdrawal, pay 15% clearance tax (RM2,220). Everyone pays this, it's normal. "
                              "System closes Friday, hurry!\"",
                   "choices": [
                       {"text": "Pay the tax, otherwise you lose everything", "next": "end_lost_big", "score": -2, "loss": 2220,
                        "note": "The 'profit' never existed. Paying just adds to your loss."},
                       {"text": "Stop, keep evidence, report to NSRC 997 and your bank", "next": "end_lost_partial", "score": 2,
                        "note": "Hard, but right. Never chase losses with more money."},
                   ]},
            "end_best": {"ending": "safe", "xp": 160, "title": "🛡️ You never got hooked!",
                         "text": "One check exposed the scheme before you spent a sen."},
            "end_close": {"ending": "close", "xp": 100, "title": "😮‍💨 Small loss, big lesson",
                          "text": "You lost about RM60 but refused every 'unlock fee'. That's the hardest part, and you did it."},
            "end_lost_small": {"ending": "lost", "xp": 40, "title": "💸 Hooked by the 'withdrawal fee'",
                               "text": "No money ever comes back. Every fee leads to a new fee. Report now and stop paying."},
            "end_lost_partial": {"ending": "lost", "xp": 50, "title": "💸 You lost your deposit, but stopped in time",
                                 "text": "The dashboard was fake numbers on a screen. You lost your deposit but refused to chase it."},
            "end_lost_big": {"ending": "lost", "xp": 20, "title": "💸 Lost to 'pig-butchering'",
                             "text": "After the tax came an 'AML fee', then a 'VIP unlock'. Every step was scripted."},
        },
        "debrief": "This pattern is called **pig-butchering**: build trust → let you win small → take a big deposit → show fake profits "
                   "→ charge endless 'fees' to withdraw. A withdrawal that works once proves nothing. **Any fee to get your own money out = scam.**",
    },
    {
        "id": "S4", "icon": "🎥", "title": "The Boss on Video", "tactic": "Voice / video deepfake",
        "subtitle": "A look-alike email, a deepfake video call with two executives, and an internship on the line.",
        "savings": 480000,
        "intro": "You're an intern in the finance team at Segar Foods Sdn Bhd (email: @segarfood.com.my). "
                 "Your director, Encik Hafiz, is overseas this week.",
        "start": "n1",
        "nodes": {
            "n1": {"channel": "Email", "sender": "Hafiz Rahman <hafiz.rahman@segarfoods-group.com>", "context": "",
                   "message": "Hi, I need your help with a confidential acquisition. Don't discuss it with anyone yet, it's market "
                              "sensitive. I'll explain on a video call in 10 minutes with our CFO. Please be ready to process a payment today.\n"
                              "— Hafiz (sent from mobile)",
                   "choices": [
                       {"text": "Join the video call", "next": "n2", "score": 0,
                        "note": "Joining isn't wrong by itself, but you skipped checking the sender."},
                       {"text": "Reply to the email to confirm it's really him", "next": "n1b", "score": 1,
                        "note": "Replying goes back to the scammer, so it can't confirm anything."},
                       {"text": "Forward it to your finance manager and call Encik Hafiz on his known mobile", "next": "end_best", "score": 3,
                        "note": "Perfect. Out-of-band verification beats any deepfake."},
                   ]},
            "n1b": {"channel": "Email", "sender": "Hafiz Rahman <hafiz.rahman@segarfoods-group.com>", "context": "",
                    "message": "\"Yes it's me. Joining the call shortly. Please keep this between us. — Hafiz\"",
                    "choices": [
                        {"text": "Join the video call", "next": "n2", "score": 0, "note": "The reply came from the scammer."},
                        {"text": "Look closely at the sender address", "next": "n1c", "score": 2, "note": "Good eye."},
                    ]},
            "n1c": {"channel": "Email", "sender": "Your observation", "context": "",
                    "message": "The address is **segarfoods-group.com**, but your company uses **segarfood.com.my**.",
                    "choices": [
                        {"text": "Report it to IT and your manager", "next": "end_best", "score": 3, "note": "Caught it before the call."},
                        {"text": "Probably his personal domain. Join the call", "next": "n2", "score": -1,
                         "note": "Directors don't run company deals from look-alike domains."},
                    ]},
            "n2": {"channel": "Video call", "sender": "'Encik Hafiz' + 'CFO'",
                   "context": "The video is a bit choppy. Both familiar faces are on screen, nodding along.",
                   "audio": "s4_n2_director.mp3", "message": clip_text("s4_n2_director.mp3"),
                   "choices": [
                       {"text": "Two senior executives approved it. Process RM480,000 now", "next": "end_lost", "score": -2, "loss": 480000,
                        "note": "Both faces were real-time deepfakes. Companies have lost millions exactly like this."},
                       {"text": "Say policy requires call-back verification, then call Encik Hafiz's known mobile", "next": "n3", "score": 3,
                        "note": "Exactly right. Policy protects you from pressure."},
                       {"text": "Ask about something from last week's real team meeting", "next": "n2b", "score": 2,
                        "note": "Clever test. Deepfakes can't know your private context."},
                   ]},
            "n2b": {"channel": "Video call", "sender": "'Encik Hafiz' + 'CFO'", "context": "",
                    "message": "'Hafiz' laughs: \"No time for that! This deal closes in 20 minutes. Do you want to be the reason we lose it?\"\n"
                               "The 'CFO' adds: \"Your internship evaluation is coming up, right?\"",
                    "choices": [
                        {"text": "Process the payment. You can't risk your evaluation", "next": "end_lost", "score": -2, "loss": 480000,
                         "note": "Dodging + pressure on your career = manipulation."},
                        {"text": "Politely refuse and verify through his known mobile", "next": "n3", "score": 3,
                         "note": "Courageous and correct."},
                    ]},
            "n3": {"channel": "Phone call", "sender": "Encik Hafiz (saved contact)", "context": "",
                   "message": "\"What acquisition? I'm at the airport, I never sent that. Don't pay anything. Call IT right now!\"",
                   "choices": [
                       {"text": "Alert IT and your manager and save all the details", "next": "end_safe", "score": 3,
                        "note": "Evidence helps IT block the domain and warn others."},
                   ]},
            "end_best": {"ending": "safe", "xp": 160, "title": "🛡️ Stopped it before the call!",
                         "text": "You verified through a known channel. IT blocked the look-alike domain company-wide."},
            "end_safe": {"ending": "safe", "xp": 140, "title": "🛡️ You beat a live deepfake!",
                         "text": "You resisted two 'executives' and career pressure. That's exactly what companies need."},
            "end_lost": {"ending": "lost", "xp": 20, "title": "💸 The company lost RM480,000",
                         "text": "The real Encik Hafiz never joined that call. Report immediately: banks can sometimes recall transfers if told fast."},
        },
        "debrief": "Real-time deepfake video calls are now used in **business email compromise**. Signs: look-alike domain, secrecy, "
                   "urgency, bypassing normal approvals, and pressure on your career. **Rule: any payment request is verified on a "
                   "second channel you already trust, no matter who's asking.**",
    },
    {
        "id": "S5", "icon": "🔁", "title": "Real Call, Fake Follow-up", "tactic": "OTP / TAC theft",
        "subtitle": "The first call is genuinely your bank. The second one isn't. Can you tell them apart?",
        "savings": 8500,
        "intro": "It's 9:20pm. You have RM8,500 in your Bank Harmoni account. Your phone rings.",
        "start": "n1",
        "nodes": {
            "n1": {"channel": "Phone call", "sender": "+603-2050 7700", "context": "",
                   "audio": "x02_bank_genuine_call.mp3", "message": clip_text("x02_bank_genuine_call.mp3"),
                   "choices": [
                       {"text": "Hang up and call the number on the back of your card to check", "next": "n2", "score": 3,
                        "note": "Best habit. Works whether the call is real or fake."},
                       {"text": "Stay on the line and read out your full card number so they can check", "next": "n1b", "score": -1,
                        "note": "Never volunteer card details on an incoming call."},
                       {"text": "Ignore it. It's probably a scam", "next": "n1c", "score": 1,
                        "note": "Safe, but if the alert is real, you should still act on it through official channels."},
                   ]},
            "n1b": {"channel": "Phone call", "sender": "+603-2050 7700", "context": "",
                    "message": "\"There's no need, please never share card details on a call, even with us. "
                               "Please hang up and call the number on the back of your card.\"",
                    "choices": [{"text": "Hang up and call the number on your card", "next": "n2", "score": 1,
                                 "note": "This one was the real bank, and it told you not to share!"}]},
            "n1c": {"channel": "SMS", "sender": "Bank Harmoni", "context": "Next morning, in your banking app inbox:",
                    "message": "Your card ending 4421 has been temporarily blocked due to suspicious activity. "
                               "Please contact us via the number on your card.",
                    "choices": [{"text": "Call the bank using the number on the card", "next": "n2", "score": 2,
                                 "note": "Verified through the app. Well done."}]},
            "n2": {"channel": "Phone call", "sender": "Unknown number",
                   "context": "The bank's official hotline confirmed the block was real; a new card is coming in 5 working days. "
                              "The next morning, a different number calls:",
                   "audio": "s5_n2_card_delivery.mp3", "message": clip_text("s5_n2_card_delivery.mp3"),
                   "choices": [
                       {"text": "Read out the code. They know about the blocked card, so it must be the bank",
                        "next": "end_lost", "score": -2, "loss": 8500,
                        "note": "Knowing true details isn't proof. Leaked data or a hacked account can reveal them."},
                       {"text": "Refuse and hang up. Banks never ask you to read out a code", "next": "end_best", "score": 3,
                        "note": "Exactly. The code was a TAC to move your money."},
                       {"text": "Ask them to call back later", "next": "n2b", "score": 1,
                        "note": "Buys time, but they'll be back."},
                   ]},
            "n2b": {"channel": "Phone call", "sender": "Unknown number", "context": "An hour later, they call again.",
                    "message": "\"Ma'am, without the code your new card will be cancelled permanently and your account frozen for 30 days. "
                               "This is your final chance.\"",
                    "choices": [
                        {"text": "Read out the code", "next": "end_lost", "score": -2, "loss": 8500,
                         "note": "Threats + a code request = scam, every time."},
                        {"text": "Hang up and call the bank's official number to report it", "next": "end_best", "score": 3,
                         "note": "Reporting also protects other customers."},
                    ]},
            "end_best": {"ending": "safe", "xp": 160, "title": "🛡️ You spotted the switch!",
                         "text": "You trusted the real call the right way (by verifying) and rejected the fake follow-up."},
            "end_lost": {"ending": "lost", "xp": 20, "title": "💸 RM8,500 gone in 3 minutes",
                         "text": "The 'code' approved a transfer to a mule account. Call the bank's official line and NSRC 997 now."},
        },
        "debrief": "Scammers love to strike **right after a real event** (a real fraud alert, a data leak, a real parcel) because "
                   "you're expecting a call. Knowing true details about you is not proof. **You make the call, using a number you trust.**",
    },
]


def get_story(story_id):
    for s in STORIES:
        if s["id"] == story_id:
            return s
    return None


# ---- voice clips used by the Co-op Simulation missions ----
from coop_content import COOP_AUDIO  # noqa: E402

AUDIO_CLIPS.update(COOP_AUDIO)
