import pandas as pd 

import streamlit as st
df= pd.read_csv("Earthquake_cleaned.csv")
st.subheader("📊 Earthquake Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Earthquakes", len(df))
col2.metric("Maximum Magnitude", df["mag"].max())
col3.metric("Average Magnitude", round(df["mag"].mean(), 2))


import pymysql

connection = pymysql.connect(
        host="localhost",
        user="root",
        password="your password",
        
        database="PROJECT",
        cursorclass=pymysql.cursors.DictCursor
    )

print("✅ Connected to MySQL successfully!")
from sqlalchemy import create_engine    
engine = create_engine("mysql+pymysql://root:deepa1810@localhost/PROJECT")    
#df.to_sql(
 #   name='EQ',
  #  con=engine,
   # if_exists='replace',
    #index=False
#)
#print("Data inserted successfully")
#print(df.columns.tolist())

queries = {

    "1. Top 10 strongest earthquakes": """
    SELECT *
    FROM EQ
    ORDER BY mag DESC
    LIMIT 10;
    """,
        "2. Top 10 deepest earthquakes": """
    SELECT *
    FROM EQ
    ORDER BY depth_km DESC
    LIMIT 10;
    """,

    "3. Shallow earthquakes < 50 km and mag > 7.5": """
    SELECT *
    FROM EQ
    WHERE depth_km < 50
      AND mag > 7.5;
    """,
        "4. Average depth per continent": """
    SELECT 'Continent logic not available in DB' AS note;
    """,

    "5. Average magnitude per magnitude type": """
    SELECT magType, AVG(mag) AS avg_mag
    FROM EQ
    GROUP BY magType;
    """,

    "6. Year with most earthquakes": """
    SELECT YEAR(time) AS year, COUNT(*) AS total
    FROM EQ
    GROUP BY YEAR(time)
    ORDER BY total DESC
    LIMIT 1;
    """,

    "7. Month with highest earthquakes": """
    SELECT MONTH(time) AS month, COUNT(*) AS total
     FROM EQ
    GROUP BY MONTH(time)
    ORDER BY total DESC
    LIMIT 1;
    """,
    "8. Day of week with most earthquakes": """
    SELECT DAYNAME(time) AS day, COUNT(*) AS total
    FROM EQ
    GROUP BY DAYNAME(time)
    ORDER BY total DESC;
    """,

    "9. Count of earthquakes per hour": """
    SELECT HOUR(time) AS hour, COUNT(*) AS total
    FROM EQ
    GROUP BY HOUR(time)
    ORDER BY hour;
    """,

    "10. Most active reporting network": """
    SELECT net, COUNT(*) AS total
    FROM EQ
    GROUP BY net
    ORDER BY total DESC
    LIMIT 1;
    """,

    "11. Top 5 places with highest casualties": """
    SELECT place, MAX(felt) AS casualties
    FROM EQ
    GROUP BY place
    ORDER BY casualties DESC
    LIMIT 5;
    """,
    "12. Total economic loss per continent": """
    SELECT 'Not available' AS note;
    """,

    "13. Average economic loss by alert level": """
      
    SELECT alert, COUNT(*) AS count
    FROM EQ
    GROUP BY alert;
    """,

    "14. Count of reviewed vs automatic (status)": """
    SELECT status, COUNT(*) AS total
    FROM EQ
    GROUP BY status;
    """,
    "15. Count by earthquake type": """
    SELECT type, COUNT(*) AS total
    FROM EQ
    GROUP BY type;
    """,

    "16. Number of earthquakes by data type (types)": """
    SELECT types, COUNT(*) AS total
    FROM EQ
    GROUP BY types;
      """,

    "17. Avg RMS and gap per continent": """

    SELECT 'Continent mapping not available' AS note;
    """,

    "18. Events with high station coverage (nst > 50)": """
    SELECT *
    FROM EQ
    WHERE nst > 50;
    """,
    "19. Number of tsunamis per year": """
    SELECT YEAR(time) AS year, COUNT(*) AS tsunamis
    FROM EQ
    WHERE tsunami = 1
    GROUP BY YEAR(time);
    """,

    "20. Earthquakes by alert level": """
    SELECT alert, COUNT(*) AS total
    FROM EQ
    GROUP BY alert;
    """,

    "21. Top 5 countries with highest avg magnitude (past 10 yrs)": """
    SELECT place, AVG(mag) AS avg_mag
    FROM EQ
    GROUP BY place
    ORDER BY avg_mag DESC
    LIMIT 5;
    """,
    "22. Countries with both shallow & deep EQ same month": """
    SELECT place
    FROM EQ
    GROUP BY place, YEAR(time), MONTH(time)
    HAVING
        SUM(depth_km < 70) > 0
        AND SUM(depth_km > 300) > 0;
    """,   
    "23. Year-over-year earthquake growth rate": """
    SELECT
        year,
        total,
        LAG(total) OVER (ORDER BY year) AS previous_year,
        ROUND(
            ((total - LAG(total) OVER (ORDER BY year))
            / LAG(total) OVER (ORDER BY year)) * 100, 2
        ) AS growth_rate
    FROM (
        SELECT YEAR(time) AS year, COUNT(*) AS total
        FROM EQ
        GROUP BY year
    ) AS yearly;
    """,

    "24. Top 3 most seismically active regions": """
    SELECT place,
           COUNT(*) AS frequency,
           AVG(mag) AS avg_mag,
           (COUNT(*) * AVG(mag)) AS score
    FROM EQ
    GROUP BY place
    ORDER BY score DESC
    LIMIT 3;
    """,

    "25. Average depth within ±5° of equator": """
    SELECT place, AVG(depth_km) AS avg_depth
    FROM EQ
    WHERE latitude BETWEEN -5 AND 5
    GROUP BY place;
    """,

    "26. Countries with highest shallow-to-deep ratio": """
    SELECT place,
           SUM(depth_km < 70) AS shallow,
           SUM(depth_km > 300) AS deep,
           SUM(depth_km < 70) / NULLIF(SUM(depth_km > 300), 0) AS ratio
    FROM EQ
    GROUP BY place
    ORDER BY ratio DESC;
    """,
    "27. Avg magnitude difference (tsunami vs non-tsunami)": """
    SELECT
        (SELECT AVG(mag) FROM EQ WHERE tsunami = 1) AS tsunami_avg,
        (SELECT AVG(mag) FROM EQ WHERE tsunami = 0) AS non_tsunami_avg,
        (SELECT AVG(mag) FROM EQ WHERE tsunami = 1)
        - (SELECT AVG(mag) FROM EQ WHERE tsunami = 0) AS difference;
    """,

    "28. Events with lowest data reliability (gap & rms)": """
    SELECT *
    FROM EQ
    ORDER BY gap DESC, rms DESC
    LIMIT 20;
    """,
    

    "30. Regions with highest deep-focus EQ (>300 km)": """
    SELECT place, COUNT(*) AS deep_events
    FROM EQ
    WHERE depth_km > 300
    GROUP BY place
    ORDER BY deep_events DESC;
    """ 
}
# Streamlit UI


st.title("🌎 Earthquake Data Analysis Dashboard")

st.write("Select any problem statement (1–30) to run the corresponding SQL query.")

task = st.selectbox(
    "Choose Task Number",
    list(queries.keys())
)
if st.button("Run Query"):

    query = queries[task]

    result = pd.read_sql(query, engine)

    st.subheader(f"Results for: {task}")

    display_result = result.drop(
        columns=["country"],
        errors="ignore"
    )

    st.dataframe(display_result, width="stretch")
