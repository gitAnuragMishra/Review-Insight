# Review-Insight

Review-Insight is an automated tool designed to extract, summarize, and analyze product details and customer reviews from Amazon HTML files. By leveraging the roBERTa model, this application provides an in-depth sentiment analysis and summary of reviews using the distilbart summarisation model to help make informed purchase decisions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Challenges](#challenges)
- [Progress](#progress)
- [Technologies](#technologies)
- [Future Work](#future-work)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8+
- pip
- CUDA-enabled GPU (optional for faster processing)

### Install Dependencies

1. Clone the repository:

    ```bash
    git clone https://github.com/gitAnuragMishra/Review-Insight.git
    cd review-insight
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Install the specific PyTorch version (with CUDA support, if available):

    ```bash
    pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118
    ```

## Usage

1. Run the Streamlit application:

    ```bash
    streamlit run runner.py
    ```

2. Use the web interface to upload your HTML files, extract and analyze product information, and view summarized results.

## Project Structure

- app.py                         # Main entry point for the Streamlit application
- config.yaml                    # Configuration file for model paths and other settings
- requirements.txt               # Python dependencies
- sentiment_analysis.py          # Contains sentiment analysis functions
- summariser.py                  # Summarization module
- html_handler.py                # Handles extraction of data from HTML files
- README.md                      # Project documentation


## Features

- **File Upload**: Supports uploading multiple Amazon HTML files for analysis.
- **Product Name Extraction**: Automatically extracts and cleans product names from the HTML files.
- **Review and Description Extraction**: Extracts reviews and product descriptions from the HTML content.
- **Summarization**: Summarizes product descriptions and reviews using pre-trained NLP models.
- **Sentiment Analysis**: Provides a detailed sentiment analysis, including an overall sentiment score and star rating.
- **UI**: A user-friendly web interface built with Streamlit for easy interaction.

## Challenges

- **Amazon Anti-Scraping Measures**: Direct scraping from Amazon is difficult due to rate limiting, CAPTCHA, and IP blocking.
- **Current Solution**: Download HTML files manually and analyze them locally.
- **Web Scraping**: Developing a robust web scraper requires a paid proxy service, which is currently not in use.


## Technologies

- **Python**: Core language for all scripts and logic.
- **Streamlit**: Used for creating the web interface.
- **BeautifulSoup**: HTML parsing library for extracting product and review data.
- **Transformers (HuggingFace)**: Used for sentiment analysis and text summarization.


## Future Work

- **Real-Time Scraping**: Integrate real-time scraping using a proxy service.
- **Model Fine-Tuning**: Fine-tune the NLP models improve to accuracy (current accuracy is around 94%).
- **Expand Analysis**: Include additional metrics and visualizations in the sentiment analysis.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
