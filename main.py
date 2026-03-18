from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="MailCraft")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "anthropic/claude-sonnet-4-20250514"


class DraftRequest(BaseModel):
    context: str
    recipient: str = ""
    tone: str = "formal"
    email_type: str = "general"
    your_name: str = ""
    variations: int = 2


@app.post("/draft")
async def create_draft(req: DraftRequest):
    if not req.context.strip():
        raise HTTPException(status_code=400, detail="Context is required")

    recipient_info = f"\nRecipient: {req.recipient}" if req.recipient.strip() else ""
    sender_info = f"\nSender name: {req.your_name}" if req.your_name.strip() else ""

    type_descriptions = {
        "cold_outreach": "a cold outreach email to someone you haven't contacted before. Make it compelling and personalized.",
        "follow_up": "a follow-up email. Reference the previous interaction naturally and add value.",
        "proposal": "a business proposal email. Be clear about the value proposition and next steps.",
        "complaint": "a complaint email. Be firm but professional. Clearly state the issue and desired resolution.",
        "thank_you": "a thank-you email. Be genuine and specific about what you're grateful for.",
        "introduction": "a self-introduction email. Be concise, relevant, and memorable.",
        "meeting_request": "a meeting request email. Be clear about the purpose, suggested times, and agenda.",
        "general": "a professional email based on the context provided.",
    }

    type_desc = type_descriptions.get(req.email_type, type_descriptions["general"])
    num_variations = min(max(req.variations, 1), 3)

    system_prompt = (
        "You are MailCraft, an expert email writer who crafts perfect professional emails. "
        "Write clear, concise, and effective emails. Avoid filler words and cliches. "
        "Each email should have a clear subject line, greeting, body, and sign-off."
    )

    user_prompt = (
        f"Write {num_variations} different variations of {type_desc}\n\n"
        f"Context/Details: {req.context}\n"
        f"Tone: {req.tone}{recipient_info}{sender_info}\n\n"
        f"Format each variation as:\n"
        f"===VARIATION 1===\n"
        f"Subject: [subject line]\n\n"
        f"[email body]\n\n"
        f"===VARIATION 2===\n"
        f"Subject: [subject line]\n\n"
        f"[email body]\n\n"
        f"(and so on for each variation)\n\n"
        f"Make each variation meaningfully different in approach, not just rewording."
    )

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 3000,
            },
            timeout=60,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="AI request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

    # Parse variations
    variations = []
    parts = content.split("===VARIATION")
    for part in parts:
        part = part.strip()
        if not part or part.startswith("Here"):
            continue
        # Remove the number and === prefix
        part = part.lstrip("0123456789= \n")

        # Extract subject
        subject = ""
        body = part
        lines = part.split("\n")
        for i, line in enumerate(lines):
            if line.strip().lower().startswith("subject:"):
                subject = line.strip()[8:].strip()
                body = "\n".join(lines[i + 1 :]).strip()
                break

        if body:
            variations.append({"subject": subject, "body": body})

    # Fallback: if parsing failed
    if not variations:
        variations = [{"subject": "Email Draft", "body": content}]

    return {"variations": variations}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")
