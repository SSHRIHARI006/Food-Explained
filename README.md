# Food, Explained

An AI-powered assistant for understanding food products through conversational analysis.

## Overview

Food, Explained is an intelligent food analysis application that combines computer vision, external data sources, and large language models to provide contextual information about food products. Users can upload product images or enter barcodes to receive detailed analysis and engage in natural conversations about ingredients, nutritional information, and dietary considerations.

## Features

### Core Functionalities

**Multi-Modal Input**
- Image upload with OCR-based text extraction
- Manual barcode entry for product lookup
- Direct question input for analysis

**Product Analysis**
- Barcode verification via OpenFoodFacts API
- Label text extraction using EasyOCR
- Confidence-based data validation
- Structured product information display

**Conversational Interface**
- Session-based conversation memory
- Context-aware follow-up questions
- Natural language dialogue with Claude AI
- Query classification for optimized responses

**User Preferences**
- Dietary goal tracking
- Restriction management
- Personalized response generation

## System Architecture

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
    ┌────▼─────────────────────────────────┐
    │         Application Layer            │
    │  ┌──────────────────────────────┐   │
    │  │  Session State Management    │   │
    │  │  - Product Data              │   │
    │  │  - Conversation History      │   │
    │  │  - User Preferences          │   │
    │  └──────────────────────────────┘   │
    └────┬─────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────┐
    │         Data Processing Layer        │
    │  ┌──────────┐  ┌──────────────────┐ │
    │  │   OCR    │  │  Barcode Lookup  │ │
    │  │ EasyOCR  │  │ OpenFoodFacts API│ │
    │  └──────────┘  └──────────────────┘ │
    └────┬─────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────┐
    │      Context Building Layer          │
    │  - Query Classification              │
    │  - Confidence Scoring                │
    │  - History Management                │
    │  - Preference Integration            │
    └────┬─────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────┐
    │       Reasoning Layer                │
    │  ┌──────────────────────────────┐   │
    │  │   LangChain + Claude API     │   │
    │  │  - Explanation Generation    │   │
    │  │  - Comparison Analysis       │   │
    │  │  - Follow-up Handling        │   │
    │  └──────────────────────────────┘   │
    └──────────────────────────────────────┘
```

## User Flow

1. **Initial Setup**
   - User opens the application
   - Optional: Configure dietary preferences in sidebar

2. **Product Input**
   - User selects input method (image upload or barcode)
   - Uploads product image or enters barcode number
   - Optionally provides an initial question

3. **Data Processing**
   - System attempts barcode lookup first (highest confidence)
   - Falls back to OCR if barcode unavailable
   - Extracts and validates product information

4. **Analysis Generation**
   - Context builder assembles available data
   - Query classifier determines response type
   - LLM generates contextual analysis
   - Product card displays structured information

5. **Conversational Interaction**
   - User asks follow-up questions via chat interface
   - System maintains conversation history
   - AI responds with context from previous exchanges
   - User preferences influence responses

6. **Session Management**
   - User can analyze new products (clears session)
   - Conversation history persists within session
   - Preferences stored in session state

## Core Logic

### Confidence Scoring System

The application uses a three-tier confidence system:

- **High Confidence**: Product data retrieved via barcode from OpenFoodFacts
- **Medium Confidence**: Information extracted via OCR from product labels
- **Low Confidence**: Limited or no product data available

### Query Classification

Incoming questions are automatically classified into three categories:

1. **Explanation**: General product analysis and information requests
2. **Comparison**: Questions comparing multiple products or alternatives
3. **Follow-up**: Context-dependent questions referencing conversation history

### Context Management

The system builds comprehensive context objects containing:
- Product data (name, brand, ingredients, nutrition)
- Data source and confidence level
- User query and classified type
- Conversation history
- User dietary preferences

This context is passed to the LLM for informed response generation.

## Technologies Used

### Frontend
- **Streamlit**: Web application framework with built-in UI components

### Computer Vision
- **EasyOCR**: Optical character recognition for label text extraction
- **PIL (Pillow)**: Image processing and manipulation

### Data Sources
- **OpenFoodFacts API**: Product database for barcode lookups
- **pyzbar**: Barcode detection and decoding

### AI & Language Processing
- **Anthropic Claude**: Large language model for analysis generation
- **LangChain**: Framework for LLM application orchestration
- **Pydantic**: Data validation and schema management

### State Management
- **Streamlit Session State**: In-memory conversation and preference storage
- **python-dotenv**: Environment variable management

## Project Structure

```
Food-Explained/
├── app.py                          # Main application entry point
├── packages.txt                    # System dependencies for deployment
├── pyproject.toml                  # Python dependencies
├── .env                            # API keys and configuration
├── src/
│   ├── config/
│   │   ├── settings.py            # Application settings and API keys
│   │   └── prompts_config.py      # LLM prompt templates
│   ├── context/
│   │   ├── schemas.py             # Pydantic data models
│   │   ├── memory.py              # Conversation history management
│   │   └── builder.py             # Context object construction
│   ├── core/
│   │   ├── barcode.py             # Barcode detection and API calls
│   │   ├── ocr.py                 # Image text extraction
│   │   └── product_preview.py     # Product card data extraction
│   ├── reasoning/
│   │   └── chains.py              # LangChain integration and LLM calls
│   └── ui/
│       └── components.py          # Reusable UI components
```

## Installation

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

Run locally:
```bash
streamlit run app.py
```

Access at `http://localhost:8501`

## Deployment

For Streamlit Cloud deployment:
1. Ensure `packages.txt` contains system dependencies (libzbar0)
2. Add `ANTHROPIC_API_KEY` to Streamlit Cloud secrets
3. Deploy via Streamlit Cloud dashboard

## License

MIT