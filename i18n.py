"""
i18n.py - English / Bahasa Melayu interface.

Usage in app.py:   T("Start mission ▶")      or   T("Round {i} of {n}", i=1, n=5)
The English text IS the key. If a Malay translation is missing, English is shown
(so the app never breaks). check_i18n.py lists any missing translations.

To add another language later (e.g. Tamil or Mandarin), add a dict like MS and
extend LANGS.
"""
import streamlit as st

LANGS = {"en": "English", "ms": "Bahasa Melayu"}


def lang():
    return st.session_state.get("lang", "en")


def tr(text, lang_code, /, **kw):
    """Translate text into lang_code ("en" or "ms"). Positional-only, so any {placeholder} name is safe."""
    s = MS.get(text, text) if lang_code == "ms" else text
    return s.format(**kw) if kw else s


def T(text, **kw):
    return tr(text, lang(), **kw)


def TT(mapper=None):
    """A format_func for menus, with the current language locked in when the menu is built."""
    lang_code = lang()
    return lambda x: tr(mapper(x) if mapper else x, lang_code)


MS = {
    # ------------------------------------------------------------ navigation
    "🏠 Home": "🏠 Utama",
    "📏 Pre-Test": "📏 Ujian Pra",
    "🎮 Training Arena": "🎮 Arena Latihan",
    "🎭 Story Missions": "🎭 Misi Cerita",
    "🗺️ Co-op Simulation": "🗺️ Simulasi Berpasukan",
    "🏁 Post-Test": "🏁 Ujian Pasca",
    "📊 My Progress": "📊 Kemajuan Saya",
    "👩‍🏫 Teacher Dashboard": "👩‍🏫 Papan Pemuka Guru",
    "🆘 Safety & Help": "🆘 Keselamatan & Bantuan",
    "👩‍🏫 Teacher / Pilot Dashboard": "👩‍🏫 Papan Pemuka Guru / Rintis",
    "🌐 Language": "🌐 Bahasa",

    # ------------------------------------------------------------ shared phone views
    "Situation:": "Situasi:",
    "TRAINING SIMULATION · ALL NAMES FICTIONAL": "SIMULASI LATIHAN · SEMUA NAMA REKAAN",
    "TRAINING SIMULATION · SYNTHETIC VOICE · ALL NAMES FICTIONAL": "SIMULASI LATIHAN · SUARA SINTETIK · SEMUA NAMA REKAAN",
    "INCOMING": "PANGGILAN MASUK",
    "🔊 Press play below and listen carefully": "🔊 Tekan main di bawah dan dengar baik-baik",
    "⚠️ Audio file missing. Run generate_audio.py. Transcript below.":
        "⚠️ Fail audio tiada. Jalankan generate_audio.py. Transkrip di bawah.",
    "📝 Show transcript (for deaf / hard-of-hearing players)": "📝 Tunjuk transkrip (untuk pemain pekak / kurang pendengaran)",

    # ------------------------------------------------------------ channels
    "SMS": "SMS", "WhatsApp": "WhatsApp", "Email": "E-mel", "Phone call": "Panggilan telefon",
    "Social media": "Media sosial", "Telegram": "Telegram", "Video call": "Panggilan video",
    "QR code": "Kod QR", "Website": "Laman web", "Story": "Cerita", "Co-op": "Berpasukan",

    # ------------------------------------------------------------ tactics
    "Parcel & delivery": "Bungkusan & penghantaran",
    "Prize & giveaway": "Hadiah & cabutan bertuah",
    "Phishing link": "Pautan pancingan data (phishing)",
    "OTP / TAC theft": "Kecurian OTP / TAC",
    "Job scam": "Penipuan kerja",
    "Investment scam": "Penipuan pelaburan",
    "Impersonating authority": "Menyamar pihak berkuasa",
    "Online shopping": "Beli-belah dalam talian",
    "Money mule": "Keldai akaun (money mule)",
    "Romance scam": "Penipuan cinta",
    "Voice / video deepfake": "Deepfake suara / video",
    "Loan scam": "Penipuan pinjaman",
    "Legit message": "Mesej sah",
    "Online meet-up lure": "Umpan pertemuan dalam talian",
    "Job scam / trafficking": "Penipuan kerja / pemerdagangan orang",
    "Doorstep impostor": "Penyamar di depan pintu",

    # ------------------------------------------------------------ difficulty
    "Easy": "Mudah", "Medium": "Sederhana", "Hard": "Sukar", "Expert": "Pakar",

    # ------------------------------------------------------------ levels & badges
    "Rookie": "Pemula", "Scam Spotter": "Pengesan Scam", "Fraud Fighter": "Pejuang Anti-Penipuan",
    "Cyber Guardian": "Penjaga Siber", "Scam Grandmaster": "Pakar Agung Anti-Scam",
    "First Catch": "Tangkapan Pertama", "Correctly caught your first scam": "Berjaya kesan scam pertama anda",
    "Sharp Eye": "Mata Helang",
    "Perfect round: right verdict, every red flag, no false alarms":
        "Pusingan sempurna: keputusan betul, semua tanda bahaya, tiada amaran palsu",
    "Calm Mind": "Minda Tenang",
    "Correctly trusted a legit message without false alarms": "Mempercayai mesej sah dengan betul tanpa amaran palsu",
    "Hot Streak": "Rentak Panas", "5 correct verdicts in a row": "5 keputusan betul berturut-turut",
    "Deepfake Buster": "Pemusnah Deepfake", "Caught a voice or video deepfake scam": "Berjaya kesan scam deepfake suara atau video",
    "Baseline Set": "Garis Dasar", "Completed the pre-test": "Selesai ujian pra",
    "Proven Growth": "Kemajuan Terbukti", "Post-test score beat your pre-test": "Markah ujian pasca mengatasi ujian pra",
    "Sharp Ears": "Telinga Tajam", "3 correct verdicts on voice / video call rounds": "3 keputusan betul untuk panggilan suara / video",
    "Expert Eye": "Mata Pakar", "5 correct verdicts on Expert rounds": "5 keputusan betul dalam pusingan Pakar",
    "Story Survivor": "Penyelamat Cerita",
    "Escaped 3 different Story Missions without losing money": "Terselamat dalam 3 Misi Cerita tanpa kehilangan wang",
    "Untouchable": "Kebal", "Escaped all 5 Story Missions without losing money": "Terselamat dalam kelima-lima Misi Cerita tanpa kehilangan wang",

    # ------------------------------------------------------------ 4P + help
    "The 4P Scam Check": "Semakan Scam 4P",
    "⏰ Pressure": "⏰ Tekanan (Pressure)",
    "Urgency, fear, threats, deadlines, \"don't tell anyone\".": "Desakan, ketakutan, ugutan, tarikh akhir, \"jangan beritahu sesiapa\".",
    "💸 Payment": "💸 Bayaran (Payment)",
    "Fees to claim prizes, deposits, transfers to personal accounts.": "Yuran tuntut hadiah, deposit, pindahan ke akaun peribadi.",
    "🔑 Private info": "🔑 Maklumat peribadi (Private info)",
    "Asks for OTP/TAC, passwords, banking login, IC photos.": "Minta OTP/TAC, kata laluan, log masuk bank, gambar IC.",
    "🧭 Path": "🧭 Laluan (Path)",
    "Pulls you off official channels: odd links, APK files, new numbers, private groups.":
        "Menarik anda keluar dari saluran rasmi: pautan pelik, fail APK, nombor baharu, kumpulan peribadi.",
    "Call NSRC 997 immediately": "Hubungi NSRC 997 segera",
    "If you've transferred money, call the National Scam Response Centre at 997 as fast as possible. Speed helps freeze funds.":
        "Jika anda sudah memindahkan wang, hubungi Pusat Respons Scam Kebangsaan di 997 secepat mungkin. Kepantasan membantu membekukan dana.",
    "Call your bank": "Hubungi bank anda",
    "Use the number on the back of your card or in the official app. Ask them to block your card or account.":
        "Guna nombor di belakang kad atau dalam aplikasi rasmi. Minta mereka sekat kad atau akaun anda.",
    "Lodge a police report": "Buat laporan polis",
    "At any police station or online. Keep screenshots, phone numbers, account numbers and receipts.":
        "Di mana-mana balai polis atau dalam talian. Simpan tangkapan skrin, nombor telefon, nombor akaun dan resit.",
    "Check before you pay": "Semak sebelum bayar",
    "Check suspicious phone numbers and bank accounts on Semak Mule (the police's online checker) before transferring money.":
        "Semak nombor telefon dan akaun bank yang mencurigakan di Semak Mule (semakan dalam talian polis) sebelum memindahkan wang.",
    "Secure your accounts": "Lindungi akaun anda",
    "Change passwords, turn on two-step verification, and never share OTP/TAC codes.":
        "Tukar kata laluan, aktifkan pengesahan dua langkah, dan jangan sekali-kali kongsi kod OTP/TAC.",
    "Talk about it": "Ceritakan kepada orang lain",
    "Being scammed is not your fault. Telling family and friends helps protect them too.":
        "Ditipu bukan salah anda. Memberitahu keluarga dan rakan membantu melindungi mereka juga.",

    # ------------------------------------------------------------ sign-in / sidebar
    "Please sign in on the Home page first. It takes 10 seconds and only needs a nickname.":
        "Sila daftar masuk di halaman Utama dahulu. Hanya 10 saat dan perlukan nama samaran sahaja.",
    "Go to Home": "Pergi ke Utama",
    "Practise on fake scams so you never fall for a real one.": "Berlatih dengan scam palsu supaya anda tidak terpedaya dengan yang sebenar.",
    "{n} to {lvl}": "{n} lagi ke {lvl}",
    "Sign out": "Daftar keluar",
    "⚙️ Live AI scenarios": "⚙️ Senario AI langsung",
    "API key loaded from server.": "Kunci API dimuatkan dari pelayan.",
    "Anthropic API key (optional)": "Kunci API Anthropic (pilihan)",
    "Without a key the app uses its built-in scenario bank.": "Tanpa kunci, aplikasi guna bank senario terbina dalam.",
    "AI message language": "Bahasa mesej AI",

    # ------------------------------------------------------------ home
    "EDUTAINMENT · ANTI-SCAM": "EDUTAINMEN · ANTI-SCAM",
    "A flight simulator for scams. Practise on fake ones, including real-sounding voice calls, spot the red flags, and prove you've levelled up.":
        "Simulator penerbangan untuk scam. Berlatih dengan scam palsu, termasuk panggilan suara yang kedengaran sebenar, "
        "kesan tanda bahaya, dan buktikan anda semakin hebat.",
    "1 · 📏 Baseline test": "1 · 📏 Ujian garis dasar",
    "10 tricky messages, including a voice call. Scam or legit, and how sure are you? This measures where you start.":
        "10 mesej yang mengelirukan, termasuk satu panggilan suara. Scam atau sah, dan sejauh mana anda yakin? Ini mengukur tahap permulaan anda.",
    "2 · 🎮 Train, 🎭 Survive, 🗺️ Team up": "2 · 🎮 Berlatih, 🎭 Bertahan, 🗺️ Berpasukan",
    "Arena missions with voice calls, branching Story Missions, and live multiplayer Co-op Simulations on a town map.":
        "Misi Arena dengan panggilan suara, Misi Cerita bercabang, dan Simulasi Berpasukan secara langsung di atas peta bandar.",
    "3 · 🏁 Prove your growth": "3 · 🏁 Buktikan kemajuan anda",
    "A new 10-message test shows how much sharper you've become.": "Ujian baharu 10 mesej menunjukkan sejauh mana anda semakin peka.",
    "🗺️ You've been invited to Co-op room **{code}**. Enter a nickname below to join.":
        "🗺️ Anda dijemput ke bilik Berpasukan **{code}**. Masukkan nama samaran di bawah untuk sertai.",
    "Start playing": "Mula bermain",
    "Nickname": "Nama samaran",
    "Class / school code (optional)": "Kod kelas / sekolah (pilihan)",
    "Age group": "Kumpulan umur",
    "🔒 Privacy: don't use your real name. We only store your nickname, age group and code.":
        "🔒 Privasi: jangan guna nama sebenar. Kami hanya simpan nama samaran, kumpulan umur dan kod anda.",
    "Enter the Arena 🚀": "Masuk ke Arena 🚀",
    "Please type a nickname.": "Sila taip nama samaran.",
    "Welcome, {name}! 👋": "Selamat datang, {name}! 👋",
    "First step: take the 2-minute **Pre-Test** so we can measure your progress.":
        "Langkah pertama: ambil **Ujian Pra** 2 minit supaya kemajuan anda boleh diukur.",
    "Start Pre-Test →": "Mula Ujian Pra →",
    "Your baseline: **{a}/{b}**. Jump into the Arena to train.": "Garis dasar anda: **{a}/{b}**. Masuk ke Arena untuk berlatih.",
    "Enter Training Arena →": "Masuk Arena Latihan →",

    # ------------------------------------------------------------ tests
    "Pre-Test": "Ujian Pra", "Post-Test": "Ujian Pasca",
    "{label} complete: **{a}/{b}** ({pct}%)": "{label} selesai: **{a}/{b}** ({pct}%)",
    "{d} points": "{d} mata",
    "Training rounds": "Pusingan latihan",
    "### 📈 You improved by {d} points. That's real, measurable growth!":
        "### 📈 Anda meningkat {d} mata. Itu kemajuan sebenar yang boleh diukur!",
    "### Same score as before. Try a Hard mission and focus on your weakest tactic in My Progress.":
        "### Markah sama seperti sebelum ini. Cuba misi Sukar dan fokus pada taktik paling lemah anda dalam Kemajuan Saya.",
    "### Tricky set! Review the explanations below and play another mission.":
        "### Set yang mencabar! Semak penerangan di bawah dan main satu lagi misi.",
    "Review answers and explanations": "Semak jawapan dan penerangan",
    "SCAM 🚩": "SCAM 🚩", "LEGIT ✅": "SAH ✅",
    "it was": "jawapannya",
    "{n} messages, including a voice call 🎧. For each one decide **Scam** or **Legit**, and say how sure you are. No hints during the test.":
        "{n} mesej, termasuk satu panggilan suara 🎧. Bagi setiap satu, tentukan **Scam** atau **Sah**, dan nyatakan sejauh mana anda yakin. Tiada petunjuk semasa ujian.",
    "Question {i} of {n}": "Soalan {i} daripada {n}",
    "Is this a scam?": "Adakah ini scam?",
    "How sure are you?": "Sejauh mana anda yakin?",
    "😬 Guessing": "😬 Teka sahaja", "🙂 Fairly sure": "🙂 Agak yakin", "😎 Certain": "😎 Pasti",
    "🚩  Scam": "🚩  Scam", "✅  Legit": "✅  Sah",
    "Take the Pre-Test first so we can measure your improvement.": "Ambil Ujian Pra dahulu supaya peningkatan anda boleh diukur.",
    "Go to Pre-Test": "Pergi ke Ujian Pra",
    "Play at least one full mission ({n} rounds) first. You've played {t}.":
        "Main sekurang-kurangnya satu misi penuh ({n} pusingan) dahulu. Anda sudah main {t}.",
    "Go to Training Arena": "Pergi ke Arena Latihan",

    # ------------------------------------------------------------ arena
    "Tip: take the Pre-Test first so you can prove your improvement later.":
        "Tip: ambil Ujian Pra dahulu supaya anda boleh buktikan peningkatan anda kemudian.",
    "Each mission has **{n} messages**. Decide *Scam* or *Legit*, then tick the details that are real red flags. Careful: some details are **decoys**.":
        "Setiap misi ada **{n} mesej**. Tentukan *Scam* atau *Sah*, kemudian tanda butiran yang benar-benar tanda bahaya. Hati-hati: sesetengah butiran adalah **umpan**.",
    "🎲 Mixed (all levels)": "🎲 Campuran (semua tahap)", "🟢 Easy": "🟢 Mudah", "🟡 Medium": "🟡 Sederhana",
    "🟠 Hard": "🟠 Sukar", "🔴 Expert (complex + voice calls, ×1.5 XP)": "🔴 Pakar (kompleks + panggilan suara, ×1.5 XP)",
    "🎯 Smart: target my weak spots": "🎯 Pintar: sasarkan kelemahan saya",
    "Difficulty": "Tahap kesukaran",
    "Scenario source": "Sumber senario",
    "Scenario bank (offline)": "Bank senario (luar talian)", "Live AI scenarios": "Senario AI langsung",
    "Add an API key in the sidebar to unlock live AI scenarios.": "Tambah kunci API di bar sisi untuk membuka senario AI langsung.",
    "Start mission ▶": "Mula misi ▶",
    "**Scoring:** correct verdict +50 · each red flag spotted +10 · each false alarm −5 · perfect round +20 · *Calm Mind* (trusting a real message) +20 · Hard ×1.2 · Expert ×1.5":
        "**Pemarkahan:** keputusan betul +50 · setiap tanda bahaya dikesan +10 · setiap amaran palsu −5 · pusingan sempurna +20 · "
        "*Minda Tenang* (mempercayai mesej sebenar) +20 · Sukar ×1.2 · Pakar ×1.5",
    "🎧 Expert includes real-sounding voice calls in Malay, English and Mandarin. Turn your sound on.":
        "🎧 Tahap Pakar ada panggilan suara yang kedengaran sebenar dalam Bahasa Melayu, Inggeris dan Mandarin. Hidupkan bunyi anda.",
    "## 🏁 Mission complete! +{xp} XP": "## 🏁 Misi selesai! +{xp} XP",
    "Correct verdicts": "Keputusan betul", "Perfect rounds": "Pusingan sempurna", "Total XP": "Jumlah XP",
    "Play another mission": "Main misi lain", "Take the Post-Test →": "Ambil Ujian Pasca →", "See my progress →": "Lihat kemajuan saya →",
    "🤖 Generating a fresh scenario...": "🤖 Menjana senario baharu...",
    "AI unavailable ({err}). Using the scenario bank.": "AI tidak tersedia ({err}). Menggunakan bank senario.",
    "Round {i} of {n} · {diff}": "Pusingan {i} daripada {n} · {diff}",
    " · 🤖 AI-generated": " · 🤖 Dijana AI",
    "**1 · Your verdict**": "**1 · Keputusan anda**",
    "🚩 Scam": "🚩 Scam", "✅ Legit": "✅ Sah",
    "**2 · Tick every detail that is a real red flag** (it's OK to tick none)":
        "**2 · Tanda setiap butiran yang benar-benar tanda bahaya** (boleh juga tidak tanda apa-apa)",
    "Lock in answer 🔒": "Kunci jawapan 🔒",
    "Choose Scam or Legit first.": "Pilih Scam atau Sah dahulu.",
    "a SCAM 🚩": "SCAM 🚩",
    "Nice catch!": "Tangkapan hebat!", "Well judged!": "Penilaian tepat!", "Not quite.": "Belum tepat.",
    "This message is {truth}": "Mesej ini adalah {truth}",
    "Tactic:": "Taktik:",
    "🎉 LEVEL UP! You are now a **{lvl}**!": "🎉 NAIK TAHAP! Anda kini **{lvl}**!",
    "✅ Red flag, you spotted it": "✅ Tanda bahaya, anda berjaya kesan",
    "⚠️ Red flag you missed": "⚠️ Tanda bahaya yang anda terlepas",
    "❌ False alarm, not a red flag": "❌ Amaran palsu, bukan tanda bahaya",
    "👍 Not a red flag, correctly left unticked": "👍 Bukan tanda bahaya, betul tidak ditanda",
    "XP breakdown": "Pecahan XP",
    "No points this round": "Tiada mata pusingan ini",
    "Correct verdict": "Keputusan betul",
    "{n} red flag(s) spotted": "{n} tanda bahaya dikesan",
    "{n} false alarm(s)": "{n} amaran palsu",
    "Perfect round bonus": "Bonus pusingan sempurna",
    "Calm Mind bonus": "Bonus Minda Tenang",
    "{diff} difficulty bonus ×{mult}": "Bonus tahap {diff} ×{mult}",
    "Finish mission 🏁": "Tamatkan misi 🏁", "Next message →": "Mesej seterusnya →", "Quit mission": "Keluar misi",

    # ------------------------------------------------------------ stories
    "🛡️ Escaped": "🛡️ Terselamat", "😮‍💨 Close call": "😮‍💨 Nyaris", "💸 Scammed": "💸 Ditipu",
    "Not played yet": "Belum dimainkan",
    "Your best:": "Terbaik anda:",
    "Real scams aren't one message. They're **conversations that escalate**: hand-offs, threats, fake proof, small wins that build trust. In Story Missions every decision changes what happens next, and **there's no feedback until the end**, just like real life. Turn your sound on 🎧.":
        "Scam sebenar bukan satu mesej sahaja. Ia **perbualan yang semakin memuncak**: diserahkan dari seorang ke seorang, ugutan, "
        "bukti palsu, kemenangan kecil untuk membina kepercayaan. Dalam Misi Cerita, setiap keputusan mengubah apa yang berlaku seterusnya, "
        "dan **tiada maklum balas sehingga tamat**, sama seperti kehidupan sebenar. Hidupkan bunyi anda 🎧.",
    "▶ Play: {title}": "▶ Main: {title}",
    "Money lost:": "Wang hilang:",
    "🔍 Debrief: your decisions": "🔍 Rumusan: keputusan anda",
    "Step {k}": "Langkah {k}",
    "You chose:": "Anda pilih:",
    "💡 Best move here:": "💡 Langkah terbaik di sini:",
    "🔁 Replay this mission": "🔁 Main semula misi ini",
    "← All Story Missions": "← Semua Misi Cerita",
    "Step {k} · 💰 Your money at stake: RM{save} · Sent to strangers so far: <b>RM{sent}</b>":
        "Langkah {k} · 💰 Wang anda yang dipertaruhkan: RM{save} · Sudah dihantar kepada orang asing: <b>RM{sent}</b>",
    "#### What do you do?": "#### Apa yang anda buat?",
    "No hints. Decide like you would in real life.": "Tiada petunjuk. Buat keputusan seperti dalam kehidupan sebenar.",
    "Leave mission": "Tinggalkan misi",

    # ------------------------------------------------------------ co-op: map
    "Taman Melur": "Taman Melur", "Harmoni Heights": "Harmoni Heights", "Town Centre": "Pusat Bandar",
    "Commercial": "Komersial", "Industrial": "Perindustrian", "Taman Hijau": "Taman Hijau",
    "Taman Melur (houses)": "Taman Melur (rumah)", "Guardhouse": "Pondok pengawal", "Danish's house": "Rumah Danish",
    "Hospital Harmoni": "Hospital Harmoni", "Kolej Harmoni": "Kolej Harmoni", "Kafe Senja": "Kafe Senja",
    "Balai Polis Bandar Harmoni": "Balai Polis Bandar Harmoni", "Bank Harmoni branch": "Bank Harmoni",
    "LRT Harmoni Sentral": "LRT Harmoni Sentral", "Segar Foods office": "Pejabat Segar Foods",
    "Hotel Seri Kota": "Hotel Seri Kota", "Harmoni Mall": "Harmoni Mall",
    "Mall back parking lot": "Tempat letak kereta belakang mall", "Old warehouse zone": "Kawasan gudang lama",
    "KilatPos hub": "Hab KilatPos", "Airport highway": "Lebuh raya lapangan terbang", "NSRC 997 hotline": "Talian NSRC 997",
    "📱 TARGET": "📱 SASARAN", "🛡️ GUARDIAN": "🛡️ PELINDUNG", "🎭 SOLO (both roles)": "🎭 SOLO (dua peranan)",

    # ------------------------------------------------------------ co-op: lobby
    "Nothing yet...": "Belum ada apa-apa...",
    "Play **together** on the same room code. One player is the **📱 Target**, who gets the scam call, chat or visitor and feels the pressure. The others are **🛡️ Guardians** beside them, who investigate on the town map. You only win if the Target makes the safe move **and** a Guardian confirms or reports it before time runs out.":
        "Main **bersama** menggunakan kod bilik yang sama. Seorang pemain menjadi **📱 Sasaran**, yang menerima panggilan, mesej atau "
        "pelawat scam dan merasai tekanan. Yang lain menjadi **🛡️ Pelindung** di sebelahnya, yang menyiasat di peta bandar. "
        "Anda hanya menang jika Sasaran membuat langkah selamat **dan** Pelindung mengesahkan atau melaporkannya sebelum masa tamat.",
    "1 · Create or join": "1 · Cipta atau sertai",
    "One player creates a room and shares the 5-letter code or link. Friends join from their own phones.":
        "Seorang pemain mencipta bilik dan berkongsi kod 5 huruf atau pautan. Rakan sertai dari telefon masing-masing.",
    "2 · Talk and investigate": "2 · Berbincang dan siasat",
    "Only the Target hears the scammer, unless they switch to speaker. Only Guardians can investigate. You need each other.":
        "Hanya Sasaran yang mendengar penipu, kecuali jika pembesar suara dihidupkan. Hanya Pelindung boleh menyiasat. Anda saling memerlukan.",
    "3 · Beat the clock": "3 · Kalahkan masa",
    "The scammer escalates every few seconds. Time out = the scammer wins.":
        "Penipu semakin mendesak setiap beberapa saat. Masa tamat = penipu menang.",
    "Create a room": "Cipta bilik", "Mission": "Misi", "Create room ➕": "Cipta bilik ➕",
    "Join a room": "Sertai bilik", "Room code": "Kod bilik", "Join ▶": "Sertai ▶",
    "Playing alone? Create a room and start it. You'll play both roles (solo practice).":
        "Main seorang? Cipta bilik dan mulakan. Anda akan main kedua-dua peranan (latihan solo).",
    "📶 How do my friends join from their phones?": "📶 Bagaimana rakan saya sertai dari telefon mereka?",
    "- **Same Wi-Fi:** open the app using the **Network URL** shown in the black window (e.g. `http://192.168.1.20:8501`), not `localhost`. Then share the room link.\n- **Anywhere:** deploy the app online (see README) and share the link.\n- Everyone must connect to the **same running app**.":
        "- **Wi-Fi yang sama:** buka aplikasi menggunakan **Network URL** yang dipaparkan dalam tetingkap hitam "
        "(cth. `http://192.168.1.20:8501`), bukan `localhost`. Kemudian kongsi pautan bilik.\n"
        "- **Di mana-mana:** letakkan aplikasi dalam talian (lihat README) dan kongsi pautan.\n"
        "- Semua orang mesti bersambung ke **aplikasi yang sama sedang berjalan**.",
    "This game started without you. Wait for the host to return to the lobby.":
        "Permainan ini sudah bermula tanpa anda. Tunggu hos kembali ke lobi.",
    "Leave room": "Tinggalkan bilik",
    "Share this link (or just the code):": "Kongsi pautan ini (atau kod sahaja):",
    "**Players in the room**": "**Pemain dalam bilik**",
    "Timer:": "Masa:",
    "Change mission": "Tukar misi",
    "📱 Who gets the scam (the Target)?": "📱 Siapa yang menerima scam (Sasaran)?",
    "Everyone else becomes a 🛡️ Guardian.": "Semua yang lain menjadi 🛡️ Pelindung.",
    "▶ Start mission": "▶ Mula misi",
    "Waiting for friends... or start now to play **both roles** (solo practice).":
        "Menunggu rakan... atau mula sekarang untuk main **kedua-dua peranan** (latihan solo).",
    "▶ Start solo practice": "▶ Mula latihan solo",
    "⏳ Waiting for the host 👑 to start the mission...": "⏳ Menunggu hos 👑 memulakan misi...",
    "No room with that code.": "Tiada bilik dengan kod itu.",
    "That game has already started. Ask the host to return to the lobby.":
        "Permainan itu sudah bermula. Minta hos kembali ke lobi.",

    # ------------------------------------------------------------ co-op: game
    "Room": "Bilik", "💰 At stake: RM{amt}": "💰 Dipertaruhkan: RM{amt}",
    "🚨 {name} is walking to the {place} ALONE: arriving in {secs}s! Stop them!":
        "🚨 {name} sedang berjalan ke {place} SEORANG DIRI: tiba dalam {secs}s! Halang dia!",
    "📱 Target phone": "📱 Telefon Sasaran", "🛡️ Guardian tools": "🛡️ Alat Pelindung",
    "**📨 Live feed**": "**📨 Suapan langsung**",
    "**Your moves**": "**Langkah anda**",
    "🔊 The call (on speaker)": "🔊 Panggilan (pembesar suara)", "🔊 The call": "🔊 Panggilan",
    "🔇 You can't hear {name}'s call. Ask {name} to put it on speaker.":
        "🔇 Anda tidak dapat dengar panggilan {name}. Minta {name} hidupkan pembesar suara.",
    "**🔍 Investigate**": "**🔍 Siasat**",
    "**📓 Notebook & feed**": "**📓 Buku nota & suapan**",
    "🗺️ Map of Bandar Harmoni": "🗺️ Peta Bandar Harmoni",
    "**📻 Team radio**": "**📻 Radio pasukan**",
    "🚨 HANG UP / STOP!": "🚨 LETAK TELEFON / BERHENTI!", "⏳ Stall them!": "⏳ Lengahkan mereka!",
    "🔊 Put it on speaker!": "🔊 Buka pembesar suara!", "❓ What are they asking?": "❓ Apa yang mereka minta?",
    "✅ Confirmed: it's a SCAM": "✅ Disahkan: ini SCAM", "👍 OK": "👍 OK",
    "Type a message to your team...": "Taip mesej kepada pasukan anda...",
    "Message": "Mesej", "Send": "Hantar",
    "Only the Target can do that.": "Hanya Sasaran boleh buat begitu.",
    "Only the Guardian can do that.": "Hanya Pelindung boleh buat begitu.",
    "Already done.": "Sudah dibuat.",
    "The game is not running.": "Permainan tidak sedang berjalan.",
    "You're not going anywhere right now.": "Anda tidak sedang pergi ke mana-mana.",

    # ------------------------------------------------------------ co-op: end
    "Team score:": "Markah pasukan:", "Time used:": "Masa digunakan:",
    "+{xp} XP for you!": "+{xp} XP untuk anda!",
    "**🏆 Winning combination:**": "**🏆 Gabungan kemenangan:**", "OR": "ATAU", "AND": "DAN",
    "**🎞️ Full replay (everyone's view)**": "**🎞️ Ulang tayang penuh (pandangan semua)**",
    "🔁 Back to lobby (next mission)": "🔁 Kembali ke lobi (misi seterusnya)",
    "The host 👑 can take everyone back to the lobby.": "Hos 👑 boleh membawa semua kembali ke lobi.",

    # ------------------------------------------------------------ progress
    "Level": "Tahap", "Arena accuracy": "Ketepatan Arena", "{n} XP to {lvl}": "{n} XP lagi ke {lvl}",
    "Badges": "Lencana", "Pre vs Post test": "Ujian Pra lwn Pasca", "Score (%)": "Markah (%)", "not yet": "belum",
    "Take the Pre-Test to see this chart.": "Ambil Ujian Pra untuk melihat carta ini.",
    "Accuracy by scam tactic": "Ketepatan mengikut taktik scam", "Accuracy (%)": "Ketepatan (%)",
    "🎯 Focus area: **{t}** ({p}% correct)": "🎯 Fokus: **{t}** ({p}% betul)",
    "Play a mission to see your strengths and weak spots.": "Main satu misi untuk melihat kekuatan dan kelemahan anda.",
    "First try": "Cubaan pertama", "Best": "Terbaik", "Plays": "Kali main",
    "🗺️ Co-op Simulations: **{n}** played · **{w}** won · best team score **{b}**":
        "🗺️ Simulasi Berpasukan: **{n}** dimainkan · **{w}** menang · markah pasukan terbaik **{b}**",
    "🎯 Confidence check": "🎯 Semakan keyakinan",
    "When you were 😎 Certain, you were right": "Apabila anda 😎 Pasti, anda betul",
    "{n} 'Certain' answers": "{n} jawapan 'Pasti'",
    "⚠️ {n} answer(s) were wrong while you felt certain. Overconfidence is exactly what scammers exploit. Slow down on those tactics.":
        "⚠️ {n} jawapan salah walaupun anda rasa pasti. Terlalu yakin ialah perkara yang dieksploitasi penipu. Perlahan-lahan pada taktik itu.",
    "No overconfident mistakes. Your confidence matches your skill.": "Tiada kesilapan kerana terlalu yakin. Keyakinan anda sepadan dengan kemahiran anda.",
    "Confidence": "Keyakinan", "Accuracy": "Ketepatan", "Answers": "Jawapan",
    "Take a test to see how well your confidence matches your accuracy.":
        "Ambil ujian untuk melihat sejauh mana keyakinan anda sepadan dengan ketepatan anda.",

    # ------------------------------------------------------------ teacher
    "Teacher PIN": "PIN Guru",
    "Set the TEACHER_PIN environment variable before a real pilot (default 1234).":
        "Tetapkan pemboleh ubah persekitaran TEACHER_PIN sebelum rintis sebenar (lalai 1234).",
    "Wrong PIN.": "PIN salah.",
    "No data yet. Ask students to sign in with the same class/school code and play.":
        "Belum ada data. Minta pelajar daftar masuk dengan kod kelas/sekolah yang sama dan bermain.",
    "Class / school code": "Kod kelas / sekolah", "All": "Semua", "(no code)": "(tiada kod)",
    "Players": "Pemain", "Mean pre-test": "Purata ujian pra", "Mean post-test": "Purata ujian pasca",
    "Mean gain (paired)": "Purata peningkatan (berpasangan)", "{g} pts": "{g} mata",
    "{n} players with both tests": "{n} pemain dengan kedua-dua ujian",
    "📈 {p}% of the {n} players who finished both tests improved.": "📈 {p}% daripada {n} pemain yang menamatkan kedua-dua ujian meningkat.",
    "Pre vs post by player": "Pra lwn pasca mengikut pemain", "Pre": "Pra", "Post": "Pasca",
    "Shows once players finish both tests.": "Dipaparkan apabila pemain menamatkan kedua-dua ujian.",
    "Cohort accuracy by tactic": "Ketepatan kohort mengikut taktik",
    "Missed scams: **{a}%** of scam rounds · False alarms on legit messages: **{b}%** of legit rounds":
        "Scam terlepas: **{a}%** daripada pusingan scam · Amaran palsu pada mesej sah: **{b}%** daripada pusingan sah",
    "No training rounds yet.": "Belum ada pusingan latihan.",
    "Deeper insights": "Analisis mendalam",
    "**🎭 Story Missions: first attempt per player**": "**🎭 Misi Cerita: cubaan pertama setiap pemain**",
    "First-try escape rate: **{p}%** · Simulated money lost on first tries: **RM{amt}**":
        "Kadar terselamat cubaan pertama: **{p}%** · Wang simulasi yang hilang pada cubaan pertama: **RM{amt}**",
    "No Story Missions played yet.": "Belum ada Misi Cerita dimainkan.",
    "**🎯 Calibration: accuracy by confidence (tests)**": "**🎯 Kalibrasi: ketepatan mengikut keyakinan (ujian)**",
    "Overconfident misses (wrong while 'Certain'): ": "Kesilapan terlalu yakin (salah ketika 'Pasti'): ",
    "Shows once players complete a test.": "Dipaparkan apabila pemain menamatkan ujian.",
    "🎧 Voice/video rounds accuracy: **{a}%** vs text rounds: **{b}%**":
        "🎧 Ketepatan pusingan suara/video: **{a}%** lwn pusingan teks: **{b}%**",
    "**🗺️ Co-op Simulations: team win rate per mission** (one row per player per game)":
        "**🗺️ Simulasi Berpasukan: kadar kemenangan pasukan setiap misi** (satu baris setiap pemain setiap permainan)",
    "Win rate": "Kadar menang", "Player-games": "Permainan pemain",
    "Raw data": "Data mentah",
    "⬇️ Download all attempts (CSV)": "⬇️ Muat turun semua cubaan (CSV)",
    "⬇️ Download story decisions (CSV)": "⬇️ Muat turun keputusan cerita (CSV)",
    "players": "pemain", "ending": "pengakhiran",

    # ------------------------------------------------------------ help page
    "**Been scammed or just transferred money?** Act fast: call the National Scam Response Centre **(NSRC) at 997** right away, then call your bank.":
        "**Ditipu atau baru memindahkan wang?** Bertindak pantas: hubungi Pusat Respons Scam Kebangsaan **(NSRC) di 997** segera, kemudian hubungi bank anda.",
    "About this app": "Tentang aplikasi ini",
    "{app} is an educational simulation. **Every organisation, person, phone number and website in the game is fictional.** The app never sends real messages and never asks for your real personal or banking information. We store only your nickname, age group and class code. All voices are synthetic (computer-generated); no real person's voice was cloned.":
        "{app} ialah simulasi pendidikan. **Setiap organisasi, individu, nombor telefon dan laman web dalam permainan ini adalah rekaan.** "
        "Aplikasi ini tidak pernah menghantar mesej sebenar dan tidak pernah meminta maklumat peribadi atau perbankan sebenar anda. "
        "Kami hanya menyimpan nama samaran, kumpulan umur dan kod kelas anda. Semua suara adalah sintetik (dijana komputer); "
        "tiada suara orang sebenar yang diklon.",
    "🌐 Scenario messages stay in their original language (a realistic mix of Malay and English, like real scams).":
        "🌐 Mesej senario kekal dalam bahasa asal (campuran Bahasa Melayu dan Inggeris yang realistik, seperti scam sebenar).",
    # ------------------------------------------------------------ pilot study (v5)
    "🔁 Retention Test": "🔁 Ujian Pengekalan", "Retention Test": "Ujian Pengekalan",
    "### Thank you! This shows how much of your skill lasted over two weeks.":
        "### Terima kasih! Ini menunjukkan berapa banyak kemahiran anda kekal selepas dua minggu.",
    "Finish the Post-Test first. The retention test comes about two weeks later.":
        "Selesaikan Ujian Pasca dahulu. Ujian pengekalan diadakan kira-kira dua minggu kemudian.",
    "The retention test isn't open yet. Your teacher will open it about two weeks after the post-test.":
        "Ujian pengekalan belum dibuka. Guru anda akan membukanya kira-kira dua minggu selepas ujian pasca.",
    "Your group takes the tests only for now. You'll get full access to the game when the study ends. Thank you for helping!":
        "Kumpulan anda hanya mengambil ujian buat masa ini. Anda akan mendapat akses penuh kepada permainan apabila kajian tamat. Terima kasih kerana membantu!",
    "Research consent: I have read the information sheet, I am 18 or older, and I agree that my anonymous answers can be used for research. (Only needed if your class is part of a study.)":
        "Persetujuan kajian: Saya telah membaca lembaran maklumat, saya berumur 18 tahun ke atas, dan saya bersetuju jawapan tanpa nama saya digunakan untuk kajian. (Hanya perlu jika kelas anda menyertai kajian.)",
    "Your class is part of a research study. Please read the information sheet and tick the consent box to continue.":
        "Kelas anda menyertai satu kajian. Sila baca lembaran maklumat dan tanda kotak persetujuan untuk teruskan.",
    "📝 Quick survey (2 minutes)": "📝 Tinjauan ringkas (2 minit)",
    "1 = strongly disagree, 5 = strongly agree. Your honest opinion helps us improve KEBAL.":
        "1 = sangat tidak setuju, 5 = sangat setuju. Pendapat jujur anda membantu kami menambah baik KEBAL.",
    "I think that I would like to use KEBAL frequently.": "Saya rasa saya ingin menggunakan KEBAL dengan kerap.",
    "I found KEBAL unnecessarily complex.": "Saya dapati KEBAL terlalu rumit tanpa sebab.",
    "I thought KEBAL was easy to use.": "Saya rasa KEBAL mudah digunakan.",
    "I think that I would need the support of a technical person to be able to use KEBAL.":
        "Saya rasa saya memerlukan bantuan orang teknikal untuk menggunakan KEBAL.",
    "I found the various functions in KEBAL were well integrated.": "Saya dapati pelbagai fungsi dalam KEBAL disepadukan dengan baik.",
    "I thought there was too much inconsistency in KEBAL.": "Saya rasa terdapat terlalu banyak ketidakselarasan dalam KEBAL.",
    "I would imagine that most people would learn to use KEBAL very quickly.":
        "Saya bayangkan kebanyakan orang akan belajar menggunakan KEBAL dengan sangat cepat.",
    "I found KEBAL very cumbersome to use.": "Saya dapati KEBAL sangat menyusahkan untuk digunakan.",
    "I felt very confident using KEBAL.": "Saya berasa sangat yakin menggunakan KEBAL.",
    "I needed to learn a lot of things before I could get going with KEBAL.":
        "Saya perlu belajar banyak perkara sebelum boleh mula menggunakan KEBAL.",
    "Which parts helped you most?": "Bahagian mana yang paling membantu anda?",
    "Training Arena": "Arena Latihan", "Story Missions": "Misi Cerita", "Co-op Simulation": "Simulasi Berpasukan",
    "Voice calls": "Panggilan suara", "Red-flag explanations": "Penerangan tanda bahaya",
    "How likely are you to recommend KEBAL to your family? (0 = not at all, 10 = definitely)":
        "Sejauh mana anda akan mencadangkan KEBAL kepada keluarga anda? (0 = langsung tidak, 10 = pasti)",
    "Anything else you want to tell us? (optional)": "Ada apa-apa lagi yang ingin anda kongsikan? (pilihan)",
    "Submit survey": "Hantar tinjauan", "Please answer all 10 statements.": "Sila jawab kesemua 10 kenyataan.",
    "Thank you! Survey saved.": "Terima kasih! Tinjauan disimpan.",
    "You are using the default PIN 1234. Set TEACHER_PIN before a real pilot.":
        "Anda menggunakan PIN lalai 1234. Tetapkan TEACHER_PIN sebelum rintis sebenar.",
    "🧪 Pilot setup: groups, consent and retention test": "🧪 Tetapan rintis: kumpulan, persetujuan dan ujian pengekalan",
    "Set each class code as the KEBAL group (plays the game) or the Control group (tests only).":
        "Tetapkan setiap kod kelas sebagai kumpulan KEBAL (bermain permainan) atau kumpulan Kawalan (ujian sahaja).",
    "Add a class code": "Tambah kod kelas", "Type a class code above to configure it.": "Taip kod kelas di atas untuk menetapkannya.",
    "Group": "Kumpulan", "KEBAL group": "Kumpulan KEBAL", "Control group": "Kumpulan Kawalan",
    "Ask for research consent": "Minta persetujuan kajian", "Retention test open": "Ujian pengekalan dibuka",
    "Saved {code}": "{code} disimpan",
    "📈 Pilot results: KEBAL group vs control group": "📈 Keputusan rintis: kumpulan KEBAL lwn kumpulan kawalan",
    "Results appear once students in configured classes finish both the pre-test and the post-test.":
        "Keputusan dipaparkan apabila pelajar dalam kelas yang ditetapkan menamatkan ujian pra dan ujian pasca.",
    "Students with pre + post": "Pelajar dengan ujian pra + pasca", "Pre-test mean": "Purata ujian pra",
    "Post-test mean": "Purata ujian pasca", "Mean gain (points)": "Purata peningkatan (mata)",
    "Retention test mean (n)": "Purata ujian pengekalan (n)", "Overconfident errors, pre → post": "Kesilapan terlalu yakin, pra → pasca",
    "SUS usability score (n)": "Skor kebolehgunaan SUS (n)", "Extra gain with KEBAL": "Peningkatan tambahan dengan KEBAL",
    "Effect size (Cohen's d)": "Saiz kesan (Cohen's d)", "p-value (permutation test)": "Nilai p (ujian permutasi)",
    "Effect size is {size}. A p-value below 0.05 means the difference is unlikely to be chance.":
        "Saiz kesan adalah {size}. Nilai p di bawah 0.05 bermaksud perbezaan itu tidak mungkin berlaku secara kebetulan.",
    "large": "besar", "medium": "sederhana", "small": "kecil", "negligible": "sangat kecil",
    "💾 Backup & restore": "💾 Sandaran & pemulihan",
    "Free hosting can wipe the app's data when it restarts. Download a backup after every session.":
        "Pengehosan percuma boleh memadam data aplikasi apabila ia dimulakan semula. Muat turun sandaran selepas setiap sesi.",
    "⬇️ Download full database backup (.db)": "⬇️ Muat turun sandaran pangkalan data penuh (.db)",
    "⬇️ Download survey answers (CSV)": "⬇️ Muat turun jawapan tinjauan (CSV)",
    "Restore from a backup file": "Pulihkan daripada fail sandaran",
    "⚠️ Replace ALL current data with this backup": "⚠️ Ganti SEMUA data semasa dengan sandaran ini",
    "That file is not a KEBAL database backup.": "Fail itu bukan sandaran pangkalan data KEBAL.",
    "That file is damaged or not a database.": "Fail itu rosak atau bukan pangkalan data.",
    "That database is missing KEBAL tables.": "Pangkalan data itu tiada jadual KEBAL.",
    "Backup restored.": "Sandaran dipulihkan.",
}
