# Food, Explained

An AI assistant that helps you understand food in context, not judge it.

## Overview

Food, Explained is an intelligent food assistant designed to help users make informed decisions about what they eat. It explains ingredients, processes, and trade-offs without resorting to fear-mongering or oversimplified good/bad labels.

## Core Philosophy

This is an AI food assistant, not a food database or rating engine.

The assistant:
- Explains food in context
- Avoids labeling foods as good, bad, healthy, or unhealthy
- Focuses on dose, frequency, role, and trade-offs
- Encourages practical, realistic decisions
- Does not chase perfect eating

## Features

### Multi-Modal Input
- Upload images of food packaging labels
- Manual barcode entry
- Natural language questions

### Product Recognition
- OCR text extraction from product images
- Barcode lookup via OpenFoodFacts API
- Explicit confidence levels for all data

### Conversational Memory
- Session-based conversation tracking
- Follow-up question support
- User dietary preferences and goals

### Intelligent Reasoning
- Query classification for targeted responses
- Comparison mode for multiple products
- Context-aware explanations
- Powered by Claude via LangChain

## Installation

This project uses uv for dependency management.

```bash
git clone https://github.com/yourusername/Food-Explained.git
cd Food-Explained
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Configuration

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the Streamlit application:

```bash
.venv/bin/python -m streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
Food-Explained/
├── app.py                 Main Streamlit application
├── src/
│   ├── config/           Configuration and prompts
│   ├── context/          Context building and memory
│   ├── core/             OCR, barcode, product preview
│   ├── reasoning/        LangChain-based reasoning
│   └── ui/               Reusable UI components
└── pyproject.toml        Project dependencies
```

## How It Works

1. User provides input via image, barcode, or text question
2. System extracts product information with confidence tracking
3. Context builder assembles all available data
4. Query classifier determines response type
5. LangChain chain generates contextual explanation
6. Conversation memory enables follow-up questions

## Key Principles

- Facts are separated from interpretation
- Barcode data is authoritative, LLM is for reasoning only
- Confidence levels are always explicit
- No hallucinated product names or details
- Memory is session-scoped and opt-in
- No autonomous agents or complex workflows

## Technology Stack

- Python 3.12+
- Streamlit for UI
- EasyOCR for text extraction
- OpenFoodFacts API for product data
- Claude (Haiku) via Anthropic API
- LangChain for prompt orchestration
- Pydantic for data validation

## Development

The codebase is organized for clarity and maintainability:

- Type-safe context objects using Pydantic
- Modular UI components
- Configurable prompts for different query types
- Clean separation between data sources and reasoning

## License

MIT

## Contributing

This project prioritizes simplicity and clarity. Contributions should maintain the core philosophy of explanation over judgment.