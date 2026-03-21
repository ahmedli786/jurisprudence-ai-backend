"""
Jurisprudence AI - RAG-Powered Legal Backend
Uses Pinecone for semantic search + optional Claude for answer generation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import cohere
from pinecone import Pinecone
import os
import re

# =====================================================
# CONFIGURATION
# =====================================================
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "3udiW6SSREbgVGtQAnZVNLhfHHQeMuawnjvEKtRA")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "pcsk_6SYbmB_CnL9qw7DW3Swx3nqAbQfbiUQxJetBTuZPUCS5u3t9N9CAgQVD7ry3U3rncp3K4z")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")  # Optional
PINECONE_INDEX_NAME = "indian-legal"

# Initialize clients
co = cohere.Client(COHERE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Optional: Anthropic client
anthropic_client = None
if ANTHROPIC_API_KEY:
    try:
        import anthropic
        anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    except:
        pass

# =====================================================
# FASTAPI APP
# =====================================================
app = FastAPI(title="Jurisprudence AI - RAG Legal Intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# MODELS
# =====================================================
class QueryRequest(BaseModel):
    query: str
    include_hindi: bool = True
    top_k: int = 5

class Citation(BaseModel):
    section: str
    act_name: str
    relevance_score: float
    text: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    answer_hindi: Optional[str] = None
    confidence_score: float
    citations: List[Dict]
    follow_up_questions: List[Dict]
    source: str = "pinecone_rag"

class DocumentRequest(BaseModel):
    doc_type: str
    name: str
    father_name: Optional[str] = ""
    address: str
    details: str
    opposite_party: Optional[str] = ""
    police_station: Optional[str] = ""
    date_of_incident: Optional[str] = ""

# =====================================================
# RAG FUNCTIONS
# =====================================================

def embed_query(query: str) -> List[float]:
    """Generate embedding for search query"""
    try:
        response = co.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        return response.embeddings[0]
    except Exception as e:
        print(f"Embedding error: {e}")
        return []

def search_pinecone(query: str, top_k: int = 5) -> List[Dict]:
    """Search Pinecone for relevant legal content"""
    query_embedding = embed_query(query)
    
    if not query_embedding:
        return []
    
    try:
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        formatted_results = []
        for match in results.matches:
            formatted_results.append({
                'score': float(match.score),
                'text': match.metadata.get('text', ''),
                'act': match.metadata.get('act', ''),
                'section': match.metadata.get('section', ''),
                'title': match.metadata.get('title', ''),
                'punishment': match.metadata.get('punishment', ''),
                'category': match.metadata.get('category', ''),
            })
        
        return formatted_results
    except Exception as e:
        print(f"Pinecone search error: {e}")
        return []

def generate_answer_with_claude(query: str, context: List[Dict]) -> str:
    """Generate answer using Claude (if available)"""
    if not anthropic_client:
        return None
    
    # Build context string
    context_str = "\n\n".join([
        f"**{c['act']} - {c['section']} ({c['title']})**\n{c['text']}"
        for c in context[:5]
    ])
    
    prompt = f"""You are an expert Indian legal assistant. Based on the following legal provisions, answer the user's question accurately and comprehensively.

LEGAL CONTEXT:
{context_str}

USER QUESTION: {query}

Provide a clear, well-structured answer citing the relevant sections. Include:
1. Direct answer to the question
2. Relevant legal provisions with section numbers
3. Key points to remember
4. Any exceptions or special cases

