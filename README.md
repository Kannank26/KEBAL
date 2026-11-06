# 🛡️ KEBAL: scam immunity training (formerly ScamShield Arena)

**A flight simulator for scams.** Learners practise on safe, simulated scam and legitimate messages *and real-sounding voice calls*, survive branching **Story Missions**, earn XP and badges, and **prove their improvement** with a built-in pre-test and post-test.

### What's new in version 5: 🧪 Pilot study tools + free online hosting
- **Teacher Dashboard → Pilot setup:** mark each class code as the **KEBAL group** or the **Control group** (tests only), require **research consent** at sign-in, and open the **Retention Test** (a delayed retest with 10 new questions).
- **Pilot results panel:** pre/post/retention means per group, extra gain with KEBAL, **Cohen's d**, a **permutation-test p-value**, overconfidence before vs after, and the **SUS usability score**.
- **In-app SUS survey** after the post-test, plus "which part helped" and "would you recommend".
- **Backup & restore** of the whole database (essential on free hosting).
- **`DEPLOY.md`:** a click-by-click guide to a free public link on Streamlit Community Cloud.
- The full pilot plan, consent form and session scripts are in the separate *KEBAL Pilot Test Kit* document.

### What's new in version 4: 🌐 Bahasa Melayu interface
- Switch **English / Bahasa Melayu** at the top of the sidebar, at any time. Or share a link ending in `?lang=ms` to open the app in Malay.
- Every menu, button, instruction, feedback heading, badge, level, scam-tactic name, map label, dashboard and the Safety & Help page is translated (380+ phrases in `i18n.py`).
- Scenario messages stay in their original language. Real scams arrive in a mix of Malay and English, so that's realistic training.
- Run `python check_i18n.py` after changing any text: it lists anything still missing a Malay translation.
- To add Tamil or Mandarin later, add another dictionary in `i18n.py`.

### What's new in version 3: 🗺️ Co-op Simulation (multiplayer)
Friends join the **same room code or link** and play one live scam together on a map of the fictional town **Bandar Harmoni**.
- **📱 Target:** gets the scam (call, chat, recruiter, stranger at the gate) and hears the voice and pressure.
- **🛡️ Guardian(s):** right beside the Target. Can't hear the call unless the Target turns on the speaker. Investigates places on the map (police station, bank, guardhouse, mall security...) and searches online. Results take time to arrive.
- **Urgency:** a shared countdown, scammer messages that escalate every few seconds, and in some missions the Target physically walking into danger on the map.
- **You only win together:** the Target makes the safe move **and** a Guardian confirms or reports it. Team radio (quick buttons + chat), team score with stars, full replay and debrief.
- **6 missions:** 🚓 The Call Beside You (fake police) · 🎙️ Kak, It's Me (voice clone) · 🌙 Meet Me Tonight (online meet-up lure / abduction risk) · ✈️ The Dream Job Abroad (job scam / trafficking) · 🔔 Knock Knock (doorstep impostors) · 🎥 The Boss on Video (deepfake executive).
- **Solo practice:** start a room alone to play both roles (great for demos).

**How friends join:** everyone must connect to the **same running app**.
- Same Wi-Fi: start the app on one laptop, then everyone opens the **Network URL** printed in the black window (e.g. `http://192.168.1.20:8501`). Create a room and share the code or link.
- Anywhere: deploy online (section 6) and share the link.

