"""
pdf_report.py – Professional PDF report generation using fpdf2.
Generates a multi-page branded PDF with summary, tables, and insights.
"""
import io
from fpdf import FPDF
from datetime import datetime


class EduRiskPDF(FPDF):
    """Custom PDF class with branded header/footer."""

    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(79, 70, 229)  # Indigo
        self.cell(0, 8, 'EDURISK AI', align='L')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(100, 116, 139)  # Slate
        self.cell(0, 8, f'Report Generated: {datetime.now().strftime("%d %b %Y, %I:%M %p")}', align='R', new_x="LMARGIN", new_y="NEXT")
        # Line
        self.set_draw_color(79, 70, 229)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'EDURISK AI - Student Performance Early Warning System  |  Page {self.page_no()}/{{nb}}',
                  align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(15, 23, 42)  # Slate-900
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(226, 232, 240)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def key_value(self, key, value, indent=10):
        self.set_x(indent)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(100, 116, 139)
        self.cell(55, 6, key)
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(15, 23, 42)
        self.cell(0, 6, str(value), new_x="LMARGIN", new_y="NEXT")

    def risk_badge(self, risk_level):
        colors = {
            'High Risk': (220, 38, 38),
            'Medium Risk': (217, 119, 6),
            'Low Risk': (5, 150, 105),
        }
        r, g, b = colors.get(risk_level, (148, 163, 184))
        self.set_fill_color(r, g, b)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 7)
        w = self.get_string_width(risk_level) + 6
        self.cell(w, 5, risk_level, fill=True, align='C')
        self.set_text_color(15, 23, 42)


