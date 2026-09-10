# Pakistan Climate Analytics & Agro-Eco Portal Core Engine

A production-grade, highly modular decoupled Streamlit framework designed for computing agricultural and climatological indexes across Pakistan's diverse coordinate zones.

## 🏗️ Decoupled Architectural Layering
- `app.py`: UI Layer (Pure visualization execution).
- `workflow.py`: Algorithmic Computation Matrix Layer (No UI dependencies).
- `environmental_rules.py`: Policy, regulatory thresholds and regional adaptation parameters.
- `prompts.py`: Large Language Model formatting configurations and narrative strings.

## 🚀 Execution Guide
```bash
pip install -r requirements.txt
streamlit run app.py
```
