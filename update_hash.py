import sqlite3

pwd_hash = "$2b$12$OZC6aeA7o35JvJvUZ9LYqzqmiZOAVzO2JeN1Z1gHsN8fg46q"

conn = sqlite3.connect('database/greenbet.db')
cur = conn.cursor()
cur.execute('UPDATE users SET password_hash = ? WHERE email = ?', (pwd_hash, 'admin@greenbet.fr'))
conn.commit()
conn.close()

print("Hash updated to:", pwd_hash)
