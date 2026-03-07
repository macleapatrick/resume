from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# --- CONFIG ---
OUTPUT = "/mnt/user-data/outputs/patrick_maclea_resume.pdf"
W, H = letter

# Colors
SIDEBAR_TOP = HexColor("#1E272E")
SIDEBAR_BOT = HexColor("#2D3436")
SIDEBAR_TEXT = HexColor("#E8E8E8")
SIDEBAR_ACCENT = HexColor("#00B894")
SIDEBAR_MUTED = HexColor("#A0A0A0")
MAIN_HEADING = HexColor("#1E272E")
MAIN_TEXT = HexColor("#333333")
DIVIDER = HexColor("#00B894")
LIGHT_GRAY = HexColor("#777777")
BULLET_COLOR = HexColor("#00B894")
ICON_BG = HexColor("#00B894")

# Layout
SIDEBAR_W = 2.4 * inch
MARGIN = 0.4 * inch
MAIN_X = SIDEBAR_W + MARGIN + 0.1 * inch
MAIN_W = W - MAIN_X - MARGIN * 0.9

c = canvas.Canvas(OUTPUT, pagesize=letter)

# ============================================================
# LEFT SIDEBAR — gradient effect via stacked rects
# ============================================================
num_bands = 40
band_h = H / num_bands
for i in range(num_bands):
    t = i / (num_bands - 1)
    r = 0x1E + (0x2D - 0x1E) * t
    g = 0x27 + (0x34 - 0x27) * t
    b_val = 0x2E + (0x36 - 0x2E) * t
    c.setFillColor(HexColor(f"#{int(r):02x}{int(g):02x}{int(b_val):02x}"))
    band_y = H - (i + 1) * band_h
    c.rect(0, band_y, SIDEBAR_W, band_h + 0.5, fill=1, stroke=0)

# Subtle accent strip on right edge of sidebar
c.setFillColor(SIDEBAR_ACCENT)
c.rect(SIDEBAR_W - 2, 0, 2, H, fill=1, stroke=0)

sx = MARGIN * 0.8
sidebar_right = SIDEBAR_W - sx - 0.06 * inch
y = H - 0.55 * inch

# --- Name ---
c.setFillColor(HexColor("#FFFFFF"))
c.setFont("Helvetica-Bold", 18)
c.drawString(sx, y, "PATRICK")
y -= 0.26 * inch
c.drawString(sx, y, "MACLEA")
y -= 0.32 * inch

c.setFillColor(SIDEBAR_ACCENT)
c.setFont("Helvetica", 7.5)
title_text = "SENIOR DATA SCIENTIST"
spaced = " ".join(title_text)
c.drawString(sx, y, spaced)
y -= 0.16 * inch

# Accent line
c.setStrokeColor(SIDEBAR_ACCENT)
c.setLineWidth(1)
c.line(sx, y, sidebar_right, y)
y -= 0.35 * inch


# --- Helpers ---
def draw_section_icon(icon_char, x_pos, y_pos, title_font_size, icon_font_size=7):
    """Draw icon circle vertically centered with title text baseline at y_pos."""
    # Center of cap-height: baseline + ~35% of font size
    text_center_y = y_pos + title_font_size * 0.35
    r = 0.085 * inch
    cx = x_pos + r
    cy = text_center_y
    c.setFillColor(ICON_BG)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", icon_font_size)
    tw = c.stringWidth(icon_char, "Helvetica-Bold", icon_font_size)
    c.drawString(cx - tw / 2, cy - icon_font_size * 0.35, icon_char)


def sidebar_section(title, y_pos, icon_char=None):
    font_size = 9
    if icon_char:
        draw_section_icon(icon_char, sx, y_pos, title_font_size=font_size)
        c.setFillColor(SIDEBAR_ACCENT)
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(sx + 0.25 * inch, y_pos, title.upper())
    else:
        c.setFillColor(SIDEBAR_ACCENT)
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(sx, y_pos, title.upper())
    y_pos -= 0.1 * inch
    c.setStrokeColor(HexColor("#3D4A4F"))
    c.setLineWidth(0.4)
    c.line(sx, y_pos, sidebar_right, y_pos)
    y_pos -= 0.22 * inch
    return y_pos


def sidebar_contact_item(label, y_pos, icon_char, url=None):
    c.setFillColor(SIDEBAR_ACCENT)
    c.setFont("Helvetica", 8)
    c.drawString(sx + 0.04 * inch, y_pos, icon_char)
    c.setFillColor(SIDEBAR_TEXT)
    c.setFont("Helvetica", 8.5)
    text_x = sx + 0.2 * inch
    c.drawString(text_x, y_pos, label)
    if url:
        tw = c.stringWidth(label, "Helvetica", 8.5)
        c.linkURL(url, (text_x, y_pos - 2, text_x + tw, y_pos + 10), relative=0)
    y_pos -= 0.21 * inch
    return y_pos


