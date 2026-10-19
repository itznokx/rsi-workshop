from flask import Flask, render_template, request, render_template_string
from datetime import datetime
import random

app = Flask(__name__)
app.config["FLAG"] = "Nada aqui, hihi!"

ZODIAC_SIGNS = [
    {"id": "aries",       "name": "Áries",       "symbol": "\u2648", "range": "21 Mar - 19 Abr",
     "desc": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Áries alimenta começos ousados.",
     "start": (3, 21), "end": (4, 19)},
    {"id": "taurus",      "name": "Touro",      "symbol": "\u2649", "range": "20 Abr - 20 Mai",
     "desc": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua para o touro constante.",
     "start": (4, 20), "end": (5, 20)},
    {"id": "gemini",      "name": "Gêmeos",      "symbol": "\u264A", "range": "21 Mai - 20 Jun",
     "desc": "Ut enim ad minim veniam, quis nostrud exercitation mentes gêmeas, curiosidade em dobro.",
     "start": (5, 21), "end": (6, 20)},
    {"id": "cancer",      "name": "Câncer",      "symbol": "\u264B", "range": "21 Jun - 22 Jul",
     "desc": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum carapaça de caranguejo.",
     "start": (6, 21), "end": (7, 22)},
    {"id": "leo",         "name": "Leão",         "symbol": "\u264C", "range": "23 Jul - 22 Ago",
     "desc": "Excepteur sint occaecat cupidatat non proident, o leão ruge sob céus dourados.",
     "start": (7, 23), "end": (8, 22)},
    {"id": "virgo",       "name": "Virgem",       "symbol": "\u264D", "range": "23 Ago - 22 Set",
     "desc": "Sunt in culpa qui officia deserunt mollit anim id est laborum, preciso e pé no chão.",
     "start": (8, 23), "end": (9, 22)},
    {"id": "libra",       "name": "Libra",       "symbol": "\u264E", "range": "23 Set - 22 Out",
     "desc": "Lorem ipsum dolor sit amet consectetur, equilíbrio e harmonia guiam as balanças.",
     "start": (9, 23), "end": (10, 22)},
    {"id": "scorpio",     "name": "Escorpião",     "symbol": "\u264F", "range": "23 Out - 21 Nov",
     "desc": "Consectetur adipiscing elit sed do eiusmod, a intensidade se esconde sob águas calmas.",
     "start": (10, 23), "end": (11, 21)},
    {"id": "sagittarius", "name": "Sagitário", "symbol": "\u2650", "range": "22 Nov - 21 Dez",
     "desc": "Tempor incididunt ut labore et dolore magna, o arqueiro mira em horizontes distantes.",
     "start": (11, 22), "end": (12, 21)},
    {"id": "capricorn",   "name": "Capricórnio",   "symbol": "\u2651", "range": "22 Dez - 19 Jan",
     "desc": "Ut enim ad minim veniam quis nostrud, a cabra do mar sobe com determinação paciente.",
     "start": (12, 22), "end": (1, 19)},
    {"id": "aquarius",    "name": "Aquário",    "symbol": "\u2652", "range": "20 Jan - 18 Fev",
     "desc": "Duis aute irure dolor in reprehenderit, o portador da água derrama visões do amanhã.",
     "start": (1, 20), "end": (2, 18)},
    {"id": "pisces",      "name": "Peixes",      "symbol": "\u2653", "range": "19 Fev - 20 Mar",
     "desc": "Excepteur sint occaecat cupidatat, dois peixes nadam entre o sonho e a realidade.",
     "start": (2, 19), "end": (3, 20)},
]

LOREM_HOROSCOPES = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. As estrelas sussurram sobre novas oportunidades chegando silenciosamente. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo. Um encontro casual hoje tem mais peso do que parece à primeira vista.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Confie em seus instintos quando o caminho a seguir parecer obscuro.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. A paciência traz clareza para um assunto que tem persistido.",
    "Curabitur pretium tincidunt lacus, et vehicula quam auctor id. As energias mudam a seu favor conforme a lua se move em sua fase atual, lorem ipsum dolor sit amet.",
]

LOREM_ASCENDANTS = [
    "Nulla facilisi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere. O seu signo ascendente colore como os outros percebem sua primeira impressão.",
    "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas, moldando a máscara que você usa perante o mundo.",
    "Integer posuere erat a ante venenatis dapibus posuere velit aliquet. O signo ascendente revela reações instintivas em situações não familiares.",
    "Aenean lacinia bibendum nulla sed consectetur, lorem ipsum dolor enquadrando seu comportamento exterior e a energia que você projeta em novos encontros.",
]

BLOCKED_KEYWORDS = [
    "os", "import", "popen", "subprocess", "system",
    "eval", "exec", "cat", "flag",
]

def contains_blocked_keyword(value: str) -> bool:
    lowered = value.lower()
    return any(keyword in lowered for keyword in BLOCKED_KEYWORDS)

def sign_index_for_date(month: int, day: int) -> int:
    """Retorna o índice do ZODIAC_SIGNS baseado num mês/dia"""
    for i, sign in enumerate(ZODIAC_SIGNS):
        s_month, s_day = sign["start"]
        e_month, e_day = sign["end"]
        if s_month == e_month:
            if month == s_month and s_day <= day <= e_day:
                return i
        else:
            if (month == s_month and day >= s_day) or (month == e_month and day <= e_day):
                return i
    return 0

@app.route("/")
def index():
    return render_template("index.html", signs=ZODIAC_SIGNS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/horoscope", methods=["GET", "POST"])
def horoscope():
    result = None
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birthdate_raw = request.form.get("birthdate", "").strip()
        if not name or not birthdate_raw:
            error = "Por favor, coloque seu nome e sua data de nascimento."
        elif contains_blocked_keyword(name):
            error = "As forças cósmicas rejeitam suas palavras com energia negativa. Por favor, digite o seu nome novamente."
        else:
            try:
                dt = datetime.strptime(birthdate_raw, "%Y-%m-%d")
            except ValueError:
                error = "Data em formato inválido."
                dt = None
            if dt is not None:
                idx = sign_index_for_date(dt.month, dt.day)
                sign = ZODIAC_SIGNS[idx]
                asc_idx = (idx + dt.day) % len(ZODIAC_SIGNS)
                ascendant = ZODIAC_SIGNS[asc_idx]
                daily_horoscope = random.choice(LOREM_HOROSCOPES)
                daily_ascendancy = random.choice(LOREM_ASCENDANTS)
                greeting_template = "Olá, " + name + "! Aqui está o seu horóscopo."
                result = {
                    "greeting": render_template_string(greeting_template),
                    "birthdate": dt.strftime("%d/%m/%Y"), # Padrão de data brasileiro (DD/MM/AAAA)
                    "sign": sign,
                    "ascendant": ascendant,
                    "daily_horoscope": daily_horoscope,
                    "daily_ascendancy": daily_ascendancy,
                }
    return render_template("horoscope.html", result=result, error=error, signs=ZODIAC_SIGNS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
