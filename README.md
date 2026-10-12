# ai-invoice-agent
# print("Hello")
# AI Invoice Review Agent
 
An AI-powered, multi-agent system that reads invoice PDFs, checks them
for problems, and decides whether to approve, escalate, or reject them.
 
## Demo Video

 
## How it works
The following three agents work in sequence:
1. Document Processing Agent — reads the uploaded invoice PDF directly
   (Gemini 3.5 Flash-Lite) and extracts structured fields.
2. Completeness Gate (Tier 1) — checks five hard requirements. Any
   failure is disqualifying; the invoice is rejected outright.
3. Soft-Signal Scoring & Decision (Tier 2) — for invoices that clear
   the gate, checks softer risk signals and produces a confidence
   score. 95+ is auto-approved; anything lower is escalated.
 
## Tech stack
- n8n (workflow orchestration)
- Google Gemini 3.5 Flash-Lite (multimodal PDF reading)
- Streamlit (frontend)
- JavaScript (n8n Code nodes — validation and decision logic)
- Python (frontend)
 
## What's implemented
- PDF-based invoice reading, no separate OCR step
- A two-tier evaluation model: hard checks first, soft scoring second
- Three-way decision routing with a full visible reasoning trail
 
## What's not implemented (yet)
- Real persistent logging — duplicate/vendor-history checks use a
  small hardcoded sample list rather than a live database
- Email or Slack notifications for escalated invoices
- Handling of scanned or low-quality images
 
## Architecture
![Architecture diagram](docs/Agent Architecture n8n.pdf)
