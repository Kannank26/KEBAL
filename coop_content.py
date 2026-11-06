"""
coop_content.py - Co-op Simulation missions (2+ players, same room code).

Roles
  📱 TARGET   - receives the scam (call / chat / visitor). Has the phone, feels the pressure.
  🛡️ GUARDIAN - is right beside the Target. Can't hear the call unless it's on speaker.
                 Investigates using the town map and their own phone.
A mission is WON only when the team completes one action from EVERY group in "win"
(usually: the Target makes the safe move AND the Guardian confirms/reports it).

All places are in the fictional town of BANDAR HARMONI. All names are fictional.
"""

# ------------------------------------------------------------------ town map
# x, y on a 0-100 grid
POIS = {
    "home":       {"name": "Taman Melur (houses)",      "icon": "🏠", "x": 14, "y": 78},
    "guardhouse": {"name": "Guardhouse",               "icon": "💂", "x": 6,  "y": 90},
    "danish":     {"name": "Danish's house",           "icon": "🏡", "x": 22, "y": 52},
    "hospital":   {"name": "Hospital Harmoni",         "icon": "🏥", "x": 12, "y": 30},
    "college":    {"name": "Kolej Harmoni",            "icon": "🎓", "x": 36, "y": 66},
    "cafe":       {"name": "Kafe Senja",               "icon": "☕", "x": 42, "y": 61},
    "police":     {"name": "Balai Polis Bandar Harmoni", "icon": "🚓", "x": 58, "y": 84},
    "bank":       {"name": "Bank Harmoni branch",      "icon": "🏦", "x": 58, "y": 56},
    "lrt":        {"name": "LRT Harmoni Sentral",      "icon": "🚉", "x": 50, "y": 44},
    "office":     {"name": "Segar Foods office",       "icon": "🏢", "x": 40, "y": 86},
    "hotel":      {"name": "Hotel Seri Kota",          "icon": "🏨", "x": 70, "y": 72},
    "mall":       {"name": "Harmoni Mall",             "icon": "🛍️", "x": 74, "y": 52},
    "backlot":    {"name": "Mall back parking lot",    "icon": "🅿️", "x": 86, "y": 40},
    "warehouse":  {"name": "Old warehouse zone",       "icon": "🏚️", "x": 90, "y": 18},
    "kilatpos":   {"name": "KilatPos hub",             "icon": "📦", "x": 64, "y": 24},
    "airport":    {"name": "Airport highway",          "icon": "✈️", "x": 96, "y": 92},
    "nsrc":       {"name": "NSRC 997 hotline",         "icon": "☎️", "x": 30, "y": 12},
}

DISTRICTS = [  # (x0, y0, x1, y1, colour, label)
    (0, 62, 30, 100, "rgba(134,239,172,0.28)", "Taman Melur"),
    (0, 20, 30, 62, "rgba(186,230,253,0.35)", "Harmoni Heights"),
    (30, 40, 66, 100, "rgba(226,232,240,0.55)", "Town Centre"),
    (66, 30, 100, 80, "rgba(254,215,170,0.35)", "Commercial"),
    (66, 0, 100, 30, "rgba(214,211,209,0.55)", "Industrial"),
    (30, 0, 66, 40, "rgba(220,252,231,0.35)", "Taman Hijau"),
]
ROADS = [  # polylines
    [(0, 70), (100, 70)], [(0, 46), (100, 46)], [(30, 0), (30, 100)], [(64, 0), (64, 100)],
    [(80, 46), (80, 0)], [(64, 70), (100, 96)], [(30, 22), (64, 22)],
]
RIVER = [(0, 8), (15, 14), (30, 6), (48, 14), (66, 6), (82, 12), (100, 4)]

ROLE_LABEL = {"target": "📱 TARGET", "guardian": "🛡️ GUARDIAN", "both": "🎭 SOLO (both roles)"}

