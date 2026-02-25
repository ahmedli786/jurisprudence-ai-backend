"""
Jurisprudence AI - Legal Intelligence API
FastAPI Backend for Indian Legal RAG System
"""

import os
import time
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cohere
from pinecone import Pinecone
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "indian-legal")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# ==================== INITIALIZE ====================
app = FastAPI(
    title="Jurisprudence AI",
    description="Legal Intelligence API for Indian Law",
    version="1.0.0"
)

# CORS - Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients (lazy loading)
cohere_client = None
pinecone_index = None
anthropic_client = None

def get_cohere():
    global cohere_client
    if cohere_client is None and COHERE_API_KEY:
        cohere_client = cohere.Client(COHERE_API_KEY)
    return cohere_client

def get_pinecone():
    global pinecone_index
    if pinecone_index is None and PINECONE_API_KEY:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        pinecone_index = pc.Index(PINECONE_INDEX)
    return pinecone_index

def get_anthropic():
    global anthropic_client
    if anthropic_client is None and ANTHROPIC_API_KEY:
        anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return anthropic_client

# ==================== MODELS ====================
class QueryRequest(BaseModel):
    query: str
    include_hindi: bool = True
    llm: str = "claude"
    top_k: int = 7
    namespace: Optional[str] = None

class Citation(BaseModel):
    source_index: int = 0
    section: Optional[str] = None
    act_name: Optional[str] = None
    case_citation: Optional[str] = None
    relevance_score: float = 0.0
    text_snippet: Optional[str] = None

class FollowUpQuestion(BaseModel):
    question: str
    intent: str = "related"

class QueryResponse(BaseModel):
    answer: str
    answer_hindi: Optional[str] = None
    confidence_score: float
    citations: List[Citation] = []
    follow_up_questions: List[FollowUpQuestion] = []
    llm_used: str
    processing_time_ms: int

class HealthResponse(BaseModel):
    status: str
    services: dict

