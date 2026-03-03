# ⚖️ Gavel AI: Court Case Intelligence & Automation

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**Gavel AI** is an end-to-end automated pipeline designed to monitor court proceedings, analyze legal discourse using AI, and distribute summarized content to social media platforms. By combining automated scouting with high-fidelity transcription and LLM-driven synthesis, it transforms raw legal data into publishable media.



## 🚀 Key Features

* **Automated Scouting:** Scans and collects court case data through `scout.py`, generating structured datasets in `scout_output.json`.
* **AI-Powered Transcription:** Leverages **OpenAI Whisper** via `analyst_whisper.py` to convert courtroom audio into high-accuracy text transcripts.
* **Intelligent Synthesis:** Processes transcripts through advanced LLM agents (`analyst_pro.py`) to extract key legal arguments and dramatic highlights.
* **Automated Video Generation:** Prepares content for distribution using `editor.py`, streamlining the transition from text to visual media.
* **YouTube Distribution:** Seamlessly uploads finalized content to YouTube via `publisher.py` using official Google API integrations.

## 🛠 Tech Stack

| Category | Tool / Technology | Description |
| :--- | :--- | :--- |
| **Core** | Python 3.10+ | Primary programming language for the entire pipeline. |
| **Speech-to-Text** | OpenAI Whisper | High-accuracy transcription of courtroom audio recordings. |
| **Intelligence** | LLM Agents | Advanced text analysis and metadata generation (`analyst_pro.py`). |
| **Distribution** | YouTube Data API v3 | Automated video uploading and channel management (`publisher.py`). |
| **Infrastructure** | Docker | Ready for containerized deployment on Ubuntu servers. |

## 📂 Project Structure

* `scout.py` – Data harvesting and case monitoring.
* `analyst_*.py` – Multi-layered analysis suite (Transcription and Summarization).
* `editor.py` – Media preparation and content assembly.
* `publisher.py` – YouTube API client for automated uploads.
* `output/` – Directory for processed JSON and text results.

## ⚙️ Installation & Usage

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/1ldarb/gavel_ai.git](https://github.com/1ldarb/gavel_ai.git)
    cd gavel_ai
    ```
2.  **Environment Setup:**
    Create a `.env` file and populate it with your OpenAI and YouTube API credentials.
    *Note: `client_secrets.json` and `token.pickle` are required for the YouTube module but are excluded from the repository for security*.
3.  **Run the Pipeline:**
    ```bash
    source venv/bin/activate
    python3 analyst_whisper.py
    ```

---

### 🛡 Security
This project uses a strict `.gitignore` policy to prevent the accidental disclosure of API keys, tokens, and local media files.
