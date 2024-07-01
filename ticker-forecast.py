import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Step 1: Data Retrieval
def get_btc_data():
    # Get BTC-USD data from Yahoo Finance
    btc_data = yf.download('BTC-USD', start='2020-01-01', end='2024-06-01', progress=False)
    return btc_data

# Step 2: Data Preprocessing and Feature Engineering
def preprocess_data(data):
    # Calculate daily returns
    data['Daily_Return'] = data['Adj Close'].pct_change()

    # Drop missing values
    data = data.dropna()

    return data

# Step 3: Feature Selection
def select_features(data):
    # For simplicity, let's use the Daily_Return as the only feature
    X = data[['Daily_Return']]
    y = data['Adj Close']
    return X, y

# Step 4: Train-Test Split
def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Model Training
def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
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
    plt.title('BTC-USD Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Main Function
def main():
    # Step 1: Data Retrieval
    btc_data = get_btc_data()

    # Step 2: Data Preprocessing and Feature Engineering
    processed_data = preprocess_data(btc_data)

    # Step 3: Feature Selection
    X, y = select_features(processed_data)

    # Step 4: Train-Test Split
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Step 5: Model Training
    model = train_model(X_train, y_train)

    # Step 6: Model Evaluation
    mae = evaluate_model(model, X_test, y_test)
    print(f'Mean Absolute Error: {mae}')

    # Step 7: Visualization
    visualize_results(btc_data, model.predict(X))

if __name__ == "__main__":
    main()
