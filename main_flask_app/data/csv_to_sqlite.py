from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, types

# Define the database file name and location
db_file = Path(__file__).parent.joinpath("users.db")

# Create a connection to file as a SQLite database (this automatically creates the file if it doesn't exist)
engine = create_engine("sqlite:///" + str(db_file), echo=False)


# Read the noc_regions data to a pandas dataframe
# The following avoids an issue whereby entries with "NA" in the csv file are treated as null values rather than valid text 'NA' which is what we want
na_values = [
    "",
    "#N/A",
    "#N/A N/A",
    "#NA",
    "-1.#IND",
    "-1.#QNAN",
    "-NaN",
    "-nan",
    "1.#IND",
    "1.#QNAN",
    "<NA>",
    "N/A",
    "NULL",
    "NaN",
    "n/a",
    "nan",
    "null",
]
noc_file = Path(__file__).parent.joinpath("users.csv")
# Read the data and handles the NA issue
noc_regions = pd.read_csv(noc_file, keep_default_na=False, na_values=na_values)

# Write the data to tables in a sqlite database
dtype_noc = {
    "event_id": types.INTEGER(),
    "type": types.TEXT(),
    "year": types.INTEGER(),
    "username": types.TEXT(),
    "email": types.TEXT(),
    "start": types.TEXT(),
    "end": types.TEXT(),
    "disabilities_included": types.TEXT(),
    "events": types.INTEGER(),
    "sports": types.INTEGER(),
    "countries": types.INTEGER(),
    "male": types.INTEGER(),
    "female": types.INTEGER(),
    "participants": types.INTEGER(),
    "highlights": types.TEXT(),
}

dtype_event = {
    "NOC": types.TEXT(),
    "region": types.TEXT(),
    "notes": types.TEXT(),
}

noc_regions.to_sql(
    "region", engine, if_exists="append", index=False, dtype=dtype_noc
)
paralympics.to_sql(
    "event", engine, if_exists="append", index=False, dtype=dtype_event
)
