import bcrypt

# Generate a REAL hash
hashed = bcrypt.hashpw(b"admin1234", bcrypt.gensalt()).decode()

with open('database/schema.sql', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Replace whatever bcrypt hash is currently in the schema
new_content = re.sub(
    r"\('\admin', 'admin@greenbet.fr', '.*?\.+",
    f"('admin', 'admin@greenbet.fr', '{hashed}', 'admin');",
    content
)

# Wait, let's use a better regex
new_content = re.sub(
    r"\('admin',\s*'admin@greenbet.fr',\s*'[^']+',\s*'admin'\);",
    f"('admin', 'admin@greenbet.fr', '{hashed}', 'admin');",
    content
)

with open('database/schema.sql', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated schema.sql with hash length:", len(hashed))

import sqlite3
conn = sqlite3.connect('database/greenbet.db')
cur = conn.cursor()
cur.execute('UPDATE users SET password_hash = ? WHERE email = ?', (hashed, 'admin@greenbet.fr'))
conn.commit()
conn.close()
print("Updated database!")
