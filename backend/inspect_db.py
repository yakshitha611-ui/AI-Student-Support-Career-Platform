import sqlite3
conn = sqlite3.connect(r'C:\Users\Venkatesh\Desktop\student support and learning platform\backend\app.db')
cur = conn.cursor()
print('TABLES', cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall())
for table in ['users','student_skills','student_profiles','student_projects','student_career_goals']:
    print(f'--- {table} schema ---')
    print(cur.execute(f'PRAGMA table_info({table})').fetchall())
    try:
        print(f'--- {table} rows ---')
        print(cur.execute(f'SELECT * FROM {table} LIMIT 10').fetchall())
    except Exception as e:
        print('ERR', e)
conn.close()
