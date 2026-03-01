import subprocess
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# ENGINEERING CALCULATOR
# ─────────────────────────────────────────────

def ideal_gas_law(P=None, V=None, n=None, T=None):
    """PV = nRT — solve for missing variable"""
    R = 8.314  # J/(mol·K)
    try:
        if P is None:
            result = (n * R * T) / V
            return f"Pressure is {result:.4f} Pascals sir."
        elif V is None:
            result = (n * R * T) / P
            return f"Volume is {result:.4f} cubic metres sir."
        elif n is None:
            result = (P * V) / (R * T)
            return f"Moles of gas is {result:.4f} mol sir."
        elif T is None:
            result = (P * V) / (n * R)
            return f"Temperature is {result:.4f} Kelvin sir."
    except Exception as e:
        return f"Could not solve ideal gas law: {e}"

def heat_transfer(Q=None, m=None, c=None, delta_T=None):
    """Q = mcΔT — solve for missing variable"""
    try:
        if Q is None:
            result = m * c * delta_T
            return f"Heat transfer is {result:.4f} Joules sir."
        elif m is None:
            result = Q / (c * delta_T)
            return f"Mass is {result:.4f} kilograms sir."
        elif c is None:
            result = Q / (m * delta_T)
            return f"Specific heat capacity is {result:.4f} J per kg K sir."
        elif delta_T is None:
            result = Q / (m * c)
            return f"Temperature change is {result:.4f} Kelvin sir."
    except Exception as e:
        return f"Could not solve heat transfer: {e}"

def reynolds_number(rho, v, L, mu):
    """Re = ρvL/μ"""
    try:
        Re = (rho * v * L) / mu
        if Re < 2300:
            flow = "laminar"
        elif Re < 4000:
            flow = "transitional"
        else:
            flow = "turbulent"
        return f"Reynolds number is {Re:.2f} — flow is {flow} sir."
    except Exception as e:
        return f"Could not calculate Reynolds number: {e}"

def stress_strain(F=None, A=None, stress=None, E=None, strain=None):
    """σ = F/A and σ = Eε"""
    try:
        results = []
        if stress is None and F and A:
            stress = F / A
            results.append(f"Stress is {stress:.4f} Pascals")
        if strain is None and stress and E:
            strain = stress / E
            results.append(f"Strain is {strain:.6f}")
        if E is None and stress and strain:
            E = stress / strain
            results.append(f"Elastic modulus is {E:.4f} Pascals")
        if results:
            return ". ".join(results) + " sir."
        return "Please provide more values sir."
    except Exception as e:
        return f"Could not solve stress strain: {e}"

def unit_convert(value, from_unit, to_unit):
    """Common engineering unit conversions"""
    # Normalize unit names
    aliases = {
        "celsius": "c", "centigrade": "c",
        "kelvin": "k",
        "fahrenheit": "f",
        "metres": "m", "meters": "m", "metre": "m", "meter": "m",
        "feet": "ft", "foot": "ft",
        "kilograms": "kg", "kilogram": "kg",
        "pounds": "lb", "pound": "lb",
        "pascals": "pa", "pascal": "pa",
        "kilopascals": "kpa", "kilopascal": "kpa",
        "megapascals": "mpa", "megapascal": "mpa",
        "joules": "j", "joule": "j",
        "kilojoules": "kj", "kilojoule": "kj",
        "watts": "w", "watt": "w",
        "kilowatts": "kw", "kilowatt": "kw",
        "newtons": "n", "newton": "n",
        "radians per second": "rad/s",
        "revolutions per minute": "rpm",
        "metres per second": "m/s", "meters per second": "m/s",
        "kilometres per hour": "km/h", "kilometers per hour": "km/h",
    }

    from_unit = aliases.get(from_unit.lower(), from_unit.lower())
    to_unit = aliases.get(to_unit.lower(), to_unit.lower())

    conversions = {
        ("c", "k"): lambda x: x + 273.15,
        ("k", "c"): lambda x: x - 273.15,
        ("f", "c"): lambda x: (x - 32) * 5/9,
        ("c", "f"): lambda x: x * 9/5 + 32,
        ("f", "k"): lambda x: (x - 32) * 5/9 + 273.15,
        ("k", "f"): lambda x: (x - 273.15) * 9/5 + 32,
        ("m", "ft"): lambda x: x * 3.28084,
        ("ft", "m"): lambda x: x / 3.28084,
        ("kg", "lb"): lambda x: x * 2.20462,
        ("lb", "kg"): lambda x: x / 2.20462,
        ("pa", "psi"): lambda x: x * 0.000145038,
        ("psi", "pa"): lambda x: x / 0.000145038,
        ("kpa", "psi"): lambda x: x * 0.145038,
        ("psi", "kpa"): lambda x: x / 0.145038,
        ("mpa", "psi"): lambda x: x * 145.038,
        ("psi", "mpa"): lambda x: x / 145.038,
        ("j", "kj"): lambda x: x / 1000,
        ("kj", "j"): lambda x: x * 1000,
        ("w", "kw"): lambda x: x / 1000,
        ("kw", "w"): lambda x: x * 1000,
        ("rpm", "rad/s"): lambda x: x * 2 * 3.14159 / 60,
        ("rad/s", "rpm"): lambda x: x * 60 / (2 * 3.14159),
        ("m/s", "km/h"): lambda x: x * 3.6,
        ("km/h", "m/s"): lambda x: x / 3.6,
        ("n", "lbf"): lambda x: x * 0.224809,
        ("lbf", "n"): lambda x: x / 0.224809,
    }

 # Full names for speech
    unit_names = {
        "c": "Celsius", "k": "Kelvin", "f": "Fahrenheit",
        "m": "metres", "ft": "feet", "kg": "kilograms",
        "lb": "pounds", "pa": "Pascals", "psi": "PSI",
        "kpa": "kilopascals", "mpa": "megapascals",
        "j": "Joules", "kj": "kilojoules", "w": "Watts",
        "kw": "kilowatts", "n": "Newtons", "lbf": "pound-force",
        "rpm": "RPM", "rad/s": "radians per second",
        "m/s": "metres per second", "km/h": "kilometres per hour"
    }
    key = (from_unit, to_unit)
    if key in conversions:
        result = conversions[key](value)
        from_name = unit_names.get(from_unit, from_unit)
        to_name = unit_names.get(to_unit, to_unit)
        return f"{value} {from_name} is {result:.2f} {to_name} sir."
    return f"I don't have a conversion from {from_unit} to {to_unit} sir."


