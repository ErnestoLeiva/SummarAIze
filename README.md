<div align="center">
    <h1>SummarAIze 🤖✨</br>
      <img src="https://img.shields.io/github/package-json/v/ErnestoLeiva/SummarAIze?style=plastic&label=🔖 Version&color=orange&cacheSeconds=60" alt="Version#" >
      <img src="https://img.shields.io/badge/Python_+_Tkinter-Backend_+_Front--end-green?style=plastic&logo=python&logoColor=%233776AB" alt="Python">
      <img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-blue?style=plastic" alt="Hugging Face">
      <img src="https://img.shields.io/badge/%F0%9F%A4%97_Model-BART-purple?style=plastic" alt="BART">
      <img src="https://img.shields.io/badge/%F0%9F%A4%97_Model-DistilBART-purple?style=plastic" alt="DistilBART">
      <img src="https://img.shields.io/badge/%F0%9F%A4%97_Model-Google--T5-purple?style=plastic" alt="T5">
      <img src="https://img.shields.io/badge/ML/DL-TensorFlow-%23FF6F00.svg?style=plastic&logo=TensorFlow&logoColor=white" alt="TensorFlow">
      <img src="https://img.shields.io/badge/ML/DL-NumPy-%23013243.svg?style=plastic&logo=numpy&logoColor=white" alt="TensorFlow">
      <a href="LICENSE">
        <img src="https://img.shields.io/badge/⚖️_License-MIT-yellow.svg?style=plastic" alt="MIT License">
      </a>
      <img src="https://img.shields.io/badge/💻_IDE-Visual_Studio_Code-0078d7.svg?style=plastic&logo=visual-studio-code&logoColor=white" alt="Visual Studio Code IDE">
    </h1>

**SummarAIze** is an AI-powered legal document summarization tool built in Python. Designed to help legal professionals, students, and researchers quickly extract key information from long contracts and legal texts, SummarAIze runs entirely offline and is built with a modular architecture for future expansion.
</div>

## 📚 Table of Contents

