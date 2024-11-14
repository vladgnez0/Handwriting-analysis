import os
import json
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier

# Author: Гнездилов Владимир

tree_classifier = DecisionTreeClassifier()
scaler = StandardScaler()
keys_encoded = None
time_on_press = None
time_on_release = None
hold_time = None
time_between_keys = None
max_keys_length = None
max_time_length = None

def start():
    global keys_encoded, time_on_press, time_on_release, hold_time, time_between_keys, max_time_length, max_keys_length

    # Путь к папке с JSON-файлами
    folder_path = 'database'
    # Список для хранения данных
    data = []
    labels = []

    # Читаем файлы JSON
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="UTF-8") as file:
                json_data = json.load(file)
                data.append(json_data)
                labels.append(json_data["name+lastname"])

    # Создание словаря для клавиш
    key_mapping = {}
    key_id = 0

    for item in data:
        keys = item["keys"]

        for key in keys:
            if key not in key_mapping:
                key_mapping[key] = key_id
                key_id += 1

    # Преобразование клавиш в числовые значения
    keys_encoded = [[key_mapping[key] for key in item["keys"]] for item in data]

    # Расчет длительности нажатия на клавиши
    time_on_press = [item["time_on_press"] for item in data]
    time_on_release = [item["time_on_release"] for item in data]
    hold_time = [item["hold_time"] for item in data]
    time_between_keys = [item["time_between_keys"] for item in data]

    # Найти максимальную длину массивов
    max_keys_length = max(len(keys_enc) for keys_enc in keys_encoded)
    max_time_length = max(len(t_press) for t_press in time_on_press)

    # Создание признакового массива
    features = []
    for keys_enc, t_press, t_release, t_hold, t_between in zip(
            keys_encoded, time_on_press, time_on_release, hold_time, time_between_keys
    ):
        # Паддинг или обрезка массивов для согласования длины
        padded_keys_enc = np.pad(keys_enc, (0, max_keys_length - len(keys_enc)), mode='constant')
        padded_t_press = np.pad(t_press, (0, max_time_length - len(t_press)), mode='constant')

        # Заполнение недостающих значений нулями
        padded_t_release = np.pad(t_release, (0, max_time_length - len(t_release)), mode='constant')
        padded_t_hold = np.pad(t_hold, (0, max_time_length - len(t_hold)), mode='constant')
        padded_t_between = np.pad(t_between, (0, max_time_length - len(t_between)), mode='constant')

        # Создание признакового вектора для каждого наблюдения
        feature_vector = np.concatenate((padded_keys_enc, padded_t_press, padded_t_release, padded_t_hold, padded_t_between), axis=0)
        features.append(feature_vector)

    # Преобразование в массив numpy
    features = np.vstack(features)

    # Нормализация данных
    normalized_features = scaler.fit_transform(features)

    # Разделение на обучающий и тестовый наборы
    X_train, X_test, y_train, y_test = train_test_split(normalized_features, labels, test_size=0.2, random_state=42)

    # Обучение модели на обучающих данных
    tree_classifier.fit(X_train, y_train)
    # проверка модели на обучающих данных
    print(tree_classifier.score(X_test, y_test))


def predict(data):
    global scaler, keys_encoded, time_on_press, time_on_release, hold_time, time_between_keys, tree_classifier, max_keys_length, max_time_length

    # Extract features from the data dictionary
    keys = data["keys"]
    t_press = data["time_on_press"]
    t_release = data["time_on_release"]
    t_hold = data["hold_time"]
    t_between = data["time_between_keys"]

    # Подготовка данных
    key_mapping = {}
    key_id = 0

    keys_encoded = []
    time_on_press = []
    time_on_release = []
    hold_time = []
    time_between_keys = []

    for key in keys:
        if key not in key_mapping:
            key_mapping[key] = key_id
            key_id += 1

    keys_encoded.append([key_mapping[key] for key in keys])
    time_on_press.append(t_press)
    time_on_release.append(t_release)
    hold_time.append(t_hold)
    time_between_keys.append(t_between)

    # Паддинг или обрезка массивов для согласования длины
    padded_keys_enc = np.pad(keys_encoded[0], (0, max_keys_length - len(keys_encoded[0])), mode='constant')
    padded_t_press = np.pad(time_on_press[0], (0, max_time_length - len(time_on_press[0])), mode='constant')
    padded_t_release = np.pad(time_on_release[0], (0, max_time_length - len(time_on_release[0])), mode='constant')
    padded_t_hold = np.pad(hold_time[0], (0, max_time_length - len(hold_time[0])), mode='constant')
    padded_t_between = np.pad(time_between_keys[0], (0, max_time_length - len(time_between_keys[0])), mode='constant')

    # Создание признакового вектора для каждого наблюдения
    feature_vector = np.concatenate((padded_keys_enc, padded_t_press, padded_t_release, padded_t_hold, padded_t_between), axis=0)

    # Normalize the feature vector
    normalized_feature = scaler.transform([feature_vector])

    # Make prediction
    predicted_label = tree_classifier.predict(normalized_feature)

    # Print the predicted label
    print("Predicted label:", predicted_label)