def solve_engineering(problem_type, **kwargs):
    """Route to correct engineering solver"""
    if problem_type == "ideal_gas":
        return ideal_gas_law(**kwargs)
    elif problem_type == "heat_transfer":
        return heat_transfer(**kwargs)
    elif problem_type == "reynolds":
        return reynolds_number(**kwargs)
    elif problem_type == "stress_strain":
        return stress_strain(**kwargs)
    elif problem_type == "unit_convert":
        return unit_convert(**kwargs)
    return "I don't have a solver for that problem type sir."

# ─────────────────────────────────────────────
# PDF SUMMARIZER
# ─────────────────────────────────────────────

def summarize_pdf(filepath):
    """Read and summarize a PDF file"""
    try:
        import PyPDF2
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:5]:  # Read first 5 pages
                text += page.extract_text()

        if not text.strip():
            return "The PDF appears to be empty or scanned sir. I cannot extract text from images."

        # Use OpenAI to summarize
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are JARVIS. Summarize this document in 3-4 sentences, focusing on the key findings and conclusions. Be concise and precise."},
                {"role": "user", "content": f"Summarize this document:\n\n{text[:4000]}"}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content

    except FileNotFoundError:
        return f"I couldn't find the file at {filepath} sir."
    except Exception as e:
        return f"I encountered an issue reading the PDF sir: {e}"

def get_latest_pdf():
    """Find the most recently downloaded PDF"""
    downloads = os.path.expanduser("~/Downloads")
    desktop = os.path.expanduser("~/Desktop")

    pdfs = []
    for folder in [downloads, desktop]:
        for f in os.listdir(folder):
            if f.endswith(".pdf"):
                full_path = os.path.join(folder, f)
                pdfs.append((os.path.getmtime(full_path), full_path))

    if pdfs:
        pdfs.sort(reverse=True)
        return pdfs[0][1]
    return None

# ─────────────────────────────────────────────
# DEADLINE TRACKER
# ─────────────────────────────────────────────

DEADLINES_FILE = "jarvis_deadlines.json"

