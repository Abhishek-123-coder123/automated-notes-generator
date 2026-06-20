# 🎙️ Corporate AI Meeting Minutes & Intelligence Canvas

A high-performance, hybrid AI application designed to transform raw acoustic conversation records into structured, multi-lingual executive briefs and visual semantic data dashboards.

## 🏛️ System Architecture Workflow
The pipeline is intentionally engineered as a hybrid framework to optimize cloud resource efficiency:
1. **Local Audio Extraction:** Processes raw audio bytes locally via `WhisperX` & `FFMPEG` wrappers to perform Voice Activity Detection (VAD) and map phoneme alignments down to the millisecond.
2. **Memory Performance Caching:** Utilizes Streamlit's `@st.cache_resource` infrastructure to isolate and store deep-learning model configurations directly in native RAM, eliminating the cold-start loading bottleneck.
3. **Cloud Cognitive Reasoning:** Transmits cleaned, timestamped text tokens to the `Gemini 2.5 Flash` engine alongside multi-lingual dynamic system prompts to translate and generate structured enterprise documentation.
4. **Data Analytics Canvas:** Leverages native arrays to scrub conversational text markers, passing structured metric arrays through `Matplotlib` to output graphic keyword frequency distributions.

## 🛠️ Tech Stack & Backend Components
- **Application Engine:** Streamlit Framework (Local Uvicorn Server Architecture)
- **Local AI Pipelines:** WhisperX Neural Networks, PyTorch Framework, Pyannote.audio VAD
- **Cognitive Cloud Model:** Google Gemini 2.5 Flash API
- **Visualization Framework:** Matplotlib
- **Document Rendering Core:** FPDF2 Vector Canvas
- **Enterprise Automation:** Python SMTP/MIME Mail Gateways

## 🚀 Installation & Local Execution
1. Clone the repository:
   ```bash
   git clone [https://github.com/Abhishek-123-coder123/automated-notes-generator.git](https://github.com/Abhishek-123-coder123/automated-notes-generator.git)