# ------------------------------------------------------------------ missions
# action kinds: fatal | win | stall | bad | info | share | doom | cancel_doom | bonus | clue
# text placeholders: {T} = target's nickname, {G} = guardian's nickname
COOP_MISSIONS = [
    {
        "id": "C1", "icon": "🚓", "title": "The Call Beside You", "tactic": "Impersonating authority",
        "summary": "A 'police inspector' calls the Target. The Guardian must expose him before the savings are gone.",
        "duration": 120, "stake": 9500, "pois": ["cafe", "police", "bank", "home", "nsrc"],
        "pos": {"target": "cafe", "guardian": "cafe"},
        "brief": "Kafe Senja, 3:40pm. {T} and {G} are having teh tarik after class. {T}'s phone rings.",
        "brief_target": "A man says he's a police inspector. He's fast and scary. You have RM9,500 in savings. "
                        "Listen and decide. {G} is right beside you.",
        "brief_guardian": "You're beside {T}. You can't hear the caller unless {T} turns on the speaker. "
                          "Investigate fast with the map and your phone.",
        "incoming": {"channel": "Phone call", "sender": "'Inspector Razak' +603-2716 8840", "context": "",
                     "audio": "s1_n2_inspector.mp3"},
        "pressure": [
            (15, "📞 'Are you alone? Walk away from your friend. Nobody must hear this call.'"),
            (35, "📞 'Transfer RM9,500 to the safe account 1029 4471 88 NOW or your account is frozen.'"),
            (60, "📞 'I'm sending the arrest warrant. Officers are on the way to your house in Taman Melur.'"),
            (85, "📞 'Last chance. If you hang up, you'll be arrested tonight.'"),
            (105, "📞 'Open your banking app. Do it NOW!'"),
        ],
        "target_actions": [
            {"id": "t_speaker", "label": "🔊 Put the call on speaker for {G}", "kind": "share",
             "text": "{T} put the call on speaker. {G} can now hear everything."},
            {"id": "t_stall", "label": "⏳ 'Let me find a quiet place, give me 2 minutes'", "kind": "stall", "seconds": 20,
             "text": "{T} stalled for time (+20s). The caller sounds annoyed."},
            {"id": "t_walk", "label": "🚶 Walk away from {G}, like the caller says", "kind": "bad", "speaker_off": True,
             "text": "{T} walked away. {G} can't hear anything now. Isolation is the scammer's goal."},
            {"id": "t_ic", "label": "🪪 Send a photo of your IC to 'verify' yourself", "kind": "bad",
             "text": "{T} sent an IC photo. It can be used to open mule accounts or loans."},
            {"id": "t_transfer", "label": "💸 Transfer RM9,500 to the 'safe account'", "kind": "fatal", "ending": "lost"},
            {"id": "t_hangup", "label": "📵 Hang up", "kind": "win",
             "text": "{T} hung up! But they keep calling back... {G}, confirm it's a scam!"},
        ],
        "guardian_tools": [
            {"id": "g_number", "label": "🔎 Search the caller's number online", "delay": 8, "kind": "clue",
             "clue": "6 people reported +603-2716 8840 as a fake 'police' caller this month."},
            {"id": "g_station", "label": "Call the station's official number (from its website)", "poi": "police", "delay": 15,
             "kind": "clue", "clue": "Duty officer: 'No Inspector Razak here. Police NEVER ask anyone to transfer money. It's a scam!'"},
            {"id": "g_semak", "label": "Check the 'safe account' on Semak Mule", "poi": "bank", "delay": 10, "kind": "clue",
             "requires": "speaker", "missing": "You don't know the account number. Ask {T} to put the call on speaker!",
             "clue": "Account 1029 4471 88 appears in 23 police reports. It's a mule account."},
            {"id": "g_photo", "label": "🖼️ Look at the 'warrant' photo on {T}'s WhatsApp", "delay": 6, "kind": "clue",
             "clue": "It has a police crest and looks official... but a picture proves nothing. Anyone can make one."},
            {"id": "g_report", "label": "Call NSRC 997 and report", "poi": "nsrc", "delay": 12, "kind": "clue",
             "clue": "NSRC: 'Classic Macau scam. Tell your friend to hang up. We've logged the number and account.'"},
        ],
        "win": [["t_hangup"], ["g_station", "g_report"]],
        "timeout": "lost",
        "endings": {
            "win": {"title": "🛡️ Scam stopped together!", "text": "{T} hung up and {G} confirmed it with an official source. RM9,500 saved."},
            "lost": {"title": "💸 RM9,500 gone", "text": "Under pressure, {T} opened the banking app and transferred everything to a mule account."},
        },
        "debrief": "Macau scams isolate the victim ('walk away from your friend'), add fear (warrant, frozen account) and a deadline. "
                   "The antidote is exactly what you practised: **stay together, put it on speaker, verify with an official number, report to NSRC 997.**",
    },
    {
        "id": "C2", "icon": "🎙️", "title": "Kak, It's Me (Co-op)", "tactic": "Voice / video deepfake",
        "summary": "A cloned voice of the Target's little brother begs for bail money. The Guardian must find the real Amir.",
        "duration": 100, "stake": 3000, "pois": ["home", "danish", "police", "hospital"],
        "pos": {"target": "home", "guardian": "home"},
        "brief": "9pm at home in Taman Melur. {T} and cousin {G} are watching TV. {T}'s little brother Amir is out. An unknown number calls {T}.",
        "brief_target": "The voice sounds EXACTLY like your brother Amir. He's crying and needs RM3,000 now.",
        "brief_guardian": "You're on the sofa beside {T}. Find out where the real Amir is, fast.",
        "incoming": {"channel": "Phone call", "sender": "Unknown number", "context": "The voice sounds exactly like Amir.",
                     "audio": "s2_n1_amir.mp3"},
        "pressure": [
            (15, "📞 'Kak please, the police are shouting at me!'"),
            (35, "📞 A man takes the phone: 'Sergeant Kamal here. 30 minutes or he goes to lockup.'"),
            (55, "💬 SMS: 'Acc 7721 0093 15 (TAN K.L.) RM3000 cepat!!'"),
            (80, "📞 'Kak, why aren't you doing anything?! Please!'"),
        ],
        "target_actions": [
            {"id": "t_speaker", "label": "🔊 Put the call on speaker for {G}", "kind": "share",
             "text": "{T} put the call on speaker."},
            {"id": "t_question", "label": "❓ Ask: 'What's our cat's name?'", "kind": "info",
             "reply": "He hesitates... 'Kak, this is NOT the time! Just send the money!' (A real Amir would answer.)"},
            {"id": "t_code", "label": "🔐 Ask for the family code word", "kind": "info",
             "reply": "Silence. Then: 'What code word? Kak please!'"},
            {"id": "t_transfer", "label": "💸 Transfer RM3,000 now", "kind": "fatal", "ending": "lost"},
            {"id": "t_hangup", "label": "📵 Hang up", "kind": "win",
             "text": "{T} hung up! The number keeps calling back... {G}, is Amir really safe?"},
        ],
        "guardian_tools": [
            {"id": "g_amir", "label": "📞 Call Amir's saved number", "delay": 10, "kind": "clue",
             "clue": "Straight to voicemail. (This proves NOTHING. His phone may just be off. Scammers count on this.)"},
            {"id": "g_mak", "label": "📞 Call Mak", "poi": "home", "delay": 15, "kind": "clue",
             "clue": "Mak: 'Amir? He's at Danish's house doing an assignment. I spoke to him 10 minutes ago!'"},
            {"id": "g_danish", "label": "Message Danish", "poi": "danish", "delay": 12, "kind": "clue",
             "clue": "Danish sends a selfie: Amir is right there eating Maggi 😂"},
            {"id": "g_station", "label": "Call the police station", "poi": "police", "delay": 15, "kind": "clue",
             "clue": "Duty officer: 'No one named Amir has been detained tonight. No Sergeant Kamal on duty.'"},
            {"id": "g_traffic", "label": "Check the traffic app for accidents", "poi": "hospital", "delay": 8, "kind": "clue",
             "clue": "No accidents reported in Bandar Harmoni in the last 2 hours."},
        ],
        "win": [["t_hangup"], ["g_mak", "g_danish", "g_station"]],
        "timeout": "lost",
        "endings": {
            "win": {"title": "🛡️ You beat the voice clone!", "text": "Amir was safe at Danish's house. The voice was cloned from his TikTok videos."},
            "lost": {"title": "💸 RM3,000 gone", "text": "The money went to a mule account. Amir was at Danish's house the whole time."},
        },
        "debrief": "A voice is no longer proof of identity. **Hang up, call back on a saved number, check with a second person, "
                   "and agree on a family code word.** Voicemail on the real number proves nothing.",
    },
    {
        "id": "C3", "icon": "🌙", "title": "Meet Me Tonight", "tactic": "Online meet-up lure",
        "summary": "An online 'friend' changes the meeting place to a dark parking lot and says 'come alone'. Stop the Target in time.",
        "duration": 120, "stake": 0, "pois": ["mall", "backlot", "warehouse", "police"],
        "pos": {"target": "mall", "guardian": "mall"},
        "brief": "8pm, Harmoni Mall food court. {T} has been chatting with 'Mia, 19' on a gaming app for two weeks. "
                 "They agreed to meet here. {G} came along.",
        "brief_target": "Mia just sent a voice note. You really want to meet her. Decide what to do.",
        "brief_guardian": "You're at the food court with {T}. Something feels off. Investigate before {T} walks off.",
        "incoming": {"channel": "WhatsApp", "sender": "Mia 🎮 (online friend)", "context": "Voice note from Mia:",
                     "audio": "c3_mia_voicenote.mp3"},
        "pressure": [
            (20, "💬 Mia: 'Change of plan, come to the BACK parking lot instead 🙈'"),
            (40, "💬 Mia: 'Come ALONE ok? Your friend will make it weird.'"),
            (60, "💬 Mia: 'Turn off your location, my cousin is very private 😅'"),
            (85, "💬 Mia: 'We're leaving in 2 min if you don't come!! Last chance 😢'"),
        ],
        "target_actions": [
            {"id": "t_walk", "label": "🚶 Walk to the back parking lot alone", "kind": "doom", "seconds": 30,
             "ending": "danger", "doom_from": "mall", "doom_to": "backlot",
             "text": "{T} is walking to the back parking lot ALONE. Arrives in 30 seconds!"},
            {"id": "t_stop", "label": "✋ Stop and turn back", "kind": "cancel_doom",
             "text": "{T} stopped and turned back."},
            {"id": "t_video", "label": "📹 Ask Mia for a quick video call first", "kind": "info",
             "reply": "Mia: 'My camera is broken 😅 just come lah!'"},
            {"id": "t_inside", "label": "🛍️ Reply: 'Let's meet inside the food court, with my friend'", "kind": "info",
             "reply": "Mia: 'No!! Too crowded. Back lot or nothing.'"},
            {"id": "t_location_off", "label": "📍 Turn off location sharing, as Mia asked", "kind": "bad",
             "text": "{T} turned off location sharing. Now nobody can find {T} if something goes wrong."},
            {"id": "t_family", "label": "👨‍👩‍👦 Share live location with family", "kind": "bonus",
             "text": "{T} shared live location with family. Smart safety move."},
            {"id": "t_block", "label": "🚫 Refuse, block Mia and stay with {G}", "kind": "win",
             "text": "{T} refused and blocked 'Mia'. Now let's make sure this account can't hurt anyone else."},
        ],
        "guardian_tools": [
            {"id": "g_reverse", "label": "🖼️ Reverse-image-search Mia's profile photo", "delay": 12, "kind": "clue",
             "clue": "The photo belongs to an overseas influencer with 2 million followers. 'Mia' is not who she says."},
            {"id": "g_backlot", "label": "Check the back parking lot", "poi": "backlot", "delay": 6, "kind": "clue",
             "reveal_danger": "backlot",
             "clue": "Poorly lit, no CCTV, next to the old warehouse zone. A white van has been parked there with its engine running for an hour."},
            {"id": "g_profile", "label": "🔎 Check Mia's gaming profile", "delay": 8, "kind": "clue",
             "clue": "Account created 3 weeks ago. Has messaged 40+ teenagers in this area."},
            {"id": "g_security", "label": "Alert mall security", "poi": "mall", "delay": 10, "kind": "clue",
             "clue": "Security: 'Thank you. We're sending guards to the back lot. Do NOT go there.'"},
            {"id": "g_police", "label": "Call the police", "poi": "police", "delay": 15, "kind": "clue",
             "clue": "Police: 'Stay inside the mall. A patrol car is on the way to check the van.'"},
            {"id": "g_follow", "label": "🏃 Secretly follow {T} to the back lot", "delay": 3, "kind": "bad",
             "clue": "Two people walking into an isolated lot is still dangerous. Get help instead of following."},
        ],
        "win": [["t_block"], ["g_security", "g_police", "g_reverse"]],
        "timeout": "close",
        "endings": {
            "win": {"title": "🛡️ Lure stopped!", "text": "Security found two men in the van. 'Mia' never existed. {T} is safe and the account was reported."},
            "danger": {"title": "⚠️ {T} reached the back lot alone", "text": "There was no Mia. Two men were waiting by a white van. "
                       "A guard on patrol shouted and they drove off. {T} was lucky. In real life, robberies, abductions "
                       "and trafficking often start exactly like this."},
            "close": {"title": "😐 'Mia' disappeared", "text": "{T} didn't go, but the account wasn't reported. It's probably messaging another teenager right now."},
        },
        "debrief": "Warning signs of a meet-up lure: **never video-calls, changes the place to somewhere isolated, says 'come alone', "
                   "asks you to turn off location, and creates a rush.** Meet online friends only in busy public places, with someone you trust, "
                   "and tell your family where you are.",
    },
    {
        "id": "C4", "icon": "✈️", "title": "The Dream Job Abroad", "tactic": "Job scam / trafficking",
        "summary": "An 'overseas customer service' job wants the Target's passport tonight. The Guardian has minutes to check the company.",
        "duration": 130, "stake": 1500, "pois": ["hotel", "airport", "police", "nsrc"],
        "pos": {"target": "hotel", "guardian": "hotel"},
        "brief": "Hotel Seri Kota lobby. {T} applied for an overseas 'customer service' job: RM8,000/month, free flight and hotel. "
                 "The recruiter, 'Ms. Vivian', is interviewing {T} right now. {G} came along.",
        "brief_target": "This job could change your family's life. Vivian is friendly but in a hurry.",
        "brief_guardian": "You're sitting at the next table. Check this company before {T} hands anything over.",
        "incoming": {"channel": "Phone call", "sender": "Ms. Vivian (recruiter), speaking in person", "context": "Face to face in the lobby:",
                     "audio": "c4_recruiter.mp3"},
        "pressure": [
            (20, "🧑‍💼 Vivian: 'Don't tell your parents yet, surprise them when you send money home 😉'"),
            (45, "🧑‍💼 Vivian: 'The job is in a big tech park. Phones are kept by security during work hours, normal.'"),
            (70, "🧑‍💼 Vivian: 'Passport now please, the agent is waiting outside in the car.'"),
            (100, "🧑‍💼 Vivian: 'If you can't decide, I'll give the seat to the next candidate.'"),
        ],
        "target_actions": [
            {"id": "t_contract", "label": "📄 Ask for a written contract, company name and address", "kind": "info",
             "reply": "Vivian: 'Company name is confidential until you arrive. Trust me la, everyone does this.'"},
            {"id": "t_stall", "label": "⏳ 'I need to discuss with my family tonight'", "kind": "stall", "seconds": 20,
             "text": "{T} asked for time (+20s). Vivian frowns."},
            {"id": "t_pay", "label": "💸 Pay the RM1,500 'visa processing fee'", "kind": "bad", "loss": 1500,
             "text": "{T} paid RM1,500. Licensed agencies don't charge workers like this."},
            {"id": "t_passport", "label": "🛂 Hand over your passport", "kind": "fatal", "ending": "trafficked"},
            {"id": "t_decline", "label": "🙅 Decline, keep your passport and leave with {G}", "kind": "win",
             "text": "{T} declined and kept the passport! {G}, let's make sure this recruiter is reported."},
        ],
        "guardian_tools": [
            {"id": "g_ssm", "label": "🔎 Check the company on the business registry", "delay": 12, "kind": "clue",
             "clue": "No company called 'Golden Bridge Services' is registered."},
            {"id": "g_licence", "label": "📋 Check if she's from a licensed employment agency", "delay": 12, "kind": "clue",
             "clue": "Not licensed. Licensed agencies never keep workers' passports or charge big upfront fees."},
            {"id": "g_news", "label": "📰 Search news: 'overseas customer service job'", "delay": 8, "kind": "clue",
             "clue": "Many reports of young people lured abroad with 'customer service' jobs, then forced to work in scam compounds with passports taken."},
            {"id": "g_agent", "label": "Look at the 'agent' waiting outside", "poi": "hotel", "delay": 6, "kind": "clue",
             "clue": "A car with two other young people inside, all with luggage. The driver is holding their phones."},
            {"id": "g_parents", "label": "📞 Call {T}'s parents", "delay": 15, "kind": "clue",
             "clue": "Mum: 'Don't give anything! Come home, we'll check together and report it.'"},
            {"id": "g_report", "label": "Report the recruiter to the police", "poi": "police", "delay": 15, "kind": "clue",
             "clue": "Police: 'Keep her messages and the car's plate number. We're sending officers to the hotel.'"},
        ],
        "win": [["t_decline"], ["g_ssm", "g_licence", "g_report"]],
        "timeout": "close",
        "endings": {
            "win": {"title": "🛡️ Trafficking trap avoided!", "text": "{T} kept the passport and the recruiter was reported. Police found the car with two other recruits."},
            "trafficked": {"title": "🚨 {T} was trafficked abroad", "text": "There was no tech job. On arrival, {T}'s passport and phone were taken. "
                           "{T} was forced to work long shifts scamming strangers and told to 'repay a debt' to leave. "
                           "Families of real victims often hear nothing for months."},
            "close": {"title": "😐 Vivian walked away", "text": "{T} still has the passport, but the recruiter wasn't reported and will try the next candidate."},
        },
        "debrief": "Job-trafficking red flags: **too-good salary, no contract, no real company, 'keep it secret', upfront fees, "
                   "and anyone asking to hold your passport or phone.** Check the company and agency licence first, and involve your family.",
    },
    {
        "id": "C5", "icon": "🔔", "title": "Knock Knock", "tactic": "Doorstep impostor",
        "summary": "Two 'utility officers' at the gate at night want to come in. Keep the doors shut and get help.",
        "duration": 100, "stake": 0, "pois": ["home", "guardhouse", "police"],
        "pos": {"target": "home", "guardian": "home"},
        "brief": "9:30pm. {T} and {G} are home alone; the parents are at a wedding. The intercom buzzes. "
                 "A man in a vest is at the gate, with another man behind him.",
        "brief_target": "You're answering the intercom. He sounds urgent and official.",
        "brief_guardian": "You're inside with {T}. Check whether these 'officers' are real.",
        "incoming": {"channel": "Phone call", "sender": "🔔 Intercom: 'Tenaga Harmoni officer'", "context": "At the gate:",
                     "audio": "c5_intercom_bm.mp3"},
        "pressure": [
            (20, "🔔 He presses the buzzer again and again: 'Cepat! The whole row could catch fire!'"),
            (40, "🔔 'Give me your phone number, I'll send an OTP to confirm the inspection.'"),
            (60, "🔔 The second man walks round towards the side gate..."),
            (80, "🔔 'If you don't open, I'll report you and your power will be cut tonight.'"),
        ],
        "target_actions": [
            {"id": "t_id", "label": "🪪 Ask to see staff ID through the gate camera", "kind": "info",
             "reply": "He flashes a card too fast to read: 'Hurry, no time!'"},
            {"id": "t_otp", "label": "📲 Give your number and read out the OTP", "kind": "bad",
             "text": "{T} read out an OTP. That code may have unlocked {T}'s e-wallet."},
            {"id": "t_photo", "label": "📸 Photograph them and their vehicle from the window", "kind": "bonus",
             "text": "{T} got clear photos of both men and the car plate."},
            {"id": "t_open", "label": "🔓 Open the gate to let them in", "kind": "fatal", "ending": "intrusion"},
            {"id": "t_lock", "label": "🔒 Keep everything locked; talk only via intercom", "kind": "win",
             "text": "{T} kept the doors locked. {G}, get help!"},
        ],
        "guardian_tools": [
            {"id": "g_guard", "label": "Call the guardhouse", "poi": "guardhouse", "delay": 10, "kind": "clue",
             "clue": "Guard: 'We didn't let anyone in. They came in by the side road. We're coming now!'"},
            {"id": "g_utility", "label": "☎️ Call Tenaga Harmoni's official hotline", "delay": 15, "kind": "clue",
             "clue": "'No inspections are scheduled in Taman Melur. Our staff never enter homes at night without an appointment.'"},
            {"id": "g_parents", "label": "📞 Call your parents", "delay": 12, "kind": "clue",
             "clue": "Dad: 'Don't open! I'm calling the police and coming home.'"},
            {"id": "g_neighbours", "label": "🏘️ Message the neighbourhood group", "poi": "home", "delay": 8, "kind": "clue",
             "clue": "Neighbour: 'The same 2 men came to No. 14 an hour ago! Don't open!'"},
            {"id": "g_police", "label": "Call 999", "poi": "police", "delay": 12, "kind": "clue",
             "clue": "Police: 'Stay inside, keep doors locked. A patrol car is on the way.'"},
        ],
        "win": [["t_lock"], ["g_guard", "g_police"]],
        "timeout": "close",
        "endings": {
            "win": {"title": "🛡️ Home kept safe!", "text": "The guard and police arrived. The two men ran off, and {T}'s photos helped identify them."},
            "intrusion": {"title": "🚨 They got inside", "text": "The 'officers' pushed in, took phones, laptops and jewellery, and left in four minutes. "
                          "Nobody was hurt this time. Many home robberies start with a fake officer at the gate."},
            "close": {"title": "😐 They left", "text": "The men gave up, but nobody reported them. They'll try another house tonight."},
        },
        "debrief": "Real utility or council staff **make appointments, carry ID you can verify by phone, and never pressure you at night.** "
                   "Keep the gate locked, verify with the official hotline or guardhouse, and call 999 if you feel unsafe.",
    },
    {
        "id": "C6", "icon": "🎥", "title": "The Boss on Video (Co-op)", "tactic": "Voice / video deepfake",
        "summary": "A deepfake director demands RM480,000. The colleague at the next desk must verify before the money moves.",
        "duration": 110, "stake": 480000, "pois": ["office", "bank", "airport"],
        "pos": {"target": "office", "guardian": "office"},
        "brief": "Segar Foods office, 4pm. {T} is a finance intern. {G} works at the next desk. "
                 "'Director Hafiz', who is overseas, starts a surprise video call with {T}.",
        "brief_target": "Your director and the CFO are both on screen. They need a payment in 30 minutes.",
        "brief_guardian": "You notice {T} looks stressed on a video call. Investigate quietly.",
        "incoming": {"channel": "Video call", "sender": "'Encik Hafiz' + 'CFO'", "context": "The video is a bit choppy.",
                     "audio": "s4_n2_director.mp3"},
        "pressure": [
            (20, "🎥 'Hafiz': 'Are you processing it? Share your screen.'"),
            (45, "🎥 'CFO': 'This is confidential. Don't involve the finance manager.'"),
            (70, "🎥 'Hafiz': 'Your internship evaluation is with me, remember.'"),
            (95, "🎥 'Hafiz': 'Five minutes before the deal collapses!'"),
        ],
        "target_actions": [
            {"id": "t_speaker", "label": "🔊 Turn your screen so {G} can see and hear", "kind": "share",
             "text": "{T} turned the screen towards {G}."},
            {"id": "t_question", "label": "❓ Ask about last week's real team meeting", "kind": "info",
             "reply": "'Hafiz' laughs: 'No time for that! Focus!'"},
            {"id": "t_policy", "label": "📜 'Policy says I must verify by phone first'", "kind": "stall", "seconds": 20,
             "text": "{T} quoted policy (+20s). 'Hafiz' gets angry."},
            {"id": "t_process", "label": "💸 Process the RM480,000 transfer", "kind": "fatal", "ending": "lost"},
            {"id": "t_refuse", "label": "🙅 Refuse to pay until it's verified", "kind": "win",
             "text": "{T} refused to pay until verified! {G}, get confirmation."},
        ],
        "guardian_tools": [
            {"id": "g_domain", "label": "📧 Check the meeting invite's email domain", "delay": 6, "kind": "clue",
             "requires": "speaker", "missing": "You can't see {T}'s screen. Ask {T} to turn it towards you!",
             "clue": "segarfoods-group.com, but the company uses segarfood.com.my!"},
            {"id": "g_director", "label": "Call Encik Hafiz's known mobile", "poi": "airport", "delay": 15, "kind": "clue",
             "clue": "Hafiz, at the airport: 'I'm not on any call! STOP the payment!'"},
            {"id": "g_manager", "label": "Walk over to the finance manager", "poi": "office", "delay": 10, "kind": "clue",
             "clue": "Manager: 'No acquisition is planned. Freeze everything.'"},
            {"id": "g_it", "label": "💻 Alert IT security", "delay": 10, "kind": "clue",
             "clue": "IT: 'We're blocking the look-alike domain company-wide now.'"},
        ],
        "win": [["t_refuse"], ["g_director", "g_manager"]],
        "timeout": "lost",
        "endings": {
            "win": {"title": "🛡️ Deepfake defeated!", "text": "The real Hafiz confirmed it was fake. RM480,000 saved and IT blocked the domain."},
            "lost": {"title": "💸 The company lost RM480,000", "text": "Both 'executives' were real-time deepfakes. The money was in an overseas account within the hour."},
        },
        "debrief": "**Any payment request is verified on a second channel you already trust, no matter how senior the person on screen is.** "
                   "Colleagues who notice stress and step in are the best defence.",
    },
]

