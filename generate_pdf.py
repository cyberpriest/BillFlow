from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def _build_invoice_pdf(invoice) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='InvoiceTitle', fontSize=24, leading=28, spaceAfter=18))
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=12, leading=14, spaceAfter=8, textColor=colors.HexColor('#333333'), bold=True))
    normal_style = styles['Normal']
    title_style = styles['InvoiceTitle']

    business = invoice.business
    client = invoice.client
    issue_date = invoice.issue_date.strftime('%Y-%m-%d') if invoice.issue_date else ''
    due_date = invoice.due_date.strftime('%Y-%m-%d') if invoice.due_date else 'N/A'

    elements = []
    elements.append(Paragraph('Invoice', title_style))
    elements.append(Paragraph(f'<b>Invoice #:</b> {invoice.invoice_no}', normal_style))
    elements.append(Paragraph(f'<b>Status:</b> {invoice.status}', normal_style))
    elements.append(Paragraph(f'<b>Issue Date:</b> {issue_date}', normal_style))
    elements.append(Paragraph(f'<b>Due Date:</b> {due_date}', normal_style))
    elements.append(Spacer(1, 18))

    if business:
        elements.append(Paragraph('Business', styles['Heading3']))
        elements.append(Paragraph(business.business_name or '', normal_style))
        elements.append(Paragraph(business.address or '', normal_style))
        elements.append(Paragraph(business.business_email or '', normal_style))
        elements.append(Paragraph(business.phone or '', normal_style))
        elements.append(Spacer(1, 12))

    if client:
        elements.append(Paragraph('Client', styles['Heading3']))
        elements.append(Paragraph(client.client_name or '', normal_style))
        elements.append(Paragraph(client.address or '', normal_style))
        elements.append(Paragraph(client.client_email or '', normal_style))
        elements.append(Paragraph(client.phone or '', normal_style))
        elements.append(Spacer(1, 16))

    table_data = [[
        'No.',
        'Description',
        'Quantity',
        'Unit price',
        'Line total'
    ]]

    for idx, item in enumerate(invoice.items or [], start=1):
        line_total = item.quantity * item.unit_price
        table_data.append([
            str(idx),
            item.description,
            str(item.quantity),
            format_currency(item.unit_price),
            format_currency(line_total),
        ])

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f2f2f2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ])

    invoice_table = Table(table_data, colWidths=[0.6 * inch, 3.6 * inch, 1 * inch, 1.2 * inch, 1.2 * inch])
    invoice_table.setStyle(table_style)
    elements.append(invoice_table)
    elements.append(Spacer(1, 18))

    total_value = format_currency(invoice.total or 0.0)
    total_table = Table([
        ['Total', total_value]
    ], colWidths=[5.4 * inch, 1.2 * inch])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8f8f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.grey),
    ]))
    elements.append(total_table)

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def render_invoice_pdf(invoice) -> bytes:
    return _build_invoice_pdf(invoice)

