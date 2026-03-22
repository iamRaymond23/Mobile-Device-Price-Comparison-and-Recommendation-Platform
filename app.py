from flask import Flask, render_template, request, redirect, url_for, flash
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Load the trained model
model = load_model('my_model.h5')

# Load the CSV data
def load_data():
    df = pd.read_csv('DataBase.csv')
    return df

# Function to assign the correct logo based on manufacturer
def get_logo(manufacturer):
    logos = {
        'Apple': 'apple_logo.png',
        'Samsung': 'samsung_logo.png',
        'Google': 'google_logo.png',
        'Motorola': 'motorola_logo.png'
    }
    return logos.get(manufacturer, 'default_logo.png')

# Function to get random deals (featured devices) for the home page
def get_random_deals(df, num_deals=8):
    sample_df = df.sample(n=num_deals)
    sample_df['logo'] = sample_df['Device manufacture'].apply(get_logo)
    deals = sample_df[['Device name', 'Device price', 'Device manufacture', 'logo', 'reviews']].to_dict(orient='records')
    return deals

# Function to recommend top devices by manufacturer
def recommend_by_manufacturer(data, manufacturer):
    filtered_data = data[data['Device manufacture'].str.lower() == manufacturer.lower()]
    
    if filtered_data.empty:
        return []

    filtered_data['logo'] = filtered_data['Device manufacture'].apply(get_logo)
    top_devices = filtered_data.sort_values(by='score', ascending=False).head(7)
    
    return top_devices.to_dict(orient='records')  # Convert to list of dictionaries

# Function to recommend top devices by platform
def recommend_by_platform(data, platform):
    filtered_data = data[data['Platform'].str.lower() == platform.lower()]
    
    if filtered_data.empty:
        return []

    filtered_data['logo'] = filtered_data['Device manufacture'].apply(get_logo)
    top_devices = filtered_data.sort_values(by='score', ascending=False).head(7)
    
    return top_devices.to_dict(orient='records')  # Convert to list of dictionaries

# Function to recommend top devices by price
def recommend_by_price(data):
    # Print the columns to verify the names
    print("Columns in the DataFrame:", data.columns)

    # Check if the correct column exists (adjust the column name based on your CSV)
    if 'price' not in data.columns:
        # Try alternative column names
        if 'Device price' in data.columns:
            data.rename(columns={'Device price': 'price'}, inplace=True)
        else:
            raise KeyError("The 'price' column is missing in the DataFrame.")

    # Convert 'price' column to numeric if necessary
    data['price'] = pd.to_numeric(data['price'], errors='coerce')

    # Handle any NaN values
    data = data.dropna(subset=['price'])

    # Sort by price and select the top 5 devices
    top_devices = data.sort_values(by='price', ascending=True).head(7)
    top_devices['logo'] = top_devices['Device manufacture'].apply(get_logo)
    return top_devices.to_dict(orient='records')

# Function to recommend top devices by reviews
def recommend_by_reviews(data):
    top_devices = data.sort_values(by='reviews', ascending=False).head(7)
    top_devices['logo'] = top_devices['Device manufacture'].apply(get_logo)
    return top_devices.to_dict(orient='records')  # Convert to list of dictionaries

# Home route
@app.route('/')
def home():
    df = load_data()
    deals = get_random_deals(df)
    return render_template('index.html', deals=deals)

# Route to handle brand-specific pages
@app.route('/brand/<brand_name>')
def show_brand_devices(brand_name):
    df = load_data()
    filtered_devices = df[df['Device manufacture'].str.lower() == brand_name.lower()]
    filtered_devices['logo'] = filtered_devices['Device manufacture'].apply(get_logo)
    devices = filtered_devices[['Device name', 'Device price', 'Device manufacture', 'logo', 'reviews']].to_dict(orient='records')
    return render_template('brand_devices.html', devices=devices, brand_name=brand_name)

# Route to handle site-specific pages
@app.route('/site/<site_name>')
def show_site_devices(site_name):
    df = load_data()
    df['Platform'] = df['Platform'].str.replace('Best Buy', 'Bestbuy')
    filtered_devices = df[df['Platform'].str.lower() == site_name.lower()]
    filtered_devices['logo'] = filtered_devices['Device manufacture'].apply(get_logo)
    devices = filtered_devices[['Device name', 'Device price', 'Device manufacture', 'logo', 'reviews']].to_dict(orient='records')
    return render_template('site_devices.html', devices=devices, site_name=site_name)

# Route to handle image upload and prediction
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Ensure the uploads directory exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        prediction = predict_device(filename)

        # Load the data
        df = load_data()
        
        # Recommend top 5 devices based on the predicted manufacturer
        top_5_devices = recommend_by_manufacturer(df, prediction)
        
        return render_template('result.html', filename=file.filename, prediction=prediction, recommendations=top_5_devices)

# Function to predict device based on uploaded image
def predict_device(image_path):
    img = load_img(image_path, target_size=(150, 150))  # Adjust the size based on your model
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Assuming the model expects images normalized between 0 and 1

    predictions = model.predict(img)
    class_indices = {0: 'Google', 1: 'Motorola', 2: 'Samsung', 3: 'Apple'}
    predicted_class = class_indices[np.argmax(predictions)]
    return predicted_class

# Route to handle recommendations based on user selection
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    df = load_data()
    recommendations = []

    if request.method == 'POST':
        recommendation_type = request.form.get('recommendation_type')

        if recommendation_type == 'manufacturer':
            manufacturer = request.form.get('manufacturer')
            recommendations = recommend_by_manufacturer(df, manufacturer)
        elif recommendation_type == 'platform':
            platform = request.form.get('platform')
            recommendations = recommend_by_platform(df, platform)
        elif recommendation_type == 'price':
            recommendations = recommend_by_price(df)
        elif recommendation_type == 'reviews':
            recommendations = recommend_by_reviews(df)

    # Ensure recommendations is a list (even if empty)
    return render_template('recommendation.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
