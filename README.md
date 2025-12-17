# NEXTIED Insurance Services Inc.

## Project Overview
This project is an AI-driven insurance automation prototype designed for **NEXTIED Insurance Services Inc.** The system centralizes the entire client workflow—from lead capture to policy submission—into a single intelligent dashboard. It demonstrates how AI and automation can simplify complex insurance operations and reduce manual efforts across departments.

## Problem Statement
Insurance operations often involve fragmented workflows, manual data entry, and disconnected systems for lead management, carrier selection, and policy submission. The client needed a solution to:
- Centralize client workflows.
- Automate lead capture and data extraction.
- Simplify the complex process of carrier recommendation and form filling.
- Reduce manual effort and errors in policy submission.

## Approach
We built a **Next.js-based unified dashboard** integrated with a **FastAPI backend** (represented by Python automation scripts in this repository) to provide real-time AI and automation capabilities. The system visualizes every stage of the insurance lifecycle:
1.  **Lead Detection**: Automatically retrieving and normalizing data from emails and other sources.
2.  **Information Gathering**: AI-guided forms to collect missing client data.
3.  **Carrier Recommendation**: AI analysis of risk profiles and appetite guides to suggest the best carriers.
4.  **AI Form Filling**: Automating the population of ACORD forms and supplemental documents.
5.  **Submission**: Automated submission to carrier portals using AI agents.

## Architecture
The system follows a modern, decoupled architecture:
- **Frontend**: Built with **Next.js**, providing an interactive dashboard, real-time updates, and a responsive UI.
- **Backend**: A **FastAPI**-based system (and supporting Python scripts) handling AI logic, data processing, and automation tasks.
- **AI & RAG**: Uses **OpenAI** for generative capabilities and **ChromaDB** (as part of the broader architecture) for Retrieval-Augmented Generation to query carrier guides and historical data.
- **Automation**: **Playwright** (via MCP) is used for browser automation to submit forms on carrier websites.
- **Communication**: Real-time AI chatbot for text and voice interactions.

## Tech Stack
- **Frontend**: Next.js, React, Tailwind CSS, Shadcn UI.
- **Backend**: Python, FastAPI (conceptual/script-based in this repo), Google Gmail API.
- **AI/ML**: OpenAI API (GPT-4o), ChromaDB (Vector Database), Agno (Agentic Framework).
- **Automation**: Playwright, Python Scripts.

---

## Detailed Explanations

### 1. File Structure & Explanation

#### `leads-workflow-app/` (Frontend)
This directory contains the Next.js application which serves as the main user interface.
- **`app/`**: Contains the application routes and pages.
    - **`page.tsx`**: The main dashboard page visualizing the workflow.
    - **`layout.tsx`**: Defines the common layout structure.
    - **`api/`**: Next.js API routes acting as a proxy or lightweight backend for specific features.
        - **`chat/route.ts`**: Handles the AI chatbot interactions, communicating directly with OpenAI.
- **`components/`**: Reusable UI components.
    - **`dashboard/`**: Components specific to the dashboard view (e.g., stats, charts).
    - **`workflow/`**: Components for the insurance workflow visualization (e.g., Kanban boards, lists).
    - **`chat/`**: Components for the AI chatbot interface.
    - **`ui/`**: Generic UI elements (buttons, inputs) based on Shadcn UI.
- **`lib/`**: Utility functions and helper classes.

#### `backend/` (Backend Logic)
This directory contains the Python logic for automation and backend processing.
- **`app.py`**: (Placeholder) Intended entry point for the FastAPI application.
- **`email.py`**: Script to authenticate with Gmail API and download attachments (leads).
- **`getLatestMails.py`**: Uses the `agno` agent framework to intelligently fetch and process the latest emails and attachments.
- **`form-filler/`**: Directory containing logic for filling PDF forms.
    - **`pdf_fillup_allfull.py`**: Script to populate ACORD forms and other PDFs with extracted data.

### 2. Flow-Based Explanation

1.  **Lead Ingestion**:
    - The process starts with `backend/getLatestMails.py` or `email.py`. These scripts connect to Gmail, identify lead emails, and extract attachments (spreadsheets, PDFs).
    - Data is normalized and made available to the system.

2.  **Dashboard Visualization**:
    - The user accesses the **Next.js Frontend** (`leads-workflow-app`).
    - The `page.tsx` renders the current state of leads, showing them in different stages (New, Processing, Submitted).

3.  **AI Interaction**:
    - Users can interact with the **AI Chatbot** (bottom right of the UI).
    - Requests are sent to `app/api/chat/route.ts`, which uses OpenAI to answer queries like "Show pending clients" or "Fill ACORD form".

4.  **Form Filling & Submission**:
    - When a lead moves to the "Form Filling" stage, the `backend/form-filler` scripts are triggered (conceptually linked via the backend API).
    - The AI maps client data to form fields and generates filled PDF documents.
    - Finally, an automation agent (Playwright) would navigate carrier portals to submit this data.

### 3. Approach & Technical Architecture

The project adopts a **Microservices-like approach** where the frontend and backend are loosely coupled but highly integrated.

- **Frontend-First Experience**: We prioritized a high-quality, responsive UI using Next.js to ensure the client (insurance agents) has a seamless experience. The dashboard is "state-aware," meaning it updates in real-time as the backend processes data.
- **Agentic Backend**: Instead of just simple CRUD APIs, the backend utilizes **AI Agents** (via `agno` and custom scripts). These agents are capable of performing complex tasks like "reading emails," "understanding form context," and "browsing websites."
- **Hybrid AI**: We use a combination of **LLMs (GPT-4o)** for reasoning and conversation, and **Deterministic Code** (Python scripts) for precise tasks like PDF manipulation and file handling. This ensures both flexibility and reliability.
