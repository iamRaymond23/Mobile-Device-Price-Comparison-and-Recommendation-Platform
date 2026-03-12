# Mobile Device Price Comparison and Recommendation Platform

## Overview

This project is a comprehensive solution designed to help consumers make informed purchasing decisions in the mobile device market. It consolidates data from leading e-commerce platforms like Amazon, Best Buy, and Walmart, integrating advanced machine learning techniques such as image recognition and personalized recommendations.

## Features

- **Data Scraping**: Automated data extraction from Amazon, Best Buy, and Walmart using Selenium and Python, generating a unified dataset of mobile devices.
- **Image Recognition**: Utilizes a Convolutional Neural Network (CNN) to identify the brand of a mobile device from an uploaded image.
- **Recommendation System**: Provides personalized device recommendations based on price, number of reviews, and user preferences.
- **Responsive Web Interface**: Built with Flask, HTML, CSS, and JavaScript, offering a user-friendly experience across different devices.

## Project Structure

- **data_scraping/**: Contains scripts used for scraping data from e-commerce platforms.
- **image_recognition/**: Includes the CNN model and training scripts for brand identification.
- **recommendation_system/**: Houses the scoring algorithm and scripts for generating device recommendations.
- **web_interface/**: Contains the Flask application and front-end files for the website.
- **docs/**: Includes the project report and the PowerPoint presentation.
- **README.md**: This file, providing an overview and instructions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/mobile-device-platform.git
    cd mobile-device-platform
    ```

2. Set up a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run the web application:
    ```bash
    python app.py
    ```

4. Access the application by navigating to `http://127.0.0.1:5000/` in your web browser.

## Usage

- **Image Recognition**: Upload an image of a mobile device to identify its brand.
- **Search and Compare**: Enter device preferences to get a list of recommended devices with prices, reviews, and links to purchase.
- **Explore Devices**: Browse devices by brand or e-commerce platform to find the best deals.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
