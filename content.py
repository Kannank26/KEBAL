"""
content.py - ScamShield Arena scenario bank.

Every organisation, person, phone number and website below is FICTIONAL.
All messages are training simulations. Links are shown as plain text only.

Schema for TRAINING scenarios (see Master Prompt section 6):
    id, channel, sender, context, message, is_scam, difficulty, tactic,
    cues: [{text, is_red_flag, why}], lesson

Schema for TEST items (pre/post): same fields, minus cues/lesson, plus "why".
"""

CHANNEL_ICONS = {
    "SMS": "💬",
    "WhatsApp": "🟢",
    "Email": "📧",
    "Phone call": "📞",
    "Social media": "📱",
    "Telegram": "✈️",
    "Video call": "🎥",
    "QR code": "🔳",
    "Website": "🌐",
}

TACTICS = [
    "Parcel & delivery",
    "Prize & giveaway",
    "Phishing link",
    "OTP / TAC theft",
    "Job scam",
    "Investment scam",
    "Impersonating authority",
    "Online shopping",
    "Money mule",
    "Romance scam",
    "Voice / video deepfake",
    "Loan scam",
    "Legit message",
]

# --------------------------------------------------------------------------
# TRAINING SCENARIOS (18: 12 scam, 6 legit; Easy / Medium / Hard)
# --------------------------------------------------------------------------
TRAINING_SCENARIOS = [
    # ----------------------------- EASY ----------------------------------
    {
        "id": "T01", "channel": "SMS", "sender": "KilatPos", "context": "",
        "message": "KilatPos: Your parcel MY8827 is on hold due to unpaid customs fee RM2.50. "
                   "Pay within 24 hours or it will be returned to sender: kilatpos-redelivery.top/pay",
        "is_scam": True, "difficulty": "Easy", "tactic": "Parcel & delivery",
        "cues": [
            {"text": "Asks for a tiny fee (RM2.50)", "is_red_flag": True,
             "why": "Small amounts lower your guard. The real goal is your card details."},
            {"text": "Must pay within 24 hours", "is_red_flag": True,
             "why": "A deadline creates panic so you act before you think."},
            {"text": "Link ends in '.top', not the courier's official site", "is_red_flag": True,
             "why": "Scammers register look-alike domains. Couriers don't collect fees via random SMS links."},
            {"text": "Includes a tracking number", "is_red_flag": False,
             "why": "Real messages have tracking numbers too. Scammers copy this to look official."},
        ],
        "lesson": "What to do: Never pay from an SMS link. Open the courier app you installed yourself "
                  "and check the tracking number there.",
    },
    {
        "id": "T02", "channel": "WhatsApp", "sender": "+60 11-2938 4471", "context": "",
        "message": "Tahniah! Nombor anda telah MENANG RM10,000 dalam cabutan bertuah ulang tahun ke-5 eWalletKu. "
                   "Untuk menuntut hadiah, sila bayar caj pemprosesan RM150 ke akaun 7766 1029 3381 (Bank Seri Nusa).",
        "is_scam": True, "difficulty": "Easy", "tactic": "Prize & giveaway",
        "cues": [
            {"text": "You 'won' a contest you never entered", "is_red_flag": True,
             "why": "You can't win a draw you didn't join."},
            {"text": "You must pay a fee to receive a prize", "is_red_flag": True,
             "why": "Real prizes never require you to pay first."},
            {"text": "Payment goes to a personal bank account", "is_red_flag": True,
             "why": "Companies don't collect fees through random personal accounts."},
            {"text": "Message is written in Bahasa Melayu", "is_red_flag": False,
             "why": "Language isn't a warning sign. Scams come in every language."},
        ],
        "lesson": "What to do: Ignore and block. If unsure, check the official eWalletKu app. A real prize never needs a fee.",
    },
    {
        "id": "T03", "channel": "SMS", "sender": "Bank Harmoni",
        "context": "You bought a book yesterday using your Bank Harmoni card.",
        "message": "Bank Harmoni: RM45.90 spent at Kedai Buku Ilmu on card ending 4421 on 03/11. "
                   "If this wasn't you, call the number on the back of your card. "
                   "We will never ask for your PIN or TAC.",
        "is_scam": False, "difficulty": "Easy", "tactic": "Legit message",
        "cues": [
            {"text": "Shows the amount and shop name", "is_red_flag": False,
             "why": "Normal transaction alerts include these details, and they match what you did."},
            {"text": "Tells you to call the number on your card", "is_red_flag": False,
             "why": "Good sign: it sends you to a number YOU already trust, not one in the message."},
            {"text": "No link, no request for information", "is_red_flag": False,
             "why": "Real alerts inform you. They don't ask you to click or reply."},
            {"text": "Shows only the last 4 digits of the card", "is_red_flag": False,
             "why": "Banks mask card numbers. That's normal and safe."},
        ],
        "lesson": "Legit! This matches a purchase you made, has no link, and sends you to a trusted number. "
                  "Being calm with real messages is a skill too.",
    },
    {
        "id": "T04", "channel": "WhatsApp", "sender": "Danial (saved contact)", "context": "",
        "message": "Bro sorry ah, I accidentally sent my 6-digit code to your number 😅 "
                   "Can you forward it to me? Urgent, I can't log in.",
        "is_scam": True, "difficulty": "Easy", "tactic": "OTP / TAC theft",
        "cues": [
            {"text": "Asks you to forward a 6-digit code", "is_red_flag": True,
             "why": "That code is YOUR login code. Sharing it hands over your account."},
            {"text": "Says it's urgent", "is_red_flag": True,
             "why": "Urgency stops you from checking."},
            {"text": "Comes from a friend's saved contact", "is_red_flag": False,
             "why": "Not a red flag by itself, but not proof of safety either. Your friend's account may already be hijacked."},
            {"text": "Uses casual slang and emoji", "is_red_flag": False,
             "why": "Scammers copy your friend's style. Tone tells you nothing."},
        ],
        "lesson": "What to do: Never share any OTP/TAC/verification code with anyone. Call your friend on a normal call "
                  "to check, then turn on two-step verification in WhatsApp.",
    },
    {
        "id": "T05", "channel": "Telegram", "sender": "Kerja Part-Time MY 💰", "context": "",
        "message": "PART-TIME JOB! Like YouTube videos & earn RM80–RM300 per day. No experience needed. "
                   "Pay RM50 registration to start, commission paid daily. Limited slots, join now!",
        "is_scam": True, "difficulty": "Easy", "tactic": "Job scam",
        "cues": [
            {"text": "Huge pay for almost no work", "is_red_flag": True,
             "why": "If it's too good to be true, it is."},
            {"text": "You must pay to start working", "is_red_flag": True,
             "why": "Real employers pay you. They don't charge you to work."},
            {"text": "'Limited slots, join now!'", "is_red_flag": True,
             "why": "Fake scarcity pushes you to decide fast."},
            {"text": "It's a part-time job offer", "is_red_flag": False,
             "why": "Part-time jobs are real and normal. The other details make this one fake."},
        ],
        "lesson": "What to do: Never pay to get a job. 'Like and earn' task jobs start with small payouts, "
                  "then ask for bigger 'top-ups' you never get back.",
    },
    {
        "id": "T06", "channel": "SMS", "sender": "TeleSatu", "context": "",
        "message": "TeleSatu: Your monthly bill of RM58.00 is ready. View and pay in the TeleSatu app. "
                   "Please ignore if already paid.",
        "is_scam": False, "difficulty": "Easy", "tactic": "Legit message",
        "cues": [
            {"text": "Directs you to the official app", "is_red_flag": False,
             "why": "Good sign: you open the app yourself. No link to click."},
            {"text": "Normal amount, no threats", "is_red_flag": False,
             "why": "No pressure, no 'account will be blocked'. Calm tone is typical of real bills."},
            {"text": "Mentions money/payment", "is_red_flag": False,
             "why": "Bills do mention payment. What matters is HOW they ask you to pay."},
            {"text": "'Ignore if already paid'", "is_red_flag": False,
             "why": "A reasonable, low-pressure note. That's normal."},
        ],
        "lesson": "Legit! It sends you to the official app, has no link and no pressure.",
    },
    # ----------------------------- MEDIUM --------------------------------
    {
        "id": "T07", "channel": "Phone call", "sender": "Unknown number (+603 transfer)", "context": "",
        "message": "[Call transcript] \"This is Inspector Razak from police headquarters. Your IC number was used to "
                   "open a bank account linked to money laundering. This case is confidential, don't tell your family. "
                   "To prove you're innocent, transfer your savings to our 'safe account' for checking, "
                   "or a warrant will be issued today.\"",
        "is_scam": True, "difficulty": "Medium", "tactic": "Impersonating authority",
        "cues": [
            {"text": "'Police' asking you to transfer money", "is_red_flag": True,
             "why": "Police never ask you to move money to any 'safe account'."},
            {"text": "Told to keep it secret from family", "is_red_flag": True,
             "why": "Secrecy cuts you off from people who'd spot the scam."},
            {"text": "Threat of arrest today", "is_red_flag": True,
             "why": "Fear + deadline = classic pressure tactic."},
            {"text": "Caller knows your full name and IC number", "is_red_flag": False,
             "why": "Not proof they're real. Personal data is often leaked and sold."},
        ],
        "lesson": "What to do: Hang up. Call the police station yourself using an official number. "
                  "No government agency asks you to transfer money over the phone.",
    },
    {
        "id": "T08", "channel": "Social media", "sender": "Sponsored ad · AI Wealth Bot", "context": "",
        "message": "🚀 Famous businessman reveals AI trading bot with GUARANTEED 30% monthly returns! "
                   "15,000 Malaysians already joined. Join our private WhatsApp group with mentor 'Dr. Lim' today.",
        "is_scam": True, "difficulty": "Medium", "tactic": "Investment scam",
        "cues": [
            {"text": "'Guaranteed' returns", "is_red_flag": True,
             "why": "No real investment can guarantee returns."},
            {"text": "30% per month", "is_red_flag": True,
             "why": "That's over 2,000% a year. Impossible for honest investing."},
            {"text": "Moves you to a private WhatsApp group", "is_red_flag": True,
             "why": "Private groups let scammers control what you see and fake other members' profits."},
            {"text": "Famous person endorses it", "is_red_flag": True,
             "why": "Celebrity ads are often deepfaked or used without permission."},
            {"text": "Mentions AI technology", "is_red_flag": False,
             "why": "AI is real and used in finance. The buzzword alone isn't the warning sign."},
        ],
        "lesson": "What to do: Check if the company is licensed with the Securities Commission before investing anything. "
                  "Guaranteed high returns = scam, every time.",
    },
    {
        "id": "T09", "channel": "WhatsApp", "sender": "Seller from PasarKu listing", "context": "",
        "message": "Hi sis! iPhone 16 Pro brand new sealed RM1,800 only 😊 (market price RM5,000). "
                   "If you pay outside the PasarKu app I give extra 10% discount. Transfer to my personal account ya.",
        "is_scam": True, "difficulty": "Medium", "tactic": "Online shopping",
        "cues": [
            {"text": "Price is far below market", "is_red_flag": True,
             "why": "Huge discounts on popular items are bait."},
            {"text": "Asks you to pay outside the platform", "is_red_flag": True,
             "why": "Paying outside the app removes your buyer protection."},
            {"text": "Payment to a personal account", "is_red_flag": True,
             "why": "No way to get your money back if the item never arrives."},
            {"text": "Seller is friendly and uses emoji", "is_red_flag": False,
             "why": "Friendliness isn't evidence either way. Scammers are often very nice."},
        ],
        "lesson": "What to do: Always pay inside the marketplace app so you're protected. "
                  "Check the seller's account and bank number on Semak Mule before any transfer.",
    },
    {
        "id": "T10", "channel": "Email", "sender": "Bank Seri Nusa <notices@bankserinusa.example>", "context": "",
        "message": "Dear customer, we have updated our Terms & Conditions effective 1 December. "
                   "No action is needed from you. To read the changes, open the Bank Seri Nusa app and go to Profile > Notices.",
        "is_scam": False, "difficulty": "Medium", "tactic": "Legit message",
        "cues": [
            {"text": "'No action needed'", "is_red_flag": False,
             "why": "Real notices often need nothing from you. No pressure."},
            {"text": "Tells you to open the app yourself", "is_red_flag": False,
             "why": "Good sign: no link to click."},
            {"text": "Starts with 'Dear customer'", "is_red_flag": False,
             "why": "Generic greetings are common in both real and fake mail. Not decisive here."},
            {"text": "It's an email from a bank", "is_red_flag": False,
             "why": "Banks do send emails. Judge by what it asks you to do."},
        ],
        "lesson": "Legit! It asks for nothing, has no link, and points you to the official app.",
    },
    {
        "id": "T11", "channel": "Telegram", "sender": "Duit Mudah Pelajar", "context": "",
        "message": "Student? Earn RM500 easily! Just rent us your bank account for 1 week. "
                   "We handle everything, you just give us your ATM card & online banking login. 100% safe.",
        "is_scam": True, "difficulty": "Medium", "tactic": "Money mule",
        "cues": [
            {"text": "Asks to 'rent' your bank account", "is_red_flag": True,
             "why": "Your account will be used to move stolen money. YOU become legally responsible."},
            {"text": "Wants your ATM card and banking login", "is_red_flag": True,
             "why": "Never hand these to anyone, for any amount."},
            {"text": "Targets students", "is_red_flag": True,
             "why": "Mule recruiters target students who need cash and have clean records."},
            {"text": "Message is short", "is_red_flag": False,
             "why": "Length doesn't matter. The request does."},
        ],
        "lesson": "What to do: Never lend or rent your account. Money mules can face criminal charges and frozen accounts. "
                  "Report recruiters to the police.",
    },
    {
        "id": "T12", "channel": "WhatsApp", "sender": "Daniel ❤️ (met online)",
        "context": "You've chatted with Daniel online for 3 weeks but never met or video-called.",
        "message": "Hi dear, I miss you so much. I sent you a box of gifts and some cash from the oil rig, "
                   "but customs is holding it. Please pay RM3,000 clearance fee, I'll pay you back double when I'm back next month 🙏",
        "is_scam": True, "difficulty": "Medium", "tactic": "Romance scam",
        "cues": [
            {"text": "Never met, never video-called", "is_red_flag": True,
             "why": "Romance scammers avoid live video because the photos aren't theirs."},
            {"text": "Asks you to pay a 'customs fee' for a gift", "is_red_flag": True,
             "why": "The parcel doesn't exist. The 'fee' is the scam."},
            {"text": "Promises to pay you back double", "is_red_flag": True,
             "why": "Promises of repayment are used to make you feel safe sending money."},
            {"text": "He has sent you photos of himself", "is_red_flag": False,
             "why": "Not proof. Photos are often stolen from real people's profiles."},
        ],
        "lesson": "What to do: Never send money to someone you've only met online. Reverse-image-search their photos "
                  "and talk to a trusted friend.",
    },
    # ------------------------------ HARD ---------------------------------
    {
        "id": "T13", "channel": "Phone call", "sender": "Unknown number",
        "context": "The voice sounds EXACTLY like your younger brother Amir.",
        "message": "[Call transcript] \"Kak, it's me Amir! I had an accident, police are here. I need RM2,000 now for bail. "
                   "My phone broke, I'm using a stranger's phone. Please don't tell Mak, she'll panic. "
                   "Transfer to this account: 1029 4471 88 (name: Tan K. L.)\"",
        "is_scam": True, "difficulty": "Hard", "tactic": "Voice / video deepfake",
        "cues": [
            {"text": "Call is from an unknown number", "is_red_flag": True,
             "why": "'My phone broke' is a classic excuse to explain a new number."},
            {"text": "Urgent money + 'don't tell Mak'", "is_red_flag": True,
             "why": "Urgency plus secrecy stops you from checking with family."},
            {"text": "Bank account is in a stranger's name", "is_red_flag": True,
             "why": "Why would your brother's bail go to a stranger's personal account?"},
            {"text": "The voice sounds exactly like Amir", "is_red_flag": False,
             "why": "Careful: this is NOT proof. AI can clone a voice from a few seconds of video online."},
        ],
        "lesson": "What to do: Hang up and call Amir (or your parents) on the number you already have saved. "
                  "Agree on a secret family code word for emergencies.",
    },
    {
        "id": "T14", "channel": "Video call", "sender": "'Encik Hafiz (Director)'",
        "context": "You're an intern in the finance team. Your director joins a surprise video call.",
        "message": "[Video call] Camera is a bit blurry. \"Hi, I'm rushing to a meeting. We must pay a new supplier today, "
                   "RM48,000, it's confidential, don't loop in the finance manager. I'll send the new account details by chat. "
                   "Do it in the next 30 minutes.\"",
        "is_scam": True, "difficulty": "Hard", "tactic": "Voice / video deepfake",
        "cues": [
            {"text": "Urgent and 'confidential' payment", "is_red_flag": True,
             "why": "Secrecy + urgency is the core of boss-impersonation scams."},
            {"text": "New, never-used account details", "is_red_flag": True,
             "why": "Changes to payment accounts must always be verified separately."},
            {"text": "Told to skip the normal approval", "is_red_flag": True,
             "why": "Bypassing approval is exactly what a scammer needs."},
            {"text": "Face and voice look like the director", "is_red_flag": False,
             "why": "Not proof. Real-time deepfake video calls have tricked companies out of millions."},
        ],
        "lesson": "What to do: Pause. Verify through a second channel: call the director on their known number "
                  "and follow normal approval rules, no matter how senior the person seems.",
    },
    {
        "id": "T15", "channel": "SMS", "sender": "KilatPos",
        "context": "You ordered shoes online 3 days ago.",
        "message": "KilatPos: Your parcel MY4410 is out for delivery today between 2pm and 6pm. "
                   "Track it in the KilatPos app.",
        "is_scam": False, "difficulty": "Hard", "tactic": "Legit message",
        "cues": [
            {"text": "Matches something you actually ordered", "is_red_flag": False,
             "why": "Context fits: you're expecting a parcel."},
            {"text": "No payment request", "is_red_flag": False,
             "why": "Real delivery updates don't ask for surprise fees."},
            {"text": "Sends you to the official app", "is_red_flag": False,
             "why": "No link, so nothing to phish you with."},
            {"text": "Comes from a courier name you know", "is_red_flag": False,
             "why": "Sender names can be faked, but here nothing else is suspicious."},
        ],
        "lesson": "Legit! Compare with T01: same courier, but no fee, no link, no pressure, and it matches your order.",
    },
    {
        "id": "T16", "channel": "Email", "sender": "Bank Harmoni Security <alert@bankharmoni.secure-login.co>", "context": "",
        "message": "⚠️ Unusual sign-in detected from Moscow, Russia. If this wasn't you, secure your account within 30 minutes "
                   "or it will be locked: bankharmoni.secure-login.co/verify",
        "is_scam": True, "difficulty": "Hard", "tactic": "Phishing link",
        "cues": [
            {"text": "The real domain is 'secure-login.co', not the bank's", "is_red_flag": True,
             "why": "Read domains right-to-left: 'bankharmoni' is just a sub-label on someone else's site."},
            {"text": "30-minute deadline", "is_red_flag": True,
             "why": "Panic deadlines are designed to stop you from checking."},
            {"text": "Scary foreign login alert", "is_red_flag": True,
             "why": "Fear makes you click first and think later."},
            {"text": "Uses the bank's name and a warning emoji", "is_red_flag": False,
             "why": "Branding is easy to copy. It proves nothing."},
        ],
        "lesson": "What to do: Never log in through an email link. Open the banking app yourself, "
                  "or call the number on the back of your card.",
    },
    {
        "id": "T17", "channel": "SMS", "sender": "+60 17-882 1190", "context": "",
        "message": "PINJAMAN PERIBADI LULUS SEGERA! Tanpa dokumen, tanpa semakan CTOS. RM20,000 masuk akaun dalam 1 jam. "
                   "Bayar deposit RM300 dahulu untuk proses. WhatsApp kami sekarang!",
        "is_scam": True, "difficulty": "Hard", "tactic": "Loan scam",
        "cues": [
            {"text": "Pay a deposit before getting the loan", "is_red_flag": True,
             "why": "Licensed lenders deduct fees from the loan. They never ask for money upfront."},
            {"text": "No documents, no credit check", "is_red_flag": True,
             "why": "Real lenders must check. 'No checks' means not licensed."},
            {"text": "Approved in 1 hour", "is_red_flag": True,
             "why": "Too fast and too easy to be real."},
            {"text": "Written in Bahasa Melayu", "is_red_flag": False,
             "why": "Language is not a warning sign."},
        ],
        "lesson": "What to do: Only borrow from licensed banks or lenders. Any 'deposit first' loan is a scam.",
    },
    {
        "id": "T18", "channel": "WhatsApp", "sender": "SMK Taman Ilmu (Official)",
        "context": "You're a student at SMK Taman Ilmu and joined the school's WhatsApp channel.",
        "message": "Makluman: Ujian Pertengahan Tahun bermula 10 Jun. Jadual boleh dilihat di papan kenyataan sekolah "
                   "dan portal rasmi sekolah. Tiada sebarang bayaran diperlukan. Terima kasih.",
        "is_scam": False, "difficulty": "Hard", "tactic": "Legit message",
        "cues": [
            {"text": "Says 'no payment required'", "is_red_flag": False,
             "why": "It asks for nothing at all."},
            {"text": "Info can be checked on the school notice board", "is_red_flag": False,
             "why": "You can verify it offline. A great sign."},
            {"text": "Sent through a group you joined", "is_red_flag": False,
             "why": "Matches your context."},
            {"text": "Formal Bahasa Melayu", "is_red_flag": False,
             "why": "Normal for school notices."},
        ],
        "lesson": "Legit! Nothing to click, nothing to pay, and you can confirm it in person.",
    },
    {
        "id": "T19", "channel": "WhatsApp", "sender": "Klinik Pergigian Sejahtera",
        "context": "You booked a dental check-up at this clinic last week.",
        "message": "Salam & hi! Reminder of your dental check-up tomorrow (Thu) at 10:00am with Dr. Aina. "
                   "Reply 1 to confirm or 2 to reschedule. Please bring your clinic card. Thank you 😊",
        "is_scam": False, "difficulty": "Medium", "tactic": "Legit message",
        "cues": [
            {"text": "Asks you to reply 1 or 2", "is_red_flag": False,
             "why": "Replying with a number shares no private info. That's a normal booking reminder."},
            {"text": "Matches an appointment you booked", "is_red_flag": False,
             "why": "Context fits what you actually did."},
            {"text": "No link and no payment request", "is_red_flag": False,
             "why": "Nothing to click, nothing to pay."},
            {"text": "Friendly tone with emoji", "is_red_flag": False,
             "why": "Tone isn't evidence either way. Here everything else checks out."},
        ],
        "lesson": "Legit! It matches your booking and asks for nothing sensitive. Not every message is a trap.",
    },
]

