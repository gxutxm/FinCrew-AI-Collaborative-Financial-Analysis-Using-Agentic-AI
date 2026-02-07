"""
PDF REPORT GENERATOR
=====================
Creates a professional PDF report with text and charts.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
import os
from datetime import datetime


def generate_pdf_report(
    ticker: str,
    start_date: str,
    end_date: str,
    market_data: dict,
    quant_data: dict,
    charts_dir: str = "data_analyst_agent/outputs",
    output_dir: str = "reports"
) -> str:
    """
    Generate a professional PDF report.
    
    Returns:
        Path to generated PDF
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{ticker}_report_{end_date}.pdf"
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#1a365d')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=HexColor('#2c5282')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=14
    )
    
    # Build content
    story = []
    
    # === TITLE PAGE ===
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(f"Financial Analysis Report", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"<b>{ticker}</b>", ParagraphStyle('Ticker', parent=styles['Heading1'], fontSize=36, textColor=HexColor('#2b6cb0'))))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Analysis Period: {start_date} to {end_date}", body_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", body_style))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Prepared by FinCrew AI", body_style))
    story.append(PageBreak())
    
    # === EXECUTIVE SUMMARY ===
    story.append(Paragraph("Executive Summary", title_style))
    
    # Market Sentiment Box
    sentiment = market_data.get('sentiment', 'N/A')
    confidence = market_data.get('confidence_score', 0)
    
    sentiment_color = '#38a169' if sentiment == 'Bullish' else '#e53e3e' if sentiment == 'Bearish' else '#718096'
    
    story.append(Paragraph("Market Sentiment", heading_style))
    story.append(Paragraph(f"<b>Overall Signal:</b> <font color='{sentiment_color}'>{sentiment}</font>", body_style))
    story.append(Paragraph(f"<b>Confidence Score:</b> {confidence:.0%}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Key Metrics Table
    story.append(Paragraph("Key Metrics", heading_style))
    
    metrics_data = [
        ['Metric', 'Value'],
        ['Average Return', f"{quant_data.get('avg_return', 0)*100:.2f}%"],
        ['Annual Volatility', f"{quant_data.get('volatility', 0)*100:.2f}%"],
        ['RSI', f"{quant_data.get('RSI', 'N/A')}"],
        ['Max Drawdown', f"{quant_data.get('max_drawdown', 0)*100:.2f}%"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0'))
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Points
    story.append(Paragraph("Key Highlights", heading_style))
    for point in market_data.get('summary', []):
        story.append(Paragraph(f"• {point}", body_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Risks
    story.append(Paragraph("Key Risks", heading_style))
    for risk in market_data.get('key_risks', []):
        story.append(Paragraph(f"• {risk}", body_style))
    
    story.append(PageBreak())
    
    # === CHARTS PAGE ===
    story.append(Paragraph("Technical Analysis", title_style))
    
    # Price Chart
    price_chart = f"{charts_dir}/{ticker}_price.png"
    if os.path.exists(price_chart):
        story.append(Paragraph("Price Chart with Moving Averages", heading_style))
        story.append(Image(price_chart, width=6*inch, height=3*inch))
        story.append(Spacer(1, 0.3*inch))
    
    # RSI Chart
    rsi_chart = f"{charts_dir}/{ticker}_rsi.png"
    if os.path.exists(rsi_chart):
        story.append(Paragraph("Relative Strength Index (RSI)", heading_style))
        story.append(Image(rsi_chart, width=6*inch, height=2*inch))
        story.append(Spacer(1, 0.3*inch))
    
    # Drawdown Chart
    drawdown_chart = f"{charts_dir}/{ticker}_drawdown.png"
    if os.path.exists(drawdown_chart):
        story.append(Paragraph("Drawdown Analysis", heading_style))
        story.append(Image(drawdown_chart, width=6*inch, height=2*inch))
    
    story.append(PageBreak())
    
    # === DISCLAIMER ===
    story.append(Paragraph("Disclaimer", heading_style))
    disclaimer = """
    This report is generated automatically by FinCrew AI and is for informational purposes only. 
    It does not constitute financial advice, investment recommendations, or an offer to buy or sell securities. 
    Past performance is not indicative of future results. Always consult with a qualified financial advisor 
    before making investment decisions.
    """
    story.append(Paragraph(disclaimer, ParagraphStyle('Disclaimer', parent=body_style, fontSize=9, textColor=HexColor('#718096'))))
    
    # Build PDF
    doc.build(story)
    
    return filename