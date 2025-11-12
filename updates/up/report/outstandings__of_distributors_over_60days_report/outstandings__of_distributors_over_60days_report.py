import frappe
from frappe.utils import today

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Customer Code", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
        {"label": "No. of Invoices", "fieldname": "invoice_count", "fieldtype": "Int", "width": 120},
        {
            "label": "Total Outstanding Amount (60+ Days)",
            "fieldname": "total_outstanding",
            "fieldtype": "Currency",
            "options": "Company:company:default_currency",
            "width": 200,
        },
        {"label": "Avg Days Overdue", "fieldname": "avg_days_overdue", "fieldtype": "Float", "width": 120},
    ]


def get_data(filters):
    query = """
        SELECT
            si.customer AS customer,
            c.customer_name AS customer_name,
            COUNT(si.name) AS invoice_count,
            SUM(si.outstanding_amount) AS total_outstanding,
            ROUND(AVG(DATEDIFF(CURDATE(), si.due_date)), 1) AS avg_days_overdue
        FROM
            `tabSales Invoice` si
        JOIN
            `tabCustomer` c ON si.customer = c.name
        WHERE
            si.docstatus = 1
            AND si.outstanding_amount > 0
            AND DATEDIFF(CURDATE(), si.due_date) > 60
            AND c.customer_group = 'Distributor'
        GROUP BY
            si.customer, c.customer_name
        ORDER BY
            total_outstanding DESC
    """

    results = frappe.db.sql(query, as_dict=True)

    # Make Total Outstanding clickable → opens filtered Sales Invoice list
    for row in results:
        row["total_outstanding"] = frappe.utils.get_link_to_form(
            "Sales Invoice",
            None,
            label=frappe.bold(f"{row['total_outstanding']:,}"),
            filters={
                "customer": row["customer"],
                "outstanding_amount": (">", 0),
                "due_date": ("<", frappe.utils.add_days(today(), -60)),
            },
        )

    return results
