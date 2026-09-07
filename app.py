import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    create_connection,
    create_table,
    insert_dataframe,
    fetch_data,
)

from data_generator import generate_fake_data


st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Personal Expense Tracker Dashboard")
st.markdown("---")


# ============================================================
# LOAD DATA
# ============================================================

connection = None
database_mode = False

try:
    connection = create_connection()
    cursor = connection.cursor()

    create_table(cursor)
    connection.commit()

    df = fetch_data(connection)

    if df.empty:
        df = generate_fake_data()

        insert_dataframe(cursor, df)
        connection.commit()

        df = fetch_data(connection)

    database_mode = True

except Exception:
    df = generate_fake_data()

    # Ensure Date and Month are available for dashboard analysis
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month_name()

    st.info(
        "Demo mode: displaying sample expense data. "
        "MySQL database connection is not available."
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Settings")

if st.sidebar.button("Generate New Fake Dataset"):

    df = generate_fake_data()

    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month_name()

    if database_mode:
        cursor.execute("DELETE FROM final")
        connection.commit()

        insert_dataframe(cursor, df)
        connection.commit()

        df = fetch_data(connection)

        st.sidebar.success("Database updated!")

    else:
        st.sidebar.success("New demo dataset generated!")


# ============================================================
# FILTERS
# ============================================================

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique(),
)

payment = st.sidebar.multiselect(
    "Payment Mode",
    options=df["Payment_Mode"].unique(),
    default=df["Payment_Mode"].unique(),
)

filtered = df[
    (df["Category"].isin(category))
    & (df["Payment_Mode"].isin(payment))
]


# ============================================================
# KPI
# ============================================================

total_expense = filtered["Amount"].sum()
cashback = filtered["Cashback"].sum()
transactions = len(filtered)

average = (
    filtered["Amount"].mean()
    if not filtered.empty
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Expense",
    f"₹{total_expense:,.2f}",
)

col2.metric(
    "🎁 Cashback",
    f"₹{cashback:,.2f}",
)

col3.metric(
    "🧾 Transactions",
    transactions,
)

col4.metric(
    "📊 Average Spend",
    f"₹{average:,.2f}",
)

st.markdown("---")


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "Dashboard",
        "Analytics",
        "SQL Queries",
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

