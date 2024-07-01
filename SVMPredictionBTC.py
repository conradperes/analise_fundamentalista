import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Step 1: Data Retrieval
def get_btc_data():
    btc_data = yf.download('BTC-USD', start='2020-01-01', end='2024-06-25', progress=False)
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
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = SVR(kernel='linear')
    model.fit(X_train_scaled, y_train)
    
    return model, scaler

# Step 6: Model Evaluation
def evaluate_model(model, X_test, y_test, scaler):
    X_test_scaled = scaler.transform(X_test)
    predictions = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, predictions)
    return mae , predictions

# Step 7: Visualization
def visualize_results(data, model, scaler, predictions):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index[-len(predictions):], data['Adj Close'].iloc[-len(predictions):], label='Actual Price', linewidth=2)
    plt.plot(data.index[-len(predictions):], predictions, label='Predicted Price', linestyle='--', linewidth=2)
    plt.title('BTC-USD Price Prediction (SVM)')
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
    model, scaler = train_model(X_train, y_train)

    # Model Evaluation
    mae , predictions= evaluate_model(model, X_test, y_test, scaler)
    print(f'Mean Absolute Error: {mae}')

    # Visualize Results
    visualize_results(btc_data, model, scaler, predictions)

if __name__ == "__main__":
    main()
