# ⚖️ Gavel AI: Court Case Intelligence & Automation

Gavel AI is an end-to-end automated pipeline designed to monitor court proceedings, analyze legal discourse using AI, and distribute summarized content to social media platforms. By combining automated scouting with high-fidelity transcription and LLM-driven synthesis, it transforms raw legal data into publishable media.

# 🚀 Key Features
Automated Scouting: Scans and collects court case data through scout.py, generating structured datasets in scout_output.json.

AI-Powered Transcription: Leverages OpenAI Whisper via analyst_whisper.py to convert courtroom audio into high-accuracy text transcripts.

Intelligent Synthesis: Processes transcripts through advanced LLM agents (analyst_pro.py) to extract key legal arguments, rulings, and dramatic highlights.

Automated Video Generation: Prepares content for distribution using editor.py, streamlining the transition from text to visual media.

YouTube Distribution: Seamlessly uploads finalized content to YouTube via publisher.py using official Google API integrations.

# 🛠 Tech Stack
Language: Python 3.10+.

Speech-to-Text: OpenAI Whisper (ASR).

AI Orchestration: Large Language Models (LLMs) for content synthesis and metadata generation.

Integrations: Google YouTube Data API v3.

Environment: Asynchronous processing and Docker-ready architecture.

# 📂 Project Structure
scout.py – Data harvesting and case monitoring.

analyst_*.py – Multi-layered analysis suite (Transcription, NLP, and Summarization).

editor.py – Media preparation and content assembly.

publisher.py – YouTube API client for automated uploads.

output/ – Directory for processed JSON and text results.

downloads/ – Local storage for raw courtroom audio and media.
