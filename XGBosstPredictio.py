import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Step 1: Data Retrieval
def get_btc_data():
    btc_data = yf.download('BTC-USD', start='2021-01-01', end='2024-06-25', progress=False)
    return btc_data

# Step 2: Data Preprocessing and Feature Engineering
def preprocess_data(data):
    data['Daily_Return'] = data['Adj Close'].pct_change()
    data = data.dropna()
    return data

# Step 3: Feature Selection
def select_features(data):
    X = data[['Daily_Return']]
    y = data['Adj Close']
    return X, y

# Step 4: Train-Test Split
def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Model Training
def train_model(X_train, y_train):
    model = XGBRegressor(objective='reg:squarederror', random_state=42)
    model.fit(X_train, y_train)
    return model

# Step 6: Model Evaluation
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    return mae

# Step 7: Visualization
def visualize_results(data, predictions):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index[-len(predictions):], data['Adj Close'].iloc[-len(predictions):], label='Actual Price', linewidth=2)
    plt.plot(data.index[-len(predictions):], predictions, label='Predicted Price', linestyle='--', linewidth=2)
    plt.title('BTC-USD Price Prediction (XGBoost)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Main Function
def main():
    btc_data = get_btc_data()
    processed_data = preprocess_data(btc_data)
    X, y = select_features(processed_data)
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Model Training
    model = train_model(X_train, y_train)

    # Model Evaluation
    mae = evaluate_model(model, X_test, y_test)
    print(f'Mean Absolute Error: {mae}')

    # Visualize Results
    visualize_results(btc_data, model.predict(X))

if __name__ == "__main__":
    main()