# Extra voice clips for co-op missions (merged into AUDIO_CLIPS by content_expert)
COOP_AUDIO = {
    "c3_mia_voicenote.mp3": {
        "voice": "en-SG-LunaNeural", "rate": "+10%", "pitch": "+12Hz", "phone": True,
        "text": "Hey! I'm already near the mall. Actually, let's not meet inside, too many people. "
                "My cousin's car is at the back parking. Come alone okay, I'm a bit shy. "
                "Don't bring your friend, it'll be awkward. Hurry, we can't wait long!"},
    "c4_recruiter.mp3": {
        "voice": "en-SG-LunaNeural", "rate": "+4%", "pitch": "-2Hz", "phone": False,
        "text": "Congratulations, you're hired! Your flight leaves tomorrow morning. No need for a contract now, we'll sign "
                "when you arrive. Just give me your passport tonight so our agent can process the work visa, and pay the "
                "one thousand five hundred ringgit processing fee. Many candidates are waiting, so I need your answer in two minutes."},
    "c5_intercom_bm.mp3": {
        "voice": "ms-MY-OsmanNeural", "rate": "+8%", "pitch": "-3Hz", "phone": True,
        "text": "Assalamualaikum, saya pegawai Tenaga Harmoni. Ada kebocoran elektrik di kawasan ni, bahaya. "
                "Saya kena masuk periksa meter dan suis dalam rumah sekarang. Buka pintu pagar cepat, kawan saya pun nak masuk sekali."},
}

TRANSLATIONS = {
    "c5_intercom_bm.mp3": "[English] Hello, I'm a Tenaga Harmoni officer. There's an electrical leak in this area, it's dangerous. "
                          "I need to come in and check the meter and switches inside the house now. Open the gate quickly, my colleague is coming in too.",
}


def get_mission(mid):
    for m in COOP_MISSIONS:
        if m["id"] == mid:
            return m
    return None
