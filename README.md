````md
#  Mumbai Construction Compliance Assistant (AI + RAG)

An **AI-powered compliance assistant** for construction projects in **Mumbai**, built using **LLMs + Retrieval-Augmented Generation (RAG)**.  
The system analyzes a project description and generates a **stage-wise, regulation-backed compliance checklist** aligned with:

-  Mumbai DCPR 2034  
-  Maharashtra Fire Prevention & Life Safety Act  
-  NBC 2016 (Part 4 – Fire & Life Safety)  
-  BMC & MPCB Circulars (environment, pollution, parking, etc.)

This tool helps builders, architects, consultants, and planners **identify mandatory approvals, NOCs, and legal obligations** before, during, and after construction.

---

##  Key Features

-  **LLM + RAG powered compliance extraction**
-  Reads official Mumbai regulation PDFs
-  Stage-wise compliance breakdown:
  - Pre-construction
  - During construction
  - Post-construction
-  Compliance progress tracking (Completed / In Progress / Pending)
-  Local project persistence (JSON-based)
-  Clean Streamlit UI with dashboard & metrics
-  Non-diagnostic, advisory-only system (no legal automation)

---

##  System Architecture

```text
User Project Description
        ↓
Vector Search (Chroma DB)
        ↓
Relevant Regulation Chunks (PDFs)
        ↓
LLM (Azure OpenAI)
        ↓
Structured Compliance JSON
        ↓
Streamlit UI (Tracking & Dashboard)
````

---

##  Tech Stack

### Frontend

* Streamlit

### Backend / AI

* Python
* LangChain
* Azure OpenAI (LLM)
* HuggingFace Embeddings
* ChromaDB (Vector Store)

### Data Sources

* Government PDFs (DCPR, Fire Act, NBC, BMC Circulars)

---

##  Project Structure

```text
mumbai-compliance-ai/
│
├── app.py                  # Streamlit application (UI + flow)
├── build_index.py          # Builds vector DB from PDFs
├── requirements.txt        # Python dependencies
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── extractor.py        # RAG-based compliance extraction
│   ├── rag.py              # Vector DB + embeddings + LLM
│   ├── planner.py          # Project & compliance logic
│   └── storage.py          # JSON persistence
│
├── data/
│   └── pdfs/               # Government regulation PDFs
│
├── examples/
│   └── project_descriptions.txt       #can ask query in given format
│
├── 
└── .gitignore
```

---

## Setup & Installation

###  Clone the Repository

```bash
git clone https://github.com/<your-username>/mumbai-compliance-ai.git
cd mumbai-compliance-ai
```

###  Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
```

###  Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file using the template below:

```env
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_VERSION=2024-02-15-preview

EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

>  Never commit `.env` to GitHub

---

## Build Vector Database (One-Time)

1. Place official regulation PDFs inside:

```text
data/pdfs/
```

2. Run:

```bash
python build_index.py
```

This creates the local **Chroma vector database** used for RAG.

---

##  Run the Application

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

##  Example Use Cases

*  Residential buildings (G+5, high-rise)
*  Commercial & office complexes
*  Hospitals & medical institutions
*  Warehouses & industrial sheds
*  Redevelopment projects (DCPR 33 regulations)
*  Mixed-use developments

---

##  Important Disclaimer

This system:

*  Does NOT replace architects, lawyers, or authorities
*  Does NOT issue approvals or NOCs
*  Provides **AI-assisted guidance** based on official documents
*  Must be verified with concerned authorities (BMC, Fire Dept, MPCB)

---