def generate_pdf_report(df, mapping, subjects):
    """
    Generate a comprehensive PDF report.
    Returns bytes of the PDF.
    """
    pdf = EduRiskPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ═══════════════════════════════════════════
    # PAGE 1: EXECUTIVE SUMMARY
    # ═══════════════════════════════════════════
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 12, 'Student Performance Analysis Report', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, 'Early Warning System - Comprehensive Analysis', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Summary metrics
    total = len(df)
    high = len(df[df['final_risk'] == 'High Risk'])
    medium = len(df[df['final_risk'] == 'Medium Risk'])
    low = len(df[df['final_risk'] == 'Low Risk'])
    avg_score = df['avg_percentage'].mean() if 'avg_percentage' in df.columns else 0

    pdf.section_title('Executive Summary')
    pdf.key_value('Total Students Analyzed', f'{total:,}')
    pdf.key_value('Average Score', f'{avg_score:.1f}%')
    pdf.key_value('High Risk Students', f'{high}  ({high/total*100:.1f}%)' if total > 0 else '0')
    pdf.key_value('Medium Risk Students', f'{medium}  ({medium/total*100:.1f}%)' if total > 0 else '0')
    pdf.key_value('Low Risk Students', f'{low}  ({low/total*100:.1f}%)' if total > 0 else '0')

    att_col = mapping.get('attendance')
    if att_col and att_col in df.columns:
        pdf.key_value('Average Attendance', f'{df[att_col].mean():.1f}%')

    pdf.ln(6)

    # Subject averages
    pdf.section_title('Subject-wise Performance')
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in df.columns:
            avg = df[pct_col].mean()
            fail_pct = (df[pct_col] < 40).mean() * 100
            pdf.key_value(sub, f'{avg:.1f}% avg  |  {fail_pct:.0f}% below passing')

    # ═══════════════════════════════════════════
    # PAGE 2: AT-RISK STUDENTS
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('At-Risk Student List')

    name_col = mapping.get('name', 'name')
    class_col = mapping.get('class')

    risk_df = df[df['final_risk'].isin(['High Risk', 'Medium Risk'])].sort_values(
        'risk_score', ascending=False
    ).head(50)

    if len(risk_df) == 0:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, 'No at-risk students identified.', new_x="LMARGIN", new_y="NEXT")
    else:
        # Table header
        pdf.set_font('Helvetica', 'B', 8)
        pdf.set_fill_color(248, 250, 252)
        pdf.set_text_color(51, 65, 85)

        col_widths = [8, 45, 18, 18, 18, 25, 58]
        headers = ['#', 'Name', 'Class', 'Avg %', 'Risk', 'Level', 'Reason']
        for i, h in enumerate(headers):
            pdf.cell(col_widths[i], 7, h, border=1, fill=True, align='C')
        pdf.ln()

        # Table rows
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(15, 23, 42)
        for idx, (_, row) in enumerate(risk_df.iterrows(), 1):
            if pdf.get_y() > 260:
                pdf.add_page()
                pdf.section_title('At-Risk Student List (continued)')
                pdf.set_font('Helvetica', 'B', 8)
                pdf.set_fill_color(248, 250, 252)
                pdf.set_text_color(51, 65, 85)
                for i, h in enumerate(headers):
                    pdf.cell(col_widths[i], 7, h, border=1, fill=True, align='C')
                pdf.ln()
                pdf.set_font('Helvetica', '', 7)
                pdf.set_text_color(15, 23, 42)

            name = str(row.get(name_col, 'N/A'))[:22]
            cls = str(row.get(class_col, '')) if class_col else ''
            avg = f"{row.get('avg_percentage', 0):.0f}%"
            risk_score = f"{row.get('risk_score', 0):.0f}"
            level = str(row.get('final_risk', ''))
            reasons = str(row.get('risk_reasons', ''))[:40]

            pdf.cell(col_widths[0], 6, str(idx), border=1, align='C')
            pdf.cell(col_widths[1], 6, name, border=1)
            pdf.cell(col_widths[2], 6, cls, border=1, align='C')
            pdf.cell(col_widths[3], 6, avg, border=1, align='C')
            pdf.cell(col_widths[4], 6, risk_score, border=1, align='C')
            pdf.cell(col_widths[5], 6, level, border=1, align='C')
            pdf.cell(col_widths[6], 6, reasons, border=1)
            pdf.ln()

    # ═══════════════════════════════════════════
    # PAGE 3: KEY FINDINGS
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('Key Findings & Recommendations')

    findings = []
    if high > 0:
        findings.append(f'{high} students require immediate intervention (High Risk).')
    if medium > 0:
        findings.append(f'{medium} students should be monitored closely (Medium Risk).')

    # Weakest subject
    subject_avgs = {}
    for sub in subjects:
        pct_col = f"{sub}_pct"
        if pct_col in df.columns:
            subject_avgs[sub] = df[pct_col].mean()
    if subject_avgs:
        weakest = min(subject_avgs, key=subject_avgs.get)
        findings.append(f'{weakest} is the weakest subject (avg: {subject_avgs[weakest]:.1f}%). '
                        f'Consider curriculum review and additional teaching resources.')

    if att_col and att_col in df.columns:
        low_att_count = (df[att_col] < 60).sum()
        if low_att_count > 0:
            findings.append(f'{low_att_count} students have attendance below 60%. '
                            f'Attendance-improvement programs are recommended.')

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(30, 41, 59)
    for i, finding in enumerate(findings, 1):
        pdf.set_x(12)
        pdf.multi_cell(0, 5.5, f'{i}. {finding}')
        pdf.ln(2)

    # Recommendations
    pdf.ln(4)
    pdf.section_title('Recommended Actions')
    recommendations = [
        'Schedule parent-teacher meetings for all High Risk students within 2 weeks.',
        'Implement peer tutoring programs for students weak in multiple subjects.',
        'Review teaching methodologies for subjects with high failure rates.',
        'Establish weekly attendance monitoring for students below 60% attendance.',
        'Create Individualized Learning Plans (ILPs) for students with z-scores below -1.5.',
        'Consider professional counseling referrals for students failing all subjects.',
    ]
    pdf.set_font('Helvetica', '', 9)
    for rec in recommendations:
        pdf.set_x(12)
        pdf.multi_cell(0, 5.5, f'- {rec}')
        pdf.ln(1)

    # ── Output ──
    return bytes(pdf.output())
