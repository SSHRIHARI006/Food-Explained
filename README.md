# Food, Explained

An AI assistant for understanding food products through conversational analysis.

## Overview

Food, Explained analyzes food products from images or barcodes and provides contextual information through an interactive chat interface. The assistant maintains conversation history, allowing natural back-and-forth dialogue about products.

## Features

- Image upload and OCR text extraction
- Barcode lookup via OpenFoodFacts API
- Conversational interface with memory
- Product preview cards with confidence indicators
- User preference tracking
- Follow-up question support with full context awareness

## Installation

```bash
git clone https://github.com/yourusername/Food-Explained.git
cd Food-Explained
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Configuration

Create a `.env` file:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

```bash
streamlit run app.py
```

Access at `http://localhost:8501`

## Workflow

1. Upload product image or enter barcode
2. Receive initial analysis with product details
3. Ask follow-up questions in the chat interface
4. AI maintains context throughout conversation
5. Set dietary preferences in sidebar for personalized responses

## Project Structure

```
Food-Explained/
├── app.py
├── src/
│   ├── config/
│   │   ├── prompts_config.py
│   │   └── settings.py
│   ├── context/
│   │   ├── builder.py
│   │   ├── memory.py
│   │   └── schemas.py
│   ├── core/
│   │   ├── barcode.py
│   │   ├── ocr.py
│   │   └── product_preview.py
│   ├── reasoning/
│   │   └── chains.py
│   └── ui/
│       └── components.py
└── pyproject.toml
```

## Technology Stack

- Python 3.12+
- Streamlit
- EasyOCR
- OpenFoodFacts API
- Claude via Anthropic API
- LangChain
- Pydantic

## License

MIT