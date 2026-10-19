# Telegram Music Bot v2 (plugins + MongoDB)

Features: /play, /search (buttons), /history, /favs, ❤️ favorite button, /ping, /id,
owner-only /stats and /broadcast. MongoDB is **optional**; without it the bot still plays songs.

## Structure
```
main.py        # starts bot, web server, auto-loads plugins
config.py      # env variables
database.py    # MongoDB (motor), safe if DB is down
plugins/       # every .py here is a plugin with register(app)
utils/         # downloader + sender
render.yaml
```
Naya plugin banane ke liye `plugins/mera.py` me `def register(app): ...` likho, restart karo. Bas.

## MongoDB Atlas (free)
1. mongodb.com/atlas -> free M0 cluster banao.
2. Database Access -> user + password banao.
3. Network Access -> Add IP `0.0.0.0/0` (Render ka IP fixed nahi hota).
4. Connect -> Drivers -> URI copy karo. Password me special characters ho to URL-encode karo.
5. `MONGO_URI` me daalo.

## Termux
```bash
pkg update && pkg upgrade -y
pkg install python git -y
cd music-bot-v2
pip install -r requirements.txt
cp .env.example .env && nano .env     # token, mongo uri bharo
python main.py
```
Background: `pkg install tmux`, `tmux new -s bot`, `termux-wake-lock`.
Agar `pymongo` install me error aaye: `pkg install clang make` phir dobara pip install.

## Render
1. Folder GitHub pe push karo (`.env` push mat karna).
2. Render -> New -> Blueprint -> repo chuno.
3. `BOT_TOKEN`, `MONGO_URI`, `OWNER_ID` paste karo -> Deploy.
4. Bot khud `RENDER_EXTERNAL_URL` ko har 10 min ping karta hai taaki free service sleep na kare.

## Dhyan rakho
- Same token se **ek hi jagah** bot chalao (Render ya Termux). Dono pe chalaoge to "Conflict" error aayega.
- YouTube Render ke server IP ko block kar sakta hai. Phir `cookies.txt` (Netscape format) repo/secret file me rakho, ya Termux pe chalao.
- Sirf wahi content download karo jiska tumhe haq hai.
