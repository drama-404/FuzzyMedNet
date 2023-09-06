import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer


def get_feature_importance(df, classifier):
    # mortality is the target variable
    target = 'hospital_expire_flag'

    # Let's separate the feature_engineering and target variable
    X = df.drop(columns=[target])
    y = df[target]
    # Split the data_preprocessing into train and test datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Create the model
    model = RandomForestClassifier(n_estimators=100, random_state=42) if classifier == 'rf' else xgb.XGBClassifier()

    # Fit the model
    model.fit(X_train, y_train)

    # Get feature importance
    importances = model.feature_importances_
    importance_dict = {name: importance for name, importance in zip(X.columns, importances)}
    sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate the accuracy
    accuracies = {"Accuracy": accuracy_score(y_test, y_pred),
                  "Precision": precision_score(y_test, y_pred),
                  "Recall": recall_score(y_test, y_pred),
                  "F1 Score": f1_score(y_test, y_pred),
                  "AUC-ROC": roc_auc_score(y_test, y_pred)}

    return sorted_importance, accuracies


def encode_features(df, binary_features=[], nominal_features=[]):
    le = LabelEncoder()
    ohe = OneHotEncoder()

    # For Binary Features - LabelEncoder
    for feature in binary_features:
        df[feature] = le.fit_transform(df[feature])

    # For Nominal Features - OneHotEncoder
    for feature in nominal_features:
        encoded_features = ohe.fit_transform(df[feature].values.reshape(-1, 1)).toarray()
        feature_labels = ohe.categories_
        encoded_labels = [f'{feature}_{label}' for label in feature_labels[0]]
        df_encoded = pd.DataFrame(encoded_features, columns=encoded_labels)

        df.drop(columns=[feature], inplace=True)
        df = pd.concat([df, df_encoded], axis=1)

    return df


def scale_features(df, numerical_features):
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), numerical_features),
        ])

    # Applying the preprocessor
    df_preprocessed = preprocessor.fit_transform(df)

    # Converting numpy array to pandas dataframe
    df_preprocessed = pd.DataFrame(df_preprocessed, columns=numerical_features)

    # Apply feature scaling
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_preprocessed), columns=df_preprocessed.columns)

    # Merge processed DataFrame with original DataFrame
    df_scaled = pd.concat([df.drop(numerical_features, axis=1), df_scaled], axis=1)

    return df_scaled