Format your answer in HTML with <strong> for emphasis and <br> for line breaks."""

    try:
        response = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Claude error: {e}")
        return None

def generate_answer_from_context(query: str, results: List[Dict]) -> str:
    """Generate answer from retrieved context (without Claude)"""
    if not results:
        return "I couldn't find relevant information for your query. Please try rephrasing or ask about specific IPC sections, CrPC procedures, or Constitutional provisions."
    
    # Build answer from top results
    answer_parts = []
    
    # Main answer header
    top_result = results[0]
    answer_parts.append(f"<strong>{top_result['act']} - {top_result['section']}</strong>")
    if top_result.get('title'):
        answer_parts.append(f"<br><em>{top_result['title']}</em><br><br>")
    
    # Main content
    answer_parts.append(top_result['text'])
    
    # Add punishment if available
    if top_result.get('punishment'):
        answer_parts.append(f"<br><br><strong>Punishment:</strong> {top_result['punishment']}")
    
    # Add related sections if multiple results
    if len(results) > 1:
        answer_parts.append("<br><br><strong>Related Provisions:</strong><br>")
        for r in results[1:3]:
            answer_parts.append(f"• {r['act']} - {r['section']}: {r.get('title', '')}<br>")
    
    return "".join(answer_parts)

def translate_to_hindi(text: str) -> str:
    """Simple translation placeholder - in production use translation API"""
    # For now, return a generic Hindi message
    # In production, integrate Google Translate or similar
    return "कृपया विस्तृत हिंदी अनुवाद के लिए हमारी वेबसाइट पर जाएं।"

def generate_followup_questions(results: List[Dict]) -> List[Dict]:
    """Generate follow-up questions based on results"""
    followups = []
    
    if results:
        top = results[0]
        act = top.get('act', '')
        section = top.get('section', '')
        
        if 'Penal Code' in act:
            followups = [
                {"question": f"What is the punishment under {section}?"},
                {"question": "How to file FIR for this offense?"},
                {"question": "Is this a bailable offense?"}
            ]
        elif 'Criminal Procedure' in act:
            followups = [
                {"question": "What are my rights during arrest?"},
                {"question": "How to apply for bail?"},
                {"question": "What is anticipatory bail?"}
            ]
        elif 'Constitution' in act:
            followups = [
                {"question": "What are fundamental rights?"},
                {"question": "How to file a writ petition?"},
                {"question": "Difference between Article 32 and 226?"}
            ]
        else:
            followups = [
                {"question": "What is Section 302 IPC?"},
                {"question": "How to file FIR?"},
                {"question": "What are fundamental rights?"}
            ]
    
    return followups

# =====================================================
# API ENDPOINTS
# =====================================================

@app.get("/")
def root():
    return {
        "name": "Jurisprudence AI",
        "version": "3.0 RAG",
        "status": "running",
        "features": ["Semantic Search", "Pinecone RAG", "84+ Legal Sections"],
        "index": PINECONE_INDEX_NAME
    }

@app.get("/health")
def health():
    try:
        # Test Pinecone connection
        stats = index.describe_index_stats()
        vector_count = stats.total_vector_count
        return {
            "status": "healthy",
            "pinecone": "connected",
            "vectors": vector_count,
            "claude": "enabled" if anthropic_client else "disabled"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    """Main query endpoint with RAG"""
    
    # Search Pinecone
    results = search_pinecone(req.query, req.top_k)
    
    if not results:
        return QueryResponse(
            answer="I couldn't find relevant legal information for your query. Please try asking about specific IPC sections, CrPC procedures, Constitutional articles, or Evidence Act provisions.",
            answer_hindi="आपके प्रश्न के लिए प्रासंगिक कानूनी जानकारी नहीं मिली। कृपया विशिष्ट IPC धाराओं, CrPC प्रक्रियाओं, या संवैधानिक अनुच्छेदों के बारे में पूछें।",
            confidence_score=0.0,
            citations=[],
            follow_up_questions=[
                {"question": "What is Section 302 IPC?"},
                {"question": "How to file FIR?"},
                {"question": "What are fundamental rights?"}
            ],
            source="no_results"
        )
    
    # Generate answer
    if anthropic_client:
        answer = generate_answer_with_claude(req.query, results)
        if not answer:
            answer = generate_answer_from_context(req.query, results)
    else:
        answer = generate_answer_from_context(req.query, results)
    
    # Build citations
    citations = [
        {
            "section": r['section'],
            "act_name": r['act'],
            "relevance_score": round(r['score'], 2),
            "title": r.get('title', '')
        }
        for r in results[:5]
    ]
    
    # Calculate confidence
    confidence = results[0]['score'] if results else 0.0
    
    # Generate Hindi translation
    hindi = translate_to_hindi(answer) if req.include_hindi else None
    
    # Follow-up questions
    followups = generate_followup_questions(results)
    
    return QueryResponse(
        answer=answer,
        answer_hindi=hindi,
        confidence_score=round(confidence, 2),
        citations=citations,
        follow_up_questions=followups,
        source="pinecone_rag"
    )

@app.get("/stats")
def get_stats():
    """Get index statistics"""
    try:
        stats = index.describe_index_stats()
        return {
            "total_vectors": stats.total_vector_count,
            "dimension": stats.dimension,
            "index_name": PINECONE_INDEX_NAME
        }
    except Exception as e:
        return {"error": str(e)}

# =====================================================
# DOCUMENT GENERATION (Keep existing functionality)
# =====================================================

DOCUMENT_TEMPLATES = {
    "fir": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">FIRST INFORMATION REPORT (FIR)</h2>
<p style="text-align: center;">(Under Section 154 Cr.P.C.)</p>

<p><strong>To,</strong><br>
The Station House Officer,<br>
{police_station}<br><br>

<strong>Subject:</strong> Complaint regarding {subject}<br><br>

<strong>Respected Sir/Madam,</strong><br><br>

I, <strong>{name}</strong>, S/o / D/o / W/o <strong>{father_name}</strong>, aged about ____ years, residing at <strong>{address}</strong>, do hereby lodge the following complaint:<br><br>

<strong>1. Date & Time of Incident:</strong> {date_of_incident}<br><br>

<strong>2. Place of Incident:</strong> _______________<br><br>

<strong>3. Details of the Incident:</strong><br>
{details}<br><br>

<strong>4. Name & Description of Accused (if known):</strong><br>
{opposite_party}<br><br>

I request you to kindly register an FIR and take necessary legal action against the accused person(s) as per law.<br><br>

I declare that the above information is true to the best of my knowledge and belief.<br><br>

<table style="width: 100%; margin-top: 30px;">
<tr>
<td style="width: 50%;"><strong>Place:</strong> _______________</td>
<td style="text-align: right;"><strong>Signature of Complainant</strong></td>
</tr>
<tr>
<td><strong>Date:</strong> _______________</td>
<td style="text-align: right;">({name})</td>
</tr>
</table>
</div>
""",
    "affidavit": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">AFFIDAVIT</h2>

