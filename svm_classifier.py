import pandas as pd
import json
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier()

def process_data():
    data = []
    listOfFiles = os.listdir('database')
    # Чтение данных из каждого файла
    for i in listOfFiles:
        with open(os.path.join('database', i), 'r', encoding="UTF-8") as file:
            data.append(json.load(file))
    return data


def preprocess_data(data):
    # Создание датафрейма из данных
    df = pd.DataFrame(data)

    # Обработка столбца "keys" с использованием One-Hot Encoding
    keys_encoded = pd.get_dummies(df['keys'].apply(pd.Series).stack(), prefix='key').sum(level=0)

    # Преобразование числовых столбцов
    numeric_columns = ['time_on_press', 'time_on_release', 'hold_time', 'time_between_keys']
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    # Объединение обработанных данных
    processed_data = pd.concat([df.drop('keys', axis=1), keys_encoded.reindex(df.index)], axis=1)
    print(df.head())
    return processed_data
X= None
def start():
    # Загрузка и предобработка данных
    data = process_data()
    processed_data = preprocess_data(data)
    global X
    # Заполнение пропущенных значений нулями
    processed_data = processed_data.fillna(0)

    # Преобразование типов данных числовых столбцов
    numeric_columns = ['time_on_press', 'time_on_release', 'hold_time', 'time_between_keys']
    processed_data[numeric_columns] = processed_data[numeric_columns].astype('float32')

    # Создание таблицы признаков и целевой переменной
    X = processed_data.drop("name+lastname", axis=1)
    y = processed_data["name+lastname"]

    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Обучение модели случайного леса
    global model
    model.fit(X_train, y_train)
    # Получение признаков из объекта модели

    # Получение признаков из набора данных
    feature_names = X.columns.tolist()
    print(feature_names)
    # Сохранение модели
    safe("save.txt", model)
    # Оценка точности модели на тестовых данных
    accuracy = model.score(X_test, y_test)
    print(f"Accuracy: {accuracy}")


def safe(filename, dump):
    pickle.dump(dump, open(filename, 'wb'))


def load(filename):
    return pickle.load(open(filename, 'rb'))
def predict(df):
    global model
    data=[]
    global X
    data.append(df)
    processed_data = preprocess_data(data)

    # Заполнение пропущенных значений нулями
    processed_data = processed_data.fillna(0)

    # Преобразование типов данных числовых столбцов
    numeric_columns = ['time_on_press', 'time_on_release', 'hold_time', 'time_between_keys']
    processed_data[numeric_columns] = processed_data[numeric_columns].astype('float32')
    expected_features =X.columns.tolist()
    missing_features = set(expected_features)-set(processed_data)
    for feature in missing_features:
        processed_data[feature] = 0
    return model.predict(processed_data)