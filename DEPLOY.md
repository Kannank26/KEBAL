# Put KEBAL online for free (Streamlit Community Cloud)

You get a public link like `https://kebal-umpsa.streamlit.app` that works on any phone. About 20 minutes, no coding.

## What you need
- A free **GitHub** account (github.com)
- The extracted `scamshield_arena` folder from `KEBAL_app.zip`

## Step 1: Put the files on GitHub
1. Sign in to github.com, click **+** (top right) → **New repository**.
2. Name: `kebal`. Choose **Public**. Click **Create repository**.
3. On the new page click **uploading an existing file**.
4. Open the `scamshield_arena` folder on your computer, select **everything inside it** (all files and the `assets` and `.streamlit` folders) and drag them into the browser.
   - Do **not** upload any `.db` file or the `.venv` folder if you have them.
5. Wait for all files to finish (the audio files take a moment), then click **Commit changes**.
6. Check that `app.py`, `requirements.txt` and the folder `assets/audio` appear in the list.

> **Hidden folder tip:** Mac and Windows sometimes hide the `.streamlit` folder, so it may not upload. The app still works, but with the default colours. To fix: in GitHub click **Add file → Create new file**, type the name `.streamlit/config.toml`, paste the contents of that file from your computer (open it with Notepad / TextEdit), and click **Commit changes**.

## Step 2: Deploy
1. Go to **share.streamlit.io** and click **Continue with GitHub**. Allow access.
2. Click **Create app** (top right) → **Deploy a public app from GitHub**.
3. Fill in:
   - **Repository:** `your-github-name/kebal`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** choose something short, e.g. `kebal-umpsa`
4. Open **Advanced settings**:
   - **Python version:** 3.12
   - **Secrets:** paste this, with your own private PIN:
     ```
     TEACHER_PIN = "choose-a-private-pin"
     ```
5. Click **Deploy**. The first start takes 2 to 5 minutes.

## Step 3: Test and share
1. Open your link on a laptop **and** two phones. Sign in, take a few test questions, play one Co-op mission with two phones.
2. Open **Teacher Dashboard** with your new PIN. The "default PIN" warning must be gone.
3. Make a QR code of your link with any free QR generator, for slides, posters and the booth.
4. Useful link versions:
   - `https://YOUR-APP.streamlit.app/?lang=ms` opens in Bahasa Melayu
   - Co-op invite links are created inside the app (Create room → share link)

## Important: protect your data
- Free hosting does **not** promise to keep the app's saved data. A restart, an update or a long sleep can wipe it.
- After **every** pilot session: Teacher Dashboard → **💾 Backup & restore** → download the database backup and the CSVs. Keep two copies.
- If data was wiped: upload your latest backup in the same panel (**Restore from a backup file**).
- Updating files on GitHub restarts the app, so **download a backup before every update**.

## Good to know
- **Sleeping:** after 12 hours without visitors the app sleeps. Anyone can wake it with one click (about 30 seconds). Open the link 10 minutes before a session or a judging slot.
- **Capacity:** fine for a class. Before the pilot, test with 10 or more phones at once.
- **Privacy:** anyone with the link can play. Players only enter a nickname. Only someone with the teacher PIN can see results.
- **Change the PIN or add an AI key later:** share.streamlit.io → your app → **⋮ → Settings → Secrets**.

## No internet at the venue? Plan B
Run KEBAL on a laptop (double-click `START_HERE_Windows.bat` / `START_HERE_Mac.command`), turn on the laptop's hotspot, and let people join with the **Network URL** shown in the black window.
