import pandas as pd
from database.database import Database

db = Database()


QUERY = """
SELECT 
    name,
    latitude,
    longitude,
    address,
    phone,
    transport,
    type,
    time_table,
    info_{language_code} as description
FROM poi;
"""


def load_data(language_code):
    query = QUERY.format(language_code=language_code)
    res = db.execute_query(query)
    res_dict = [dict(row) for row in res]
    return res_dict
    # df = pd.read_csv('data/servizi.csv', sep=",")
    # df = df.astype(str)
    # return df.dropna().to_dict(orient='records')