# ==================== LEGAL KNOWLEDGE ====================
# Built-in legal knowledge for common queries (fallback when no vector DB)
LEGAL_KNOWLEDGE = {
    "302": {
        "answer": """<strong>Section 302 of the Indian Penal Code (IPC)</strong> deals with the <strong>punishment for murder</strong>.

According to this section, whoever commits murder shall be punished with:
• <strong>Death penalty</strong>, or
• <strong>Imprisonment for life</strong>, and shall also be liable to <strong>fine</strong>.

<strong>Key Legal Principles:</strong>
1. The prosecution must prove the accused caused the death with intention or knowledge
2. The Supreme Court in <em>Bachan Singh vs State of Punjab (1980)</em> established the "rarest of rare" doctrine for death penalty
3. Life imprisonment means imprisonment for the remainder of natural life unless commuted

<strong>Related Sections:</strong>
• Section 300 - Definition of Murder
• Section 299 - Culpable Homicide
• Section 304 - Culpable Homicide not amounting to Murder""",
        "hindi": "भारतीय दंड संहिता की <strong>धारा 302</strong> हत्या की सजा से संबंधित है। इस धारा के अनुसार, जो कोई हत्या करता है उसे मृत्यु दंड या आजीवन कारावास से दंडित किया जाएगा, और जुर्माना भी देना होगा।",
        "citations": [
            {"section": "Section 302", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.98},
            {"case_citation": "Bachan Singh vs State of Punjab (1980) 2 SCC 684", "relevance_score": 0.92},
            {"section": "Section 300", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.85}
        ],
        "followups": ["What is culpable homicide not amounting to murder?", "Explain the rarest of rare doctrine", "Difference between Section 302 and 304 IPC"]
    },
    "498a": {
        "answer": """<strong>Section 498A of the IPC</strong> deals with <strong>cruelty by husband or his relatives</strong> against a married woman.

<strong>Key Points:</strong>
• It is a <strong>cognizable</strong> and <strong>non-bailable</strong> offense
• Punishment: Imprisonment up to <strong>3 years</strong> and fine
• Covers both <strong>physical and mental cruelty</strong>
• Includes harassment for <strong>dowry demands</strong>

<strong>What constitutes cruelty:</strong>
1. Willful conduct likely to drive the woman to suicide
2. Conduct likely to cause grave injury to life, limb, or health
3. Harassment for dowry demands

<strong>Important Judgments:</strong>
• <em>Arnesh Kumar vs State of Bihar (2014)</em> - Guidelines to prevent misuse
• <em>Rajesh Sharma vs State of UP (2017)</em> - Family Welfare Committees

<strong>Note:</strong> False cases can be quashed under Section 482 CrPC if found to be malicious.""",
        "hindi": "आईपीसी की <strong>धारा 498A</strong> पति या उसके रिश्तेदारों द्वारा विवाहित महिला के साथ क्रूरता से संबंधित है। यह एक संज्ञेय और गैर-जमानती अपराध है। सजा: 3 साल तक की कैद और जुर्माना।",
        "citations": [
            {"section": "Section 498A", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.97},
            {"case_citation": "Arnesh Kumar vs State of Bihar (2014) 8 SCC 273", "relevance_score": 0.91},
            {"case_citation": "Rajesh Sharma vs State of UP (2017) 8 SCC 446", "relevance_score": 0.86}
        ],
        "followups": ["How to file a 498A complaint?", "Can 498A case be quashed?", "What is the procedure after 498A FIR?"]
    },
    "420": {
        "answer": """<strong>Section 420 of the IPC</strong> deals with <strong>cheating and dishonestly inducing delivery of property</strong>.

<strong>Punishment:</strong>
• Imprisonment up to <strong>7 years</strong>, AND
• <strong>Fine</strong>

<strong>Essential Elements:</strong>
1. Deception of any person
2. Fraudulent or dishonest inducement
3. Delivery of property or valuable security
4. Intention to cheat from the beginning

<strong>What constitutes cheating (Section 415):</strong>
• Making false representation
• Fraudulent concealment of facts
• Causing wrongful loss to another

<strong>Common Examples:</strong>
• Fraud in property deals
• Fake investment schemes
• Bounced cheques with dishonest intent
• Online/cyber fraud""",
        "hindi": "आईपीसी की <strong>धारा 420</strong> धोखाधड़ी और बेईमानी से संपत्ति प्राप्त करने से संबंधित है। सजा: 7 साल तक की कैद और जुर्माना।",
        "citations": [
            {"section": "Section 420", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.96},
            {"section": "Section 415", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.88}
        ],
        "followups": ["How to file cheating complaint?", "Difference between 406 and 420 IPC", "Is bounced cheque covered under 420?"]
    },
    "fir": {
        "answer": """<strong>FIR (First Information Report)</strong> is the first step in criminal proceedings.

<strong>How to File an FIR:</strong>
1. Go to the <strong>police station</strong> having jurisdiction
2. Provide <strong>written or oral</strong> information about the offense
3. Information is recorded by the officer in charge
4. Get a <strong>free copy</strong> of the FIR (your right under Section 154 CrPC)

<strong>Key Legal Provisions:</strong>
• <strong>Section 154 CrPC</strong> - Recording of FIR
• <strong>Section 155 CrPC</strong> - Non-cognizable offenses
• <strong>Zero FIR</strong> - Can be filed at ANY police station

<strong>Your Rights:</strong>
• Police CANNOT refuse to register FIR for cognizable offense
• If refused, complaint to SP or Magistrate (Section 156(3) CrPC)
• Free copy of FIR must be provided
• Woman complainant can record statement at her residence

<strong>Time Limit:</strong>
• No time limit, but delay must be explained
• Early filing strengthens the case""",
        "hindi": "<strong>FIR (प्रथम सूचना रिपोर्ट)</strong> आपराधिक कार्यवाही का पहला कदम है। आप किसी भी पुलिस स्टेशन में FIR दर्ज करा सकते हैं। पुलिस संज्ञेय अपराध के लिए FIR दर्ज करने से मना नहीं कर सकती।",
        "citations": [
            {"section": "Section 154", "act_name": "Code of Criminal Procedure, 1973", "relevance_score": 0.95},
            {"section": "Section 156(3)", "act_name": "Code of Criminal Procedure, 1973", "relevance_score": 0.89}
        ],
        "followups": ["What if police refuses to file FIR?", "What is Zero FIR?", "Difference between FIR and complaint"]
    },
    "bail": {
        "answer": """<strong>Bail in Indian Law</strong> - Your right to freedom during trial.

<strong>Types of Bail:</strong>

1. <strong>Regular Bail (Section 437/439 CrPC)</strong>
   • Applied after arrest
   • Granted by Magistrate or Sessions Court

2. <strong>Anticipatory Bail (Section 438 CrPC)</strong>
   • Applied BEFORE arrest
   • Granted by Sessions Court or High Court
   • Protection against arrest

3. <strong>Interim Bail</strong>
   • Temporary bail pending final decision
   • Usually for short duration

<strong>Factors Courts Consider:</strong>
• Nature and gravity of offense
• Criminal antecedents
• Flight risk
• Tampering with evidence/witnesses
• Health conditions

<strong>Landmark Cases:</strong>
• <em>Sushila Aggarwal vs State (2020)</em> - Anticipatory bail guidelines
• <em>Arnesh Kumar (2014)</em> - Arrest guidelines""",
        "hindi": "<strong>जमानत</strong> मुकदमे के दौरान स्वतंत्रता का अधिकार है। नियमित जमानत गिरफ्तारी के बाद और अग्रिम जमानत गिरफ्तारी से पहले ली जाती है।",
        "citations": [
            {"section": "Section 437", "act_name": "Code of Criminal Procedure, 1973", "relevance_score": 0.94},
            {"section": "Section 438", "act_name": "Code of Criminal Procedure, 1973", "relevance_score": 0.93},
            {"case_citation": "Sushila Aggarwal vs State (2020) 5 SCC 1", "relevance_score": 0.88}
        ],
        "followups": ["How to apply for anticipatory bail?", "Can bail be cancelled?", "What is the bail amount decided?"]
    },
    "fundamental": {
        "answer": """<strong>Fundamental Rights</strong> are guaranteed under <strong>Part III (Articles 12-35)</strong> of the Indian Constitution.

<strong>The Six Fundamental Rights:</strong>

1. <strong>Right to Equality (Articles 14-18)</strong>
   • Equality before law
   • No discrimination
   • Abolition of untouchability

2. <strong>Right to Freedom (Articles 19-22)</strong>
   • Speech and expression
   • Assembly, association, movement
   • Protection of life and liberty (Article 21)

3. <strong>Right Against Exploitation (Articles 23-24)</strong>
   • No human trafficking
   • No child labor in hazardous industries

4. <strong>Right to Freedom of Religion (Articles 25-28)</strong>
   • Freedom of conscience and religion

5. <strong>Cultural & Educational Rights (Articles 29-30)</strong>
   • Protection of minorities

6. <strong>Right to Constitutional Remedies (Article 32)</strong>
   • Right to approach Supreme Court
   • Dr. Ambedkar called it "Heart and Soul of Constitution"

<strong>Writs Available:</strong> Habeas Corpus, Mandamus, Certiorari, Prohibition, Quo Warranto""",
        "hindi": "<strong>मौलिक अधिकार</strong> भारतीय संविधान के भाग III (अनुच्छेद 12-35) में दिए गए हैं। ये छह प्रकार के हैं: समानता, स्वतंत्रता, शोषण के विरुद्ध, धार्मिक स्वतंत्रता, सांस्कृतिक और शैक्षिक, और संवैधानिक उपचार का अधिकार।",
        "citations": [
            {"section": "Part III", "act_name": "Constitution of India", "relevance_score": 0.97},
            {"section": "Article 21", "act_name": "Constitution of India", "relevance_score": 0.94},
            {"section": "Article 32", "act_name": "Constitution of India", "relevance_score": 0.91}
        ],
        "followups": ["Can fundamental rights be suspended?", "What is Article 21?", "How to file writ petition?"]
    },
    "rti": {
        "answer": """<strong>Right to Information (RTI) Act, 2005</strong> empowers citizens to seek information from public authorities.

<strong>How to File RTI:</strong>

1. <strong>Write Application</strong> to Public Information Officer (PIO)
2. <strong>Fee:</strong> ₹10 (postal order/DD/cash)
3. <strong>Response Time:</strong> 30 days (48 hours for life/liberty matters)
4. <strong>First Appeal:</strong> To First Appellate Authority within 30 days
5. <strong>Second Appeal:</strong> To Information Commission within 90 days

<strong>What You Can Ask:</strong>
• Government records, documents, files
• Decisions and reasons
• Expenditure details
• Contract copies

<strong>Exemptions (Section 8):</strong>
• National security
• Cabinet papers
• Personal privacy
• Trade secrets

<strong>Key Points:</strong>
• BPL applicants: No fee
• No reason needed for seeking information
• PIO must help if request is vague""",
        "hindi": "<strong>सूचना का अधिकार (RTI) अधिनियम, 2005</strong> नागरिकों को सरकारी अधिकारियों से जानकारी मांगने का अधिकार देता है। आवेदन शुल्क ₹10 है और जवाब 30 दिनों में मिलना चाहिए।",
        "citations": [
            {"section": "Section 6", "act_name": "Right to Information Act, 2005", "relevance_score": 0.96},
            {"section": "Section 7", "act_name": "Right to Information Act, 2005", "relevance_score": 0.93},
            {"section": "Section 8", "act_name": "Right to Information Act, 2005", "relevance_score": 0.89}
        ],
        "followups": ["RTI application format", "What if RTI is not answered?", "Can RTI be filed online?"]
    }
}