# --------------------------------------------------------------------------
# PRE-TEST and POST-TEST (10 each: 6 scam + 4 legit, parallel, 1 voice item each)
# Harder than the Easy arena rounds on purpose, so scores don't hit 100% (ceiling effect).
# --------------------------------------------------------------------------
PRE_TEST = [
    {"id": "P01", "channel": "SMS", "sender": "eWalletKu",
     "context": "This SMS appears in the same thread as your real eWalletKu messages.",
     "message": "eWalletKu: Your daily transfer limit has been raised to RM20,000. Not you? Cancel within 1 hour: ewalletku.com.my-secure-cancel.net",
     "is_scam": True, "tactic": "Phishing link",
     "why": "Sender IDs can be spoofed into the real thread. The real domain is '…-secure-cancel.net'."},
    {"id": "P02", "channel": "SMS", "sender": "Bank Seri Nusa",
     "context": "You just started a RM120 transfer to your friend Ahmad in your banking app.",
     "message": "Bank Seri Nusa: Your TAC for transfer RM120 to AHMAD is 448210. Never share this TAC with anyone, including bank staff.",
     "is_scam": False, "tactic": "Legit message",
     "why": "You requested it, the details match, and it warns you not to share it."},
    {"id": "P03", "channel": "WhatsApp", "sender": "+60 12-554 0093", "context": "",
     "message": "Hi, I'm HR from GlobalMart. You're shortlisted for a remote job RM5,000/month. Download this app (GM-Interview.apk) to start your interview.",
     "is_scam": True, "tactic": "Job scam",
     "why": "Unsolicited job + APK file. APKs can install malware that steals your banking info."},
    {"id": "P04", "channel": "WhatsApp", "sender": "+60 16-882 4410",
     "context": "You're expecting a parcel today. You're at work, not at home.",
     "message": "Hi, KilatPos rider here. I'm at your house gate, nobody answering. Can I leave the parcel with your neighbour at No. 12? Already paid, no need to pay anything 👍",
     "is_scam": False, "tactic": "Legit message",
     "why": "Matches your parcel, asks for nothing but a yes/no, and no payment."},
    {"id": "P05", "channel": "Phone call", "sender": "Automated call", "context": "",
     "audio": "p05_tax_robocall.mp3",
     "message": "This is the tax department. Our records show you owe eight thousand four hundred ringgit in unpaid tax. A warrant for your arrest will be issued today. Press one now to speak with an enforcement officer.",
     "is_scam": True, "tactic": "Impersonating authority",
     "why": "Arrest threat by robocall. Agencies send official letters, not 'press 1' threats."},
    {"id": "P06", "channel": "Email", "sender": "Bank Seri Nusa <service@bankseri-nusa.com.my>", "context": "Your bank's real domain is bankserinusa.com.my.",
     "message": "Dear customer, a new secure message is waiting in your inbox. Please log in to read it: bankseri-nusa.com.my/messages",
     "is_scam": True, "tactic": "Phishing link",
     "why": "Look-alike domain with a hyphen, and a login link. No urgency, but still phishing."},
    {"id": "P07", "channel": "Email", "sender": "University Library", "context": "You borrowed a book last month.",
     "message": "Reminder: the book 'Intro to Python' is due on 12 Nov. You can renew it through the student portal you normally use. Late fine: RM0.20/day.",
     "is_scam": False, "tactic": "Legit message",
     "why": "Matches your situation, small normal fine, no link, sends you to your usual portal."},
    {"id": "P08", "channel": "WhatsApp", "sender": "+60 19-330 7781", "context": "",
     "message": "Hi sayang, this is Mum, new number. My phone fell in water. Can you help pay my bill RM850 urgently? I'll explain later.",
     "is_scam": True, "tactic": "Voice / video deepfake",
     "why": "'New number' + urgent money. Call Mum on her old number first."},
    {"id": "P09", "channel": "WhatsApp", "sender": "+60 11-2093 5517",
     "context": "Your banking app really shows: 'Received RM650 from LEE C.H.' You don't know this person.",
     "message": "Sorry bro, wrong transfer 🙏 Please return RM650 to my company account instead, mine got problem: 5510 2287 3301. Urgent!",
     "is_scam": True, "tactic": "Money mule",
     "why": "The money is real but probably stolen. Sending it to another account makes you a mule. Let your bank reverse it."},
    {"id": "P10", "channel": "Website", "sender": "eWalletKu app (you opened it yourself)",
     "context": "You opened the official eWalletKu app from your home screen.",
     "message": "Verify your identity to unlock higher limits: scan your MyKad, then take a short selfie video.",
     "is_scam": False, "tactic": "Legit message",
     "why": "eKYC inside the official app you opened is normal. The same request via a sent link would be a scam."},
]

