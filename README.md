# Food, Explained

**Food, Explained exists because most food apps optimize for judgment, not understanding.**

This is an AI-powered assistant that helps you make informed decisions about food products through calm, contextual analysis and natural conversation.

## Philosophy

We explain, not judge.

Most food apps give you a red light or green light. We give you context. The same food can fit different lives, goals, and moments. What matters is dose, frequency, role, and trade-offs.

**Core Principles:**
- **Facts over fear**: No alarmist language or moral judgments about ingredients
- **Trade-offs over absolutes**: Everything has context—we explain, you decide
- **Transparency first**: Confidence levels are always explicit (barcode data is authoritative, LLM reasons only)
- **Practical over perfect**: Real-world guidance, not unrealistic ideals
- **User autonomy**: You know your life better than we do

**What This Is:**
- A tool for understanding ingredients and nutritional information
- A conversational interface that maintains context across questions
- A system that respects the complexity of food choices

**What This Is NOT:**
- Not a food rating or scoring system
- Not a health tracker or calorie counter
- Not medical advice or a replacement for healthcare professionals
- Not promoting diet culture or "clean eating" narratives
- Not a replacement for human judgment or personal context

## Overview

Food, Explained combines computer vision, external data sources, and large language models to provide contextual information about food products. Upload product images or enter barcodes to receive detailed analysis and engage in natural conversations about ingredients, nutritional information, and dietary considerations.

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

## Demo Scenarios

### Flagship: Dietary Restriction Check

**Context**: You're at the grocery store holding a packaged snack. You're vegetarian and lactose intolerant.

**Flow:**
1. Enter barcode: `737628064502`
2. System retrieves verified product data (high confidence)
3. Set preferences: "vegetarian, lactose intolerant"
4. Ask: "Can I eat this?"

**AI Response:**
```
## Short answer
This product contains milk powder—not suitable for lactose intolerance.
It is vegetarian (no meat/fish ingredients).

## What to know
Milk powder appears as the 4th ingredient. For lactose intolerance,
even small amounts can cause discomfort depending on your sensitivity.

## Trade-off
If your lactose intolerance is mild, you might tolerate this occasionally.
If severe, look for explicitly lactose-free alternatives.

## Practical takeaway
Keep this for non-restricted friends, or try the brand's dairy-free line.
```

**Follow-up**: "What if I have one occasionally?"

**AI Response:**
```
Depends on your sensitivity. Lactose intolerance varies:
- Some people handle small amounts fine
- Others react to traces

Since milk powder is mid-list (not the main ingredient), occasional
consumption might work if you're on the milder end. Pay attention to
how you feel after one serving.

Not medical advice—trust your body's signals.
```

**What This Shows:**
- High-confidence barcode data
- Preference-aware reasoning
- No judgment ("bad" vs "good")
- Practical, dose-aware guidance
- Honest about uncertainty

---

### Supporting: Ingredient Curiosity

**Context**: You're looking at a beverage with artificial sweeteners.

**Flow:**
1. Upload label image
2. System extracts "sucralose" via OCR
3. Ask: "What's sucralose?"

**AI Response:**
```
## Short answer
Sucralose is an artificial sweetener—much sweeter than sugar, zero calories.

## How it works
It passes through your body mostly unchanged. Your taste buds detect
sweetness, but it doesn't spike blood sugar like regular sugar.

## Trade-offs
- Sweetness without calories (useful for diabetes or weight goals)
- Some people report digestive discomfort at high doses
- Doesn't provide energy like sugar

## Practical takeaway
If you're trying to reduce sugar intake, this is one option. If you
prefer natural sweeteners, look for stevia or monk fruit instead.
```

**What This Shows:**
- OCR-based extraction
- Calm ingredient explanation
- Trade-offs without fear
- Alternative suggestions

---

### Supporting: Comparison Reasoning

**Context**: Deciding between two yogurt brands.

**Flow:**
1. User describes two products in a question
2. Ask: "Greek yogurt vs regular yogurt—which is better?"

**AI Response:**
```
## Key differences
Greek yogurt: strained (thicker), higher protein, lower sugar
Regular yogurt: more liquid, less protein, sometimes more sugar

## What to consider
If you want more protein → Greek
If you prefer smoother texture → Regular
If watching sugar → Check labels (both vary by brand)

## Practical takeaway
Neither is "better"—depends on your goal. Greek works well for
breakfast protein, regular works for smoothies or snacks.
```

**What This Shows:**
- Comparison without declaring winners
- Context-dependent reasoning
- Acknowledges both have valid use cases

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