# ==================== HELPER FUNCTIONS ====================
def find_matching_knowledge(query: str) -> Optional[dict]:
    """Find matching built-in knowledge based on query keywords"""
    query_lower = query.lower()
    
    # Check for matches
    if "302" in query_lower or "murder" in query_lower:
        return LEGAL_KNOWLEDGE["302"]
    elif "498" in query_lower or "cruelty" in query_lower or "dowry" in query_lower:
        return LEGAL_KNOWLEDGE["498a"]
    elif "420" in query_lower or "cheat" in query_lower or "fraud" in query_lower:
        return LEGAL_KNOWLEDGE["420"]
    elif "fir" in query_lower or "first information" in query_lower or "police complaint" in query_lower:
        return LEGAL_KNOWLEDGE["fir"]
    elif "bail" in query_lower or "anticipatory" in query_lower:
        return LEGAL_KNOWLEDGE["bail"]
    elif "fundamental" in query_lower or "rights" in query_lower or "article 21" in query_lower:
        return LEGAL_KNOWLEDGE["fundamental"]
    elif "rti" in query_lower or "information act" in query_lower or "सूचना" in query_lower:
        return LEGAL_KNOWLEDGE["rti"]
    
    return None

def generate_with_claude(query: str, context: str, include_hindi: bool) -> dict:
    """Generate response using Claude API"""
    client = get_anthropic()
    if not client:
        return None
    
    hindi_instruction = """

Also provide a Hindi translation of your answer in a separate paragraph starting with "हिंदी में:" """ if include_hindi else ""
    
    prompt = f"""You are Jurisprudence AI, an expert legal assistant specializing in Indian law. 
Answer the following legal question accurately with citations to relevant sections and case laws.

Context from legal database:
{context}

Question: {query}

Provide a comprehensive answer with:
1. Clear explanation of the law
2. Relevant sections/acts
3. Important case laws if applicable
4. Practical implications{hindi_instruction}

Format your answer with HTML tags for emphasis (<strong>, <em>) where appropriate."""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"text": response.content[0].text}
    except Exception as e:
        print(f"Claude API error: {e}")
        return None