- [Overview](#overview)
- [Motivation & Objectives](#motivation--objectives)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap & Milestones](#roadmap--milestones)
- [Maintenance](#maintenance)
- [License](#license)
- [Contact](#contact)

## <a id="overview"></a>📖 Overview

SummarAIze leverages lightweight, pre-trained NLP models such as **T5-Small**, **DistilBART**, and **BART** to perform extractive summarization of legal texts—focusing on contracts. The tool offers a simple command-line interface (CLI) and **runs entirely offline for enhanced privacy and accessibility**.

## <a id="motivation--objectives"></a>🎯 Motivation & Objectives

Legal documents are notoriously lengthy and complex. SummarAIze was created to:

- **📚 Summarize Legal Texts:**
  - Quickly condense contracts into clear, concise summaries.
- **🔑 Highlight Key Terms:**
  - Identify and display important legal terms to aid understanding.
- **🔒 Maintain Privacy:**
  - Operate offline so that sensitive legal data remains secure.
- **🧩 Establish a Modular Foundation:**
  - Enable future enhancements such as multi-format support and a graphical interface.

## <a id="features"></a>✨ Features

- **📝 Legal Document Summarization:**
  - Extracts key sentences from contracts and legal texts.
- **⚖️ Key Term Identification:**
  - Highlights frequently occurring legal terms and clauses.
- **🔧 Modular Design:**
  - Built as a command-line tool with future enhancements in mind.
- **📄 Format Support:**
  - Initially supports plain text (.txt) files with plans for support of more file types in the future.
- **💻 Offline Processing:**
  - Runs locally on standard hardware *without* the need for a GPU.

## <a id="installation"></a>💾 Installation

### 🔹 Prerequisites

- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)

### 🔹 Clone the Repository

```bash
git clone https://github.com/ErnestoLeiva/SummarAIze.git
cd SummarAIze
```

### 🔹 Install Dependencies

You can install the required dependencies using one of the following methods:

#### - Option 1: Using pip
![STANDARD](https://img.shields.io/badge/Universal%20(Mac%2FLinux%2FWindows)-gray?style=plastic&label=STANDARD&labelColor=blue)

```bash
pip install -r requirements.txt
```

#### - Option 2: Windows Installation Option (Using rqinst.bat)

- **Double-Click Method**
![EASIEST](https://img.shields.io/badge/Windows%20Only*-gray?style=plastic&label=EASIEST&labelColor=brightgreen)
  - If you prefer not to use the terminal, simply **double-click** the `rqinst.bat` file in File Explorer. The script will launch and guide you through the installation process interactively.
  
- **Using Visual Studio Code Terminal:**
![MANUAL](https://img.shields.io/badge/Windows%20Only*-gray?style=plastic&label=MANUAL&labelColor=orange)
  1. **Run Visual Studio Code as Administrator.**
  2. Open the integrated terminal.
  3. Run the following command:

     ```bat
     .\rqinst.bat
     ```

  4. Follow the on-screen instructions. The script will:
     - Check if *Python* is installed properly.
     - Verify that *pip* is available.
     - Install the specific versions of packages required for our project.

## <a id="usage"></a>🏃‍♂️ Usage

The basic usage of the tool via the command-line is as follows:

``` bash
python ai-sum.py --summarize "../PATH/TO/FILE"
```

### 🔹 CLI Examples

#### The usage screen showing available flags

<img src="https://i.imgur.com/iaetR92.png" alt="summarAIze"><br />

``` bash
python ai-sum.py --help
```

#### Example: Input flag using test file 'roman.txt'

``` bash
python ai-sum.py --summarize /test_files/roman.txt
```

#### Example: Input & Output flags using the test file 'roman.txt'

``` bash
python ai-sum.py --summarize /test_files/roman.txt --output /test_files/output.txt
```

#### Example: Input & Output & Model flags using the test file 'roman.txt'

``` bash
python ai-sum.py --summarize /test_files/roman.txt --output /test_files/output.txt --model distilbart
```

### 🔹 GUI Example

#### All the GUI features are visible from the main window, featured in the image below

<img src="https://i.imgur.com/DcKFcjH.png" alt="summarAIze"><br />



## <a id="roadmap--milestones"></a>🚀 Roadmap & Milestones

### 🎯 Immediate Objectives

- ~~**🛠️ Core Summarization Engine:**~~ ✅
  - ~~Implement extractive summarization using T5-Small/DistilBART/BART.~~
- ~~**📄 Text Format Support:**~~ ✅
  - ~~Focus on plain text (.txt) files with clear formatting guidelines.~~
- ~~**⌨️ CLI Implementation:**~~ ✅
  - ~~Allow users to input file paths and specify model.~~
- **🔑 Key Term Identification:**
  - Highlight and list frequently occurring legal terms.

### 📅 Milestones

- ~~**Week 1:** Set up the repository, install dependencies, and test NLP models with sample legal texts.~~ ✅
- ~~**Week 2:** Develop the basic summarization module with sentence extraction.~~ ✅
- ~~**Week 3:** Integrate key term identification and summary length customization.~~ 📝 ***under review***
- ~~**Week 4:** Finalize the CLI and improve text preprocessing for legal documents.~~ 📝 ***under review***
- ~~**Week 5:** Test with sample contracts and refine summary quality.~~ 📝 ***under review***
- **Week 6:** Complete documentation and prepare for the project demonstration.

### 🔮 Future Enhancements

- ~~**📑 Additional Format Support:**~~ ✅
  - ~~Expand support to additional file formats (PDF, DOCX).~~
- ~~**🏛️ Document Type Expansion:**~~ ✅
  - ~~Broaden to other legal document types (e.g., court opinions, regulations).~~
- **⚖️ Advanced Legal Clause Identification:**
  - Enhance identification of critical legal clauses.
- ~~**🖥️ GUI Development:**~~ ✅
  - ~~Develop a graphical user interface for a more user-friendly experience.~~

## <a id="maintenance"></a>⚒️ Maintenance

### Developer Responsibilities

- **📦 Versioning:**  
  - Use `upd-ver.bat` windows script or `npm version <type>` terminal command to manage semantic versioning (Patch/Minor/Major/Custom).
  - Update versions after significant changes and coordinate with the team.
- **🔍 Code Revisions:**  
  - Review your code for scalability, conflict prevention, and efficiency before pushing changes.
- **🔗 Consistency:**  
  - Follow established formatting, naming conventions, and folder structures.
- **🌿 Branching & Contributions:**  
  - Always pull the latest `main` before starting work, commit incrementally, and resolve conflicts before merging.
- **📚 Documentation:**  
  - Update the README, code comments, and roadmap as needed.

## <a id="license"></a>📝 License

This project is open source and free to use under the MIT License. All derivative works must retain the original credits to Ernesto Leiva and the project contributors. See the **[LICENSE](LICENSE)** file for full details.

## <a id="contact"></a>📫 Contact

For questions, suggestions, or feedback, please reach out to:

- Ernesto Leiva – <contact@ernestoleiva.com> *(Project Lead)*
- Claudia Saleem - <clau050994@gmail.com>
- Gavin Greene - <Gavingreene528@gmail.com>
- Martin Valenica - <mvale148@fiu.edu>
- Sidney Bobadilla - <Sidneybobadillaborjas@gmail.com>
