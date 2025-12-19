<div align="center">
  <img src="logo.png" alt="Project Logo" width="120" height="120">
  
  # FB Marketplace Scraper Indonesia V1
  
  **A Python-based Desktop Automation Tool for mass product data scraping from Facebook Marketplace.**
  
  Developed by **Kyra-Code**
  
  ---
</div>

## 📋 Description
A desktop application based on GUI (Graphical User Interface) designed to scrape product data from Facebook Marketplace. This tool is specifically optimized for target locations in major cities across **Indonesia**.

The application utilizes **Selenium** for browser automation and **BeautifulSoup** for data parsing, wrapped in a modern and responsive interface using **CustomTkinter**.

## ✨ Key Features
* **Modern GUI:** Clean interface with full support for **Dark Mode / Light Mode**.
* **Responsive Layout:** Flexible window sizing with a responsive grid layout.
* **Advanced Search Filters:**
    * Keywords.
    * Location (Pre-set major cities in Indonesia).
    * Price Range (Minimum & Maximum).
* **Smart Automation:**
    * **Login Detection:** Automatically detects if Facebook requires a login and pauses to allow manual user login (helps prevent bot detection).
    * **Auto Scroll:** Automatically handles infinite scrolling to load products.
* **Data Export:** Scraped data is automatically saved to **Excel (.xlsx)** format.
* **Comprehensive Data:** Captures Title, Price, Location, Description, Product Link, and even estimates RAM/ROM specs (optimized for Mobile Phones).
* **Safe Stop:** The scraping process can be stopped/cancelled at any time without losing the data that has already been collected.

## 🛠️ Built With
* [Python](https://www.python.org/) - Main programming language.
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI library.
* [Selenium](https://www.selenium.dev/) - Web browser automation.
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing.
* [Pandas](https://pandas.pydata.org/) - Data management and Excel export.

## 🚀 Installation (For Developers)

If you wish to run the source code or contribute:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/repo-name.git](https://github.com/your-username/repo-name.git)
    cd repo-name
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # For Windows
    # source venv/bin/activate  # For Mac/Linux
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure the following are installed: customtkinter, pandas, selenium, webdriver-manager, beautifulsoup4, pillow, openpyxl, packaging, requests)*

4.  **Run the Application**
    ```bash
    python scraper_v2.py
    ```

## 📦 Build to .EXE
You can convert this script into a portable Executable file using **Auto-Py-To-Exe** or **PyInstaller**.

**PyInstaller Command:**
```bash
pyinstaller --noconsole --onefile --windowed --icon=icon.ico --add-data "logo.png;." --collect-all customtkinter --hidden-import PIL --hidden-import Pillow scraper_v2.py
```

## ⚠️ Disclaimer
This tool is created for Educational and Research purposes only. The developer is not responsible for any misuse of this application or any violations of Facebook's Terms of Service (ToS). Please use this tool responsibly.

© 2025 Kyra-Code. All rights reserved.
