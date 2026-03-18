# MailCraft

Describe what you need to say and get multiple polished email drafts with different approaches. Supports cold outreach, follow-ups, proposals, complaints, and more.

![MailCraft Screenshot](static/screenshot.png)
<!-- Replace with actual screenshot -->

## Features

- **Multiple Variations** -- Get 1-3 meaningfully different email drafts per request
- **8 Email Types** -- Cold outreach, follow-up, proposal, complaint, thank-you, introduction, meeting request, and general
- **Tone Control** -- Formal, casual, friendly, assertive, or any custom tone
- **Smart Formatting** -- Each draft includes a subject line, greeting, body, and sign-off
- **Recipient & Sender Aware** -- Personalizes emails when you provide names
- **Instant Generation** -- All variations generated in a single request

## Supported Email Types

| Type | Description |
|------|-------------|
| `cold_outreach` | First contact with someone new -- compelling and personalized |
| `follow_up` | Reference a previous interaction and add value |
| `proposal` | Clear value proposition with next steps |
| `complaint` | Firm but professional with desired resolution |
| `thank_you` | Genuine and specific gratitude |
| `introduction` | Concise, relevant self-introduction |
| `meeting_request` | Purpose, suggested times, and agenda |
| `general` | Professional email from any context |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| AI Model | Claude Sonnet 4 via OpenRouter |
| Frontend | HTML + TailwindCSS (CDN) |

## Quick Start

### Prerequisites

- Python 3.10+
- OpenRouter API key ([get one here](https://openrouter.ai/keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/Seven7000000/mailcraft.git
cd mailcraft

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENROUTER_API_KEY="your-key-here"

# Run the server
uvicorn main:app --port 8005 --reload
```

Open [http://localhost:8005](http://localhost:8005) in your browser.

## API Reference

### `POST /draft`

Generate email draft variations.

**Request:**
```json
{
  "context": "I want to pitch my SaaS product to a marketing agency",
  "recipient": "Sarah Chen, CEO of BrightMedia",
  "tone": "professional",
  "email_type": "cold_outreach",
  "your_name": "Mustafa",
  "variations": 2
}
```

**Response:**
```json
{
  "variations": [
    {
      "subject": "Quick question about BrightMedia's content workflow",
      "body": "Hi Sarah,\n\nI noticed BrightMedia recently..."
    },
    {
      "subject": "Helping agencies like BrightMedia save 10hrs/week",
      "body": "Hi Sarah,\n\nMost marketing agencies spend..."
    }
  ]
}
```

### Parameters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `context` | string | required | What the email is about |
| `recipient` | string | `""` | Who you're writing to |
| `tone` | string | `"formal"` | Writing tone |
| `email_type` | string | `"general"` | See email types table above |
| `your_name` | string | `""` | Your name for sign-off |
| `variations` | int | `2` | Number of drafts (1-3) |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | Your OpenRouter API key |

## Project Structure

```
mailcraft/
  main.py             # FastAPI application
  requirements.txt    # Python dependencies
  static/
    index.html         # Single-page frontend
```

## License

MIT