def sidebar_skill_category(cat_name, skills_list, y_pos):
    c.setFillColor(SIDEBAR_ACCENT)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(sx, y_pos, cat_name)
    y_pos -= 0.15 * inch
    style = ParagraphStyle(
        'skill',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=SIDEBAR_TEXT,
    )
    text = ", ".join(skills_list)
    p = Paragraph(text, style)
    pw, ph = p.wrap(sidebar_right - sx, 200)
    p.drawOn(c, sx, y_pos - ph + 9)
    y_pos = y_pos - ph - 0.04 * inch
    return y_pos


# Consistent gap between sidebar sections
SIDEBAR_GAP = 0.2 * inch

# --- Contact ---
y = sidebar_section("Contact", y, icon_char="@")
y = sidebar_contact_item("macleapatrick@gmail.com", y, "\u2709")
y = sidebar_contact_item("(781) 361-4045", y, "\u260E")
y = sidebar_contact_item("Boston, MA", y, "\u25C8")
y = sidebar_contact_item("LinkedIn", y, "\u25B6", url="https://www.linkedin.com/in/patrick-maclea-5460b098/")
y = sidebar_contact_item("GitHub", y, "\u25B6", url="https://github.com/macleapatrick")
y -= SIDEBAR_GAP

# --- Education ---
y = sidebar_section("Education", y, icon_char="E")
c.setFillColor(SIDEBAR_TEXT)
c.setFont("Helvetica-Bold", 8)
c.drawString(sx, y, "University of New Hampshire")
y -= 0.16 * inch
c.setFont("Helvetica", 7.5)
c.drawString(sx, y, "B.Sc. Mechanical Engineering")
y -= 0.14 * inch
c.setFillColor(SIDEBAR_MUTED)
c.setFont("Helvetica-Oblique", 7)
c.drawString(sx, y, "Cum Laude, 2018")
y -= SIDEBAR_GAP + 0.14 * inch

# --- Skills ---
y = sidebar_section("Skills", y, icon_char="S")

y = sidebar_skill_category("Machine Learning & AI", [
    "PyTorch", "TensorFlow", "Scikit-Learn",
    "MLflow", "LangGraph", "LLM Pipelines",
    "Knowledge Graphs", "Deep Learning", "NLP", "RAG",
    "Embeddings", "XGBoost", "Feature Engineering", "Model Evaluation"
], y)

y = sidebar_skill_category("Data & Systems", [
    "SQL", "Pandas", "NumPy", "MongoDB", "Kafka",
    "ETL Pipelines", "Streaming Data Systems"
], y)

y = sidebar_skill_category("Infrastructure", [
    "AWS", "Docker", "Terraform", "Git", "Bash"
], y)

y = sidebar_skill_category("Languages", [
    "Python", "SQL", "C/C++"
], y)

y = sidebar_skill_category("Industrial Domain", [
    "Automated Manufacturing", "Industrial Robotics",
    "PLC Controls", "Electromechanical Systems",
    "Predictive Maintenance", "MES Integration"
], y)

y -= SIDEBAR_GAP

# --- Interests ---
y = sidebar_section("Interests", y, icon_char="*")
interests_style = ParagraphStyle(
    'interests',
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    textColor=SIDEBAR_TEXT,
)
interests_text = "Skiing, Markets & Investing, Mountain Biking, Guitar"
p = Paragraph(interests_text, interests_style)
pw, ph = p.wrap(sidebar_right - sx, 200)
p.drawOn(c, sx, y - ph + 9)
y = y - ph - 0.06 * inch


# ============================================================
# MAIN CONTENT
# ============================================================
y = H - 0.55 * inch
mx = MAIN_X



def main_section(title, y_pos, icon_char=None):
    font_size = 11.5
    if icon_char:
        draw_section_icon(icon_char, mx, y_pos, title_font_size=font_size, icon_font_size=8)
        c.setFillColor(MAIN_HEADING)
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(mx + 0.28 * inch, y_pos, title.upper())
    else:
        c.setFillColor(MAIN_HEADING)
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(mx, y_pos, title.upper())
    y_pos -= 0.08 * inch
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(1.2)
    c.line(mx, y_pos, mx + MAIN_W, y_pos)
    y_pos -= 0.22 * inch
    return y_pos


def draw_bullet(text, y_pos, indent=0.08 * inch):
    style = ParagraphStyle(
        'bullet',
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=MAIN_TEXT,
    )
    p = Paragraph(text, style)
    pw, ph = p.wrap(MAIN_W - 0.28 * inch, 200)
    c.setFillColor(BULLET_COLOR)
    c.setFont("Helvetica-Bold", 7)
    bullet_y = y_pos - ph + 9 + ph - 8
    c.drawString(mx + indent, bullet_y, "\u2022")
    p.drawOn(c, mx + 0.22 * inch, y_pos - ph + 9)
    y_pos = y_pos - ph - 0.02 * inch
    return y_pos


# --- Professional Summary ---
y = main_section("Professional Summary", y, icon_char="P")

