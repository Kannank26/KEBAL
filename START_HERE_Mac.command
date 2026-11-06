#!/bin/bash
# ScamShield Arena launcher for macOS / Linux
cd "$(dirname "$0")" || exit 1
echo "============================================"
echo "   KEBAL - starting up..."
echo "============================================"

if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else
  echo "[X] Python is not installed. Download it from python.org, install, then run this again."
  (command -v open >/dev/null && open https://www.python.org/downloads/) 2>/dev/null
  read -r -p "Press Enter to close..."; exit 1
fi
echo "[OK] Found $($PY --version)"

if [ ! -f .venv/installed.ok ]; then
  echo "First run: installing what the app needs (2-5 minutes, needs internet)..."
  $PY -m venv .venv || { echo "[X] Could not create environment."; read -r -p "Press Enter..."; exit 1; }
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -r requirements.txt || { echo "[X] Install failed. Check internet."; read -r -p "Press Enter..."; exit 1; }
  touch .venv/installed.ok
fi

echo "[OK] Opening KEBAL in your browser. Keep this window open; press Ctrl+C to stop."
.venv/bin/python -m streamlit run app.py
