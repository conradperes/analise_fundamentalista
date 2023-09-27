import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# Step 1: Data Retrieval
def get_btc_data():
    btc_data = yf.download('BTC-USD', start='2021-01-01', end='2023-01-01', progress=False)
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

# Step 5: Neural Network Model
def build_neural_network(input_shape):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(input_shape,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)  # Output layer (single output for regression)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Step 6: Model Training
def train_neural_network(X_train, y_train, epochs=50):
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_train_scaled = scaler_X.fit_transform(X_train)
    y_train_scaled = scaler_y.fit_transform(y_train.values.reshape(-1, 1))

    model = build_neural_network(X_train.shape[1])
    model.fit(X_train_scaled, y_train_scaled, epochs=epochs, batch_size=32, verbose=1)

    return model, scaler_X, scaler_y

# Step 7: Model Evaluation
def evaluate_neural_network(model, X_test, scaler_X, scaler_y):
    X_test_scaled = scaler_X.transform(X_test)
    predictions_scaled = model.predict(X_test_scaled)
    predictions = scaler_y.inverse_transform(predictions_scaled)
    return predictions

# Step 8: Visualization
def visualize_results(data, predictions):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index[-len(predictions):], data['Adj Close'].iloc[-len(predictions):], label='Actual Price', linewidth=2)
    plt.plot(data.index[-len(predictions):], predictions, label='Predicted Price', linestyle='--', linewidth=2)
    plt.title('BTC-USD Price Prediction (Neural Network)')
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
    model, scaler_X, scaler_y = train_neural_network(X_train, y_train)

    # Model Evaluation
    predictions = evaluate_neural_network(model, X_test, scaler_X, scaler_y)

    # Visualize Results
    visualize_results(btc_data, predictions)

if __name__ == "__main__":
    main()
