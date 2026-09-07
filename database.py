import pymysql
import pandas as pd


HOST = "localhost"
USER = "root"
PASSWORD = "Dhashvinth"      # Change if your MySQL password is different
DATABASE = "expense_new"


def create_connection():
    return pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        autocommit=False
    )


def create_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS final(

        Date DATE,

        Category VARCHAR(100),

        Payment_Mode VARCHAR(50),

        Description VARCHAR(500),

        Amount DECIMAL(10,2),

        Cashback DECIMAL(10,2)

    )
    """

    cursor.execute(query)


def insert_dataframe(cursor, df):

    sql = """
    INSERT INTO final
    (
        Date,
        Category,
        Payment_Mode,
        Description,
        Amount,
        Cashback
    )

    VALUES(%s,%s,%s,%s,%s,%s)
    """

    values = list(
        df[
            [
                "Date",
                "Category",
                "Payment_Mode",
                "Description",
                "Amount",
                "Cashback"
            ]
        ].itertuples(index=False, name=None)
    )

    cursor.executemany(sql, values)


def fetch_data(connection):

    df = pd.read_sql("SELECT * FROM final", connection)

    if not df.empty:

        df["Date"] = pd.to_datetime(df["Date"])

        df["Month"] = df["Date"].dt.month_name()

    return df