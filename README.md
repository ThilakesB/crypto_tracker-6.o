# Cryptocurrency Price Tracker

A clean, production-ready Python application that scrapes real-time cryptocurrency data (Name, Price, 24h Change, Market Cap) from CoinMarketCap and saves it to a CSV file.

## Features
- **Real-time Scraping**: Fetches the latest data for top 10 cryptocurrencies.
- **Headless Browser**: Runs in the background without opening a visible window (configurable).
- **Auto-CSV Export**: Appends data to `crypto_prices.csv` with timestamps.
- **Dockerized**: Fully containerized for easy deployment.
- **Zero Config**: Uses `webdriver_manager` to handle ChromeDriver automatically.

## Prerequisites
- **Python 3.9+** (for local execution) and/or **Docker**.
- **Google Chrome** installed (for local execution).

## Installation & Usage

### Method 1: Run Locally with VS Code (Recommended)
1.  **Open the folder** in VS Code.
2.  **Install Dependencies**:
    Open a terminal in VS Code (`Ctrl+` `) and run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Script**:
    ```bash
    python crypto_tracker.py
    ```
    *Output:* You will see logs in the terminal, and a `crypto_prices.csv` file will be created/updated in the content root.

### Method 2: Run with Docker
This method is best if you don't want to install Python or Chrome dependencies manually.

1.  **Build the Image**:
    ```bash
    docker build -t crypto-tracker .
    ```
2.  **Run the Container**:
    To see the output and save the CSV file to your local machine, use a volume mount:
    ```bash
    # Windows (PowerShell)
    docker run -v ${PWD}:/app crypto-tracker
    
    # Mac/Linux
    docker run -v $(pwd):/app crypto-tracker
    ```

### Method 3: Docker in VS Code
1.  Ensure the "Docker" extension is installed in VS Code.
2.  Right-click `Dockerfile` in the explorer -> **Build Image**.
3.  Go to the Docker tab, find the image `crypto-tracker` (or the generic name created), right-click -> **Run**.
    *Note: To persist the CSV file back to your host, you still need to configure the volume mount in the run options or use the terminal command from Method 2.*

## Troubleshooting
- **Chrome Version Mismatch**: The script uses `webdriver_manager` to prevent this. If issues persist, ensure your local Chrome browser is up to date.
- **Network Errors**: CoinMarketCap may block automated requests if too frequent. The script includes basic waiting, but do not run it in a tight infinite loop without delays.
