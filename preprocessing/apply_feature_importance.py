import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def get_feature_importance(df, classifier):
    # mortality is the target variable
    target = 'expire_flag'

    # Let's separate the features and target variable
    X = df.drop(columns=[target])
    y = df[target]
    # Split the data into train and test datasets
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