<p style="text-align: right;"><strong>BEFORE THE NOTARY PUBLIC / OATH COMMISSIONER</strong></p>

<p>I, <strong>{name}</strong>, S/o / D/o / W/o <strong>{father_name}</strong>, aged about ____ years, resident of <strong>{address}</strong>, do hereby solemnly affirm and declare as under:</p>

<ol style="line-height: 2;">
<li>That I am the deponent herein and competent to swear this affidavit.</li>
<li>That I am a citizen of India.</li>
<li>{details}</li>
<li>That the contents of this affidavit are true and correct.</li>
</ol>

<p style="margin-top: 30px;"><strong>VERIFICATION</strong></p>
<p>Verified at _____________ on this _____ day of _____________, 20____.</p>

<p style="text-align: right; margin-top: 40px;"><strong>DEPONENT</strong><br>({name})</p>
</div>
""",
    "legal_notice": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">LEGAL NOTICE</h2>

<p style="text-align: right;"><strong>Date:</strong> _______________</p>

<p><strong>To,</strong><br>{opposite_party}<br><br>

<strong>From:</strong><br>{name}<br>{address}<br><br>

<strong>Subject:</strong> Legal Notice<br><br>

Under instructions from my client <strong>{name}</strong>, I hereby serve upon you the following Legal Notice:<br><br>

<strong>FACTS:</strong><br>{details}<br><br>

You are hereby called upon to comply within <strong>15 days</strong> from receipt of this notice, failing which legal proceedings shall be initiated.<br><br>

<p style="text-align: right;"><strong>Advocate for {name}</strong></p>
</div>
""",
    "rti": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">RTI APPLICATION</h2>
<p style="text-align: center;">(Under Right to Information Act, 2005)</p>

<p><strong>To,</strong><br>The Public Information Officer,<br>{opposite_party}<br><br>

<strong>From:</strong><br>{name}<br>{address}<br><br>

<strong>Subject:</strong> Application seeking information under RTI Act, 2005<br><br>

I, <strong>{name}</strong>, an Indian citizen, request the following information:<br><br>

<strong>INFORMATION SOUGHT:</strong><br>{details}<br><br>

<strong>FEE:</strong> Rs. 10/- enclosed via _____________ No. _____________<br><br>

