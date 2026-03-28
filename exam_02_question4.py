import re

text = "Guadalajara: 145M, Zapopan: 178 million, Tlajomulco: 100.15m, Lagos: 110k"

pattern = r'(\d+(?:\.\d+)?)\s*(millions|million|[MmKk])'

total = 0

for value, unit in re.findall(pattern, text):
    value = float(value)

    if unit.lower().startswith('m'):
        total += value * 1_000_000
    elif unit.lower().startswith('k'):
        total += value * 1_000

print(float(total))