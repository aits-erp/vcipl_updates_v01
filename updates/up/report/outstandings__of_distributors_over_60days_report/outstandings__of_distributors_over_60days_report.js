// Copyright (c) 2025, Sai More
// For license information, please see license.txt

frappe.query_reports["Outstanding 60 Days Distributor"] = {
    // ----------------------------
    // 1️⃣ FILTER SECTION
    // ----------------------------
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -2),
            reqd: 0
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 0
        },
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 0
        },
        {
            fieldname: "customer_group",
            label: __("Customer Group"),
            fieldtype: "Link",
            options: "Customer Group",
            default: "Distributor",
            reqd: 0
        },
        {
            fieldname: "show_invoices",
            label: __("Show Invoice List"),
            fieldtype: "Check",
            default: 0
        }
    ],

    // ----------------------------
    // 2️⃣ ON LOAD ACTIONS
    // ----------------------------
    onload: function (report) {
        report.page.set_title(__("Outstanding (60+ Days) - Distributor"));
        frappe.msgprint({
            title: __("Note"),
            indicator: "blue",
            message: __("This report shows all Distributor customers with invoices overdue by more than 60 days.")
        });
    },

    // ----------------------------
    // 3️⃣ FORMATTERS (optional styling)
    // ----------------------------
    formatter: function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // Highlight overdue customers
        if (column.fieldname === "avg_days_overdue" && data && data.avg_days_overdue > 90) {
            value = `<span style='color:red; font-weight:600;'>${value}</span>`;
        }

        // Highlight clickable total
        if (column.fieldname === "total_outstanding") {
            value = `<span style='color:#007bff; font-weight:600; cursor:pointer;'>${value}</span>`;
        }

        return value;
    }
};
