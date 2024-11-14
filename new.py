import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
def start():
    import os
    import json
    import numpy as np

    data_folder = 'database'
    all_keys = []
    all_hold_time = []
    all_time_between_keys = []

    for filename in os.listdir(data_folder):
        if filename.endswith('.json'):
            with open(os.path.join(data_folder, filename),encoding="utf-8") as file:
                data = json.load(file)
                keys = data['keys']
                hold_time = data['hold_time']
                time_between_keys = data['time_between_keys']

                # Обрабатываем каждую запись
                for i in range(len(keys)):
                    key = keys[i]
                    if key.startswith("Key"):
                        # Преобразуем обозначение специальной клавиши в строку
                        key = key.replace("Key.", "")
                    elif key.startswith("'") and key.endswith("'"):
                        # Удаляем кавычки из символов
                        key = key.strip("'")
                    else:
                        # Обрабатываем пробелы и другие символы
                        key = key.strip()

                    all_keys.append(key)
                    all_hold_time.append(hold_time[i])
                    all_time_between_keys.append(time_between_keys[i])

    X_keys = np.array(all_keys)
    X_hold_time = np.array(all_hold_time)
    X_time_between_keys = np.array(all_time_between_keys)

    # Продолжите обработку данных и обучение модели...
