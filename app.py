from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import pandas as pd
import os
import json
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

# Official BGMI Point System
POINT_SYSTEM = {1: 10, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 1, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}

# Team Data for Each Group
GROUP_A_TEAMS = [
    "AM BOYZZ Esports", "Team LOSS_X", "MITxSQUADUP", "BOB ESPORTS",
    "Team_OG", "Alpha_x", "TSM", "Team Gardians",
    "Team TED", "INSAS ESPORTS", "CFS ESPORTS", "XSPARK",
    "Team Swarajya", "Team Homelanders", "Team NV", "IMMORTAL THUNDERS"
]

GROUP_B_TEAMS = [
    "RushX", "ALPHA GAMING", "Team Arise", "97",
    "Team Trust", "Strawts", "Team Shadow", "Team Ethnic",
    "Curse breakers", "TEAM APEX", "1v4", "AERO SCISSORS ESPORTS",
    "Inferno 5", "6INE", "TEAM RAVEN ESPORTS", "SelfishPlayers"
]

GROUP_C_TEAMS = [
    "Team Wushang", "Team Xtreme", "Team Beast", "FST Fraggers",
    "VP GAMING", "Team_OG", "Chaos Knight", "KALKI ESPORTS",
    "Divas", "TEAM NS", "Team Nirbhay", "Team Sword",
    "Flow Esport", "Team Yaurus", "Team KUKD"
]

GROUPS = {
    'A': GROUP_A_TEAMS,
    'B': GROUP_B_TEAMS,
    'C': GROUP_C_TEAMS
}

def create_data_folders():
    """Create separate folders for each group's match data"""
    for group in ['A', 'B', 'C']:
        folder = f"Group_{group}_Data"
        if not os.path.exists(folder):
            os.makedirs(folder)

def generate_group_leaderboard(group):
    """Generate leaderboard for a specific group"""
    folder = f"Group_{group}_Data"
    if not os.path.exists(folder):
        return None
    
    files = [f for f in os.listdir(folder) if f.startswith(f'group_{group}_match_') and f.endswith('.csv')]
    
    if not files:
        return None

    # Combine all match data
    all_matches = pd.concat([pd.read_csv(os.path.join(folder, f)) for f in files])
    
    # Aggregate data by Team
    leaderboard = all_matches.groupby('Team').agg({
        'WWCD': 'sum',
        'PLCT': 'sum',
        'Kills': 'sum'
    }).reset_index()

    # Calculate Total
    leaderboard['TOTAL'] = leaderboard['PLCT'] + leaderboard['Kills']
    leaderboard['Group'] = group
    
    # Sort by Total, then Kills, then WWCD
    leaderboard = leaderboard.sort_values(by=['TOTAL', 'Kills', 'WWCD'], ascending=False)
    
    # Add Rank Column
    leaderboard.insert(0, 'RANK', range(1, len(leaderboard) + 1))
    
    return leaderboard

def get_match_count(group):
    """Get the number of matches for a group"""
    folder = f"Group_{group}_Data"
    if not os.path.exists(folder):
        return 0
    files = [f for f in os.listdir(folder) if f.startswith(f'group_{group}_match_') and f.endswith('.csv')]
    return len(files)

@app.route('/')
def index():
    """Main dashboard"""
    create_data_folders()
    
    match_counts = {
        'A': get_match_count('A'),
        'B': get_match_count('B'),
        'C': get_match_count('C')
    }
    
    return render_template('index.html', match_counts=match_counts)

@app.route('/add-match/<group>')
def add_match_page(group):
    """Page to add match data"""
    if group not in ['A', 'B', 'C']:
        return redirect(url_for('index'))
    
    match_no = get_match_count(group) + 1
    teams = GROUPS[group]
    
    return render_template('add_match.html', group=group, match_no=match_no, teams=teams)

@app.route('/api/save-match', methods=['POST'])
def save_match():
    """API endpoint to save match data"""
    data = request.json
    group = data.get('group')
    match_data = data.get('match_data')
    
    if not group or not match_data:
        return jsonify({'success': False, 'message': 'Invalid data'})
    
    folder = f"Group_{group}_Data"
    match_no = get_match_count(group) + 1
    
    # Prepare DataFrame
    teams_data = []
    for entry in match_data:
        teams_data.append({
            'Group': group,
            'Team': entry['team'],
            'Rank': entry['rank'],
            'Kills': entry['kills'],
            'WWCD': 1 if entry['rank'] == 1 else 0,
            'PLCT': POINT_SYSTEM.get(entry['rank'], 0)
        })
    
    df = pd.DataFrame(teams_data)
    filepath = os.path.join(folder, f"group_{group}_match_{match_no}.csv")
    df.to_csv(filepath, index=False)
    
    return jsonify({'success': True, 'message': f'Match {match_no} saved successfully!', 'match_no': match_no})

@app.route('/leaderboard/<group>')
def leaderboard(group):
    """Display leaderboard for a specific group"""
    if group not in ['A', 'B', 'C']:
        return redirect(url_for('index'))
    
    lb = generate_group_leaderboard(group)
    
    if lb is None:
        leaderboard_data = []
    else:
        leaderboard_data = lb.to_dict('records')
    
    match_count = get_match_count(group)
    
    return render_template('leaderboard.html', 
                          group=group, 
                          leaderboard=leaderboard_data,
                          match_count=match_count)

