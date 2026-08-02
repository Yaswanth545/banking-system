from io import BytesIO,StringIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib.pagesizes import A4

from accounts.models import Account
from .models import Transaction

import csv






class StatementService:

    @staticmethod
    def generate_pdf(user,start_date=None,end_date=None,):
        account = Account.objects.get(
            user=user
        )

        transactions = (
            Transaction.objects
            .filter(account=account)
            .order_by("-created_at")
        )

        if start_date:
            transactions = transactions.filter(
                created_at__date__gte=start_date
            )

        if end_date:
            transactions = transactions.filter(
                created_at__date__lte=end_date
            )

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "ABC Bank Account Statement",
                styles["Title"],
            )
        )

        elements.append(
            Spacer(
                1,
                0.25 * inch,
            )
        )

        table_data = [
            [
                "Date",
                "Transaction Type",
                "Amount (INR)",
                "Balance (INR)",
            ]
        ]

        for transaction in transactions:
            table_data.append([
                transaction.created_at.strftime("%d-%m-%Y %H:%M"),
                transaction.transaction_type,
                f"{transaction.amount:.2f}",
                f"{transaction.balance_after_transaction:.2f}",
            ])

        table = Table(table_data)

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ])
        )

        elements.append(table)

        elements.append(
            Spacer(
                1,
                0.30 * inch,
            )
        )

        elements.append(
            Paragraph(
                f"<b>Current Balance:</b> ₹ {account.balance}",
                styles["Heading2"],
            )
        )

        doc.build(elements)

        buffer.seek(0)

        return buffer
    

    @staticmethod
    def generate_csv(user,start_date=None,end_date=None,):
        account = Account.objects.get(user=user)

        transactions = (Transaction.objects.filter(account=account).order_by("-created_at"))

        if start_date:
            transactions = transactions.filter(
                created_at__date__gte=start_date
            )

        if end_date:
            transactions = transactions.filter(
                created_at__date__lte=end_date
            )

        buffer = StringIO()

        writer = csv.writer(buffer)

        writer.writerow([
            "Date",
            "Transaction Type",
            "Amount",
            "Balance",
        ])


        for transaction in transactions:
            writer.writerow([
                transaction.created_at.strftime("%d-%m-%Y %H:%M"),
                transaction.transaction_type,
                transaction.amount,
                transaction.balance_after_transaction,
            ])

        buffer.seek(0)

        return buffer