summary_style = ParagraphStyle(
    'summary',
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    textColor=MAIN_TEXT,
)
summary = (
    "Senior Data Scientist with experience building production ML, NLP, and LLM systems "
    "and leading automation software at Tesla\u2019s EV manufacturing lines. Combines "
    "industrial systems expertise with modern machine learning and statistical modeling "
    "to deliver measurable business impact. Long-term focused on applying AI to "
    "transform and fully automate manufacturing."
)
p = Paragraph(summary, summary_style)
pw, ph = p.wrap(MAIN_W, 200)
p.drawOn(c, mx, y - ph + 9)
y = y - ph - 0.25 * inch

# --- Experience ---
y = main_section("Experience", y, icon_char="W")

# Standardized spacing constants for job entries
JOB_TITLE_TO_COMPANY = 0.16 * inch
COMPANY_TO_PREV = 0.14 * inch
PREV_TO_BULLETS = 0.16 * inch
COMPANY_TO_BULLETS = 0.16 * inch
BETWEEN_JOBS = 0.1 * inch


def draw_job(title, company, dates, bullets, y_pos, previous=None):
    """Draw a job entry with perfectly consistent spacing."""
    # Title + dates
    c.setFillColor(MAIN_HEADING)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(mx, y_pos, title)
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 7.5)
    dw = c.stringWidth(dates, "Helvetica", 7.5)
    c.drawString(mx + MAIN_W - dw, y_pos + 1, dates)
    y_pos -= JOB_TITLE_TO_COMPANY

    # Company
    c.setFillColor(BULLET_COLOR)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(mx, y_pos, company)

    if previous:
        y_pos -= COMPANY_TO_PREV
        c.setFillColor(LIGHT_GRAY)
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(mx, y_pos, f"Previously: {previous}")
        y_pos -= PREV_TO_BULLETS
    else:
        y_pos -= COMPANY_TO_BULLETS

    # Bullets
    for b in bullets:
        y_pos = draw_bullet(b, y_pos)

    return y_pos


# ---- Recorded Future ----
y = draw_job(
    "Senior Data Scientist",
    "Recorded Future",
    "Jan 2025 \u2013 Present",
    [
        "Promoted twice within first year, from intern to senior data scientist.",
        "Built NLP-driven synonymization of software product entities in the knowledge graph using text classification and embedding models, increasing client coverage of software vulnerability-to-watchlist connections by 10%.",
        "Architected a multi-stage NLP and ML pipeline for domain ownership resolution using transformer models, large-scale internet metadata, and active-learning training loops, expanding TPI coverage of domain ownership by 10% and growing.",
        "Built end-to-end entity resolution systems combining knowledge-graph ontologies, LLM-generated training data, and ML scoring to link entities across Recorded Future and partner platforms \u2014 automatically resolving ~75% of entities from the partner dataset to Recorded Future\u2019s intelligence graph at 98% precision, enabling cross-platform data and frontend integration.",
        "Developed internal data and ML platform tooling (ETL pipelines, MLflow integration, LangGraph orchestration, CI/CD workflows) that standardized how the team builds and ships ML and LLM systems.",
    ],
    y,
    previous="Data Engineer, Data Science Intern",
)
y -= BETWEEN_JOBS

# ---- Tesla ----
y = draw_job(
    "Sr. Automation Software Engineer, Team Lead",
    "Tesla",
    "2020 \u2013 Dec 2023",
    [
        "Led a cross-functional team managing software, controls, and data systems for fully automated EV battery manufacturing equipment.",
        "Improved manufacturing cycle time by 20% (+1,000 packs/week) through software-driven process optimizations.",
        "Designed conveyance optimization algorithms, reducing product starvation to the next production zone from 5% to 2%.",
        "Drove data-driven process improvements using statistical analysis that increased equipment availability from ~80% to 90% across the production zone.",
        "Developed Python REST APIs, real-time data visualization dashboards, and anomaly detection systems that connected equipment data to MES and monitoring platforms \u2014 enabling bottleneck analysis, quality issue identification, and predictive maintenance across the production zone.",
        "Led Beckhoff PLC development standards and mentored engineers and technicians on troubleshooting across the production line.",
    ],
    y,
    previous="Automation Software Engineer",
)
y -= BETWEEN_JOBS

# ---- Superior Controls ----
y = draw_job(
    "Automation Engineer",
    "Superior Controls",
    "2018 \u2013 2020",
    [
        "Developed and integrated Allen-Bradley PLC ControlLogix software for biopharma manufacturing processes, including authoring design specifications and validation protocols.",
        "Created automated PLC code generation tooling from functional specifications, reducing manual programming effort.",
        "Led customer-facing requirements gathering, functional specification development, and acceptance testing.",
    ],
    y,
)


# ============================================================
c.save()
print(f"Resume saved to {OUTPUT}")
print(f"Final y position: {y:.1f} (page bottom is 0)")