with tab1:

    left, right = st.columns(2)

    monthly = (
        filtered.groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    monthly["Month"] = pd.Categorical(
        monthly["Month"],
        categories=month_order,
        ordered=True,
    )

    monthly = monthly.sort_values("Month")

    fig = px.line(
        monthly,
        x="Month",
        y="Amount",
        markers=True,
        title="Monthly Expense",
    )

    left.plotly_chart(
        fig,
        use_container_width=True,
    )

    category_chart = (
        filtered.groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_chart,
        names="Category",
        values="Amount",
        hole=0.45,
        title="Expense by Category",
    )

    right.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader("Recent Transactions")

    st.dataframe(
        filtered.sort_values(
            "Date",
            ascending=False,
        ),
        use_container_width=True,
    )


# ============================================================
# ANALYTICS
# ============================================================

with tab2:

    col1, col2 = st.columns(2)

    cashback_chart = (
        filtered.groupby("Payment_Mode")["Cashback"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        cashback_chart,
        x="Payment_Mode",
        y="Cashback",
        color="Payment_Mode",
        title="Cashback by Payment Mode",
    )

    col1.plotly_chart(
        fig,
        use_container_width=True,
    )

    payment_chart = (
        filtered.groupby("Payment_Mode")
        .size()
        .reset_index(name="Transactions")
    )

    fig = px.bar(
        payment_chart,
        x="Payment_Mode",
        y="Transactions",
        color="Payment_Mode",
        title="Transactions by Payment Mode",
    )

    col2.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader("Category Summary")

    summary = (
        filtered.groupby("Category")
        .agg(
            Total_Expense=("Amount", "sum"),
            Average=("Amount", "mean"),
            Cashback=("Cashback", "sum"),
        )
        .reset_index()
    )

    st.dataframe(
        summary,
        use_container_width=True,
    )


# ============================================================
# SQL QUERIES
# ============================================================

with tab3:

    query = st.selectbox(
        "Choose SQL Query",
        [
            "Total Expense and Cashback",
            "Cashback by Payment Mode",
            "Average Expense by Category",
            "Top 10 Highest Transactions",
            "Monthly Expense",
        ],
    )

    if database_mode:

        if query == "Total Expense and Cashback":

            sql = """
            SELECT
                SUM(Amount) AS Total_Expense,
                SUM(Cashback) AS Total_Cashback
            FROM final
            """

        elif query == "Cashback by Payment Mode":

            sql = """
            SELECT
                Payment_Mode,
                SUM(Cashback) AS Cashback
            FROM final
            GROUP BY Payment_Mode
            """

        elif query == "Average Expense by Category":

            sql = """
            SELECT
                Category,
                AVG(Amount) AS Average_Expense
            FROM final
            GROUP BY Category
            """

        elif query == "Top 10 Highest Transactions":

            sql = """
            SELECT *
            FROM final
            ORDER BY Amount DESC
            LIMIT 10
            """

        else:

            sql = """
            SELECT
                MONTHNAME(Date) AS Month,
                SUM(Amount) AS Total
            FROM final
            GROUP BY MONTH(Date), MONTHNAME(Date)
            ORDER BY MONTH(Date)
            """

        result = pd.read_sql(
            sql,
            connection,
        )

        st.code(
            sql,
            language="sql",
        )

        st.dataframe(
            result,
            use_container_width=True,
        )

    else:

        st.info(
            "SQL queries are shown below for demonstration. "
            "The live demo does not connect to a MySQL database."
        )

        if query == "Total Expense and Cashback":

            sql = """
SELECT
    SUM(Amount) AS Total_Expense,
    SUM(Cashback) AS Total_Cashback
FROM final;
"""

            result = pd.DataFrame(
                {
                    "Total_Expense": [
                        df["Amount"].sum()
                    ],
                    "Total_Cashback": [
                        df["Cashback"].sum()
                    ],
                }
            )

        elif query == "Cashback by Payment Mode":

            sql = """
SELECT
    Payment_Mode,
    SUM(Cashback) AS Cashback
FROM final
GROUP BY Payment_Mode;
"""

            result = (
                df.groupby("Payment_Mode")["Cashback"]
                .sum()
                .reset_index()
            )

        elif query == "Average Expense by Category":

            sql = """
SELECT
    Category,
    AVG(Amount) AS Average_Expense
FROM final
GROUP BY Category;
"""

            result = (
                df.groupby("Category")["Amount"]
                .mean()
                .reset_index(
                    name="Average_Expense"
                )
            )

        elif query == "Top 10 Highest Transactions":

            sql = """
SELECT *
FROM final
ORDER BY Amount DESC
LIMIT 10;
"""

            result = (
                df.sort_values(
                    "Amount",
                    ascending=False,
                )
                .head(10)
            )

        else:

            sql = """
SELECT
    MONTHNAME(Date) AS Month,
    SUM(Amount) AS Total
FROM final
GROUP BY MONTH(Date), MONTHNAME(Date)
ORDER BY MONTH(Date);
"""

            result = (
                df.groupby("Month")["Amount"]
                .sum()
                .reset_index(
                    name="Total"
                )
            )

        st.code(
            sql,
            language="sql",
        )

        st.dataframe(
            result,
            use_container_width=True,
        )


# ============================================================
# DOWNLOAD
# ============================================================

st.download_button(
    "⬇ Download CSV",
    filtered.to_csv(index=False),
    file_name="expense_tracker.csv",
    mime="text/csv",
)


# ============================================================
# CLOSE DATABASE CONNECTION
# ============================================================

if connection is not None:
    connection.close()
