# SummarAIze 🤖✨

**SummarAIze** is an AI-powered document processing tool built in Python. It focuses on summarizing long documents quickly and accurately, and it’s designed with extensibility in mind—allowing you to add additional features such as rewriting, table extraction, and more.

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

## <a id="overview"></a>📖 Overview

SummarAIze aims to solve the problem of digesting lengthy documents by leveraging state-of-the-art NLP models like BART or Deepseek’s R1 model for summarization. The tool is designed as a command-line application initially, with plans to evolve into a full-featured UI-based tool after thorough testing. Its modular design leaves plenty of room for additional functionalities such as text rewriting, structured table extraction, and more.

## <a id="features"></a>✨ Features

- **📝 Document Summarization:** Quickly condense long texts into concise summaries.
- **🔧 Modular Design:** Easily extend the tool with additional NLP features like rewriting or table extraction.
- **📄 Multi-Format Support:** Initial support for text and PDF files with potential expansion to other formats (e.g., Word documents).
- **💻 Command-Line Interface (CLI):** Simple and effective terminal-based usage.
- **🖥️ Future UI Integration:** Plans for a graphical user interface to enhance usability.

## <a id="installation"></a>💾 Installation

### 🔹 Prerequisites

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)

### 🔹 Clone the Repository

```bash
git clone https://github.com/ErnestoLeiva/SummarAIze.git
cd SummarAIze
```

### 🔹 Install Dependencies

```bash
pip install -r requirements.txt
```

## <a id="usage"></a>🏃‍♂️ Usage

The basic usage of the tool via the command-line is as follows:
```bash
python ai-sum.py --summarize "PATH/TO/FILE"
```

### 🔹 Example

```bash
python ai-sum.py --summarize ./documents/sample.pdf
```
This command will process the specified file and output a concise summary to the terminal.

## <a id="roadmap"></a>🚀 Roadmap

- CLI Enhancements: Additional command-line options for custom summarization parameters (e.g., summary length, model selection).
- Feature Expansion:
  - ✍️ Rewriting: Allow users to rephrase or rewrite summaries.
  - 📊 Table Extraction: Parse and create structured tables from document data.
- 🖥️ UI Development: Transition from a CLI to a fully functional desktop/web UI.
- ⚙️ Performance Optimization: Fine-tune and optimize the summarization models for different types of documents.
- 📂 Multi-format Support: Extend support to additional document formats such as DOCX, HTML, etc.

## <a id="license"></a>📝 License
This project is open source and free to use under the MIT License. All derivative works must retain the original credits to Ernesto Leiva and the project contributors. See the **LICENSE** file for full details.

## <a id="contact"></a>📫 Contact

For questions, suggestions, or feedback, please reach out to:
- Ernesto Leiva – contact@ernestoleiva.com *(Project Lead)*
- Claudia Saleem - clau050994@gmail.com
- Gavin Greene - Gavingreene528@gmail.com
- Martin Valenica - mvale148@fiu.edu
- Sidney Bobadilla - Sidneybobadillaborjas@gmail.com
  
