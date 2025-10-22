# Week 7 – Store Logs in SQLite & Basic Query

## Objective

This week, you will migrate your system monitor from CSV to a **SQLite database**.  
SQLite allows structured data storage and retrieval using SQL queries.

---

## Tasks

1. Create a new SQLite database called `log.db`
2. Create a table `system_log` with the following columns:
   - id (INTEGER, auto-increment)
   - timestamp (TEXT)
   - cpu (REAL)
   - memory (REAL)
   - disk (REAL)
   - ping_status (TEXT)
   - ping_ms (REAL)
3. Modify your code to:
   - Insert 5 new log entries (one every 10 seconds)
   - Print the last 5 records from the database

---

## Instructions

- Use `sqlite3` to connect and execute SQL commands
- You can use your previous `ping_host()` and `psutil` code from Week 5
- Use `print()` to display logs in the terminal

---

## Example Output

Logged: ('2025-10-21 14:00:00', 17.3, 41.2, 58.9, 'UP', 22.1)

Logged: ('2025-10-21 14:00:10', 19.1, 42.4, 59.0, 'UP', 21.3)

...
Last 5 entries:

(21, '2025-10-21 14:00:00', 17.3, 41.2, 58.9, 'UP', 22.1)

(22, '2025-10-21 14:00:10', 19.1, 42.4, 59.0, 'UP', 21.3)

---

## Submission Checklist

- [ ] `main.py` with all TODOs completed  
- [ ] `log.db` created successfully  
- [ ] Screenshot showing last 5 entries in terminal  
- [ ] Code committed and pushed to GitHub

---

## Bonus (Optional)

- Add a query function to filter by Ping_Status (e.g., only show “DOWN”)
- Count total records and display at the end
