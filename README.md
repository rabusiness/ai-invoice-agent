# ai-invoice-agent
# print("Hello")
# AI Invoice Review Agent
 
An AI-powered, multi-agent system that reads invoice PDFs, checks them
for problems, and decides whether to approve, escalate, or reject them.
 
## Demo Video

 
## How it works
Three agents work in sequence:
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
docs/Agent Architecture n8n.pdf


The Problem:
Small and medium-sized businesses process invoices largely by hand: someone opens each PDF, reads the vendor and amount, checks it against what was actually ordered, and decides whether to pay it. This is slow, error-prone, and does not scale — a growing business either hires more people to do this same manual work, or starts making mistakes: paying duplicate invoices, missing math errors, or approving fraudulent-looking submissions simply because no one caught them in time. Larger enterprises solve this with expensive accounts-payable automation software; most small businesses cannot justify that cost, and end up with no automation at all.

The Approach: A Multi-Agent Pipeline
This project addresses that gap with a three-stage pipeline, where each stage has a single, well-defined job and hands its output to the next stage.

Agent 1 — Document Processing. Reads an uploaded invoice PDF directly using a multimodal AI model (Gemini 3.5 Flash-Lite) and converts it into structured data: vendor, invoice number, date, line items, tax, and total. This is the one stage that genuinely requires AI rather than conventional code — invoices arrive in wildly different layouts and formats from vendor to vendor, and a rule-based parser would need custom logic for every format it encounters, breaking the moment it saw something new. A multimodal model reads the document the way a person would, understanding structure and meaning rather than matching a fixed template.

Agent 2 — The Completeness Gate. Checks five hard requirements: is the vendor present, is the invoice number present, is the total valid, does the line-item math reconcile with the total, and is this a duplicate of a known invoice. Any single failure here is disqualifying — the invoice is rejected outright, with no further evaluation. This stage exists because certain problems are not "somewhat risky"; they mean the invoice cannot be processed at all until a human corrects it.

Agent 3 — Confidence Scoring & Decision. Runs only for invoices that have already passed the gate, and checks softer, genuinely uncertain signals: a first-time vendor, a suspiciously round total, a very small rounding discrepancy, or an unusual invoice date. None of these disqualify an invoice on their own — they simply indicate whether a quick human glance is warranted. Invoices scoring 95 or above are auto-approved; anything below is escalated for review.
