# CognitivePenalty v0.1

CognitivePenalty is a Windows-only productivity enforcement tool that blocks selected applications unless the user passes a cognitive challenge.

Instead of silently denying access, CognitivePenalty introduces **intentional friction**: if you truly want to open an app, you can—but you must prove it to yourself first.

This project is intentionally minimal, opinionated, and difficult to bypass through trivial tricks like renaming executables.

---

## ✨ Features

- 🔒 Blocks apps using **SHA-256 fingerprints**
- 🧠 Cognitive gate instead of simple deny/allow
- 🔁 Correct multi-instance handling (same app won’t re-trigger endlessly)
- 🪶 Lightweight polling-based watcher
- 🧊 Persistent hash cache to avoid CPU abuse
- 🧪 Rename & path spoofing resistance
- 🧩 System tray UI with configuration window

---

## 🖥️ Platform & Requirements

- **Windows only**
- Python **3.10+**
- Administrator privileges recommended

---

## 🚀 How It Works

1. A background watcher scans running processes
2. If a blocked app is detected:
   - The process is terminated
   - A challenge prompt appears
3. If answered correctly:
   - The app is unlocked
   - All instances of that app are allowed until **every instance exits**
4. When the last instance closes, the app is locked again

---

## 🔧 Configuration (IMPORTANT)

Blocked applications can be managed through the system tray **Settings** window.

### 📂 `data/blocked_apps.json`

You can still edit this file directly if needed. Each entry needs the **full absolute path** to the executable you want to block.

Example:

```json
[
  {
    "name": "ULTRAKILL",
    "path": "D:\\Apps\\Ultrakill\\ULTRAKILL.exe"
  }
]
```

### Rules:
- Paths must be absolute
- Escaped backslashes are required (`\\`)
- Do **not** manually edit `sha256` once generated

On first run, CognitivePenalty will:
- Compute the SHA-256 hash
- Store it automatically
- Cache it in `hash_cache.json` for future runs

---

## ▶️ Running the App

```bash
python main.py
```

Once running, CognitivePenalty stays in the background and watches for restricted apps.

### Headless mode (no UI)

If you need to run without a GUI (for example, on a headless Linux environment), set:

```bash
CP_HEADLESS=1 python main.py
```

---

## 📂 Project Structure

```
CognitivePenalty/
│
├── main.py
├── watcher.py
├── unlock_state.py
├── fingerprint.py
├── gate.py
├── storage.py
├── config.py
│
├── data/
│   ├── blocked_apps.json
│   └── hash_cache.json
│
├── README.md
├── LICENSE
└── .gitignore
```

---

## ⚠️ Known Limitations (v0.1)

- Windows-only
- No installer or auto-start

These are intentional for the first release.

---

## 🧠 Philosophy

This is **not** a nanny tool.

CognitivePenalty does not try to stop you forever.
It simply slows you down enough to ask:

> “Do I actually want to open this?”

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.

See the `LICENSE` file for full terms.
