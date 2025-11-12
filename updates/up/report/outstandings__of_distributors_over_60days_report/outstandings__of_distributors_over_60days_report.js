frappe.query_reports["Outstandings  Of Distributors Over 60Days-Report"] = {
    "filters": [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            reqd: 1,
            default: frappe.defaults.get_user_default("Company")
        },
        {
            fieldname: "month_date",
            label: __("Select Month"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.nowdate(),
            description: __("Select any date within the desired month")
        }
    ],

    formatter: function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "outstanding_amount" && data && data.distributor) {
            const distributor = data.distributor;
            const company = frappe.query_report.get_filter_value("company");
            const selected_date = frappe.query_report.get_filter_value("month_date");

            // derive month start & end from selected date
            const from_date = frappe.datetime.month_start(selected_date);
            const to_date = frappe.datetime.month_end(selected_date);

            const route_options = {
                customer: distributor,
                company: company,
                posting_date: ["between", [from_date, to_date]]
            };

            // clickable link
            value = `<a href="#List/Sales Invoice/List?${frappe.utils.get_query_string(route_options)}"
                      target="_blank" style="color: var(--text-on-blue); text-decoration: underline; font-weight: 500;">
                        ${data.outstanding_amount}
                     </a>`;
        }

        return value;
    }
};
