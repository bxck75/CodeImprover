import csv
import random
from pathlib import Path

csv_file_path=f"{str(Path(__file__).parent)}/Roles.csv"

def select_role(path=csv_file_path):
    lines = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            lines.append(line)
    random_line = random.choice(lines)
    return random_line