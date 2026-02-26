from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os

app = FastAPI(title="Jurisprudence AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    include_hindi: bool = True

LEGAL_KB = {
    "302": {
        "answer": "<strong>Section 302 IPC</strong> - Punishment for Murder<br><br>Whoever commits murder shall be punished with:<br>• <strong>Death</strong>, or<br>• <strong>Life imprisonment</strong> + fine<br><br>Key case: <em>Bachan Singh vs State of Punjab (1980)</em>",
        "hindi": "धारा 302 - हत्या की सजा। मृत्यु दंड या आजीवन कारावास।",
        "citations": [{"section": "Section 302", "act_name": "IPC 1860", "relevance_score": 0.98}],
        "followups": ["What is culpable homicide?", "Rarest of rare doctrine?"]
    },
    "rarest": {
        "answer": "<strong>Rarest of Rare Doctrine</strong><br><br>Established in <em>Bachan Singh vs State of Punjab (1980)</em>, this doctrine states that <strong>death penalty should only be imposed in the 'rarest of rare' cases</strong> when the alternative of life imprisonment is unquestionably foreclosed.<br><br><strong>Key Principles:</strong><br>• Death penalty is an exception, not the rule<br>• Court must consider both aggravating and mitigating circumstances<br>• Life imprisonment is the rule; death penalty is the exception<br><br><strong>Aggravating factors:</strong><br>• Extreme brutality<br>• Murder for gain<br>• Murder of multiple persons<br>• Murder of child/woman/elderly<br><br><strong>Mitigating factors:</strong><br>• Young age of accused<br>• No prior criminal record<br>• Possibility of reformation<br>• Mental condition<br><br><strong>Key Cases:</strong><br>• <em>Machhi Singh vs State of Punjab (1983)</em> - Expanded guidelines<br>• <em>Santosh Kumar vs State (2009)</em> - Balance sheet approach",
        "hindi": "दुर्लभतम सिद्धांत - मृत्युदंड केवल 'दुर्लभतम से दुर्लभ' मामलों में दिया जाना चाहिए। बचन सिंह बनाम पंजाब राज्य (1980) में स्थापित।",
        "citations": [{"case_citation": "Bachan Singh vs State of Punjab (1980)", "relevance_score": 0.99}, {"case_citation": "Machhi Singh vs State of Punjab (1983)", "relevance_score": 0.95}],
        "followups": ["What is Section 302?", "What is culpable homicide?", "Can death penalty be commuted?"]
    },
    "culpable": {
        "answer": "<strong>Culpable Homicide (Section 299 IPC)</strong><br><br>Causing death by an act with:<br>• <strong>Intention</strong> of causing death, OR<br>• <strong>Intention</strong> of causing bodily injury likely to cause death, OR<br>• <strong>Knowledge</strong> that the act is likely to cause death<br><br><strong>Culpable Homicide vs Murder:</strong><br>• <strong>Murder (Section 300)</strong>: Higher degree of intention<br>• <strong>Culpable Homicide not amounting to Murder (Section 304)</strong>: Lesser intention/knowledge<br><br><strong>Section 304 Punishment:</strong><br>• <strong>Part I</strong>: Life imprisonment or up to 10 years + fine (if intention)<br>• <strong>Part II</strong>: Up to 10 years or fine or both (if knowledge only)<br><br><strong>Key Difference:</strong> Murder requires a higher degree of intention than culpable homicide.",
        "hindi": "सदोष मानव वध (धारा 299) - ऐसा कार्य जिससे मृत्यु हो और मृत्यु कारित करने का इरादा या ज्ञान हो। हत्या (धारा 300) में इरादे की डिग्री अधिक होती है।",
        "citations": [{"section": "Section 299", "act_name": "IPC 1860", "relevance_score": 0.97}, {"section": "Section 300", "act_name": "IPC 1860", "relevance_score": 0.96}, {"section": "Section 304", "act_name": "IPC 1860", "relevance_score": 0.95}],
        "followups": ["What is Section 302?", "Difference between 299 and 300?"]
    },
    "498": {
        "answer": "<strong>Section 498A IPC</strong> - Cruelty by Husband/Relatives<br><br>• <strong>Cognizable</strong> and <strong>Non-bailable</strong> offense<br>• Punishment: Up to <strong>3 years imprisonment</strong> + fine<br>• Covers <strong>physical and mental cruelty</strong><br>• Includes <strong>dowry harassment</strong><br><br><strong>What constitutes cruelty:</strong><br>• Willful conduct likely to drive woman to suicide<br>• Conduct causing grave injury to life/limb/health<br>• Harassment for dowry demands<br><br><strong>Key Guidelines:</strong><br>• <em>Arnesh Kumar vs State of Bihar (2014)</em> - Police must follow checklist before arrest<br>• <em>Rajesh Sharma vs State of UP (2017)</em> - Family Welfare Committees",
        "hindi": "धारा 498A - पति या रिश्तेदारों द्वारा क्रूरता। संज्ञेय और गैर-जमानती अपराध। 3 साल तक कैद और जुर्माना।",
        "citations": [{"section": "Section 498A", "act_name": "IPC 1860", "relevance_score": 0.97}, {"case_citation": "Arnesh Kumar vs State of Bihar (2014)", "relevance_score": 0.93}],
        "followups": ["How to file 498A?", "Can 498A be quashed?"]
    },
    "420": {
        "answer": "<strong>Section 420 IPC</strong> - Cheating and Dishonestly Inducing Delivery of Property<br><br><strong>Punishment:</strong> Up to <strong>7 years imprisonment</strong> + fine<br><br><strong>Essential Elements:</strong><br>• Deception of any person<br>• Fraudulent or dishonest inducement<br>• Delivery of property or valuable security<br>• Intentional dishonesty from beginning<br><br><strong>Common Examples:</strong><br>• Fraud in property deals<br>• Fake investment schemes<br>• Online/cyber fraud<br>• Bounced cheques (if dishonest intent)",
        "hindi": "धारा 420 - धोखाधड़ी और बेईमानी से संपत्ति प्राप्त करना। 7 साल तक कैद और जुर्माना।",
        "citations": [{"section": "Section 420", "act_name": "IPC 1860", "relevance_score": 0.96}, {"section": "Section 415", "act_name": "IPC 1860", "relevance_score": 0.90}],
        "followups": ["How to file cheating case?", "Difference between 406 and 420?"]
    },
    "fir": {
        "answer": "<strong>FIR (First Information Report)</strong><br><br><strong>How to file:</strong><br>1. Go to police station with <strong>jurisdiction</strong><br>2. Give <strong>written or oral</strong> information<br>3. Get <strong>free copy</strong> (Section 154 CrPC)<br><br><strong>Key Points:</strong><br>• Police <strong>CANNOT refuse</strong> FIR for cognizable offense<br>• <strong>Zero FIR</strong> can be filed at ANY police station<br>• If refused → Complain to <strong>SP</strong> or <strong>Magistrate (Section 156(3))</strong><br>• Woman can give statement at her residence<br><br><strong>Online FIR:</strong> Many states allow e-FIR for certain offenses",
        "hindi": "FIR (प्रथम सूचना रिपोर्ट) - किसी भी पुलिस स्टेशन में Zero FIR दर्ज करा सकते हैं। पुलिस संज्ञेय अपराध के लिए FIR दर्ज करने से मना नहीं कर सकती।",
        "citations": [{"section": "Section 154", "act_name": "CrPC 1973", "relevance_score": 0.95}, {"section": "Section 156(3)", "act_name": "CrPC 1973", "relevance_score": 0.92}],
        "followups": ["What if police refuses FIR?", "What is Zero FIR?", "How to file online FIR?"]
    },
    "bail": {
        "answer": "<strong>Bail in Indian Law</strong><br><br><strong>Types of Bail:</strong><br><br>1. <strong>Regular Bail (Section 437/439 CrPC)</strong><br>• Applied after arrest<br>• Magistrate or Sessions Court<br><br>2. <strong>Anticipatory Bail (Section 438 CrPC)</strong><br>• Applied BEFORE arrest<br>• Sessions Court or High Court<br>• Protection against arrest<br><br>3. <strong>Interim Bail</strong><br>• Temporary bail pending decision<br><br><strong>Factors Considered:</strong><br>• Nature of offense<br>• Flight risk<br>• Tampering with evidence<br>• Criminal history",
        "hindi": "जमानत - नियमित जमानत (गिरफ्तारी के बाद), अग्रिम जमानत (गिरफ्तारी से पहले), अंतरिम जमानत (अस्थायी)।",
        "citations": [{"section": "Section 437", "act_name": "CrPC 1973", "relevance_score": 0.94}, {"section": "Section 438", "act_name": "CrPC 1973", "relevance_score": 0.96}, {"section": "Section 439", "act_name": "CrPC 1973", "relevance_score": 0.93}],
        "followups": ["How to apply for anticipatory bail?", "Can bail be cancelled?", "Bail in non-bailable offense?"]
    },
    "anticipatory": {
        "answer": "<strong>Anticipatory Bail (Section 438 CrPC)</strong><br><br>Bail granted <strong>before arrest</strong> in anticipation of arrest.<br><br><strong>Who can apply:</strong><br>• Any person who has reason to believe they may be arrested<br><br><strong>Where to apply:</strong><br>• <strong>Sessions Court</strong> or <strong>High Court</strong><br><br><strong>Key Points:</strong><br>• Court may impose conditions<br>• Can be granted with or without time limit<br>• <em>Sushila Aggarwal vs State (2020)</em> - No fixed time limit; continues till end of trial<br><br><strong>Conditions may include:</strong><br>• Joining investigation when required<br>• Not leaving India without permission<br>• Not tampering with evidence",
        "hindi": "अग्रिम जमानत (धारा 438) - गिरफ्तारी से पहले जमानत। सेशन कोर्ट या हाई कोर्ट में आवेदन करें।",
        "citations": [{"section": "Section 438", "act_name": "CrPC 1973", "relevance_score": 0.98}, {"case_citation": "Sushila Aggarwal vs State (2020)", "relevance_score": 0.94}],
        "followups": ["Regular bail vs anticipatory bail?", "Can anticipatory bail be cancelled?"]
    },
    "fundamental": {
        "answer": "<strong>Fundamental Rights</strong> (Part III, Articles 12-35)<br><br><strong>Six Fundamental Rights:</strong><br><br>1. <strong>Right to Equality (Art 14-18)</strong><br>• Equality before law<br>• No discrimination<br>• Abolition of untouchability<br><br>2. <strong>Right to Freedom (Art 19-22)</strong><br>• Speech, assembly, movement<br>• <strong>Article 21</strong>: Right to Life and Liberty<br><br>3. <strong>Right Against Exploitation (Art 23-24)</strong><br>• No human trafficking<br>• No child labor<br><br>4. <strong>Right to Freedom of Religion (Art 25-28)</strong><br><br>5. <strong>Cultural & Educational Rights (Art 29-30)</strong><br><br>6. <strong>Right to Constitutional Remedies (Art 32)</strong><br>• Right to approach Supreme Court<br>• <strong>Writs:</strong> Habeas Corpus, Mandamus, Certiorari, Prohibition, Quo Warranto",
        "hindi": "मौलिक अधिकार (भाग III) - समानता, स्वतंत्रता, शोषण के विरुद्ध, धार्मिक स्वतंत्रता, सांस्कृतिक और शैक्षिक, संवैधानिक उपचार का अधिकार।",
        "citations": [{"section": "Part III", "act_name": "Constitution of India", "relevance_score": 0.97}, {"section": "Article 21", "act_name": "Constitution of India", "relevance_score": 0.95}, {"section": "Article 32", "act_name": "Constitution of India", "relevance_score": 0.93}],
        "followups": ["What is Article 21?", "Types of writs?", "Can fundamental rights be suspended?"]
    },
    "article21": {
        "answer": "<strong>Article 21 - Right to Life and Personal Liberty</strong><br><br><em>'No person shall be deprived of his life or personal liberty except according to procedure established by law.'</em><br><br><strong>Expanded Scope includes:</strong><br>• Right to live with dignity<br>• Right to livelihood<br>• Right to privacy (<em>Puttaswamy case, 2017</em>)<br>• Right to clean environment<br>• Right to health<br>• Right to education<br>• Right to shelter<br>• Right to speedy trial<br>• Right to legal aid<br>• Right against solitary confinement<br>• Right to sleep<br>• Right against handcuffing<br><br><strong>Landmark Case:</strong><br><em>Maneka Gandhi vs Union of India (1978)</em> - Procedure must be fair, just and reasonable",
        "hindi": "अनुच्छेद 21 - जीवन और व्यक्तिगत स्वतंत्रता का अधिकार। इसमें गरिमा से जीने का अधिकार, निजता का अधिकार, स्वास्थ्य का अधिकार आदि शामिल हैं।",
        "citations": [{"section": "Article 21", "act_name": "Constitution of India", "relevance_score": 0.99}, {"case_citation": "Maneka Gandhi vs Union of India (1978)", "relevance_score": 0.96}, {"case_citation": "Puttaswamy vs Union of India (2017)", "relevance_score": 0.94}],
        "followups": ["What are fundamental rights?", "Right to privacy judgment?"]
    },
    "writ": {
        "answer": "<strong>Types of Writs in India</strong><br><br>Under <strong>Article 32</strong> (Supreme Court) and <strong>Article 226</strong> (High Court):<br><br>1. <strong>Habeas Corpus</strong> ('To have the body')<br>• Against illegal detention<br>• To produce detained person before court<br><br>2. <strong>Mandamus</strong> ('We command')<br>• To compel public official to perform duty<br>• Not against private persons<br><br>3. <strong>Certiorari</strong> ('To be certified')<br>• To quash order of lower court/tribunal<br>• Against judicial/quasi-judicial bodies<br><br>4. <strong>Prohibition</strong><br>• To prohibit lower court from proceeding<br>• Issued during pending proceedings<br><br>5. <strong>Quo Warranto</strong> ('By what authority')<br>• To question authority of person holding public office<br>• Against usurpation of public office",
        "hindi": "रिट के प्रकार - बंदी प्रत्यक्षीकरण, परमादेश, उत्प्रेषण, प्रतिषेध, अधिकार पृच्छा। अनुच्छेद 32 (सुप्रीम कोर्ट) और अनुच्छेद 226 (हाई कोर्ट) के तहत।",
        "citations": [{"section": "Article 32", "act_name": "Constitution of India", "relevance_score": 0.97}, {"section": "Article 226", "act_name": "Constitution of India", "relevance_score": 0.96}],
        "followups": ["How to file writ petition?", "Difference between Art 32 and 226?"]
    },
    "rti": {
        "answer": "<strong>Right to Information Act, 2005</strong><br><br><strong>How to File RTI:</strong><br>1. Write application to <strong>Public Information Officer (PIO)</strong><br>2. <strong>Fee:</strong> ₹10 (cash/DD/postal order)<br>3. <strong>Response time:</strong> 30 days (48 hours for life/liberty)<br><br><strong>Appeals:</strong><br>• <strong>First Appeal:</strong> To First Appellate Authority within 30 days<br>• <strong>Second Appeal:</strong> To Information Commission within 90 days<br><br><strong>Exemptions (Section 8):</strong><br>• National security<br>• Cabinet papers<br>• Personal privacy<br>• Trade secrets<br><br><strong>Key Points:</strong><br>• BPL applicants: No fee<br>• No reason needed for seeking info<br>• Online RTI: rtionline.gov.in",
        "hindi": "सूचना का अधिकार (RTI) अधिनियम 2005 - आवेदन शुल्क ₹10, जवाब 30 दिनों में। ऑनलाइन RTI: rtionline.gov.in",
        "citations": [{"section": "Section 6", "act_name": "RTI Act 2005", "relevance_score": 0.96}, {"section": "Section 7", "act_name": "RTI Act 2005", "relevance_score": 0.94}, {"section": "Section 8", "act_name": "RTI Act 2005", "relevance_score": 0.92}],
        "followups": ["RTI application format?", "What if RTI not answered?", "Online RTI filing?"]
    },
    "divorce": {
        "answer": "<strong>Divorce in India</strong><br><br><strong>Hindu Marriage Act, 1955:</strong><br><br><strong>Section 13 - Grounds for Divorce:</strong><br>• Adultery<br>• Cruelty (mental/physical)<br>• Desertion (2+ years)<br>• Conversion to another religion<br>• Unsound mind<br>• Leprosy/venereal disease<br>• Renunciation of world<br>• Not heard alive for 7+ years<br><br><strong>Section 13B - Mutual Consent Divorce:</strong><br>• Both parties agree<br>• Living separately for 1+ year<br>• 6-month cooling period (can be waived)<br><br><strong>Other Laws:</strong><br>• Muslim: Muslim Personal Law<br>• Christian: Indian Divorce Act, 1869<br>• Special Marriage Act, 1954",
        "hindi": "तलाक - हिंदू विवाह अधिनियम की धारा 13 में तलाक के आधार दिए गए हैं। धारा 13B के तहत आपसी सहमति से तलाक।",
        "citations": [{"section": "Section 13", "act_name": "Hindu Marriage Act 1955", "relevance_score": 0.97}, {"section": "Section 13B", "act_name": "Hindu Marriage Act 1955", "relevance_score": 0.96}],
        "followups": ["Mutual consent divorce procedure?", "Alimony laws in India?"]
    },
    "consumer": {
        "answer": "<strong>Consumer Protection Act, 2019</strong><br><br><strong>Who is a Consumer:</strong><br>• Person who buys goods/services for personal use<br>• Does NOT include commercial purpose buyers<br><br><strong>Consumer Rights:</strong><br>• Right to safety<br>• Right to information<br>• Right to choose<br>• Right to be heard<br>• Right to redressal<br>• Right to consumer education<br><br><strong>Where to File Complaint:</strong><br>• <strong>District Commission:</strong> Up to ₹1 crore<br>• <strong>State Commission:</strong> ₹1 crore to ₹10 crore<br>• <strong>National Commission:</strong> Above ₹10 crore<br><br><strong>Online Filing:</strong> edaakhil.nic.in<br><strong>Time Limit:</strong> 2 years from cause of action",
        "hindi": "उपभोक्ता संरक्षण अधिनियम 2019 - जिला आयोग (₹1 करोड़ तक), राज्य आयोग (₹10 करोड़ तक), राष्ट्रीय आयोग (₹10 करोड़ से ऊपर)।",
        "citations": [{"section": "Consumer Protection Act", "act_name": "Consumer Protection Act 2019", "relevance_score": 0.97}],
        "followups": ["How to file consumer complaint?", "Consumer court fees?"]
    },
    "cyber": {
        "answer": "<strong>Cyber Crimes in India</strong><br><br><strong>IT Act, 2000 - Key Sections:</strong><br><br>• <strong>Section 66</strong>: Computer hacking - 3 years + ₹5 lakh fine<br>• <strong>Section 66C</strong>: Identity theft - 3 years + ₹1 lakh fine<br>• <strong>Section 66D</strong>: Cheating by personation - 3 years + ₹1 lakh fine<br>• <strong>Section 66E</strong>: Privacy violation - 3 years + ₹2 lakh fine<br>• <strong>Section 67</strong>: Publishing obscene content - 3-5 years<br>• <strong>Section 67A</strong>: Sexually explicit content - 5-7 years<br>• <strong>Section 67B</strong>: Child pornography - 5-7 years<br><br><strong>Where to Report:</strong><br>• cybercrime.gov.in (National Portal)<br>• Local Cyber Cell<br>• Nearest Police Station",
        "hindi": "साइबर अपराध - IT Act 2000 के तहत। शिकायत cybercrime.gov.in पर करें।",
        "citations": [{"section": "Section 66", "act_name": "IT Act 2000", "relevance_score": 0.96}, {"section": "Section 67", "act_name": "IT Act 2000", "relevance_score": 0.94}],
        "followups": ["How to report cyber crime?", "Online fraud complaint?"]
    },
}

def find_knowledge(q):
    q = q.lower()
    if "302" in q or "murder" in q:
        return LEGAL_KB["302"]
    if "rarest" in q or "rare" in q:
        return LEGAL_KB["rarest"]
    if "culpable" in q or "homicide" in q or "299" in q or "304" in q:
        return LEGAL_KB["culpable"]
    if "498" in q or "cruelty" in q or "dowry" in q:
        return LEGAL_KB["498"]
    if "420" in q or "cheat" in q or "fraud" in q:
        return LEGAL_KB["420"]
    if "fir" in q or "police complaint" in q:
        return LEGAL_KB["fir"]
    if "anticipatory" in q:
        return LEGAL_KB["anticipatory"]
    if "bail" in q:
        return LEGAL_KB["bail"]
    if "article 21" in q or "right to life" in q:
        return LEGAL_KB["article21"]
    if "writ" in q or "habeas" in q or "mandamus" in q:
        return LEGAL_KB["writ"]
    if "fundamental" in q or "rights" in q:
        return LEGAL_KB["fundamental"]
    if "rti" in q or "information act" in q:
        return LEGAL_KB["rti"]
    if "divorce" in q or "marriage" in q or "13b" in q:
        return LEGAL_KB["divorce"]
    if "consumer" in q or "complaint" in q:
        return LEGAL_KB["consumer"]
    if "cyber" in q or "hack" in q or "online" in q or "internet" in q:
        return LEGAL_KB["cyber"]
    return None

@app.get("/")
def root():
    return {"name": "Jurisprudence AI", "status": "running", "topics": len(LEGAL_KB)}

@app.get("/health")
def health():
    return {"status": "healthy", "topics_covered": len(LEGAL_KB)}

@app.post("/query")
def query(req: QueryRequest):
    kb = find_knowledge(req.query)
    if kb:
        return {
            "answer": kb["answer"],
            "answer_hindi": kb.get("hindi") if req.include_hindi else None,
            "confidence_score": 0.92,
            "citations": kb.get("citations", []),
            "follow_up_questions": [{"question": q} for q in kb.get("followups", [])]
        }
    return {
        "answer": "Thank you for your question. This topic is not yet in our database. Please consult a legal expert for detailed advice.",
        "answer_hindi": "धन्यवाद। यह विषय अभी हमारे डेटाबेस में नहीं है। कृपया विस्तृत सलाह के लिए कानूनी विशेषज्ञ से परामर्श करें।",
        "confidence_score": 0.4,
        "citations": [],
        "follow_up_questions": [{"question": "What is Section 302 IPC?"}, {"question": "How to file FIR?"}, {"question": "What are fundamental rights?"}]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
