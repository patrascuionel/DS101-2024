import pandas as pd
import numpy as np
import joblib
import json

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
folder = 'notebook_output'

# CORS allow all origins this is dev
CORS(app, resources={r"/*": {"origins": "*"}})



def predict_price(model_path, scaler_path, columns_path, raw_input_df):
    # Load the trained model, scaler, and training column names
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    with open(columns_path, 'r') as f:
        training_columns = json.load(f) # These are the column names the model was trained on

    input_df = raw_input_df.copy()

    # --- 1. Feature Engineering (must be consistent with training data processing) ---
    # Create 'Car Age'
    current_year = 2025 # Ensure this matches the year used during training
    input_df['Car Age'] = current_year - input_df['Year']

    # Create 'Is_xDrive' from 'Model' column
    input_df['Is_xDrive'] = input_df['Is_xDrive'].astype(int)  # Ensure it's binary (0 or 1)

    # Simplify 'Fuel Type' (example: 'Benzina + GPL' -> 'Benzina')
    input_df['Fuel Type'] = input_df['Fuel Type'].replace({
        'Benzina + GPL': 'Benzina',
        'Hibrid Plug-In': 'Hibrid'
        # Add other mappings if they were used in training
    })
    
    # Define original categorical columns that were one-hot encoded during training
    # These are the names *before* dummification (e.g., 'Fuel Type', not 'Fuel Type_Diesel')
    original_categorical_cols = ['Fuel Type', 'Region', 'Engine_Badge']

    # --- 2. One-Hot Encoding ---
    # Apply one-hot encoding. drop_first must match the setting used during training.
    input_df_dummified = pd.get_dummies(input_df, columns=original_categorical_cols)
    
    # --- 3. Align Columns with Training Data ---
    # Reindex the dummified input to match the columns seen by the model during training.
    # This adds missing columns (e.g., other Engine_Badge types) with fill_value=0
    # and ensures the correct order.
    input_df_aligned = input_df_dummified.reindex(columns=training_columns, fill_value=0)
    
    # --- 4. Scaling Numerical Features ---
    # List of numerical features that were scaled (excluding the target variable 'Price_log')
    numerical_features_to_scale = ['Engine Size (cm3)', 'Horse Power (HP)', 'Kilometers', 'Car Age']
    
    # List of all features the scaler was originally fit on, in order.
    # 'Price_log' was the 5th element (index 4) in this example list. Adjust if your order was different.
    scaler_fit_features_ordered = ['Engine Size (cm3)', 'Horse Power (HP)', 'Kilometers', 'Car Age', 'Price_log']

    for col_name in numerical_features_to_scale:
        if col_name in input_df_aligned.columns: # Ensure column exists
            try:
                # Find the index of this column in the list of features the scaler was fit on
                scaler_col_idx = scaler_fit_features_ordered.index(col_name)
                mean_val = scaler.mean_[scaler_col_idx]
                scale_val = scaler.scale_[scaler_col_idx]
                input_df_aligned[col_name] = (input_df_aligned[col_name] - mean_val) / scale_val
            except ValueError:
                print(f"Warning: Column '{col_name}' was intended for scaling but not found in scaler's original fit features list: {scaler_fit_features_ordered}")
            except IndexError:
                print(f"Warning: Index issue for column '{col_name}' during scaling. Scaler might not have been fit on this feature correctly.")
        else:
            print(f"Warning: Numerical column '{col_name}' not found in the aligned input data for scaling.")

    # --- 5. Prediction ---
    # The input_df_aligned should now have the exact feature set (names and order) as X_train.
    scaled_price_log_pred = model.predict(input_df_aligned)

    # --- 6. Inverse Transform the Prediction ---
    # 'Price_log' was the last feature the scaler was trained on (index -1).
    price_log_mean_at_fit = scaler.mean_[-1]  # Mean of 'Price_log' during scaler fit
    price_log_scale_at_fit = scaler.scale_[-1] # Scale of 'Price_log' during scaler fit
    
    # Inverse scaling for the predicted 'Price_log'
    original_price_log_pred = (scaled_price_log_pred * price_log_scale_at_fit) + price_log_mean_at_fit
    
    # Convert from log price back to actual price using np.exp()
    actual_price_pred = np.exp(original_price_log_pred)
    
    return actual_price_pred

# simple flask endpoint to return the prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame(data)
        
        # Validate input DataFrame
        required_columns = ['Engine Size (cm3)', 'Horse Power (HP)', 'Kilometers', 'Year', 'Is_xDrive', 'Fuel Type', 'Region', 'Engine_Badge']
        if not all(col in input_df.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in input data'}), 400
        
        predicted_price = predict_price(
            f'{folder}/best_model.pkl', 
            f'{folder}/scaler.pkl', 
            f'{folder}/training_columns.json', 
            input_df)
        
        return jsonify({'predicted_price': predicted_price[0]})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/')
def index():
    return "Welcome to the Car Price Prediction API! Use the /predict endpoint to get predictions."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
