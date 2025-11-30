# 🗂️ FileWrangler
A powerful and user-friendly desktop utility built with Python to bulk rename and organize thousands of files with ease.
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

## 📸 Screenshots

*Coming soon - Application screenshots will be added*

## 🎯 Use Cases

- **Photographers** - Batch rename photos from camera (IMG_1234.jpg → Wedding_001.jpg)
- **Content Creators** - Organize video files by project and date
- **Office Workers** - Bulk rename scanned documents with proper naming
- **Digital Archivists** - Organize large file collections systematically
- **Students** - Rename assignment files to match submission requirements
- **Developers** - Rename project assets and resources efficiently

## 🔧 System Requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher (for running from source)
- **RAM**: 512MB minimum
- **Disk Space**: 100MB

## 🛠️ Built With

- **Python 3** - Core programming language
- **CustomTkinter** - Modern UI framework with gradient support
- **Pillow (PIL)** - Image metadata extraction (EXIF data)
- **PyInstaller** - Package into standalone executable

## 📌 Features Roadmap

- [ ] Dark/Light theme toggle
- [ ] Batch file conversion (format changes)
- [ ] Advanced regex pattern matching
- [ ] Preset templates for common renaming tasks
- [ ] Undo history with multiple levels
- [ ] File tagging system
- [ ] Cloud storage integration

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- UI/UX improvements
- New renaming patterns
- Bug fixes and optimizations
- Documentation improvements
- Test coverage

## 🐛 Known Issues

- Large file operations (>10,000 files) may take time on older systems
- EXIF data extraction works best with JPEG files

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📚 Documentation

For detailed documentation on advanced features and usage patterns, visit the [Wiki](https://github.com/scmandolikar/FileWrangler/wiki).

## ⭐ Star History

If you find FileWrangler useful, please consider giving it a star! ⭐

## 📧 Contact & Support

**Sakshath Mandolikar**
- Email: scmandolikar@gmail.com
- GitHub: [@scmandolikar](https://github.com/scmandolikar)
- LinkedIn: [Sakshath Mandolikar](https://www.linkedin.com/in/sushant-mandolikar-71a519256/)

For bug reports and feature requests, please use the [GitHub Issues](https://github.com/scmandolikar/FileWrangler/issues) page.

---

**Built with ❤️ by Sakshath Mandolikar** | TY BScIT Student | Made with Python & CustomTkinter
