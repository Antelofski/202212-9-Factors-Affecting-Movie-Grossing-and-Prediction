import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump, load

from sklearn.linear_model import LinearRegression

# features = ['year', 'title', 'imdbRate', 'runtime', 'genres', 'directors']
def predict(year, title, imdbRate, runtime, genres, directors):
    DATA_PATH = 'https://raw.githubusercontent.com/HanlunWang/EECS6893_Final_Project/main/dataset/combine.dataset.csv'

    input = {'year': year, 'title': title, 'imdbRate': imdbRate, 'runtime': runtime, 'genres': genres, 'directors': directors}

    # Read the data
    X_full = pd.read_csv(DATA_PATH)

    # Drop irrelative columns
    X_full = X_full.drop(columns=['rank', 'tconst', 'page'])

    # Drop rows including na or invalid value
    X_full = X_full.dropna()
    X_full = X_full[X_full.runtime != '\\'+'N']
    X_full = X_full[X_full.genres != str(['\\N'])]

    # Convert dollar format to float
    X_full[['worldwide']] = X_full[['worldwide']].replace('[\$,]','',regex=True).astype(float)

    # Convert string format to int 
    X_full[['runtime']] = X_full[['runtime']].astype(int)

    # Convert string to list
    X_full['genres'] = X_full['genres'].str[2:-2].str.split(',')

    # Get X and y
    features = ['year', 'title', 'imdbRate', 'runtime', 'genres', 'directors']
    X = X_full[features]
    X = X.append(input, ignore_index = True)

    y = X_full.worldwide
    y = y.append(pd.Series([0.0]), ignore_index = True)

    from sklearn.preprocessing import MultiLabelBinarizer

    # Encode genres
    mlb = MultiLabelBinarizer()
    genres_df = pd.DataFrame(mlb.fit_transform(X['genres']),columns=mlb.classes_, index=X.index)
    X = X.join(genres_df)
    X = X.drop(columns=['genres'])

    X_size = X.shape[0]
    y_size = y.shape[0]

    # Break off validation set from training data
    X_train = X.iloc[:X_size - 2]
    X_valid = X.iloc[X_size-2:X_size]
    y_train = y.iloc[:y_size - 2]
    y_valid = y.iloc[y_size-2:y_size]

    

    from sklearn.preprocessing import OneHotEncoder
    object_cols = ['title', 'directors']
    # Apply one-hot encoder to each column with categorical data
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
    OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))

    # One-hot encoding removed index; put it back
    OH_cols_train.index = X_train.index
    OH_cols_valid.index = X_valid.index

    # Remove categorical columns (will replace with one-hot encoding)
    num_X_train = X_train.drop(object_cols, axis=1)
    num_X_valid = X_valid.drop(object_cols, axis=1)

    # Add one-hot encoded columns to numerical features
    OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
    OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)
    
    lr_model = LinearRegression()

    # Fit the model to the training data
    lr_model.fit(OH_X_train.values, y_train)
    result = lr_model.predict(OH_X_valid.tail(1))

    return result