@app.route('/combined-leaderboard')
def combined_leaderboard():
    """Display combined leaderboard from all groups"""
    all_leaderboards = []
    
    for group in ['A', 'B', 'C']:
        lb = generate_group_leaderboard(group)
        if lb is not None:
            all_leaderboards.append(lb)
    
    if not all_leaderboards:
        combined_data = []
    else:
        # Combine all groups
        combined = pd.concat(all_leaderboards, ignore_index=True)
        
        # Sort by Total, then Kills, then WWCD
        combined = combined.sort_values(by=['TOTAL', 'Kills', 'WWCD'], ascending=False)
        
        # Reset Rank
        combined['RANK'] = range(1, len(combined) + 1)
        
        combined_data = combined.to_dict('records')
    
    total_matches = sum([get_match_count(g) for g in ['A', 'B', 'C']])
    
    return render_template('combined_leaderboard.html', 
                          leaderboard=combined_data,
                          total_matches=total_matches)

def generate_leaderboard_pdf(group, leaderboard_df, match_count):
    """Generate PDF for group leaderboard"""
    buffer = BytesIO()
    
    # Create PDF in portrait mode
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.5*inch, rightMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title Style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#58a6ff'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Subtitle Style
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#8b949e'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Add Title
    title = Paragraph(f"AAROHAN BGMI ELIMS - GROUP {group}", title_style)
    elements.append(title)
    
    # Add Subtitle
    subtitle = Paragraph(f"Points Table | {match_count} Matches | {datetime.now().strftime('%B %d, %Y')}", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.25*inch))
    
    # Prepare table data
    table_data = [['RANK', 'TEAM NAME', 'WWCD', 'PLCT.', 'KILLS', 'TOTAL']]
    
    for _, row in leaderboard_df.iterrows():
        wwcd_val = int(row['WWCD']) if row['WWCD'] > 0 else '-'
        table_data.append([
            int(row['RANK']),
            row['Team'],
            wwcd_val,
            int(row['PLCT']),
            int(row['Kills']),
            int(row['TOTAL'])
        ])
    
    # Create table with optimized column widths for portrait
    table = Table(table_data, colWidths=[0.5*inch, 3.5*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.7*inch], repeatRows=1)
    
    # Table Style
    table_style = TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c2128')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#58a6ff')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#161b22')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#e6edf3')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#30363d')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#58a6ff')),
        
        # Team name left aligned
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('LEFTPADDING', (1, 1), (1, -1), 12),
        
        # Highlight top 3
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#1c3d5a')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#1a3851')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#183349')),
        
        # Total column bold
        ('FONTNAME', (5, 1), (5, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (5, 1), (5, -1), colors.HexColor('#58a6ff')),
    ])
    
    table.setStyle(table_style)
    elements.append(table)
    
    # Add footer
    elements.append(Spacer(1, 0.25*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#8b949e'),
        alignment=TA_CENTER
    )
    footer = Paragraph("AAROHAN BGMI ELIMS - Official Tournament Points Table", footer_style)
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

@app.route('/download-leaderboard/<group>')
def download_leaderboard(group):
    """Download leaderboard as PDF"""
    if group not in ['A', 'B', 'C']:
        return redirect(url_for('index'))
    
    lb = generate_group_leaderboard(group)
    
    if lb is None:
        return "No data available", 404
    
    match_count = get_match_count(group)
    pdf_buffer = generate_leaderboard_pdf(group, lb, match_count)
    
    filename = f"AAROHAN_BGMI_Group_{group}_Leaderboard.pdf"
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

@app.route('/download-combined-leaderboard')
def download_combined_leaderboard():
    """Download combined leaderboard as PDF"""
    all_leaderboards = []
    
    for group in ['A', 'B', 'C']:
        lb = generate_group_leaderboard(group)
        if lb is not None:
            all_leaderboards.append(lb)
    
    if not all_leaderboards:
        return "No data available", 404
    
    # Combine all groups
    combined = pd.concat(all_leaderboards, ignore_index=True)
    combined = combined.sort_values(by=['TOTAL', 'Kills', 'WWCD'], ascending=False)
    combined['RANK'] = range(1, len(combined) + 1)
    
    total_matches = sum([get_match_count(g) for g in ['A', 'B', 'C']])
    
    # Generate PDF in portrait orientation
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.5*inch, rightMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#58a6ff'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#8b949e'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    title = Paragraph("AAROHAN BGMI ELIMS - OVERALL STANDINGS", title_style)
    elements.append(title)
    
    subtitle = Paragraph(f"All Groups | {total_matches} Matches | {datetime.now().strftime('%B %d, %Y')}", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.25*inch))
    
    # Table data with group column
    table_data = [['RANK', 'TEAM NAME', 'GROUP', 'WWCD', 'PLCT.', 'KILLS', 'TOTAL']]
    
    for _, row in combined.iterrows():
        wwcd_val = int(row['WWCD']) if row['WWCD'] > 0 else '-'
        table_data.append([
            int(row['RANK']),
            row['Team'],
            row['Group'],
            wwcd_val,
            int(row['PLCT']),
            int(row['Kills']),
            int(row['TOTAL'])
        ])
    
    table = Table(table_data, colWidths=[0.45*inch, 3.0*inch, 0.5*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.65*inch], repeatRows=1)
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c2128')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#58a6ff')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#161b22')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#e6edf3')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#30363d')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#58a6ff')),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('LEFTPADDING', (1, 1), (1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#1c3d5a')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#1a3851')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#183349')),
        ('FONTNAME', (6, 1), (6, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (6, 1), (6, -1), colors.HexColor('#58a6ff')),
    ])
    
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 0.25*inch))
    
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9,
                                  textColor=colors.HexColor('#8b949e'), alignment=TA_CENTER)
    footer = Paragraph("AAROHAN BGMI ELIMS - Official Tournament Points Table", footer_style)
    elements.append(footer)
    
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True,
                    download_name="AAROHAN_BGMI_Combined_Leaderboard.pdf",
                    mimetype='application/pdf')

if __name__ == '__main__':
    create_data_folders()
    app.run(debug=True, host='0.0.0.0', port=5000)