<p style="text-align: right;"><strong>Signature</strong><br>({name})</p>
</div>
""",
    "bail": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">BAIL APPLICATION</h2>
<p style="text-align: center;">(Under Section 437/439 Cr.P.C.)</p>

<p><strong>IN THE COURT OF _______________</strong></p>

<p><strong>{name}</strong>, S/o {father_name}, R/o {address}<br>... Applicant/Accused</p>
<p style="text-align: center;"><strong>VERSUS</strong></p>
<p><strong>State</strong> through SHO, {police_station}<br>... Respondent</p>

<p><strong>FIR No.:</strong> _____  <strong>U/s:</strong> _______________</p>

<p><strong>GROUNDS:</strong></p>
<ol>
<li>The applicant is innocent and has been falsely implicated.</li>
<li>{details}</li>
<li>The applicant has no criminal antecedents.</li>
<li>The applicant undertakes to cooperate with investigation.</li>
</ol>

<p><strong>PRAYER:</strong> Grant bail to the applicant.</p>

<p style="text-align: right;"><strong>Applicant/Through Counsel</strong></p>
</div>
""",
    "complaint_consumer": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">CONSUMER COMPLAINT</h2>
<p style="text-align: center;">(Under Consumer Protection Act, 2019)</p>

<p><strong>BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION</strong></p>

<p><strong>{name}</strong>, {address}<br>... COMPLAINANT</p>
<p style="text-align: center;"><strong>VERSUS</strong></p>
<p><strong>{opposite_party}</strong><br>... OPPOSITE PARTY</p>

<p><strong>FACTS:</strong></p>
<ol>
<li>The complainant is a consumer as defined under the Act.</li>
<li>{details}</li>
<li>The above acts amount to deficiency in service / unfair trade practice.</li>
</ol>

<p><strong>PRAYER:</strong> Direct the opposite party to refund/compensate as appropriate.</p>

<p style="text-align: right;"><strong>COMPLAINANT</strong><br>({name})</p>
</div>
""",
    "poa": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">POWER OF ATTORNEY</h2>

<p>I, <strong>{name}</strong>, S/o / D/o / W/o <strong>{father_name}</strong>, residing at <strong>{address}</strong>, do hereby appoint:</p>

<p><strong>{opposite_party}</strong></p>

<p>as my true and lawful Attorney to do the following on my behalf:</p>

<ol>
<li>{details}</li>
<li>To sign, execute documents as necessary.</li>
<li>To appear before any authority on my behalf.</li>
</ol>

<p><strong>IN WITNESS WHEREOF</strong>, I have signed on this _____ day of _____________, 20____.</p>

<p style="text-align: right;"><strong>PRINCIPAL</strong><br>({name})</p>
</div>
"""
}

@app.get("/document-types")
def get_document_types():
    return {
        "available_documents": [
            {"type": "fir", "name": "FIR Draft", "description": "Police complaint"},
            {"type": "affidavit", "name": "Affidavit", "description": "Sworn statement"},
            {"type": "legal_notice", "name": "Legal Notice", "description": "Formal notice"},
            {"type": "rti", "name": "RTI Application", "description": "Information request"},
            {"type": "bail", "name": "Bail Application", "description": "Bail petition"},
            {"type": "complaint_consumer", "name": "Consumer Complaint", "description": "Consumer forum"},
            {"type": "poa", "name": "Power of Attorney", "description": "Authorization"}
        ]
    }

@app.post("/generate-document")
def generate_document(req: DocumentRequest):
    doc_type = req.doc_type.lower()
    
    if doc_type not in DOCUMENT_TEMPLATES:
        return {"success": False, "error": "Invalid document type"}
    
    template = DOCUMENT_TEMPLATES[doc_type]
    subject = req.details[:50] if req.details else "Legal Matter"
    
    document = template.format(
        name=req.name or "_______________",
        father_name=req.father_name or "_______________",
        address=req.address or "_______________",
        details=req.details or "_______________",
        opposite_party=req.opposite_party or "_______________",
        police_station=req.police_station or "_______________",
        date_of_incident=req.date_of_incident or "_______________",
        subject=subject
    )
    
    instructions = {
        "fir": "Print and submit to Police Station. Keep a copy.",
        "affidavit": "Get notarized from a Notary Public.",
        "legal_notice": "Send via Registered Post AD. Keep receipt.",
        "rti": "Submit with Rs.10 fee. Keep acknowledgment.",
        "bail": "File through your lawyer in court.",
        "complaint_consumer": "File at edaakhil.nic.in or Consumer Forum.",
        "poa": "Get registered at Sub-Registrar for property matters."
    }
    
    return {
        "success": True,
        "document_type": doc_type,
        "document_html": document,
        "instructions": instructions.get(doc_type, "Consult a lawyer.")
    }

# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