def load_deadlines():
    if os.path.exists(DEADLINES_FILE):
        with open(DEADLINES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_deadlines(deadlines):
    with open(DEADLINES_FILE, 'w') as f:
        json.dump(deadlines, f, indent=2)

def add_deadline(title, course, due_date_str, assignment_type="assignment"):
    """Add a deadline"""
    deadlines = load_deadlines()
    deadline = {
        "title": title,
        "course": course,
        "due_date": due_date_str,
        "type": assignment_type,
        "added": datetime.now().strftime("%Y-%m-%d")
    }
    deadlines.append(deadline)
    save_deadlines(deadlines)
    return f"Deadline added — {title} for {course} due {due_date_str} sir."

def get_deadlines():
    """Get all upcoming deadlines sorted by date"""
    deadlines = load_deadlines()
    if not deadlines:
        return "No upcoming deadlines sir. Either you're very organised or very behind."

    now = datetime.now()
    result = "Upcoming deadlines sir. "
    urgent = []
    upcoming = []

    for d in deadlines:
        try:
            due = datetime.strptime(d["due_date"], "%Y-%m-%d")
            days_left = (due - now).days
            if days_left < 0:
                continue
            elif days_left <= 3:
                urgent.append((days_left, d))
            else:
                upcoming.append((days_left, d))
        except:
            continue

    urgent.sort()
    upcoming.sort()

    if urgent:
        result += "Urgent — "
        for days, d in urgent:
            if days == 0:
                result += f"{d['title']} for {d['course']} is due TODAY. "
            elif days == 1:
                result += f"{d['title']} for {d['course']} is due TOMORROW. "
            else:
                result += f"{d['title']} for {d['course']} is due in {days} days. "

    if upcoming:
        result += "Upcoming — "
        for days, d in upcoming[:3]:
            result += f"{d['title']} for {d['course']} in {days} days. "

    return result

def check_urgent_deadlines():
    """Check for deadlines due within 48 hours — called on boot"""
    deadlines = load_deadlines()
    now = datetime.now()
    urgent = []

    for d in deadlines:
        try:
            due = datetime.strptime(d["due_date"], "%Y-%m-%d")
            days_left = (due - now).days
            if 0 <= days_left <= 2:
                urgent.append((days_left, d))
        except:
            continue

    if urgent:
        result = "Sir, urgent academic alert. "
        for days, d in urgent:
            if days == 0:
                result += f"{d['title']} for {d['course']} is due today. "
            elif days == 1:
                result += f"{d['title']} for {d['course']} is due tomorrow. "
            else:
                result += f"{d['title']} for {d['course']} is due in {days} days. "
        return result
    return None

# ─────────────────────────────────────────────
# LAB REPORT ASSISTANT
# ─────────────────────────────────────────────

LAB_NOTES_FILE = "lab_notes.json"

def load_lab_notes():
    if os.path.exists(LAB_NOTES_FILE):
        with open(LAB_NOTES_FILE, 'r') as f:
            return json.load(f)
    return {"current_lab": None, "sections": {}}

def save_lab_notes(notes):
    with open(LAB_NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)

def start_lab_report(lab_name):
    """Start a new lab report"""
    notes = {
        "current_lab": lab_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sections": {
            "objective": "",
            "equipment": "",
            "procedure": "",
            "observations": [],
            "results": [],
            "conclusion": ""
        }
    }
    save_lab_notes(notes)
    return f"Lab report started for {lab_name} sir. You can now dictate observations, results, or conclusions."

def add_lab_observation(observation):
    """Add an observation to current lab report"""
    notes = load_lab_notes()
    if not notes.get("current_lab"):
        return "No active lab report sir. Say 'start lab report' first."
    timestamp = datetime.now().strftime("%H:%M:%S")
    notes["sections"]["observations"].append({
        "time": timestamp,
        "note": observation
    })
    save_lab_notes(notes)
    return f"Observation recorded at {timestamp} sir."

def add_lab_result(result):
    """Add a result to current lab report"""
    notes = load_lab_notes()
    if not notes.get("current_lab"):
        return "No active lab report sir. Say 'start lab report' first."
    notes["sections"]["results"].append(result)
    save_lab_notes(notes)
    return "Result recorded sir."

def set_lab_section(section, content):
    """Set a section of the lab report"""
    notes = load_lab_notes()
    if not notes.get("current_lab"):
        return "No active lab report sir."
    if section in notes["sections"]:
        notes["sections"][section] = content
        save_lab_notes(notes)
        return f"{section.capitalize()} updated sir."
    return f"Unknown section {section} sir."

def export_lab_report():
    """Export lab report as a text file"""
    notes = load_lab_notes()
    if not notes.get("current_lab"):
        return "No active lab report to export sir."

    filename = f"lab_report_{notes['current_lab'].replace(' ', '_')}_{notes['date']}.txt"
    filepath = os.path.expanduser(f"~/Desktop/{filename}")

    with open(filepath, 'w') as f:
        f.write(f"LAB REPORT — {notes['current_lab'].upper()}\n")
        f.write(f"Date: {notes['date']}\n")
        f.write("=" * 50 + "\n\n")

        f.write("OBJECTIVE\n" + "-" * 20 + "\n")
        f.write(notes["sections"]["objective"] + "\n\n")

        f.write("EQUIPMENT\n" + "-" * 20 + "\n")
        f.write(notes["sections"]["equipment"] + "\n\n")

        f.write("PROCEDURE\n" + "-" * 20 + "\n")
        f.write(notes["sections"]["procedure"] + "\n\n")

        f.write("OBSERVATIONS\n" + "-" * 20 + "\n")
        for obs in notes["sections"]["observations"]:
            f.write(f"[{obs['time']}] {obs['note']}\n")
        f.write("\n")

        f.write("RESULTS\n" + "-" * 20 + "\n")
        for res in notes["sections"]["results"]:
            f.write(f"- {res}\n")
        f.write("\n")

        f.write("CONCLUSION\n" + "-" * 20 + "\n")
        f.write(notes["sections"]["conclusion"] + "\n")

    subprocess.run(['open', filepath])
    return f"Lab report exported to your Desktop as {filename} sir."