### What's new in version 2
- **Expert level:** 17 complex scenarios (spoofed SMS threads, look-alike domains like `bankharrnoni`, business email compromise, wedding-invite APKs, "accidental transfer" mule traps, recovery scams, fake flood charities, QR "quishing", sponsored-ad phishing, fake AI support bots) with **4 tricky legit cases** where context changes the answer.
- **🎧 Voice scams:** 15 synthetic voice clips with a phone-line effect, in **Bahasa Melayu, English and Mandarin** (Macau-scam robocalls, voice-clone family emergencies, a deepfake director, a genuine bank call). Transcripts available for deaf/hard-of-hearing players.
- **🎭 Story Missions:** 5 branching scenarios (85 possible paths) where every decision changes what happens next, with no hints until a full debrief at the end. Money-at-stake tracking and a "best move here" for every mistake.
- **🎯 Smart mode:** adaptive missions that target each player's weakest scam tactics.
- **Confidence ratings** in the tests: measures *overconfidence*, a key reason people fall for scams.
- Harder 10-question pre/post tests (each with a voice item) to avoid ceiling effects.
- Rename the product in one place: `APP_NAME` in `app.py` or the `APP_NAME` environment variable.

Built in Python with Streamlit, from `ScamShield_Master_Prompt.md`.

---

## 1. Run it (5 minutes)

You need Python 3.10 or newer from python.org (3.12 recommended) (Windows: tick **"Add python.exe to PATH"** when installing).

**Easiest:** extract the zip, open the folder, and double-click **`START_HERE_Windows.bat`** (Windows) or right-click **`START_HERE_Mac.command` → Open** (Mac). The first run installs everything automatically. See `HOW_TO_RUN.txt` if anything goes wrong.

**Manual way** (terminal opened inside this folder):

```bash
cd scamshield_arena
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Your browser opens at `http://localhost:8501`. That's it. No API key needed.

**Try it on your phone** (same Wi-Fi): Streamlit prints a *Network URL* such as `http://192.168.1.20:8501`. Open that on your phone.

## 2. Turn on live AI scenarios (optional)

The app has 19 hand-written training scenarios built in. To generate unlimited fresh ones with Claude:

- **Easiest:** open the sidebar → *⚙️ Live AI scenarios* → paste your Anthropic API key.
- **For a server:** set environment variables before running:
  ```bash
  export ANTHROPIC_API_KEY="sk-ant-..."
  export SCAMSHIELD_MODEL="claude-sonnet-4-5"   # optional; use any current Claude model name
  ```

Then in the Arena choose **Live AI scenarios**. You can pick English, Bahasa Melayu or Manglish in the sidebar. If the AI fails for any reason, the app quietly falls back to the built-in bank, so your demo never breaks.

## 3. Project structure

| File | What it does |
|---|---|
| `app.py` | All screens: Home, Pre-Test, Training Arena, Post-Test, My Progress, Teacher Dashboard, Safety & Help |
| `content.py` | Scenario bank: 19 core training scenarios (Easy/Medium/Hard), 10 pre-test + 10 post-test items, help steps |
| `content_expert.py` | Expert pack: 17 complex scenarios, 5 branching Story Missions, and the scripts for every voice clip |
| `assets/audio/` | 15 ready-made voice clips (MP3). No internet needed to play them |
| `generate_audio.py` | Optional: recreate or add voice clips (`pip install edge-tts`, needs internet) |
| `coop_content.py` | Co-op Simulation: the town map (places, districts, roads) and the 6 multiplayer missions |
| `coop.py` | Multiplayer engine: rooms, roles, shared timer, investigations, win/lose rules (stored in SQLite) |
| `i18n.py` | English / Bahasa Melayu interface text (`T()` function + Malay dictionary) |
| `pilot_stats.py` | Pilot study statistics: score gains, Cohen's d, permutation-test p-value |
| `DEPLOY.md` | How to put KEBAL online for free |
| `check_i18n.py` | Lists any interface text that has no Malay translation yet |
| `engine.py` | Game rules: missions (incl. Smart adaptive mode), XP scoring, levels, badges, story scoring, AI scenario generator and validator |
| `storage.py` | SQLite database (`scamshield.db`, created automatically) |
| `.streamlit/config.toml` | Theme colours |

### Add your own scenario
Copy any block in `TRAINING_SCENARIOS` inside `content.py`, give it a new `id` (e.g. `T20`), and edit the text. Rules:
- 4–5 cues, with at least one cue that is *not* a red flag (a decoy).
- Legit messages: all cues `"is_red_flag": False` and `"tactic": "Legit message"`.
- Use **fictional** organisation names only.

