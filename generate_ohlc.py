import json
import random

# Список символов активов
symbols = ["BTCUSD", "ETHUSD", "XRPUSD"]

# Создаем структуру данных для каждого символа
data = {}

for symbol in symbols:
    series = []
    for i in range(1000):  # Генерируем 1000 свечей для каждого символа
        ohlc = {
            "open": round(random.uniform(1000, 50000), 2),
            "high": round(random.uniform(1000, 50000), 2),
            "low": round(random.uniform(1000, 50000), 2),
            "close": round(random.uniform(1000, 50000), 2),
        }
        series.append(ohlc)
    data[symbol] = series

# Сохраняем данные в файл
file_path = "./data/ohcl.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"OHLC данные сохранены в {file_path}")