POST_TEST = [
    {"id": "Q01", "channel": "SMS", "sender": "PasarKu",
     "context": "This SMS appears in the same thread as your real PasarKu messages.",
     "message": "PasarKu: Your account was used to buy an iPad (RM2,999). Not you? Cancel within 30 min: pasarku.com.my-order-cancel.co",
     "is_scam": True, "tactic": "Phishing link",
     "why": "Spoofed into the real thread. The real domain is '…-order-cancel.co'. Check orders in the app."},
    {"id": "Q02", "channel": "SMS", "sender": "PasarKu",
     "context": "You just tried to log into PasarKu on a new laptop.",
     "message": "PasarKu: Your login code is 731942. Do not share this code with anyone.",
     "is_scam": False, "tactic": "Legit message",
     "why": "You triggered it yourself, and it warns you not to share it."},
    {"id": "Q03", "channel": "Telegram", "sender": "Hotel Review Jobs MY", "context": "",
     "message": "Earn RM300/day reviewing hotels online! Top up RM100 to unlock premium tasks. Withdraw anytime.",
     "is_scam": True, "tactic": "Job scam",
     "why": "Paying to 'unlock tasks' is the classic task-job scam."},
    {"id": "Q04", "channel": "SMS", "sender": "KilatPos", "context": "You were expecting a parcel today.",
     "message": "KilatPos: Your parcel has been delivered and received by GUARDHOUSE at 2:14pm.",
     "is_scam": False, "tactic": "Legit message",
     "why": "Informational only: no link, no fee, matches your situation."},
    {"id": "Q05", "channel": "Phone call", "sender": "'Bank Harmoni Fraud Dept'", "context": "",
     "audio": "q05_fraud_dept_tac.mp3",
     "message": "Hello, this is Bank Harmoni's fraud department. We've detected suspicious activity and need to protect your money. We just sent you a six-digit TAC. Please read it out to me now so we can secure your account.",
     "is_scam": True, "tactic": "OTP / TAC theft",
     "why": "Banks never ask you to read out a TAC. That code approves a transaction."},
    {"id": "Q06", "channel": "Email", "sender": "TeleSatu Billing <billing@teIesatu.com.my>", "context": "Your telco's real domain is telesatu.com.my.",
     "message": "Your auto-debit payment could not be processed. Please update your card details to avoid service interruption: teIesatu.com.my/billing",
     "is_scam": True, "tactic": "Phishing link",
     "why": "'teIesatu' uses a capital I instead of a lowercase l. A look-alike domain asking for card details."},
    {"id": "Q07", "channel": "Email", "sender": "TeleSatu", "context": "",
     "message": "TeleSatu: Scheduled network maintenance in your area on 15 Nov, 1am–4am. No action needed. Sorry for any inconvenience.",
     "is_scam": False, "tactic": "Legit message",
     "why": "Asks nothing of you, no link, no urgency."},
    {"id": "Q08", "channel": "WhatsApp", "sender": "+60 16-221 9004", "context": "",
     "message": "Salam, ini Pak Long. Using my friend's phone. I'm stuck at the hospital and need RM1,200 urgently for deposit. Please transfer to my friend's account first.",
     "is_scam": True, "tactic": "Voice / video deepfake",
     "why": "Unknown number + urgent money + someone else's account. Call Pak Long's real number."},
    {"id": "Q09", "channel": "WhatsApp", "sender": "+60 12-7781 0042",
     "context": "Your eWallet really shows: 'Received RM300 from +60 12-7781 0042'.",
     "message": "Aiyo sorry, I topped up to wrong number 😭 Can you send RM300 to my boss's eWallet 017-220 9183? I'll get in trouble!",
     "is_scam": True, "tactic": "Money mule",
     "why": "Real money, but returning it to a different account makes you a mule. Ask eWalletKu support (in-app) to reverse it."},
    {"id": "Q10", "channel": "Website", "sender": "Bank Harmoni app (you opened it yourself)",
     "context": "Your new debit card arrived by post. You opened the official Bank Harmoni app.",
     "message": "Activate your new card ending 7730: set a 6-digit card PIN below. Never share your PIN with anyone.",
     "is_scam": False, "tactic": "Legit message",
     "why": "Setting a PIN inside the official app you opened is normal. The danger is sharing it with a person."},
]