# ==================== ENDPOINTS ====================
@app.get("/", tags=["Root"])
async def root():
    return {
        "name": "Jurisprudence AI",
        "version": "1.0.0",
        "description": "Legal Intelligence API for Indian Law",
        "endpoints": {
            "query": "/query",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and service status"""
    services = {
        "cohere": COHERE_API_KEY is not None,
        "pinecone": PINECONE_API_KEY is not None,
        "anthropic": ANTHROPIC_API_KEY is not None,
        "knowledge_base": True  # Built-in knowledge always available
    }
    
    all_healthy = any(services.values())
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        services=services
    )

@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def query_legal(request: QueryRequest):
    """Query the legal knowledge base"""
    start_time = time.time()
    
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # First, check built-in knowledge
    knowledge = find_matching_knowledge(query)
    
    if knowledge:
        # Use built-in knowledge
        citations = [
            Citation(
                source_index=i+1,
                section=c.get("section"),
                act_name=c.get("act_name"),
                case_citation=c.get("case_citation"),
                relevance_score=c.get("relevance_score", 0.8)
            )
            for i, c in enumerate(knowledge.get("citations", []))
        ]
        
        followups = [
            FollowUpQuestion(question=q, intent="related")
            for q in knowledge.get("followups", [])
        ]
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return QueryResponse(
            answer=knowledge["answer"],
            answer_hindi=knowledge.get("hindi") if request.include_hindi else None,
            confidence_score=0.92,
            citations=citations,
            follow_up_questions=followups,
            llm_used="knowledge_base",
            processing_time_ms=processing_time
        )
    
    # Try Claude API if available
    client = get_anthropic()
    if client:
        try:
            claude_response = generate_with_claude(query, "", request.include_hindi)
            if claude_response:
                answer = claude_response["text"]
                answer_hindi = None
                
                # Extract Hindi if present
                if "हिंदी में:" in answer:
                    parts = answer.split("हिंदी में:")
                    answer = parts[0].strip()
                    answer_hindi = parts[1].strip() if len(parts) > 1 else None
                
                processing_time = int((time.time() - start_time) * 1000)
                
                return QueryResponse(
                    answer=answer,
                    answer_hindi=answer_hindi,
                    confidence_score=0.85,
                    citations=[],
                    follow_up_questions=[
                        FollowUpQuestion(question="Tell me more about this topic", intent="deeper"),
                        FollowUpQuestion(question="What are the related laws?", intent="related")
                    ],
                    llm_used="claude",
                    processing_time_ms=processing_time
                )
        except Exception as e:
            print(f"Claude error: {e}")
    
    # Fallback response
    processing_time = int((time.time() - start_time) * 1000)
    
    return QueryResponse(
        answer=f"""Thank you for your question about <strong>"{query}"</strong>.

This is a complex legal topic. For accurate and detailed information, I recommend:

1. <strong>Consult a qualified advocate</strong> for specific legal advice
2. <strong>Check official sources</strong> like India Code (indiacode.nic.in)
3. <strong>Visit Indian Kanoon</strong> (indiankanoon.org) for case laws

<em>Note: This response is generated because your specific query isn't in our knowledge base yet. We're constantly expanding our legal database.</em>""",
        answer_hindi="यह एक जटिल कानूनी विषय है। सटीक जानकारी के लिए किसी योग्य वकील से परामर्श करें।" if request.include_hindi else None,
        confidence_score=0.4,
        citations=[],
        follow_up_questions=[
            FollowUpQuestion(question="What are my fundamental rights?", intent="suggestion"),
            FollowUpQuestion(question="How to file an FIR?", intent="suggestion")
        ],
        llm_used="fallback",
        processing_time_ms=processing_time
    )

@app.get("/acts", tags=["Reference"])
async def list_acts():
    """List available acts in knowledge base"""
    return {
        "acts": [
            {"name": "Indian Penal Code, 1860", "short": "IPC"},
            {"name": "Code of Criminal Procedure, 1973", "short": "CrPC"},
            {"name": "Constitution of India", "short": "COI"},
            {"name": "Right to Information Act, 2005", "short": "RTI"},
        ],
        "topics": [
            "Murder (Section 302 IPC)",
            "Cruelty/Dowry (Section 498A IPC)",
            "Cheating (Section 420 IPC)",
            "FIR Filing",
            "Bail",
            "Fundamental Rights",
            "RTI Applications"
        ]
    }

# ==================== RUN ====================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