## 4. Scoring

| Action | XP |
|---|---|
| Correct verdict (Scam/Legit) | +50 |
| Each real red flag ticked | +10 |
| Each false alarm (decoy ticked) | −5 |
| Perfect round | +20 |
| Calm Mind: trusting a real message with no false alarms | +20 |

Hard rounds earn ×1.2 XP and Expert rounds ×1.5. Story Missions give 20–160 XP depending on the ending.

Levels: 🐣 Rookie → 🔍 Scam Spotter (200) → 🥊 Fraud Fighter (500) → 🛡️ Cyber Guardian (900) → 🏆 Scam Grandmaster (1400)

## 5. Teacher dashboard

Default PIN is **1234**. **Change it before a real pilot:**
```bash
export TEACHER_PIN="your-secret-pin"
```
The dashboard shows players, mean pre/post scores, paired gain, % improved, accuracy by scam tactic, missed-scam vs false-alarm rates, **Story Mission first-try escape rate and simulated money lost**, **calibration (accuracy by confidence, overconfident misses)**, voice vs text accuracy, and **CSV exports** (attempts + every story decision) for your competition report.

## 6. Put it online (free)

**Streamlit Community Cloud** (easiest):
1. Push this folder to a GitHub repository.
2. Go to share.streamlit.io → *New app* → pick the repo and `app.py`.
3. Under *Advanced settings → Secrets*, add `ANTHROPIC_API_KEY` and `TEACHER_PIN` if you want them.

Note: free cloud hosts can reset the SQLite file when the app restarts. For a pilot, **download the CSV from the Teacher Dashboard at the end of each session**, or run the app on a school laptop.

## 7. School pilot protocol (how to get evidence judges trust)

> For the UMPSA pilot, follow the *KEBAL Pilot Test Kit* document and the in-app **Teacher Dashboard → Pilot setup** (KEBAL group vs Control group). The steps below are the short version.

1. **Get permission** from the school and parents/guardians. Students use nicknames only.
2. Give the class one **class code** (e.g. `SMKTI-4A`), so all their data groups together.
3. **Session 1 (≈40 min):** Pre-Test (6 min, headphones on) → 2 Arena missions (Mixed) → short discussion of the 4P Scam Check.
4. **Session 2 (a few days later, ≈40 min):** 1 Smart mission → 2 Story Missions → Post-Test.
5. **Optional Session 3 (≈30 min):** pairs play 3 Co-op Simulations, swapping Target and Guardian. Great for showing teamwork and bystander intervention.
5. Export the CSV. Report: number of students, mean pre vs post, mean gain, % improved, and which tactics were hardest.
6. Be honest about limits (small sample, no control group). Better still, run a **control class** that does only the two tests, so you can show the gain comes from the game.

Aim for at least 30 students. A real chart from a real classroom is worth more than any slide.

## 8. Safety rules built into the app

- Every organisation, person, phone number and website is **fictional**.
- Links are shown as plain text and can't be clicked. The app never sends messages, SMS or calls.
- No real names, IC numbers, phone numbers or banking info are collected.
- All AI-generated text is HTML-escaped before display.
- Help page points to real Malaysian support: **NSRC 997**, your bank, police report, Semak Mule.
- All voices are **synthetic** (computer-generated). No real person's voice is cloned. If you add consented voices later, keep written consent.

## 9. Name check before competing

"ScamShield" is already the name of Singapore's official anti-scam app (National Crime Prevention Council). Before entering international competitions, choose a distinct name, set it in `APP_NAME`, and check trademark availability (e.g. MyIPO).

## 10. Ideas for the next version

real voice-clone audio rounds (consented voices only) · large-text Grandparent Mode · class leaderboard · teachers create custom scenarios · Flutter mobile front end on the same Python backend · ASEAN country packs.
