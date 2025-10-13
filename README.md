# 🌐 iOS Localization Automation Script

Easily automate translation for iOS localization files (`.strings`) using **Google Translate API** via `googletrans`.
This script saves hours of manual work by automatically generating translated `.strings` files for multiple languages.

---

## 🚀 Features

* ✅ Automatically translates your base `Localizable.strings` file
* 🌍 Supports multiple target languages
* ⚡ Fast translation with progress tracking (`tqdm`)
* 🧩 Simple configuration for any iOS project structure

---

## 📦 Project Setup

### 1. Clone or Download the Repository

You can either:

* Click **Code → Download ZIP** on GitHub, then extract the files, or
* Clone the repository using **GitHub Desktop** or command line:

```bash
git clone https://github.com/MianMHaroon/translate_strings_xcode-iOS.git
```

---

### 2. Add the Script

Place the file **`translate_strings.py`** in the **root folder** of your iOS project.

Your project structure should look like this:

```
/MyProject
├── translate_strings.py
└── (your existing folders and files)
```

---

### 3. Install Python

Ensure you have **Python 3.x** installed.
You can download it from: [https://www.python.org/downloads](https://www.python.org/downloads)

To verify installation, open your terminal and run:

```bash
python --version
```

You should see something like:

```
Python 3.10.12
```

---

### 4. Install Required Libraries

Open your terminal and run:

```bash
pip install googletrans==4.0.0-rc1 tqdm
```

This installs:

* **googletrans** → for automatic translations via Google Translate
* **tqdm** → for displaying progress bars during translation

#### ⚙️ Alternatives if installation fails

**Option 1 — Use pip3 (macOS/Linux):**

```bash
pip3 install googletrans==4.0.0-rc1 tqdm
```

**Option 2 — Use Python’s module installer:**

```bash
python -m pip install googletrans==4.0.0-rc1 tqdm
```

**Option 3 — Install latest working version from GitHub:**

```bash
pip install git+https://github.com/ssut/py-googletrans.git
```

✅ **Tip:** Upgrade pip and setuptools if you face issues:

```bash
pip install --upgrade pip setuptools
```

---

### 5. Configure Your Project Path

Open **`translate_strings.py`** in a text editor and update:

```python
PROJECT_PATH = "./aichat3/Resources/Localization"
BASE_FILENAME = "Localizable.strings"
```

Example:

```python
PROJECT_PATH = "./MyApp/Resources/Localization"
BASE_FILENAME = "Base.strings"
```

> **Note:** `PROJECT_PATH` should point to the folder containing all `.lproj` folders (e.g., `en.lproj`, `fr.lproj`, `de.lproj`). Ensure each target language folder and `.strings` file exists.

---

### 6. Navigate to Your Project Directory

```bash
cd path/to/your/project
```

Example:

```bash
cd Desktop/MyProject
```

---

### 7. Run the Script

```bash
python translate_strings.py
```

Or, if Python 3 is default:

```bash
python3 translate_strings.py
```

---

## 🧠 Example Output

```
🌍 Translating 120 keys to 'fr'...
FR Progress: 100%|████████████████████| 120/120 [00:08<00:00, 14.83it/s]
🎉 fr: Translation file written to: ./MyApp/Resources/Localization/fr.lproj/Localizable.strings
```

---

## 💡 Notes & Tips

* Ensure your base `.strings` file is correctly formatted before running.
* Translations are powered by Google Translate; review results before release.
* You can extend this script to include custom APIs or additional file types.
* Ensure you have an active internet connection during translation.

---

## 🧩 Example Folder Structure

```
MyApp/
├── Resources/
│   └── Localization/
│       ├── en.lproj/
│       │   └── Localizable.strings
│       ├── fr.lproj/
│       │   └── Localizable.strings
│       ├── es.lproj/
│       │   └── Localizable.strings
│       └── de.lproj/
│           └── Localizable.strings
├── translate_strings.py
└── ...
```

---

---

## 🤝 Contributing

Pull requests are welcome! Open an **issue** on GitHub for bugs or improvements.

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute with attribution.
