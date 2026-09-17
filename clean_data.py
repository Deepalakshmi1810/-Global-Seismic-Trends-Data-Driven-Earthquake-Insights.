import pandas as pd
import re

df = pd.read_csv("Earthquake_final.csv")

def extract_country(place):
    if pd.isna(place):
        return "Unknown"

    match = re.search(r",\s*([^,]+)$", place)

    if match:
        return match.group(1).strip()

    if "Fiji" in place:
        return "Fiji"

    return "Unknown"

df["country"] = df["place"].apply(extract_country)

print(df[["place", "country"]].head(10))

df.to_csv("Earthquake_cleaned.csv", index=False)

print("Country column created successfully!")
# Save cleaned data
df.to_csv("Earthquake_cleaned.csv", index=False)
# Convert time to datetime
df["time"] = pd.to_datetime(df["time"])

# Derived date fields
df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

# Depth category
df["depth_category"] = df["depth_km"].apply(
    lambda x: "Shallow" if x < 70 else "Deep"
)

# Magnitude category
df["strength_category"] = df["mag"].apply(
    lambda x: "Strong" if x >= 6 else "Moderate"
)

# Check derived columns
print(df[[
    "country",
    "year",
    "month",
    "day",
    "day_of_week",
    "depth_category",
    "strength_category"
]].head())

print("Cleaned data saved successfully!")