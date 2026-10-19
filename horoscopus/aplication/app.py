from flask import Flask, render_template, request, render_template_string
from datetime import datetime
import random
app = Flask(__name__)
app.config["FLAG"] = "NOTHING HERE";
ZODIAC_SIGNS = [
    {"id": "aries",       "name": "Aries",       "symbol": "\u2648", "range": "Mar 21 - Apr 19",
     "desc": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aries fuels bold beginnings.",
     "start": (3, 21), "end": (4, 19)},
    {"id": "taurus",      "name": "Taurus",      "symbol": "\u2649", "range": "Apr 20 - May 20",
     "desc": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua for the steady bull.",
     "start": (4, 20), "end": (5, 20)},
    {"id": "gemini",      "name": "Gemini",      "symbol": "\u264A", "range": "May 21 - Jun 20",
     "desc": "Ut enim ad minim veniam, quis nostrud exercitation twin minds, double curiosity.",
     "start": (5, 21), "end": (6, 20)},
    {"id": "cancer",      "name": "Cancer",      "symbol": "\u264B", "range": "Jun 21 - Jul 22",
     "desc": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum crab shell.",
     "start": (6, 21), "end": (7, 22)},
    {"id": "leo",         "name": "Leo",         "symbol": "\u264C", "range": "Jul 23 - Aug 22",
     "desc": "Excepteur sint occaecat cupidatat non proident, the lion roars under golden skies.",
     "start": (7, 23), "end": (8, 22)},
    {"id": "virgo",       "name": "Virgo",       "symbol": "\u264D", "range": "Aug 23 - Sep 22",
     "desc": "Sunt in culpa qui officia deserunt mollit anim id est laborum, precise and grounded.",
     "start": (8, 23), "end": (9, 22)},
    {"id": "libra",       "name": "Libra",       "symbol": "\u264E", "range": "Sep 23 - Oct 22",
     "desc": "Lorem ipsum dolor sit amet consectetur, balance and harmony guide the scales.",
     "start": (9, 23), "end": (10, 22)},
    {"id": "scorpio",     "name": "Scorpio",     "symbol": "\u264F", "range": "Oct 23 - Nov 21",
     "desc": "Consectetur adipiscing elit sed do eiusmod, intensity hides beneath still water.",
     "start": (10, 23), "end": (11, 21)},
    {"id": "sagittarius", "name": "Sagittarius", "symbol": "\u2650", "range": "Nov 22 - Dec 21",
     "desc": "Tempor incididunt ut labore et dolore magna, the archer aims toward distant horizons.",
     "start": (11, 22), "end": (12, 21)},
    {"id": "capricorn",   "name": "Capricorn",   "symbol": "\u2651", "range": "Dec 22 - Jan 19",
     "desc": "Ut enim ad minim veniam quis nostrud, the sea-goat climbs with patient resolve.",
     "start": (12, 22), "end": (1, 19)},
    {"id": "aquarius",    "name": "Aquarius",    "symbol": "\u2652", "range": "Jan 20 - Feb 18",
     "desc": "Duis aute irure dolor in reprehenderit, the water bearer pours visions of tomorrow.",
     "start": (1, 20), "end": (2, 18)},
    {"id": "pisces",      "name": "Pisces",      "symbol": "\u2653", "range": "Feb 19 - Mar 20",
     "desc": "Excepteur sint occaecat cupidatat, two fish swim between dream and reality.",
     "start": (2, 19), "end": (3, 20)},
]
LOREM_HOROSCOPES = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. The stars whisper of new opportunities "
    "arriving quietly. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo. "
    "A chance encounter today carries more weight than it first appears.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
    "pariatur. Trust your instincts when the path forward seems unclear.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id "
    "est laborum. Patience brings clarity to a matter that has lingered.",
    "Curabitur pretium tincidunt lacus, et vehicula quam auctor id. Energy shifts in your favor as the "
    "moon moves through its current phase, lorem ipsum dolor sit amet.",
]

LOREM_ASCENDANTS = [
    "Nulla facilisi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere. Your "
    "rising sign colors how others perceive your first impression.",
    "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas, "
    "shaping the mask you wear before the world.",
    "Integer posuere erat a ante venenatis dapibus posuere velit aliquet. The ascendant sign reveals "
    "instinctive reactions in unfamiliar situations.",
    "Aenean lacinia bibendum nulla sed consectetur, lorem ipsum dolor framing your outward demeanor "
    "and the energy you project onto new encounters.",
]
BLOCKED_KEYWORDS = [
    "os", "import", "popen", "subprocess", "system",
    "eval", "exec", "cat", "flag",
]
def contains_blocked_keyword(value: str) -> bool:
    lowered = value.lower()
    return any(keyword in lowered for keyword in BLOCKED_KEYWORDS)
def sign_index_for_date(month: int, day: int) -> int:
    """Return the index in ZODIAC_SIGNS for a given month/day."""
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
            error = "Please provide both your name and your birth date."
        elif contains_blocked_keyword(name):
            error = "The cosmic veil rejects words of negative energy. Please rephrase your name. \u2728"
        else:
            try:
                dt = datetime.strptime(birthdate_raw, "%Y-%m-%d")
            except ValueError:
                error = "Invalid date format."
                dt = None
            if dt is not None:
                idx = sign_index_for_date(dt.month, dt.day)
                sign = ZODIAC_SIGNS[idx]
                asc_idx = (idx + dt.day) % len(ZODIAC_SIGNS)
                ascendant = ZODIAC_SIGNS[asc_idx]
                daily_horoscope = random.choice(LOREM_HOROSCOPES)
                daily_ascendancy = random.choice(LOREM_ASCENDANTS)
                greeting_template = "Hello, " + name + "! Here is what the stars have aligned for you."
                result = {
                    "greeting": render_template_string(greeting_template),
                    "birthdate": dt.strftime("%d %B, %Y"),
                    "sign": sign,
                    "ascendant": ascendant,
                    "daily_horoscope": daily_horoscope,
                    "daily_ascendancy": daily_ascendancy,
                }
    return render_template("horoscope.html", result=result, error=error, signs=ZODIAC_SIGNS)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
