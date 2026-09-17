import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("Earthquake_cleaned.csv")

engine = create_engine(
    "mysql+pymysql://root:deepa1810@localhost/PROJECT"
)

df.to_sql(
    name="eq",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data inserted successfully")