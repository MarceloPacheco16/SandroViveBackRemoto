import re
import fileinput
import tempfile
from optparse import OptionParser

IGNORED_PREFIXES = [
    'PRAGMA',
    'BEGIN TRANSACTION;',
    'COMMIT;',
    'DELETE FROM sqlite_sequence;',
    'INSERT INTO "sqlite_sequence"',
]

def replace_sqlite_to_mysql(line):
    if any(line.lstrip().startswith(prefix) for prefix in IGNORED_PREFIXES):
        return None  # Ignorar líneas con los prefijos ignorados
    
    # Realizar reemplazos específicos para adaptar el SQL de SQLite a MySQL
    line = line.replace("INTEGER PRIMARY KEY", "INTEGER AUTO_INCREMENT PRIMARY KEY")
    line = line.replace("AUTOINCREMENT", "AUTO_INCREMENT")
    line = line.replace("DEFAULT 't'", "DEFAULT '1'")
    line = line.replace("DEFAULT 'f'", "DEFAULT '0'")
    line = line.replace(",'t'", ",'1'")
    line = line.replace(",'f'", ",'0'")
    
    return line

def main():
    op = OptionParser()
    op.add_option('-d', '--database')
    op.add_option('-u', '--username')
    op.add_option('-p', '--password')
    opts, args = op.parse_args()

    if not args:
        print("Debe proporcionar el archivo SQL de entrada.")
        return
    
    input_file = args[0]

    # Abrir el archivo de entrada bbdd.sql en modo binario para leer
    with open(input_file, 'rb') as f:
        lines = f.readlines()

    # Procesar cada línea del archivo
    processed_lines = []
    for line_bytes in lines:
        # Decodificar la línea como UTF-8
        line = line_bytes.decode('utf-8', errors='ignore').rstrip('\r\n')
        processed_line = replace_sqlite_to_mysql(line)
        if processed_line:
            processed_lines.append(processed_line)

    # Escribir las líneas procesadas en el archivo de salida bbdd.mysql
    output_file = input_file.replace('.sql', '.mysql')
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in processed_lines:
            f.write(re.sub(r'\s+', ' ', line) + '\n')

    print(f"Archivo '{output_file}' generado exitosamente.")

if __name__ == "__main__":
    main()