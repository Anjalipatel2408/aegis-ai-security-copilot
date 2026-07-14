from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

REPORTS_DIR = "generated_reports"

def generate_incident_report(log_filename, attacks):
    os.makedirs(REPORTS_DIR, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(REPORTS_DIR, f"incident_report_{timestamp}.pdf")

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AEGIS AI – Security Incident Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Log File: {log_filename}", styles["Normal"]))
    elements.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]))
    elements.append(Paragraph(f"Total Attacks Detected: {len(attacks)}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    table_data = [["IP Address", "Endpoint", "Attack Type", "MITRE Technique"]]
    for a in attacks:
        table_data.append([
            a.get("ip_address", "N/A"),
            a.get("endpoint", "N/A"),
            a.get("attack_type", "N/A"),
            f"{a.get('mitre_technique_id', '')} - {a.get('mitre_technique_name', '')}"
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
    ]))
    elements.append(table)

    doc.build(elements)
    return file_path