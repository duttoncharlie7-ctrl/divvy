import requests
from data_analyzer import analyze_data

# -----------------------------------------
# INSERT YOUR VALUES HERE
BOT_TOKEN = "8421856026:AAFJLbpKG2T2qmS8uAovbUFioUejrFDV9y0"   # <-- your real token
CHAT_ID = "8026833130"                                        # <-- your real chat id
# -----------------------------------------

def format_station_message(station):
    return (
        f"🚲 *{station['name']}*\n"
        f"• Ebikes: *{station['ebikes']}*\n"
        f"• Regular bikes: *{station['regular_bikes']}*\n"
        f"• Docks available: *{station['docks_available']}*\n"
        f"• Renting: *{station['is_renting']}*\n"
        f"• Status Up: *{station['status_up']}*\n"
    )

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def main():
    data = analyze_data()
    stations = data["stations"]

    if not stations:
        send_message("No station data found.")
        return

    msg = "📊 *Divvy Station Status Update*\n\n"
    for s in stations:
        msg += format_station_message(s) + "\n"

    send_message(msg)

if __name__ == "__main__":
    main()

