"""Export entries from a Timebook database into a Timetrap database.

Usage:
1. Edit the paths below if you are using non-default paths.
2. Ensure the Timetrap database exists and has no entries.
3. python timebook_to_timetrap.py
"""

import os
import sqlite3

# Establish connection with Timebook database.
timebook_config_dir = os.path.expanduser(
    os.path.join('~', '.config', 'timebook'))
timebook_db_path = os.path.join(timebook_config_dir, 'sheets.db')
timebook_db_connection = sqlite3.connect(timebook_db_path)
timebook_db_connection.row_factory = sqlite3.Row
timebook_db_cursor = timebook_db_connection.cursor()

# Establish connection with Timetrap database.
timetrap_db_path = os.path.expanduser(os.path.join('~', '.timetrap.db'))
timetrap_db_connection = sqlite3.connect(timetrap_db_path)
timetrap_db_cursor = timetrap_db_connection.cursor()

# Export entries from Timebook to Timetrap.
export_query = "SELECT id, sheet, start_time, end_time, description FROM entry"
for row in timebook_db_cursor.execute(export_query):
    import_row_query = ("INSERT INTO entries VALUES (:id, :description,"
        " DATETIME(:start_time, 'unixepoch', 'localtime'),"
        " DATETIME(:end_time, 'unixepoch', 'localtime'), :sheet)")
    parameters = dict(zip(row.keys(), row))
    timetrap_db_cursor.execute(import_row_query, parameters)
timetrap_db_connection.commit()

# Close connections.
timebook_db_connection.close()
timetrap_db_connection.close()