# --------------------------------------------------------------------------
# RETENTION TEST (delayed retest, ~2 weeks after the post-test): 10 new parallel items
# --------------------------------------------------------------------------
RETENTION_TEST = [
    {"id": "R01", "channel": "SMS", "sender": "TeleSatu",
     "context": "This SMS appears in the same thread as your real TeleSatu messages.",
     "message": "TeleSatu: Your number will be DEACTIVATED in 24 hours due to incomplete SIM registration. Update now: telesatu.com.my-sim-update.co",
     "is_scam": True, "tactic": "Phishing link",
     "why": "Spoofed into the real thread, with a deadline. The real domain is '…-sim-update.co'. Check in the official app."},
    {"id": "R02", "channel": "SMS", "sender": "eWalletKu",
     "context": "You just asked to change your eWalletKu PIN inside the app.",
     "message": "eWalletKu: Your verification code is 552901. It expires in 5 minutes. Never share this code with anyone.",
     "is_scam": False, "tactic": "Legit message",
     "why": "You started the action yourself, and it tells you not to share the code."},
    {"id": "R03", "channel": "Social media", "sender": "@glow.beauty.my (Instagram DM)", "context": "",
     "message": "Hi dear! We're hiring brand ambassadors, RM200/day just posting reviews 💄 First buy our RM150 starter kit from this link, then start earning today!",
     "is_scam": True, "tactic": "Job scam",
     "why": "Pay-to-start 'jobs' are scams. Real employers don't make you buy anything first."},
    {"id": "R04", "channel": "SMS", "sender": "KilatRide",
     "context": "You just booked a ride in the KilatRide app.",
     "message": "KilatRide: Your driver Azman (WXY 1234, silver Myvi) is arriving in 3 minutes.",
     "is_scam": False, "tactic": "Legit message",
     "why": "Matches the ride you booked, asks for nothing, no link."},
    {"id": "R05", "channel": "Phone call", "sender": "Automated call", "context": "",
     "audio": "r05_bank_login_bm.mp3",
     "message": "Ini panggilan automatik daripada Bank Seri Nusa. Kami mengesan log masuk ke akaun anda dari peranti baharu. Untuk membatalkan log masuk ini, tekan satu dan masukkan kata laluan perbankan dalam talian anda sekarang.\n\n[English] This is an automated call from Bank Seri Nusa. We detected a login to your account from a new device. To cancel it, press 1 and enter your online banking password now.",
     "is_scam": True, "tactic": "OTP / TAC theft",
     "why": "No bank asks for your password over the phone. Hang up and check in the official app."},
    {"id": "R06", "channel": "Email", "sender": "PasarKu Support <support@pasarku-help.com.my>",
     "context": "PasarKu's real domain is pasarku.com.my.",
     "message": "We noticed a problem with your last payment. Please re-enter your card details within 24 hours to avoid order cancellation: pasarku-help.com.my/payment",
     "is_scam": True, "tactic": "Phishing link",
     "why": "Look-alike domain ('pasarku-help') plus a deadline and a request for card details."},
    {"id": "R07", "channel": "Email", "sender": "Exam Unit", "context": "Your final exams start next month.",
     "message": "Your examination slip is now available. Please download it from the student portal you normally use and bring it to every paper.",
     "is_scam": False, "tactic": "Legit message",
     "why": "Matches your situation and sends you to your usual portal, with no link or request."},
    {"id": "R08", "channel": "WhatsApp", "sender": "+60 14-773 2016", "context": "",
     "message": "Bro, it's Hafiz, new number. Stuck at the airport, my card kena block. Can you transfer RM400 now? I'll pay you back tonight, promise!",
     "is_scam": True, "tactic": "Voice / video deepfake",
     "why": "'New number' plus urgent money. Call Hafiz on his old number first."},
    {"id": "R09", "channel": "WhatsApp", "sender": "Jason (friend of your cousin)", "context": "",
     "message": "Hi, can I borrow your bank account for one day? I'm getting a RM2,000 refund but my account is under maintenance. Just send it to me after it arrives, I'll give you RM200 for helping.",
     "is_scam": True, "tactic": "Money mule",
     "why": "Letting someone use your account to move money makes you a money mule, and you can be charged."},
    {"id": "R10", "channel": "Website", "sender": "Bank Harmoni app (you opened it yourself)",
     "context": "You opened the official Bank Harmoni app from your home screen.",
     "message": "Set up face recognition for faster login? You can turn this off any time in Settings.",
     "is_scam": False, "tactic": "Legit message",
     "why": "An optional setting inside the official app you opened. Nothing is sent to anyone."},
]

HELP_STEPS = [
    ("Call NSRC 997 immediately", "If you've transferred money, call the National Scam Response Centre at 997 as fast as possible. Speed helps freeze funds."),
    ("Call your bank", "Use the number on the back of your card or in the official app. Ask them to block your card or account."),
    ("Lodge a police report", "At any police station or online. Keep screenshots, phone numbers, account numbers and receipts."),
    ("Check before you pay", "Check suspicious phone numbers and bank accounts on Semak Mule (the police's online checker) before transferring money."),
    ("Secure your accounts", "Change passwords, turn on two-step verification, and never share OTP/TAC codes."),
    ("Talk about it", "Being scammed is not your fault. Telling family and friends helps protect them too."),
]


# ---- merge in the Expert pack (complex scenarios + voice scams) ----
from content_expert import EXPERT_SCENARIOS, STORIES, AUDIO_CLIPS, get_story  # noqa: E402

TRAINING_SCENARIOS = TRAINING_SCENARIOS + EXPERT_SCENARIOS
DIFFICULTIES = ["Easy", "Medium", "Hard", "Expert"]


def get_training(scenario_id):
    for s in TRAINING_SCENARIOS:
        if s["id"] == scenario_id:
            return s
    return None
