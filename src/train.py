import pandas as pd
import numpy as np 
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from imblearn.over_sampling import SMOTE
from data_loader import load_data
from feature_engineer import engineer_features
import os
import joblib

def train_model():
    data = load_data('data/')
    df = engineer_features(data)

    y = df['TARGET']
    X = df.drop('TARGET' , axis = 1)

    X_train , X_test , y_train , y_test = train_test_split(
        X,y , test_size=0.2, random_state=42, stratify= y
    )

    smote = SMOTE(random_state=42)
    X_train,y_train = smote.fit_resample(X_train, y_train)

    model = XGBClassifier(
        n_estimators = 300,
        max_depth = 6,
        learning_rate = 0.05,
        random_state = 42,
        eval_metric='auc'
    )

    model.fit(X_train, y_train, eval_set=[(X_test,y_test)],verbose=50)

    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
    print(f"\nAUC: {auc:.4f}")

    os.makedirs('models' , exist_ok=True)
    joblib.dump(model, 'models/credit_model.pkl')
    joblib.dump(X.columns.tolist(), 'models/features_name.pkl')
    print("Model saved.")

if __name__ == "__main__":
    train_model()
