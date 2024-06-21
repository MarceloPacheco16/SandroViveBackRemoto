# sqlite3-to-mysql.py
import re
import sys

def translate_line(line):
    # Replace SQLite specific types with MySQL types
    line = re.sub(r'INTEGER PRIMARY KEY AUTOINCREMENT', 'INTEGER AUTO_INCREMENT PRIMARY KEY', line)
    line = re.sub(r'TEXT', 'VARCHAR(255)', line)
    line = re.sub(r'BLOB', 'LONGBLOB', line)
    line = re.sub(r'REAL', 'DOUBLE', line)
    line = re.sub(r'(?i)PRAGMA.+;', '', line)  # Remove SQLite pragmas
    line = re.sub(r'DEFAULT (\'|\")?true(\'|\")?', 'DEFAULT 1', line)
    line = re.sub(r'DEFAULT (\'|\")?false(\'|\")?', 'DEFAULT 0', line)
    return line

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sqlite3-to-mysql.py input_file.sql > output_file.sql")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, 'r') as infile:
        for line in infile:
            translated_line = translate_line(line)
            sys.stdout.write(translated_line)
