from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import time
import os

app = FastAPI(title="Jurisprudence AI")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    query: str
    include_hindi: bool = True

class QueryResponse(BaseModel):
    answer: str
    answer_hindi: Optional[str] = None
    confidence_score: float
    citations: List[dict] = []
    follow_up_questions: List[dict] = []

LEGAL_KB = {
    "302": {"answer": "<strong>Section 302 IPC</strong> - Punishment for Murder<br><br>Whoever commits murder shall be punished with:<br>• <strong>Death</strong>, or<br>• <strong>Life imprisonment</strong> + fine<br><br>Key case: <em>Bachan Singh vs State of Punjab (1980)</em>", "hindi": "धारा 302 - हत्या की सजा। मृत्यु दंड या आजीवन कारावास।", "citations": [{"section": "Section 302", "act_name": "IPC 1860", "relevance_score": 0.98}], "followups": ["What is culpable homicide?", "Rarest of rare doctrine?"]},
    "498": {"answer": "<strong>Section 498A IPC</strong> - Cruelty by Husband/Relatives<br><br>• Cognizable & Non-bailable<br>• Up to 3 years imprisonment + fine<br>• Covers physical & mental cruelty", "hindi": "धारा 498A - पति द्वारा क्रूरता। 3 साल तक कैद।", "citations": [{"section": "Section 498A", "act_name": "IPC 1860", "relevance_score": 0.97}], "followups": ["How to file 498A?"]},
    "420": {"answer": "<strong>Section 420 IPC</strong> - Cheating<br><br>Punishment: Up to 7 years imprisonment + fine", "hindi": "धारा 420 - धोखाधड़ी। 7 साल तक कैद।", "citations": [{"section": "Section 420", "act_name": "IPC 1860", "relevance_score": 0.96}], "followups": ["How to file cheating case?"]},
    "fir": {"answer": "<strong>FIR (First Information Report)</strong><br><br>1. Go to police station<br>2. Give written/oral info<br>3. Get free copy (Sec 154 CrPC)<br>• Zero FIR can be filed anywhere", "hindi": "FIR किसी भी पुलिस स्टेशन में दर्ज करा सकते हैं।", "citations": [{"section": "Section 154", "act_name": "CrPC 1973", "relevance_score": 0.95}], "followups": ["What if police refuses?"]},
    "bail": {"answer": "<strong>Bail Types</strong><br><br>1. Regular Bail (Sec 437/439)<br>2. Anticipatory Bail (Sec 438)<br>3. Interim Bail", "hindi": "जमानत - नियमित और अग्रिम जमानत।", "citations": [{"section": "Section 438", "act_name": "CrPC 1973", "relevance_score": 0.94}], "followups": ["Anticipatory bail process?"]},
    "fundamental": {"answer": "<strong>Fundamental Rights</strong> (Part III)<br><br>1. Equality (Art 14-18)<br>2. Freedom (Art 19-22)<br>3. Against Exploitation (Art 23-24)<br>4. Religion (Art 25-28)<br>5. Cultural (Art 29-30)<br>6. Constitutional Remedies (Art 32)", "hindi": "मौलिक अधिकार - संविधान के भाग III में।", "citations": [{"section": "Part III", "act_name": "Constitution", "relevance_score": 0.97}], "followups": ["What is Article 21?"]},
}

def find_knowledge(q):
    q = q.lower()
    if "302" in q or "murder" in q: return LEGAL_KB["302"]
    if "498" in q or "cruelty" in q or "dowry" in q: return LEGAL_KB["498"]
    if "420" in q or "cheat" in q: return LEGAL_KB["420"]
    if "fir" in q or "police" in q: return LEGAL_KB["fir"]
    if "bail" in q: return LEGAL_KB["bail"]
    if "fundamental" in q or "rights" in q: return LEGAL_KB["fundamental"]
    return None

@app.get("/")
def root():
    return {"name": "Jurisprudence AI", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/query")
def query(req: QueryRequest):
    kb = find_knowledge(req.query)
    if kb:
        return {"answer": kb["answer"], "answer_hindi": kb.get("hindi") if req.include_hindi else None, "confidence_score": 0.92, "citations": kb.get("citations", []), "follow_up_questions": [{"question": q} for q in kb.get("followups", [])]}
    return {"answer": f"Thank you for asking about <strong>{req.query}</strong>.", "answer_hindi": "धन्यवाद।" if req.include_hindi else None, "confidence_score": 0.4, "citations": [], "follow_up_questions": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
```    


