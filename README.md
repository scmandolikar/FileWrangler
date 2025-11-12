# 🗂️ FileWrangler
A powerful and user-friendly desktop utility built with Python to bulk rename and organize thousands of files with ease.

![FileWrangler Home Page](httpsimg-here)  
*(Hint: Take a screenshot of your app's home page, upload it to your GitHub repository, and replace `img-here` with the image's URL to make it show up here!)*

---

FileWrangler is the perfect tool for photographers, office workers, digital archivists, or anyone with a messy "Downloads" folder. It transforms a tedious, manual task into a simple, two-click process.

## ✨ Key Features

* **Clean, Multi-Page Interface:** A simple, welcoming home screen guides you to either the Renamer or Organizer.
* **Modern & Stylish UI:** Built with `customtkinter`, featuring a beautiful gradient background and clear, easy-to-read buttons.
* **Safe & Reversible:** The "Undo" button gives you complete peace of mind, instantly reverting your last renaming operation.

### Rename Module
* **Powerful Renaming Engine:** Add prefixes/suffixes, replace text, and change case.
* **Live Preview:** See all your changes in real-time *before* you apply them.
* **Advanced Renaming:**
    * Add sequential numbering to your files.
    * Automatically rename photos using their **EXIF data** (date/time taken).
* **Recursive Processing:** Option to rename files in all subfolders at once.

### Organize Module
* **Smart File Organizer:** Clean up a messy folder in seconds.
* **Multiple Sorting Methods:**
    * By **File Extension** (e.g., `jpg_files`, `pdf_files`)
    * By **Date Modified** (e.g., `2025-10`, `2025-11`)
    * By **File Category** (e.g., `Images`, `Documents`, `Video`)
    * By **Custom Pattern** (e.g., move all files starting with `Invoice-*` to an `Invoices` folder).

## 💻 Tech Stack
* **Python 3**
* **CustomTkinter:** For the modern graphical user interface.
* **Pillow (PIL):** For reading image metadata (EXIF data).
* **PyInstaller:** Used to package the application into a standalone `.exe`.

## 🚀 How to Use

### For Users (Recommended)
1.  Go to the **[Releases](https://github.com/YOUR-USERNAME/FileWrangler/releases)** page of this repository.
2.  Download the `FileWrangler.exe` file from the latest release.
3.  Run the file. No installation is needed!

### For Developers (Running from Source)
1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR-USERNAME/FileWrangler.git](https://github.com/YOUR-USERNAME/FileWrangler.git)
    cd FileWrangler
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the application:
    ```bash
    python app.py
    ```