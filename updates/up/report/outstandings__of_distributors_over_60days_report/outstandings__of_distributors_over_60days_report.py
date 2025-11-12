import frappe
from frappe.utils import get_first_day, get_last_day, nowdate
from datetime import datetime

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {"label": "Distributor", "fieldname": "distributor", "fieldtype": "Link", "options": "Customer", "width": 220},
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 220},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 180},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 130},
        {"label": "Outstanding Amount", "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 160},
        {"label": "Days Overdue", "fieldname": "days_overdue", "fieldtype": "Int", "width": 130},
    ]


def get_data(filters):
    # Extract month-year from filter
    selected_month = filters.get("month")
    if not selected_month:
        selected_month = datetime.today().strftime("%Y-%m")  # default to current month

    # Calculate first and last day of the selected month
    from_date = get_first_day(selected_month + "-01")
    to_date = get_last_day(selected_month + "-01")

    query = f"""
        SELECT
            si.customer AS distributor,
            si.customer_name,
            si.company,
            si.posting_date,
            si.outstanding_amount,
            DATEDIFF(CURDATE(), si.posting_date) AS days_overdue
        FROM
            `tabSales Invoice` si
        WHERE
            si.outstanding_amount > 0
            AND DATEDIFF(CURDATE(), si.posting_date) > 60
            AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
        ORDER BY
            si.posting_date DESC
    """

    return frappe.db.sql(query, {"from_date": from_date, "to_date": to_date}, as_dict=True)
