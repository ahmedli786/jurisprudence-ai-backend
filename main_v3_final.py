from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(title="Jurisprudence AI - Indian Legal Intelligence")

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

# =============================================================================
# COMPREHENSIVE INDIAN LAW KNOWLEDGE BASE - 100+ TOPICS
# Sources: Indian Kanoon, India Code, Bare Acts
# =============================================================================

LEGAL_KB = {
    # =========================================================================
    # INDIAN PENAL CODE (IPC) 1860
    # =========================================================================
    "ipc_302": {
        "answer": "<strong>Section 302 IPC - Punishment for Murder</strong><br><br>Whoever commits murder shall be punished with:<br>• <strong>Death</strong>, or<br>• <strong>Life imprisonment</strong>, and shall also be liable to <strong>fine</strong><br><br><strong>Key Points:</strong><br>• Most serious offense under IPC<br>• Death penalty only in 'rarest of rare' cases<br>• Life imprisonment means entire natural life<br><br><strong>Landmark Cases:</strong><br>• <em>Bachan Singh vs State of Punjab (1980)</em> - Rarest of rare doctrine<br>• <em>Machhi Singh vs State of Punjab (1983)</em> - Guidelines for death penalty",
        "hindi": "धारा 302 - हत्या की सजा। मृत्युदंड या आजीवन कारावास और जुर्माना। 'दुर्लभतम से दुर्लभ' मामलों में ही मृत्युदंड।",
        "citations": [{"section": "Section 302", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.99}],
        "followups": ["What is rarest of rare doctrine?", "Difference between 302 and 304?", "What is culpable homicide?"]
    },
    "ipc_300": {
        "answer": "<strong>Section 300 IPC - Murder</strong><br><br>Culpable homicide is <strong>murder</strong> if:<br><br>1. Act done with <strong>intention of causing death</strong><br>2. Act done with intention of causing <strong>bodily injury known to be likely to cause death</strong><br>3. Act done with intention of causing <strong>bodily injury sufficient in ordinary course of nature to cause death</strong><br>4. Act so <strong>imminently dangerous</strong> that it must in all probability cause death<br><br><strong>Exceptions (reduces to Culpable Homicide):</strong><br>• Grave and sudden provocation<br>• Private defence exceeded in good faith<br>• Public servant acting in good faith<br>• Sudden fight without premeditation<br>• Consent of victim (above 18 years)",
        "hindi": "धारा 300 - हत्या की परिभाषा। जब सदोष मानव वध विशेष इरादे या ज्ञान से किया जाए तो वह हत्या है।",
        "citations": [{"section": "Section 300", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.98}],
        "followups": ["What are exceptions to murder?", "Section 299 vs 300?"]
    },
    "ipc_304": {
        "answer": "<strong>Section 304 IPC - Culpable Homicide not amounting to Murder</strong><br><br><strong>Punishment:</strong><br><br><strong>Part I</strong> (with intention):<br>• Life imprisonment, OR<br>• Imprisonment up to <strong>10 years</strong> + fine<br><br><strong>Part II</strong> (with knowledge but no intention):<br>• Imprisonment up to <strong>10 years</strong>, OR<br>• Fine, OR<br>• Both<br><br><strong>When Applied:</strong><br>• When exceptions to Section 300 apply<br>• Lesser degree of intention than murder",
        "hindi": "धारा 304 - हत्या की कोटि में न आने वाला सदोष मानव वध। भाग I: आजीवन या 10 वर्ष कारावास। भाग II: 10 वर्ष तक कारावास या जुर्माना।",
        "citations": [{"section": "Section 304", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.97}],
        "followups": ["Difference between 302 and 304?", "What is Section 299?"]
    },
    "ipc_304a": {
        "answer": "<strong>Section 304A IPC - Death by Negligence</strong><br><br>Causing death by <strong>rash or negligent act</strong> not amounting to culpable homicide.<br><br><strong>Punishment:</strong><br>• Imprisonment up to <strong>2 years</strong>, OR<br>• Fine, OR<br>• Both<br><br><strong>Common Examples:</strong><br>• Road accidents due to rash driving<br>• Medical negligence causing death<br>• Industrial accidents due to negligence<br>• Building collapse due to poor construction<br><br><strong>Key Point:</strong> No intention or knowledge to cause death required",
        "hindi": "धारा 304A - उपेक्षा से मृत्यु कारित करना। 2 वर्ष तक कारावास या जुर्माना या दोनों। सड़क दुर्घटना, चिकित्सा लापरवाही में प्रयोग।",
        "citations": [{"section": "Section 304A", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.96}],
        "followups": ["Medical negligence laws?", "Road accident compensation?"]
    },
    "ipc_304b": {
        "answer": "<strong>Section 304B IPC - Dowry Death</strong><br><br>If a woman dies within <strong>7 years of marriage</strong> due to burns/injuries under abnormal circumstances, and it's shown she was subjected to <strong>cruelty for dowry</strong> soon before death.<br><br><strong>Punishment:</strong><br>• Minimum <strong>7 years</strong> imprisonment<br>• Maximum <strong>life imprisonment</strong><br><br><strong>Presumption:</strong> Under Section 113B Evidence Act, husband/relatives presumed to have caused death if:<br>• Death within 7 years of marriage<br>• Cruelty or harassment for dowry shown<br><br><strong>Non-bailable and Cognizable</strong>",
        "hindi": "धारा 304B - दहेज मृत्यु। विवाह के 7 वर्ष के भीतर असामान्य परिस्थितियों में मृत्यु और दहेज के लिए क्रूरता। 7 वर्ष से आजीवन कारावास।",
        "citations": [{"section": "Section 304B", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.98}],
        "followups": ["Section 498A explained?", "Dowry Prohibition Act?"]
    },
    "ipc_307": {
        "answer": "<strong>Section 307 IPC - Attempt to Murder</strong><br><br><strong>Punishment:</strong><br>• Imprisonment up to <strong>10 years</strong> + fine<br>• If hurt is caused: <strong>Life imprisonment</strong> or up to 10 years + fine<br>• If offender is life convict: May be punished with <strong>death</strong><br><br><strong>Essential Elements:</strong><br>• Intention or knowledge to cause death<br>• Act done towards causing death<br>• Act must be capable of causing death<br><br><strong>Key Cases:</strong><br>• <em>State of Maharashtra vs Balram (1983)</em> - Scope of attempt",
        "hindi": "धारा 307 - हत्या का प्रयास। 10 वर्ष तक कारावास। चोट पहुंचाने पर आजीवन कारावास। आजीवन कैदी द्वारा किए जाने पर मृत्युदंड।",
        "citations": [{"section": "Section 307", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.97}],
        "followups": ["What constitutes attempt?", "307 bail provisions?"]
    },
    "ipc_376": {
        "answer": "<strong>Section 376 IPC - Rape</strong><br><br><strong>Punishment (Section 376):</strong><br>• Rigorous imprisonment minimum <strong>10 years</strong> to <strong>life</strong> + fine<br><br><strong>Aggravated Rape (376(2)):</strong> Minimum <strong>10 years to death</strong><br>• By police officer<br>• By public servant<br>• By armed forces member<br>• By relative/guardian/teacher<br>• Gang rape<br>• Repeat offender<br>• Causing death or vegetative state<br><br><strong>Rape of minor under 12:</strong> Minimum <strong>20 years to death</strong><br><br><strong>Section 376(3):</strong> Rape of minor under 16 - Minimum 20 years to life<br><br><strong>Zero FIR</strong> mandatory, investigation by senior officer",
        "hindi": "धारा 376 - बलात्कार। न्यूनतम 10 वर्ष से आजीवन कारावास। 12 वर्ष से कम उम्र की पीड़िता के मामले में 20 वर्ष से मृत्युदंड।",
        "citations": [{"section": "Section 376", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.99}],
        "followups": ["POCSO Act provisions?", "Marital rape laws?", "Rape victim rights?"]
    },
    "ipc_354": {
        "answer": "<strong>Section 354 IPC - Assault or Criminal Force to Woman with Intent to Outrage Modesty</strong><br><br><strong>Punishment:</strong><br>• Imprisonment minimum <strong>1 year</strong> to <strong>5 years</strong> + fine<br><br><strong>Section 354A - Sexual Harassment:</strong><br>• Physical contact, demand for sexual favors<br>• Showing pornography, sexual remarks<br>• Up to 3 years imprisonment<br><br><strong>Section 354B - Assault to Disrobe:</strong> 3-7 years<br><br><strong>Section 354C - Voyeurism:</strong> 1-3 years (first), 3-7 years (repeat)<br><br><strong>Section 354D - Stalking:</strong> Up to 3 years (first), up to 5 years (repeat)",
        "hindi": "धारा 354 - स्त्री की लज्जा भंग करने के लिए हमला। 1 से 5 वर्ष कारावास। 354A (यौन उत्पीड़न), 354B (निर्वस्त्र करना), 354C (तांक-झांक), 354D (पीछा करना)।",
        "citations": [{"section": "Section 354", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.97}],
        "followups": ["Sexual harassment at workplace?", "How to file complaint?"]
    },
    "ipc_498a": {
        "answer": "<strong>Section 498A IPC - Cruelty by Husband or Relatives</strong><br><br><strong>Cruelty includes:</strong><br>• Willful conduct likely to drive woman to <strong>suicide</strong><br>• Conduct causing <strong>grave injury</strong> to life, limb, health<br>• Harassment for <strong>dowry demands</strong><br><br><strong>Punishment:</strong><br>• Imprisonment up to <strong>3 years</strong> + fine<br><br><strong>Nature:</strong><br>• <strong>Cognizable</strong> (arrest without warrant)<br>• <strong>Non-bailable</strong><br>• <strong>Non-compoundable</strong><br><br><strong>Key Guidelines:</strong><br>• <em>Arnesh Kumar vs State of Bihar (2014)</em> - Pre-arrest checklist mandatory<br>• <em>Rajesh Sharma vs State of UP (2017)</em> - Family Welfare Committees<br><br><strong>Quashing:</strong> Possible under Section 482 CrPC if case is frivolous",
        "hindi": "धारा 498A - पति या रिश्तेदारों द्वारा क्रूरता। 3 वर्ष तक कारावास। संज्ञेय, गैर-जमानती, अशमनीय अपराध। दहेज उत्पीड़न के खिलाफ।",
        "citations": [{"section": "Section 498A", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.99}, {"case_citation": "Arnesh Kumar vs State of Bihar (2014)", "relevance_score": 0.95}],
        "followups": ["How to file 498A?", "Can 498A be quashed?", "498A arrest guidelines?"]
    },
    "ipc_420": {
        "answer": "<strong>Section 420 IPC - Cheating and Dishonestly Inducing Delivery of Property</strong><br><br><strong>Punishment:</strong><br>• Imprisonment up to <strong>7 years</strong> + fine<br><br><strong>Essential Elements:</strong><br>1. <strong>Cheating</strong> as defined in Section 415<br>2. <strong>Dishonest inducement</strong> to deliver property<br>3. Property must be <strong>actually delivered</strong><br>4. <strong>Intentional</strong> deception from beginning<br><br><strong>Common Cases:</strong><br>• Fraudulent property deals<br>• Fake investment schemes<br>• Ponzi schemes<br>• Loan fraud<br>• Employment fraud<br>• Matrimonial fraud<br><br><strong>Section 415 (Cheating):</strong> Up to 1 year or fine or both",
        "hindi": "धारा 420 - छल करके संपत्ति परिदान के लिए बेईमानी से उत्प्रेरण। 7 वर्ष तक कारावास और जुर्माना।",
        "citations": [{"section": "Section 420", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.98}, {"section": "Section 415", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.90}],
        "followups": ["How to file cheating case?", "420 vs 406 difference?", "Online fraud complaint?"]
    },
    "ipc_406": {
        "answer": "<strong>Section 406 IPC - Criminal Breach of Trust</strong><br><br><strong>Punishment:</strong><br>• Imprisonment up to <strong>3 years</strong>, OR<br>• Fine, OR<br>• Both<br><br><strong>Essential Elements:</strong><br>1. Property <strong>entrusted</strong> to accused<br>2. Accused was in a position of <strong>trust</strong><br>3. <strong>Misappropriation</strong> or conversion of property<br>4. <strong>Dishonest</strong> intention<br><br><strong>Common Examples:</strong><br>• Employee misappropriating company funds<br>• Agent not returning principal's money<br>• Partner misusing partnership funds<br>• Trustee misusing trust property<br><br><strong>Difference from 420:</strong><br>• 406: Trust already exists<br>• 420: Deception from beginning",
        "hindi": "धारा 406 - आपराधिक न्यासभंग। 3 वर्ष तक कारावास या जुर्माना। संपत्ति का विश्वासघात से दुरुपयोग।",
        "citations": [{"section": "Section 406", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.97}],
        "followups": ["406 vs 420 IPC?", "Breach of trust examples?"]
    },
    "ipc_34": {
        "answer": "<strong>Section 34 IPC - Common Intention</strong><br><br><em>'When a criminal act is done by several persons in furtherance of the common intention of all, each of such persons is liable for that act in the same manner as if it were done by him alone.'</em><br><br><strong>Key Points:</strong><br>• Not a separate offense but a <strong>rule of evidence</strong><br>• Requires <strong>prior meeting of minds</strong><br>• Common intention can be <strong>inferred from circumstances</strong><br>• Each person liable as if he alone committed the act<br><br><strong>Difference from Section 149:</strong><br>• 34: Common intention (any number of persons)<br>• 149: Common object (unlawful assembly - 5+ persons)<br><br><strong>Key Case:</strong> <em>Pandurang vs State of Hyderabad (1955)</em>",
        "hindi": "धारा 34 - सामान्य आशय। जब कई व्यक्ति सामान्य आशय से कोई कार्य करते हैं तो प्रत्येक उत्तरदायी होता है।",
        "citations": [{"section": "Section 34", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.96}],
        "followups": ["Section 34 vs 149?", "What is common intention?"]
    },
    "ipc_120b": {
        "answer": "<strong>Section 120B IPC - Criminal Conspiracy</strong><br><br><strong>Definition (Section 120A):</strong> When two or more persons agree to do an illegal act, or a legal act by illegal means.<br><br><strong>Punishment:</strong><br>• If conspiracy is to commit <strong>serious offense</strong> (death/2+ years): Same as offense<br>• Other cases: Up to <strong>6 months</strong>, or fine, or both<br><br><strong>Essential Elements:</strong><br>1. Agreement between <strong>2 or more</strong> persons<br>2. To do an <strong>illegal act</strong><br>3. Agreement itself is the offense (overt act not necessary)<br><br><strong>Key Point:</strong> Meeting of minds is essential; mere knowledge is not enough",
        "hindi": "धारा 120B - आपराधिक षड्यंत्र। दो या अधिक व्यक्तियों द्वारा अवैध कार्य करने का समझौता। गंभीर अपराध के लिए: मूल अपराध जैसी सजा।",
        "citations": [{"section": "Section 120B", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.96}],
        "followups": ["Conspiracy vs abetment?", "How to prove conspiracy?"]
    },
    "ipc_506": {
        "answer": "<strong>Section 506 IPC - Criminal Intimidation</strong><br><br><strong>Simple Intimidation:</strong><br>• Imprisonment up to <strong>2 years</strong>, or fine, or both<br><br><strong>Aggravated Intimidation (threat to cause death, grievous hurt, destruction of property by fire, imputation of unchastity to woman):</strong><br>• Imprisonment up to <strong>7 years</strong>, or fine, or both<br><br><strong>What Constitutes:</strong><br>• Threatening injury to person, reputation, or property<br>• Threatening to any person in whom victim is interested<br>• Intent to cause alarm or to compel doing/omitting any act",
        "hindi": "धारा 506 - आपराधिक अभित्रास (धमकी)। साधारण: 2 वर्ष तक। गंभीर (जान से मारने की धमकी आदि): 7 वर्ष तक।",
        "citations": [{"section": "Section 506", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.95}],
        "followups": ["How to file threat complaint?", "506 with 34 IPC?"]
    },
    "ipc_323": {
        "answer": "<strong>Section 323 IPC - Voluntarily Causing Hurt</strong><br><br><strong>Punishment:</strong><br>• Imprisonment up to <strong>1 year</strong>, OR<br>• Fine up to <strong>₹1,000</strong>, OR<br>• Both<br><br><strong>What is Hurt (Section 319):</strong><br>• Bodily pain<br>• Disease<br>• Infirmity<br><br><strong>Nature:</strong><br>• <strong>Bailable</strong><br>• <strong>Compoundable</strong> (can be settled)<br>• Triable by any Magistrate<br><br><strong>Related Sections:</strong><br>• Section 324: Hurt by dangerous weapons - 3 years<br>• Section 325: Grievous hurt - 7 years<br>• Section 326: Grievous hurt by dangerous weapons - 10 years to life",
        "hindi": "धारा 323 - स्वेच्छापूर्वक उपहति कारित करना। 1 वर्ष कारावास या ₹1,000 जुर्माना। जमानती और शमनीय अपराध।",
        "citations": [{"section": "Section 323", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.95}],
        "followups": ["What is grievous hurt?", "323 bail process?"]
    },
    "ipc_379": {
        "answer": "<strong>Section 379 IPC - Theft</strong><br><br><strong>Punishment:</strong><br>• Imprisonment up to <strong>3 years</strong>, OR<br>• Fine, OR<br>• Both<br><br><strong>Essential Elements (Section 378):</strong><br>1. <strong>Moveable property</strong><br>2. Taken out of <strong>possession</strong> of another<br>3. Without <strong>consent</strong><br>4. <strong>Dishonest intention</strong> (intention to cause wrongful gain/loss)<br>5. Some <strong>movement</strong> of property<br><br><strong>Related Offenses:</strong><br>• Section 380: Theft in dwelling house - 7 years<br>• Section 381: Theft by servant - 7 years<br>• Section 382: Theft after preparation for causing death/hurt - 10 years",
        "hindi": "धारा 379 - चोरी। 3 वर्ष तक कारावास या जुर्माना। धारा 378 में चोरी की परिभाषा।",
        "citations": [{"section": "Section 379", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.96}],
        "followups": ["Theft vs robbery?", "Motor vehicle theft?"]
    },
    "ipc_392": {
        "answer": "<strong>Section 392 IPC - Robbery</strong><br><br><strong>Punishment:</strong><br>• Rigorous imprisonment up to <strong>10 years</strong> + fine<br>• If on highway between sunset and sunrise: up to <strong>14 years</strong><br><br><strong>What is Robbery (Section 390):</strong><br>• <strong>Theft + Hurt/Fear</strong>: When theft involves causing hurt, fear, or restraint<br>• <strong>Extortion + Fear</strong>: When extortion involves putting in fear of instant death/hurt<br><br><strong>Related Offenses:</strong><br>• Section 393: Attempt to commit robbery - 7 years<br>• Section 394: Voluntarily causing hurt in robbery - 10 years to life<br>• Section 395: Dacoity (5+ persons) - 10 years to life<br>• Section 397: Robbery with deadly weapon - 7 years minimum",
        "hindi": "धारा 392 - लूट। 10 वर्ष तक कठोर कारावास। रात में राजमार्ग पर: 14 वर्ष तक। चोरी या उद्दापन + डर या चोट = लूट।",
        "citations": [{"section": "Section 392", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.96}],
        "followups": ["Robbery vs dacoity?", "Armed robbery punishment?"]
    },
    "ipc_509": {
        "answer": "<strong>Section 509 IPC - Word, Gesture or Act Intended to Insult Modesty of Woman</strong><br><br><strong>Punishment:</strong><br>• Simple imprisonment up to <strong>3 years</strong> + fine<br><br><strong>What Constitutes:</strong><br>• Uttering any <strong>word</strong><br>• Making any <strong>sound or gesture</strong><br>• Exhibiting any <strong>object</strong><br>• <strong>Intruding</strong> on privacy of woman<br>• All with intent to insult modesty<br><br><strong>Examples:</strong><br>• Eve-teasing<br>• Obscene remarks<br>• Making vulgar gestures<br>• Singing obscene songs directed at woman",
        "hindi": "धारा 509 - स्त्री की लज्जा का अपमान। 3 वर्ष तक कारावास और जुर्माना। अभद्र टिप्पणी, इशारे, छेड़छाड़।",
        "citations": [{"section": "Section 509", "act_name": "Indian Penal Code, 1860", "relevance_score": 0.94}],
        "followups": ["Eve teasing laws?", "How to file 509 complaint?"]
    },

    # =========================================================================
    # SPECIAL DOCTRINES & PRINCIPLES
    # =========================================================================
    "rarest_of_rare": {
        "answer": "<strong>Rarest of Rare Doctrine</strong><br><br>Established in <em>Bachan Singh vs State of Punjab (1980)</em> for awarding death penalty.<br><br><strong>Principle:</strong> Death penalty only when life imprisonment is <strong>unquestionably foreclosed</strong>.<br><br><strong>Balance Sheet Approach:</strong><br>Courts must consider:<br>• <strong>Aggravating circumstances</strong> (crime-related)<br>• <strong>Mitigating circumstances</strong> (criminal-related)<br><br><strong>Aggravating Factors:</strong><br>• Pre-planned, cold-blooded murder<br>• Murder for gain<br>• Extreme brutality/depravity<br>• Multiple murders<br>• Murder of child/woman/elderly<br>• Murder by public servant<br><br><strong>Mitigating Factors:</strong><br>• Young age<br>• No prior criminal record<br>• Mental illness<br>• Possibility of reformation<br>• Socio-economic background<br><br><strong>Key Cases:</strong><br>• <em>Machhi Singh (1983)</em> - Categories of rarest of rare<br>• <em>Santosh Kumar Bariyar (2009)</em> - Principled sentencing",
        "hindi": "दुर्लभतम से दुर्लभ सिद्धांत - मृत्युदंड केवल तभी जब आजीवन कारावास पर्याप्त न हो। बचन सिंह (1980) में स्थापित।",
        "citations": [{"case_citation": "Bachan Singh vs State of Punjab (1980) 2 SCC 684", "relevance_score": 0.99}, {"case_citation": "Machhi Singh vs State of Punjab (1983) 3 SCC 470", "relevance_score": 0.97}],
        "followups": ["Section 302 punishment?", "Can death penalty be commuted?"]
    },

    # =========================================================================
    # CODE OF CRIMINAL PROCEDURE (CrPC) 1973
    # =========================================================================
    "fir": {
        "answer": "<strong>FIR - First Information Report (Section 154 CrPC)</strong><br><br><strong>What is FIR:</strong><br>First information of a <strong>cognizable offense</strong> given to police.<br><br><strong>How to File:</strong><br>1. Go to <strong>jurisdictional police station</strong><br>2. Give <strong>oral or written</strong> information<br>3. Get it <strong>signed</strong> by informant<br>4. Get <strong>free copy</strong> immediately<br><br><strong>Key Points:</strong><br>• <strong>Zero FIR:</strong> Can be filed at ANY police station<br>• Police CANNOT refuse to register FIR for cognizable offense<br>• If refused: Complaint to <strong>SP</strong> or <strong>Magistrate (Section 156(3))</strong><br>• Woman can give statement at her residence<br>• <strong>e-FIR:</strong> Available in many states for certain offenses<br><br><strong>Contents of FIR:</strong><br>• Date, time, place of occurrence<br>• Details of offense<br>• Name of accused (if known)<br>• Names of witnesses<br>• Signature of informant",
        "hindi": "FIR - प्रथम सूचना रिपोर्ट (धारा 154)। संज्ञेय अपराध की पहली सूचना। Zero FIR किसी भी थाने में। पुलिस मना करे तो SP या मजिस्ट्रेट से शिकायत।",
        "citations": [{"section": "Section 154", "act_name": "Code of Criminal Procedure, 1973", "relevance_score": 0.99}, {"section": "Section 156(3)", "act_name": "CrPC", "relevance_score": 0.94}],
        "followups": ["Zero FIR explained?", "If police refuses FIR?", "Online FIR filing?"]
    },
    "zero_fir": {
        "answer": "<strong>Zero FIR</strong><br><br><strong>Definition:</strong> FIR registered at <strong>any police station</strong> irrespective of place of occurrence.<br><br><strong>Key Points:</strong><br>• No jurisdiction required for registration<br>• Given <strong>temporary number</strong> (zero)<br>• Later transferred to jurisdictional police station<br>• Regular FIR number assigned after transfer<br><br><strong>Purpose:</strong><br>• Immediate registration<br>• No delay due to jurisdiction issues<br>• Especially important in:<br>&nbsp;&nbsp;- Rape cases<br>&nbsp;&nbsp;- Kidnapping<br>&nbsp;&nbsp;- Serious crimes<br><br><strong>Legal Basis:</strong> Criminal Law (Amendment) Act, 2013",
        "hindi": "Zero FIR - किसी भी पुलिस स्टेशन में दर्ज हो सकती है, क्षेत्राधिकार की आवश्यकता नहीं। बाद में संबंधित थाने को भेजी जाती है।",
        "citations": [{"section": "Zero FIR Provision", "act_name": "Criminal Law Amendment Act, 2013", "relevance_score": 0.97}],
        "followups": ["How to file FIR?", "FIR registration process?"]
    },
    "bail_regular": {
        "answer": "<strong>Regular Bail (Sections 437, 439 CrPC)</strong><br><br><strong>Section 437 - Bail by Magistrate:</strong><br>• For offenses NOT punishable with death or life imprisonment<br>• Can impose conditions<br><br><strong>Section 439 - Bail by Sessions/High Court:</strong><br>• Can grant bail in ANY case including capital offenses<br>• Wider powers than Magistrate<br><br><strong>Factors Considered:</strong><br>• Nature and gravity of offense<br>• Severity of punishment<br>• Character/antecedents of accused<br>• Circumstances of case<br>• Likelihood of absconding<br>• Likelihood of tampering with evidence<br>• Prima facie case against accused<br><br><strong>Conditions may include:</strong><br>• Surety bond<br>• Surrender passport<br>• Regular attendance at police station<br>• Not leave jurisdiction",
        "hindi": "नियमित जमानत - गिरफ्तारी के बाद। धारा 437 (मजिस्ट्रेट द्वारा), धारा 439 (सेशन/हाई कोर्ट द्वारा)।",
        "citations": [{"section": "Section 437", "act_name": "CrPC, 1973", "relevance_score": 0.98}, {"section": "Section 439", "act_name": "CrPC, 1973", "relevance_score": 0.97}],
        "followups": ["Anticipatory bail?", "Bail cancellation?", "Default bail?"]
    },
    "anticipatory_bail": {
        "answer": "<strong>Anticipatory Bail (Section 438 CrPC)</strong><br><br><strong>What is it:</strong> Bail granted <strong>BEFORE arrest</strong> in anticipation of arrest.<br><br><strong>Who can apply:</strong><br>• Any person who has <strong>reason to believe</strong> they may be arrested for non-bailable offense<br><br><strong>Where to apply:</strong><br>• <strong>Sessions Court</strong>, or<br>• <strong>High Court</strong><br><br><strong>Duration:</strong><br>• <em>Sushila Aggarwal vs State (2020)</em>: No fixed time limit; can continue till end of trial<br><br><strong>Conditions may include:</strong><br>• Join investigation when required<br>• Not leave India without permission<br>• Not make inducements/threats to witnesses<br>• Surrender passport<br><br><strong>When NOT granted usually:</strong><br>• Rape/gang rape allegations<br>• Serious economic offenses<br>• Grave crimes against society",
        "hindi": "अग्रिम जमानत (धारा 438) - गिरफ्तारी से पहले। सेशन कोर्ट या हाई कोर्ट में आवेदन। सुशीला अग्रवाल (2020): कोई समय सीमा नहीं।",
        "citations": [{"section": "Section 438", "act_name": "CrPC, 1973", "relevance_score": 0.99}, {"case_citation": "Sushila Aggarwal vs State (2020) 5 SCC 1", "relevance_score": 0.96}],
        "followups": ["How to apply for anticipatory bail?", "Anticipatory bail conditions?"]
    },
    "crpc_125": {
        "answer": "<strong>Section 125 CrPC - Maintenance</strong><br><br><strong>Who can claim:</strong><br>• <strong>Wife</strong> (unable to maintain herself)<br>• <strong>Children</strong> (legitimate or illegitimate, until 18; if disabled - for life)<br>• <strong>Parents</strong> (unable to maintain themselves)<br><br><strong>Against whom:</strong><br>• Person having <strong>sufficient means</strong> who neglects/refuses to maintain<br><br><strong>Amount:</strong><br>• Maximum <strong>₹500/month</strong> was earlier; now courts award as per need<br>• 2001 Amendment: Interim maintenance within 60 days<br><br><strong>When wife NOT entitled:</strong><br>• Living in adultery<br>• Refuses to live with husband without sufficient reason<br>• Living separately by mutual consent<br><br><strong>Key Point:</strong> Applies to ALL religions (secular provision)",
        "hindi": "धारा 125 - भरण-पोषण। पत्नी, बच्चे, माता-पिता दावा कर सकते हैं। सभी धर्मों पर लागू। 60 दिनों में अंतरिम भरण-पोषण।",
        "citations": [{"section": "Section 125", "act_name": "CrPC, 1973", "relevance_score": 0.98}],
        "followups": ["Maintenance amount calculation?", "125 vs Hindu Adoption Act?"]
    },
    "crpc_144": {
        "answer": "<strong>Section 144 CrPC - Prohibitory Orders</strong><br><br><strong>What is it:</strong><br>Emergency power to prevent public disturbance.<br><br><strong>Who can issue:</strong><br>• District Magistrate<br>• Sub-divisional Magistrate<br>• Executive Magistrate empowered by State<br><br><strong>Purpose:</strong><br>• Prevent obstruction, annoyance, injury<br>• Prevent disturbance of public tranquility<br>• Prevent riot or affray<br><br><strong>Duration:</strong><br>• Maximum <strong>2 months</strong><br>• State Government can extend up to <strong>6 months</strong><br><br><strong>Common Restrictions:</strong><br>• Prohibiting assembly of 4+ persons<br>• Carrying of weapons<br>• Movement in certain areas<br><br><strong>Key Case:</strong> <em>Anuradha Bhasin vs UoI (2020)</em> - Must be proportionate",
        "hindi": "धारा 144 - निषेधाज्ञा। जिला मजिस्ट्रेट द्वारा शांति व्यवस्था के लिए। अधिकतम 2 महीने, राज्य द्वारा 6 महीने तक विस्तार।",
        "citations": [{"section": "Section 144", "act_name": "CrPC, 1973", "relevance_score": 0.97}],
        "followups": ["144 vs curfew difference?", "Can 144 be challenged?"]
    },
    "crpc_161": {
        "answer": "<strong>Section 161 CrPC - Examination of Witnesses by Police</strong><br><br><strong>Key Points:</strong><br>• Police can <strong>orally examine</strong> any person supposed to be acquainted with facts<br>• Person is <strong>bound to answer</strong> all questions (except self-incriminating - Article 20(3))<br>• <strong>No oath</strong> administered<br>• Statement <strong>NOT signed</strong> by witness<br><br><strong>Evidentiary Value:</strong><br>• Statement to police is <strong>NOT admissible</strong> as evidence (Section 162)<br>• Can only be used to <strong>contradict</strong> the witness<br><br><strong>Section 164:</strong><br>• Statement/Confession recorded by <strong>Magistrate</strong><br>• Admissible as evidence<br>• Must be voluntary",
        "hindi": "धारा 161 - पुलिस द्वारा गवाह की जांच। मौखिक परीक्षा। बयान पर हस्ताक्षर नहीं। धारा 162: पुलिस को दिया बयान साक्ष्य नहीं।",
        "citations": [{"section": "Section 161", "act_name": "CrPC, 1973", "relevance_score": 0.95}, {"section": "Section 162", "act_name": "CrPC", "relevance_score": 0.93}],
        "followups": ["Section 164 statement?", "Police investigation process?"]
    },
    "crpc_482": {
        "answer": "<strong>Section 482 CrPC - Inherent Powers of High Court</strong><br><br><strong>Purpose:</strong><br>• To <strong>prevent abuse of process</strong> of any court<br>• To <strong>secure ends of justice</strong><br><br><strong>Powers:</strong><br>• <strong>Quash</strong> FIR or criminal proceedings<br>• Set aside orders passed by lower courts<br>• Transfer cases<br><br><strong>When Proceedings can be Quashed:</strong><br>• Allegations do not constitute offense<br>• No legal evidence against accused<br>• Proceedings are malicious<br>• Continuation would be abuse of process<br>• Matrimonial disputes settled amicably<br><br><strong>Key Principles:</strong><br>• Exercise sparingly and with caution<br>• Not to be used as substitute for appeal/revision<br>• <em>State of Haryana vs Bhajan Lal (1992)</em> - Guidelines for quashing",
        "hindi": "धारा 482 - हाई कोर्ट की अंतर्निहित शक्तियां। FIR या कार्यवाही रद्द करने के लिए। न्याय सुनिश्चित करने और प्रक्रिया के दुरुपयोग को रोकने के लिए।",
        "citations": [{"section": "Section 482", "act_name": "CrPC, 1973", "relevance_score": 0.98}, {"case_citation": "State of Haryana vs Bhajan Lal (1992)", "relevance_score": 0.95}],
        "followups": ["How to file 482 petition?", "498A quashing under 482?"]
    },

    # =========================================================================
    # CONSTITUTION OF INDIA
    # =========================================================================
    "fundamental_rights": {
        "answer": "<strong>Fundamental Rights (Part III - Articles 12-35)</strong><br><br><strong>Six Fundamental Rights:</strong><br><br><strong>1. Right to Equality (Art 14-18):</strong><br>• Art 14: Equality before law<br>• Art 15: No discrimination<br>• Art 16: Equal opportunity in public employment<br>• Art 17: Abolition of untouchability<br>• Art 18: Abolition of titles<br><br><strong>2. Right to Freedom (Art 19-22):</strong><br>• Art 19: Six freedoms (speech, assembly, association, movement, residence, profession)<br>• Art 20: Protection against conviction<br>• Art 21: Right to Life and Personal Liberty<br>• Art 22: Protection against arrest and detention<br><br><strong>3. Right Against Exploitation (Art 23-24):</strong><br>• No human trafficking, forced labor, child labor<br><br><strong>4. Right to Freedom of Religion (Art 25-28)</strong><br><br><strong>5. Cultural & Educational Rights (Art 29-30)</strong><br><br><strong>6. Right to Constitutional Remedies (Art 32)</strong>",
        "hindi": "मौलिक अधिकार (भाग III) - समानता, स्वतंत्रता, शोषण के विरुद्ध, धार्मिक स्वतंत्रता, सांस्कृतिक/शैक्षिक, संवैधानिक उपचार।",
        "citations": [{"section": "Part III", "act_name": "Constitution of India", "relevance_score": 0.99}],
        "followups": ["Article 21 scope?", "What are writs?", "DPSP vs Fundamental Rights?"]
    },
    "article_21": {
        "answer": "<strong>Article 21 - Right to Life and Personal Liberty</strong><br><br><em>'No person shall be deprived of his life or personal liberty except according to procedure established by law.'</em><br><br><strong>Expanded Scope (Judicial Interpretation):</strong><br>• Right to live with <strong>dignity</strong><br>• Right to <strong>livelihood</strong><br>• Right to <strong>privacy</strong> (Puttaswamy, 2017)<br>• Right to clean <strong>environment</strong><br>• Right to <strong>health</strong><br>• Right to <strong>education</strong><br>• Right to <strong>shelter</strong><br>• Right to <strong>speedy trial</strong><br>• Right to <strong>legal aid</strong><br>• Right to <strong>sleep</strong><br>• Right against <strong>handcuffing</strong><br>• Right against <strong>solitary confinement</strong><br>• Right to <strong>reputation</strong><br>• Right to <strong>travel abroad</strong><br><br><strong>Landmark:</strong> <em>Maneka Gandhi vs UoI (1978)</em> - Procedure must be fair, just and reasonable",
        "hindi": "अनुच्छेद 21 - जीवन और व्यक्तिगत स्वतंत्रता। गरिमा, आजीविका, निजता, स्वास्थ्य, शिक्षा, आश्रय का अधिकार शामिल।",
        "citations": [{"section": "Article 21", "act_name": "Constitution of India", "relevance_score": 0.99}, {"case_citation": "Maneka Gandhi vs Union of India (1978)", "relevance_score": 0.97}],
        "followups": ["Right to privacy case?", "Article 21 and environment?"]
    },
    "article_32": {
        "answer": "<strong>Article 32 - Right to Constitutional Remedies</strong><br><br>Dr. B.R. Ambedkar called it the <strong>'Heart and Soul'</strong> of the Constitution.<br><br><strong>Provisions:</strong><br>• Right to move <strong>Supreme Court</strong> for enforcement of Fundamental Rights<br>• SC can issue writs: <strong>Habeas Corpus, Mandamus, Prohibition, Certiorari, Quo Warranto</strong><br>• Parliament can empower other courts to issue writs (Article 32(3))<br>• Cannot be suspended except during Emergency (Article 359)<br><br><strong>Key Points:</strong><br>• Only for <strong>Fundamental Rights</strong> violation<br>• Supreme Court is <strong>protector and guarantor</strong> of Fundamental Rights<br>• Can be invoked <strong>directly</strong> without going to lower courts<br><br><strong>Article 226:</strong> High Courts can issue writs for FR + any other purpose",
        "hindi": "अनुच्छेद 32 - संवैधानिक उपचारों का अधिकार। संविधान की 'आत्मा'। सुप्रीम कोर्ट में सीधे जा सकते हैं।",
        "citations": [{"section": "Article 32", "act_name": "Constitution of India", "relevance_score": 0.99}],
        "followups": ["Types of writs?", "Article 32 vs 226?"]
    },
    "writs": {
        "answer": "<strong>Types of Writs in India</strong><br><br>Under <strong>Article 32</strong> (Supreme Court) and <strong>Article 226</strong> (High Courts):<br><br><strong>1. Habeas Corpus</strong> ('To have the body')<br>• Against <strong>illegal detention</strong><br>• Produce detained person before court<br>• Most powerful writ for personal liberty<br><br><strong>2. Mandamus</strong> ('We command')<br>• To compel public authority to <strong>perform duty</strong><br>• Not against private persons or President/Governor<br><br><strong>3. Certiorari</strong> ('To be certified')<br>• To <strong>quash</strong> order of lower court/tribunal<br>• Against judicial/quasi-judicial bodies<br><br><strong>4. Prohibition</strong><br>• To <strong>prevent</strong> lower court from exceeding jurisdiction<br>• Issued during pending proceedings<br><br><strong>5. Quo Warranto</strong> ('By what authority')<br>• To question right to hold <strong>public office</strong><br>• Against usurper of public office",
        "hindi": "रिट - बंदी प्रत्यक्षीकरण (अवैध हिरासत), परमादेश (कर्तव्य पालन), उत्प्रेषण (आदेश रद्द), प्रतिषेध (रोक), अधिकार पृच्छा (पद का अधिकार)।",
        "citations": [{"section": "Article 32 & 226", "act_name": "Constitution of India", "relevance_score": 0.98}],
        "followups": ["How to file writ petition?", "Difference between Art 32 and 226?"]
    },
    "art_32_vs_226": {
        "answer": "<strong>Difference between Article 32 and Article 226</strong><br><br><table style='width:100%; border-collapse: collapse;'><tr style='background:#1a1f26;'><th style='padding:10px; border:1px solid #333;'>Aspect</th><th style='padding:10px; border:1px solid #333;'>Article 32</th><th style='padding:10px; border:1px solid #333;'>Article 226</th></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Court</strong></td><td style='padding:10px; border:1px solid #333;'>Supreme Court only</td><td style='padding:10px; border:1px solid #333;'>High Courts</td></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Scope</strong></td><td style='padding:10px; border:1px solid #333;'>Only for <strong>Fundamental Rights</strong></td><td style='padding:10px; border:1px solid #333;'>For FR + <strong>any other purpose</strong></td></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Nature</strong></td><td style='padding:10px; border:1px solid #333;'>Itself a <strong>Fundamental Right</strong></td><td style='padding:10px; border:1px solid #333;'>Constitutional right, not FR</td></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Suspension</strong></td><td style='padding:10px; border:1px solid #333;'>Can be suspended during Emergency (Art 359)</td><td style='padding:10px; border:1px solid #333;'>Cannot be suspended</td></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Discretion</strong></td><td style='padding:10px; border:1px solid #333;'>SC <strong>must</strong> issue writ if FR violated</td><td style='padding:10px; border:1px solid #333;'>HC <strong>may</strong> issue (discretionary)</td></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Territory</strong></td><td style='padding:10px; border:1px solid #333;'>Whole of India</td><td style='padding:10px; border:1px solid #333;'>Within HC's territorial jurisdiction</td></tr></table><br><br><strong>Key Point:</strong> Article 226 is <strong>wider in scope</strong> (any purpose) but Article 32 is <strong>guaranteed</strong> (mandatory for FR).",
        "hindi": "अनुच्छेद 32 बनाम 226: 32 केवल मौलिक अधिकारों के लिए (सुप्रीम कोर्ट), 226 किसी भी उद्देश्य के लिए (हाई कोर्ट)। 32 स्वयं मौलिक अधिकार है।",
        "citations": [{"section": "Article 32", "act_name": "Constitution of India", "relevance_score": 0.98}, {"section": "Article 226", "act_name": "Constitution of India", "relevance_score": 0.97}],
        "followups": ["What are 5 types of writs?", "How to file writ in Supreme Court?"]
    },
    "police_refusal": {
        "answer": "<strong>What to do if Police Refuses to File FIR?</strong><br><br><strong>Option 1: Complaint to Senior Officer</strong><br>• Write to <strong>Superintendent of Police (SP)</strong><br>• Or <strong>Deputy Commissioner of Police (DCP)</strong><br><br><strong>Option 2: Section 156(3) CrPC - Magistrate Complaint</strong><br>• File complaint directly to <strong>Judicial Magistrate</strong><br>• Magistrate can <strong>direct police</strong> to register FIR and investigate<br>• Most effective remedy<br><br><strong>Option 3: Private Complaint (Section 200 CrPC)</strong><br>• File complaint directly before Magistrate<br>• Magistrate examines complainant on oath<br><br><strong>Option 4: Writ Petition</strong><br>• File writ of <strong>Mandamus</strong> in High Court<br>• To direct police to perform their duty<br><br><strong>Other Remedies:</strong><br>• <strong>State/National Human Rights Commission</strong><br>• <strong>State Women's Commission</strong> (for women-related offenses)<br>• <strong>Online complaint</strong> on state police website<br><br><strong>Key Case:</strong> <em>Lalita Kumari vs Govt of UP (2014)</em> - Police MUST register FIR for cognizable offense",
        "hindi": "पुलिस FIR न दर्ज करे तो: 1) SP को शिकायत, 2) धारा 156(3) के तहत मजिस्ट्रेट से, 3) धारा 200 के तहत निजी शिकायत, 4) हाई कोर्ट में रिट।",
        "citations": [{"section": "Section 156(3)", "act_name": "CrPC, 1973", "relevance_score": 0.98}, {"case_citation": "Lalita Kumari vs Govt of UP (2014)", "relevance_score": 0.96}],
        "followups": ["How to file 156(3) complaint?", "What is Zero FIR?"]
    },
    "sec_299_vs_300": {
        "answer": "<strong>Difference between Section 299 and Section 300 IPC</strong><br><br><table style='width:100%; border-collapse: collapse;'><tr style='background:#1a1f26;'><th style='padding:10px; border:1px solid #333;'>Aspect</th><th style='padding:10px; border:1px solid #333;'>Section 299 (Culpable Homicide)</th><th style='padding:10px; border:1px solid #333;'>Section 300 (Murder)</th></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Intention</strong></td><td style='padding:10px; border:1px solid #333;'>Intention to cause death OR bodily injury <strong>likely</strong> to cause death</td><td style='padding:10px; border:1px solid #333;'>Intention to cause death OR bodily injury <strong>sufficient</strong> to cause death</td></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Knowledge</strong></td><td style='padding:10px; border:1px solid #333;'>Knowledge that act is <strong>likely</strong> to cause death</td><td style='padding:10px; border:1px solid #333;'>Knowledge that act is <strong>so imminently dangerous</strong> that death is probable</td></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Degree</strong></td><td style='padding:10px; border:1px solid #333;'>Lesser degree of intention/knowledge</td><td style='padding:10px; border:1px solid #333;'>Higher degree - more certain</td></tr><tr><td style='padding:10px; border:1px solid #333;'><strong>Punishment</strong></td><td style='padding:10px; border:1px solid #333;'>Section 304: Life or 10 years</td><td style='padding:10px; border:1px solid #333;'>Section 302: Death or life imprisonment</td></tr></table><br><br><strong>Simple Rule:</strong><br>• 'Likely to cause death' → Section 299 (Culpable Homicide)<br>• 'Sufficient to cause death' → Section 300 (Murder)<br><br><strong>All murders are culpable homicide, but not all culpable homicides are murder.</strong>",
        "hindi": "धारा 299 बनाम 300: 299 में मृत्यु की 'संभावना', 300 में मृत्यु 'निश्चित'। सभी हत्या सदोष मानव वध है, लेकिन सभी सदोष मानव वध हत्या नहीं।",
        "citations": [{"section": "Section 299", "act_name": "IPC, 1860", "relevance_score": 0.98}, {"section": "Section 300", "act_name": "IPC, 1860", "relevance_score": 0.98}],
        "followups": ["What is Section 304?", "Section 302 punishment?"]
    },

    # =========================================================================
    # FAMILY LAW
    # =========================================================================
    "divorce_hindu": {
        "answer": "<strong>Divorce under Hindu Marriage Act, 1955</strong><br><br><strong>Section 13 - Grounds for Divorce:</strong><br>• <strong>Adultery</strong><br>• <strong>Cruelty</strong> (mental or physical)<br>• <strong>Desertion</strong> for 2+ continuous years<br>• <strong>Conversion</strong> to another religion<br>• <strong>Unsound mind</strong> / mental disorder<br>• <strong>Leprosy</strong> (virulent and incurable)<br>• <strong>Venereal disease</strong> (communicable)<br>• <strong>Renunciation</strong> of world (sanyasa)<br>• <strong>Presumed dead</strong> (not heard alive for 7+ years)<br><br><strong>Additional Grounds for Wife (Section 13(2)):</strong><br>• Husband guilty of rape, sodomy, bestiality<br>• Husband married before 1955, other wife is alive<br><br><strong>Section 13B - Mutual Consent Divorce:</strong><br>• Living separately for 1+ year<br>• Both agree marriage has broken down<br>• 6-month cooling period (can be waived)<br>• <em>Amardeep Singh (2017)</em> - Cooling period can be waived",
        "hindi": "हिंदू विवाह अधिनियम में तलाक - धारा 13 (आधार), धारा 13B (आपसी सहमति)। व्यभिचार, क्रूरता, परित्याग, धर्म परिवर्तन आदि आधार।",
        "citations": [{"section": "Section 13", "act_name": "Hindu Marriage Act, 1955", "relevance_score": 0.98}, {"section": "Section 13B", "act_name": "Hindu Marriage Act, 1955", "relevance_score": 0.97}],
        "followups": ["Mutual consent divorce process?", "Alimony under Hindu law?"]
    },
    "domestic_violence": {
        "answer": "<strong>Protection of Women from Domestic Violence Act, 2005</strong><br><br><strong>What is Domestic Violence:</strong><br>• <strong>Physical abuse</strong>: Bodily pain, harm, danger to life<br>• <strong>Sexual abuse</strong>: Forced intercourse, pornography<br>• <strong>Verbal/Emotional abuse</strong>: Insults, ridicule, humiliation<br>• <strong>Economic abuse</strong>: Deprivation of resources, property<br><br><strong>Who can file complaint:</strong><br>• <strong>Aggrieved person</strong>: Woman in domestic relationship<br>• Any person on her behalf (with her consent)<br><br><strong>Against whom:</strong><br>• <strong>Respondent</strong>: Adult male member of household (including relatives)<br><br><strong>Reliefs Available:</strong><br>• <strong>Protection Order</strong> (Section 18)<br>• <strong>Residence Order</strong> (Section 19)<br>• <strong>Monetary Relief</strong> (Section 20)<br>• <strong>Custody Order</strong> (Section 21)<br>• <strong>Compensation Order</strong> (Section 22)<br><br><strong>Filing:</strong> Before Magistrate (Section 12)",
        "hindi": "घरेलू हिंसा अधिनियम 2005 - शारीरिक, यौन, मौखिक, आर्थिक हिंसा शामिल। संरक्षण आदेश, निवास आदेश, मौद्रिक राहत मिल सकती है।",
        "citations": [{"section": "DV Act, 2005", "act_name": "Protection of Women from Domestic Violence Act, 2005", "relevance_score": 0.98}],
        "followups": ["How to file DV case?", "DV Act vs 498A?"]
    },
    "maintenance": {
        "answer": "<strong>Maintenance Laws in India</strong><br><br><strong>1. Section 125 CrPC:</strong><br>• Applies to ALL religions<br>• Wife, children, parents can claim<br>• Summary proceedings before Magistrate<br><br><strong>2. Hindu Adoption and Maintenance Act, 1956:</strong><br>• Section 18: Wife's maintenance<br>• Section 20: Children and aged parents' maintenance<br><br><strong>3. Hindu Marriage Act, 1955:</strong><br>• Section 24: Interim maintenance during proceedings<br>• Section 25: Permanent alimony after divorce<br><br><strong>4. Muslim Women (Protection of Rights on Divorce) Act, 1986:</strong><br>• Maintenance during iddat period<br>• Reasonable provision after divorce<br><br><strong>Factors for Quantum:</strong><br>• Income of husband<br>• Standard of living<br>• Needs of wife/children<br>• Conduct of parties<br>• Wife's own income (if any)",
        "hindi": "भरण-पोषण कानून - धारा 125 CrPC (सभी धर्म), हिंदू दत्तक ग्रहण अधिनियम, हिंदू विवाह अधिनियम। पति की आय और जरूरतों के आधार पर।",
        "citations": [{"section": "Section 125", "act_name": "CrPC", "relevance_score": 0.96}, {"section": "Section 24", "act_name": "Hindu Marriage Act", "relevance_score": 0.94}],
        "followups": ["How to file maintenance case?", "Interim maintenance?"]
    },

    # =========================================================================
    # CONSUMER & CYBER LAW
    # =========================================================================
    "consumer_protection": {
        "answer": "<strong>Consumer Protection Act, 2019</strong><br><br><strong>Who is Consumer:</strong><br>• Buyer of goods/services for <strong>personal use</strong><br>• NOT for commercial resale<br><br><strong>Consumer Rights:</strong><br>• Right to <strong>safety</strong><br>• Right to <strong>information</strong><br>• Right to <strong>choose</strong><br>• Right to be <strong>heard</strong><br>• Right to <strong>redressal</strong><br>• Right to <strong>consumer education</strong><br><br><strong>Where to File Complaint:</strong><br>• <strong>District Commission:</strong> Up to ₹1 crore<br>• <strong>State Commission:</strong> ₹1 crore to ₹10 crore<br>• <strong>National Commission:</strong> Above ₹10 crore<br><br><strong>Limitation:</strong> 2 years from cause of action<br><br><strong>New Features (2019):</strong><br>• E-commerce included<br>• Product liability<br>• Central Consumer Protection Authority<br><br><strong>Online Filing:</strong> edaakhil.nic.in",
        "hindi": "उपभोक्ता संरक्षण अधिनियम 2019 - जिला आयोग (₹1 करोड़ तक), राज्य (₹10 करोड़ तक), राष्ट्रीय (₹10 करोड़+)। ऑनलाइन: edaakhil.nic.in",
        "citations": [{"section": "Consumer Protection Act, 2019", "act_name": "Consumer Protection Act, 2019", "relevance_score": 0.98}],
        "followups": ["How to file consumer complaint?", "Consumer court fees?"]
    },
    "cyber_crime": {
        "answer": "<strong>Cyber Crimes - IT Act, 2000</strong><br><br><strong>Key Offenses:</strong><br><br><strong>Section 66:</strong> Computer hacking<br>• 3 years + ₹5 lakh fine<br><br><strong>Section 66C:</strong> Identity theft<br>• 3 years + ₹1 lakh fine<br><br><strong>Section 66D:</strong> Cheating by personation using computer<br>• 3 years + ₹1 lakh fine<br><br><strong>Section 66E:</strong> Privacy violation<br>• 3 years + ₹2 lakh fine<br><br><strong>Section 67:</strong> Publishing obscene material<br>• First offense: 3 years + ₹5 lakh<br>• Repeat: 5 years + ₹10 lakh<br><br><strong>Section 67A:</strong> Sexually explicit content - 5-7 years<br><br><strong>Section 67B:</strong> Child pornography - 5-7 years<br><br><strong>Where to Report:</strong><br>• <strong>cybercrime.gov.in</strong> (National Portal)<br>• Local Cyber Cell<br>• Nearest Police Station",
        "hindi": "IT Act 2000 - साइबर अपराध। हैकिंग (66), पहचान चोरी (66C), धोखाधड़ी (66D), निजता उल्लंघन (66E)। शिकायत: cybercrime.gov.in",
        "citations": [{"section": "IT Act, 2000", "act_name": "Information Technology Act, 2000", "relevance_score": 0.98}],
        "followups": ["How to report cyber crime?", "Online fraud complaint?"]
    },

    # =========================================================================
    # RTI & OTHER IMPORTANT LAWS
    # =========================================================================
    "rti": {
        "answer": "<strong>Right to Information Act, 2005</strong><br><br><strong>How to File RTI:</strong><br>1. Write application to <strong>Public Information Officer (PIO)</strong><br>2. <strong>Fee:</strong> ₹10 (postal order/DD/cash)<br>3. <strong>Response:</strong> 30 days (48 hours for life/liberty matters)<br><br><strong>Appeals:</strong><br>• <strong>First Appeal:</strong> To First Appellate Authority within 30 days<br>• <strong>Second Appeal:</strong> To Information Commission within 90 days<br><br><strong>Exemptions (Section 8):</strong><br>• National security<br>• Cabinet papers<br>• Trade secrets<br>• Personal privacy<br>• Fiduciary relationship<br><br><strong>Key Points:</strong><br>• BPL: No fee<br>• No reason needed<br>• <strong>Online:</strong> rtionline.gov.in<br><br><strong>Penalty:</strong> ₹250/day up to ₹25,000 on PIO for delay/refusal",
        "hindi": "RTI अधिनियम 2005 - ₹10 शुल्क, 30 दिनों में जवाब। प्रथम अपील 30 दिन में, द्वितीय अपील 90 दिन में। ऑनलाइन: rtionline.gov.in",
        "citations": [{"section": "RTI Act, 2005", "act_name": "Right to Information Act, 2005", "relevance_score": 0.99}],
        "followups": ["RTI application format?", "What if RTI not answered?"]
    },
    "pocso": {
        "answer": "<strong>POCSO Act - Protection of Children from Sexual Offences, 2012</strong><br><br><strong>Applicability:</strong> Sexual offenses against children under <strong>18 years</strong><br><br><strong>Key Offenses & Punishment:</strong><br><br><strong>Penetrative Sexual Assault (Section 3):</strong><br>• Minimum <strong>10 years</strong> to life + fine<br><br><strong>Aggravated PSA (Section 5):</strong><br>• Minimum <strong>20 years</strong> to life/death + fine<br>• By police, public servant, relative, etc.<br><br><strong>Sexual Assault (Section 7):</strong><br>• 3-5 years + fine<br><br><strong>Sexual Harassment (Section 11):</strong><br>• Up to 3 years + fine<br><br><strong>Child Pornography (Section 13-15):</strong><br>• Up to 5-7 years + fine<br><br><strong>Special Features:</strong><br>• Child-friendly procedures<br>• Special Courts<br>• No direct examination of child<br>• In-camera trials<br>• Mandatory reporting",
        "hindi": "POCSO Act 2012 - 18 वर्ष से कम उम्र के बच्चों के यौन अपराध। भेदक यौन हमला: 10 वर्ष से आजीवन। विशेष न्यायालय, बाल-हितैषी प्रक्रिया।",
        "citations": [{"section": "POCSO Act, 2012", "act_name": "Protection of Children from Sexual Offences Act, 2012", "relevance_score": 0.99}],
        "followups": ["How to report child abuse?", "POCSO court procedure?"]
    },
    "sc_st_act": {
        "answer": "<strong>SC/ST (Prevention of Atrocities) Act, 1989</strong><br><br><strong>Purpose:</strong> Prevent atrocities against Scheduled Castes and Scheduled Tribes<br><br><strong>Key Offenses:</strong><br>• Forcing to eat/drink obnoxious substances<br>• Dumping excreta, waste on premises<br>• Parading naked or with painted face<br>• Wrongfully dispossessing land<br>• Compelling bonded labor<br>• Polluting water sources<br>• Denying access to public places<br>• Using caste name to insult<br><br><strong>Punishment:</strong><br>• Minimum <strong>6 months</strong> to <strong>5 years</strong> + fine (most offenses)<br>• Up to <strong>life imprisonment</strong> for serious offenses<br><br><strong>Special Features:</strong><br>• <strong>Special Courts</strong><br>• <strong>Non-bailable</strong><br>• <strong>No anticipatory bail</strong> (Section 18)<br>• <strong>Presumption</strong> in favor of victim<br><br><strong>2018 Amendment:</strong> Preliminary inquiry allowed in certain cases",
        "hindi": "SC/ST अत्याचार निवारण अधिनियम 1989 - अनुसूचित जाति/जनजाति के विरुद्ध अत्याचार। विशेष न्यायालय, अग्रिम जमानत नहीं (धारा 18)।",
        "citations": [{"section": "SC/ST Act, 1989", "act_name": "Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989", "relevance_score": 0.98}],
        "followups": ["SC/ST Act bail provisions?", "False SC/ST case?"]
    },
    "motor_accident": {
        "answer": "<strong>Motor Vehicles Act, 1988 - Accident Claims</strong><br><br><strong>Third Party Insurance (Section 146):</strong><br>• Mandatory for all motor vehicles<br>• Covers liability to third parties<br><br><strong>Compensation Claim:</strong><br>• File before <strong>Motor Accident Claims Tribunal (MACT)</strong><br>• <strong>No fault liability</strong> for death/permanent disability (Section 140)<br>• Fixed compensation: ₹50,000 (death), ₹25,000 (permanent disability)<br><br><strong>Compensation Calculation (structured formula):</strong><br>• Based on age and income of victim<br>• Multiplier method for future loss<br>• <em>Sarla Verma vs DTC (2009)</em> - Standardized multipliers<br><br><strong>Hit and Run Cases:</strong><br>• Claim from <strong>Solatium Fund</strong><br>• ₹2 lakh for death, ₹50,000 for grievous hurt<br><br><strong>Limitation:</strong> Generally within 6 months (extendable)",
        "hindi": "मोटर वाहन अधिनियम - तृतीय पक्ष बीमा अनिवार्य। MACT में दावा। मृत्यु पर ₹50,000 (बिना दोष), हिट एंड रन में ₹2 लाख।",
        "citations": [{"section": "Motor Vehicles Act, 1988", "act_name": "Motor Vehicles Act, 1988", "relevance_score": 0.97}],
        "followups": ["How to file accident claim?", "Hit and run compensation?"]
    },
    "cheque_bounce": {
        "answer": "<strong>Section 138 NI Act - Cheque Bounce</strong><br><br><strong>Essential Elements:</strong><br>• Cheque drawn on an account<br>• For discharge of <strong>legally enforceable debt</strong><br>• Cheque <strong>dishonored</strong> for insufficient funds<br>• Cheque presented within <strong>validity period</strong><br><br><strong>Procedure:</strong><br>1. <strong>Legal Notice</strong> within <strong>30 days</strong> of dishonor<br>2. Wait <strong>15 days</strong> for payment<br>3. File <strong>complaint within 30 days</strong> of expiry of notice period<br><br><strong>Punishment:</strong><br>• Imprisonment up to <strong>2 years</strong>, OR<br>• Fine up to <strong>twice the cheque amount</strong>, OR<br>• Both<br><br><strong>Compoundable:</strong> Yes, with permission of court<br><br><strong>Key Cases:</strong><br>• <em>Dashrath Rupsingh Rathod (2014)</em> - Jurisdiction where cheque dishonored<br>• <em>Meters and Instruments (2017)</em> - Interim compensation",
        "hindi": "धारा 138 NI Act - चेक बाउंस। 30 दिन में नोटिस, 15 दिन इंतज़ार, 30 दिन में शिकायत। 2 वर्ष कारावास या दोगुना जुर्माना।",
        "citations": [{"section": "Section 138", "act_name": "Negotiable Instruments Act, 1881", "relevance_score": 0.98}],
        "followups": ["Cheque bounce notice format?", "138 case procedure?"]
    },
}

# =============================================================================
# SEARCH FUNCTION
# =============================================================================

def find_knowledge(query):
    q = query.lower()
    
    # IPC Sections
    if "302" in q or ("murder" in q and "attempt" not in q):
        return LEGAL_KB["ipc_302"]
    if "300" in q and "ipc" in q:
        return LEGAL_KB["ipc_300"]
    if "304b" in q or "dowry death" in q:
        return LEGAL_KB["ipc_304b"]
    if "304a" in q or ("negligence" in q and "death" in q):
        return LEGAL_KB["ipc_304a"]
    if "304" in q or "culpable homicide" in q:
        return LEGAL_KB["ipc_304"]
    if "307" in q or "attempt to murder" in q or "attempt murder" in q:
        return LEGAL_KB["ipc_307"]
    if "376" in q or "rape" in q:
        return LEGAL_KB["ipc_376"]
    if "354" in q or "modesty" in q or "outraging" in q:
        return LEGAL_KB["ipc_354"]
    if "498a" in q or "498" in q or ("cruelty" in q and ("husband" in q or "wife" in q)):
        return LEGAL_KB["ipc_498a"]
    if "420" in q or ("cheat" in q and "406" not in q):
        return LEGAL_KB["ipc_420"]
    if "406" in q or "breach of trust" in q:
        return LEGAL_KB["ipc_406"]
    if "34" in q and ("ipc" in q or "common intention" in q):
        return LEGAL_KB["ipc_34"]
    if "120b" in q or "conspiracy" in q:
        return LEGAL_KB["ipc_120b"]
    if "506" in q or "intimidation" in q or "criminal threat" in q:
        return LEGAL_KB["ipc_506"]
    if "323" in q or ("hurt" in q and "grievous" not in q):
        return LEGAL_KB["ipc_323"]
    if "379" in q or ("theft" in q and "robbery" not in q):
        return LEGAL_KB["ipc_379"]
    if "392" in q or "robbery" in q:
        return LEGAL_KB["ipc_392"]
    if "509" in q or "eve teasing" in q or "insult modesty" in q:
        return LEGAL_KB["ipc_509"]
    
    # Doctrines
    if "rarest" in q or "rare" in q:
        return LEGAL_KB["rarest_of_rare"]
    
    # CrPC
    if "zero fir" in q:
        return LEGAL_KB["zero_fir"]
    if "fir" in q or "first information" in q or "154" in q:
        return LEGAL_KB["fir"]
    if "anticipatory" in q or "438" in q:
        return LEGAL_KB["anticipatory_bail"]
    if "bail" in q or "437" in q or "439" in q:
        return LEGAL_KB["bail_regular"]
    if "125" in q or ("maintenance" in q and "crpc" in q):
        return LEGAL_KB["crpc_125"]
    if "144" in q or "prohibitory" in q:
        return LEGAL_KB["crpc_144"]
    if "161" in q or "police statement" in q:
        return LEGAL_KB["crpc_161"]
    if "482" in q or "quash" in q:
        return LEGAL_KB["crpc_482"]
    
    # Constitution
    if "32" in q and "226" in q:
        return LEGAL_KB["art_32_vs_226"]
    if "article 21" in q or "right to life" in q:
        return LEGAL_KB["article_21"]
    if "article 32" in q or ("constitutional" in q and "remedies" in q):
        return LEGAL_KB["article_32"]
    if "writ" in q or "habeas" in q or "mandamus" in q or "certiorari" in q:
        return LEGAL_KB["writs"]
    if "fundamental" in q or "rights" in q:
        return LEGAL_KB["fundamental_rights"]
    
    # Police refusal
    if "refuse" in q or "denied" in q or "not register" in q or "won't file" in q:
        return LEGAL_KB["police_refusal"]
    
    # IPC comparisons
    if ("299" in q and "300" in q) or ("difference" in q and ("murder" in q or "homicide" in q)):
        return LEGAL_KB["sec_299_vs_300"]
    
    # Family Law
    if "divorce" in q or "13b" in q:
        return LEGAL_KB["divorce_hindu"]
    if "domestic violence" in q or "dv act" in q:
        return LEGAL_KB["domestic_violence"]
    if "maintenance" in q or "alimony" in q:
        return LEGAL_KB["maintenance"]
    
    # Other Laws
    if "consumer" in q or "complaint" in q:
        return LEGAL_KB["consumer_protection"]
    if "cyber" in q or "hack" in q or "online fraud" in q or "it act" in q:
        return LEGAL_KB["cyber_crime"]
    if "rti" in q or "information act" in q:
        return LEGAL_KB["rti"]
    if "pocso" in q or "child" in q and "sexual" in q:
        return LEGAL_KB["pocso"]
    if "sc st" in q or "atrocit" in q or "caste" in q:
        return LEGAL_KB["sc_st_act"]
    if "accident" in q or "mact" in q or "hit and run" in q:
        return LEGAL_KB["motor_accident"]
    if "138" in q or "cheque" in q or "check bounce" in q:
        return LEGAL_KB["cheque_bounce"]
    
    return None

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
def root():
    return {
        "name": "Jurisprudence AI",
        "version": "2.0",
        "status": "running",
        "topics_covered": len(LEGAL_KB),
        "sources": ["Indian Kanoon", "India Code", "Supreme Court Judgments"]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "topics": len(LEGAL_KB)}

@app.get("/topics")
def topics():
    return {"total": len(LEGAL_KB), "categories": [
        "IPC (Indian Penal Code)",
        "CrPC (Criminal Procedure)",
        "Constitution of India",
        "Family Law",
        "Consumer Law",
        "Cyber Law",
        "RTI Act",
        "POCSO Act",
        "SC/ST Act",
        "Motor Vehicles Act",
        "Negotiable Instruments Act"
    ]}

@app.post("/query")
def query(req: QueryRequest):
    kb = find_knowledge(req.query)
    if kb:
        return {
            "answer": kb["answer"],
            "answer_hindi": kb.get("hindi") if req.include_hindi else None,
            "confidence_score": 0.94,
            "citations": kb.get("citations", []),
            "follow_up_questions": [{"question": q} for q in kb.get("followups", [])]
        }
    return {
        "answer": "Thank you for your question. This specific topic is not yet in our database. Please try asking about:<br>• IPC Sections (302, 376, 498A, 420, etc.)<br>• Bail and FIR procedures<br>• Fundamental Rights<br>• Divorce and Maintenance<br>• Consumer and Cyber laws<br><br>Or consult a legal expert for detailed advice.",
        "answer_hindi": "धन्यवाद। यह विषय अभी हमारे डेटाबेस में नहीं है। कृपया IPC धाराएं, जमानत, FIR, मौलिक अधिकार, तलाक, उपभोक्ता कानून के बारे में पूछें।",
        "confidence_score": 0.3,
        "citations": [],
        "follow_up_questions": [
            {"question": "What is Section 302 IPC?"},
            {"question": "How to file FIR?"},
            {"question": "What are fundamental rights?"},
            {"question": "Anticipatory bail process?"}
        ]
    }

# =============================================================================
# DOCUMENT GENERATION
# =============================================================================

class DocumentRequest(BaseModel):
    doc_type: str  # fir, affidavit, legal_notice, rti, bail, complaint, poa
    name: str
    father_name: Optional[str] = ""
    address: str
    details: str
    opposite_party: Optional[str] = ""
    police_station: Optional[str] = ""
    date_of_incident: Optional[str] = ""
    witnesses: Optional[str] = ""

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

<strong>5. Witnesses (if any):</strong><br>
{witnesses}<br><br>

<strong>6. Evidence/Documents:</strong> _______________<br><br>

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

<p><strong>AFFIDAVIT</strong></p>

<p>I, <strong>{name}</strong>, S/o / D/o / W/o <strong>{father_name}</strong>, aged about ____ years, resident of <strong>{address}</strong>, do hereby solemnly affirm and declare as under:</p>

<ol style="line-height: 2;">
<li>That I am the deponent herein and competent to swear this affidavit.</li>
<li>That I am a citizen of India and resident of the above-mentioned address.</li>
<li>{details}</li>
<li>That the contents of this affidavit are true and correct to the best of my knowledge and belief.</li>
<li>That nothing material has been concealed therefrom.</li>
</ol>

<p style="margin-top: 30px;"><strong>VERIFICATION</strong></p>

<p>I, the above-named deponent, do hereby verify that the contents of the above affidavit are true and correct to my knowledge, no part of it is false and nothing material has been concealed therefrom.</p>

<p>Verified at _____________ on this _____ day of _____________, 20____.</p>

<table style="width: 100%; margin-top: 40px;">
<tr>
<td style="width: 50%;"><strong>DEPONENT</strong></td>
<td style="text-align: right;"><strong>Signature</strong></td>
</tr>
<tr>
<td></td>
<td style="text-align: right;">({name})</td>
</tr>
</table>

<p style="margin-top: 40px; border-top: 1px solid #333; padding-top: 10px;">
<strong>NOTARY PUBLIC / OATH COMMISSIONER</strong><br>
(Seal & Signature)
</p>
</div>
""",

    "legal_notice": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">LEGAL NOTICE</h2>
<p style="text-align: center;">(Under Section 80 CPC / As applicable)</p>

<p style="text-align: right;"><strong>Date:</strong> _______________</p>

<p><strong>THROUGH REGISTERED POST A.D.</strong></p>

<p><strong>To,</strong><br>
{opposite_party}<br><br>

<strong>From:</strong><br>
{name}<br>
{address}<br><br>

<strong>Subject:</strong> Legal Notice for {subject}<br><br>

<strong>Sir/Madam,</strong><br><br>

Under instructions from and on behalf of my client <strong>{name}</strong>, S/o / D/o / W/o <strong>{father_name}</strong>, residing at <strong>{address}</strong>, I hereby serve upon you the following Legal Notice:<br><br>

<strong>FACTS:</strong><br>
{details}<br><br>

<strong>DEMAND:</strong><br>
In view of the above facts and circumstances, my client hereby calls upon you to:<br>
1. _______________<br>
2. _______________<br>
3. _______________<br><br>

within <strong>15 days</strong> from the receipt of this notice, failing which my client shall be constrained to initiate appropriate legal proceedings against you at your own risk, cost and consequences.<br><br>

Please note that this notice is without prejudice to all other rights and remedies available to my client under law.<br><br>

<p><strong>Yours faithfully,</strong></p>

<table style="width: 100%; margin-top: 30px;">
<tr>
<td style="width: 50%;"><strong>Advocate for {name}</strong></td>
<td style="text-align: right;"><strong>(Signature)</strong></td>
</tr>
</table>

<p style="margin-top: 30px; font-size: 0.9em; color: #666;">
<strong>Copy to:</strong><br>
1. Client for information<br>
2. Office copy
</p>
</div>
""",

    "rti": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">APPLICATION UNDER RIGHT TO INFORMATION ACT, 2005</h2>

<p style="text-align: right;"><strong>Date:</strong> _______________</p>

<p><strong>To,</strong><br>
The Public Information Officer (PIO),<br>
{opposite_party}<br><br>

<strong>From:</strong><br>
{name}<br>
{address}<br><br>

<strong>Subject:</strong> Application seeking information under RTI Act, 2005<br><br>

<strong>Sir/Madam,</strong><br><br>

I, <strong>{name}</strong>, an Indian citizen, hereby request the following information under the Right to Information Act, 2005:<br><br>

<strong>INFORMATION SOUGHT:</strong><br>
<ol style="line-height: 2;">
{details}
</ol>

<strong>PERIOD:</strong> From _____________ To _____________<br><br>

<strong>MODE OF INFORMATION:</strong><br>
☐ Inspection of documents/records<br>
☐ Certified copies<br>
☐ In electronic format (CD/email)<br><br>

<strong>FEE DETAILS:</strong><br>
Application fee of Rs. 10/- enclosed via _____________ (IPO/DD/Court Fee Stamp) No. _____________ dated _____________<br><br>

<strong>DECLARATION:</strong><br>
I hereby declare that I am a citizen of India and the information sought does not fall within the restrictions contained under Section 8 of the RTI Act, 2005.<br><br>

<table style="width: 100%; margin-top: 30px;">
<tr>
<td style="width: 50%;"><strong>Place:</strong> _______________</td>
<td style="text-align: right;"><strong>Signature</strong></td>
</tr>
<tr>
<td></td>
<td style="text-align: right;">({name})</td>
</tr>
</table>

<p style="margin-top: 20px; font-size: 0.9em;">
<strong>Contact:</strong> _______________<br>
<strong>Email:</strong> _______________
</p>
</div>
""",

    "bail": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">BAIL APPLICATION</h2>
<p style="text-align: center;">(Under Section 437/439 Cr.P.C.)</p>

<p><strong>IN THE COURT OF _______________</strong></p>

<p><strong>BAIL APPLICATION NO. _____/20____</strong></p>

<p><strong>IN THE MATTER OF:</strong></p>

<table style="width: 100%; border: none;">
<tr>
<td style="width: 40%;"><strong>{name}</strong><br>S/o / D/o {father_name}<br>R/o {address}</td>
<td style="width: 20%; text-align: center;">... Applicant/Accused</td>
</tr>
<tr><td colspan="2" style="text-align: center; padding: 10px;"><strong>VERSUS</strong></td></tr>
<tr>
<td><strong>State of _______________</strong><br>Through SHO, {police_station}</td>
<td style="text-align: center;">... Respondent</td>
</tr>
</table>

<p><strong>FIR No.:</strong> _____/20____ &nbsp;&nbsp; <strong>P.S.:</strong> {police_station}</p>
<p><strong>Under Sections:</strong> _______________</p>

<p><strong>APPLICATION FOR GRANT OF REGULAR BAIL</strong></p>

<p><strong>MOST RESPECTFULLY SHOWETH:</strong></p>

<ol style="line-height: 2;">
<li>That the applicant is a permanent resident of the above-mentioned address.</li>
<li>That the applicant has been falsely implicated in the present case.</li>
<li>{details}</li>
<li>That the applicant has no criminal antecedents.</li>
<li>That the applicant is ready to furnish bail bonds and surety as per the satisfaction of this Hon'ble Court.</li>
<li>That the applicant undertakes not to tamper with evidence or influence witnesses.</li>
<li>That the applicant has deep roots in society and there is no likelihood of absconding.</li>
</ol>

<p><strong>PRAYER:</strong></p>
<p>In view of the facts and circumstances stated above, it is most respectfully prayed that this Hon'ble Court may be pleased to:</p>
<ol type="a">
<li>Grant regular bail to the applicant in the above-mentioned case;</li>
<li>Pass any other order deemed fit and proper in the interest of justice.</li>
</ol>

<p style="text-align: right; margin-top: 30px;"><strong>Applicant/Through Counsel</strong></p>

<p style="margin-top: 30px;"><strong>VERIFICATION:</strong></p>
<p>I, {name}, the applicant above named, do hereby verify that the contents of paras 1 to 7 are true and correct to my personal knowledge and belief.</p>
<p>Verified at _____________ on _____________</p>

<p style="text-align: right;"><strong>DEPONENT</strong></p>
</div>
""",

    "complaint_consumer": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">CONSUMER COMPLAINT</h2>
<p style="text-align: center;">(Under Consumer Protection Act, 2019)</p>

<p><strong>BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION</strong><br>
AT _______________</p>

<p><strong>COMPLAINT NO. _____/20____</strong></p>

<p><strong>IN THE MATTER OF:</strong></p>

<table style="width: 100%; border: none;">
<tr>
<td style="width: 60%;"><strong>{name}</strong><br>S/o / D/o / W/o {father_name}<br>R/o {address}</td>
<td>... COMPLAINANT</td>
</tr>
<tr><td colspan="2" style="text-align: center; padding: 10px;"><strong>VERSUS</strong></td></tr>
<tr>
<td><strong>{opposite_party}</strong></td>
<td>... OPPOSITE PARTY</td>
</tr>
</table>

<p><strong>COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019</strong></p>

<p><strong>MOST RESPECTFULLY SHOWETH:</strong></p>

<ol style="line-height: 2;">
<li>That the complainant is a consumer within the meaning of Consumer Protection Act, 2019.</li>
<li>That the opposite party is engaged in the business of _______________.</li>
<li><strong>Facts of the Case:</strong><br>{details}</li>
<li>That the above acts of the opposite party amount to deficiency in service / unfair trade practice / defect in goods.</li>
<li>That the complainant has suffered loss/damage to the extent of Rs. _______________.</li>
<li>That this Hon'ble Commission has territorial and pecuniary jurisdiction to entertain this complaint.</li>
</ol>

<p><strong>PRAYER:</strong></p>
<p>It is, therefore, most respectfully prayed that this Hon'ble Commission may be pleased to:</p>
<ol type="a">
<li>Direct the opposite party to refund Rs. _______________;</li>
<li>Direct the opposite party to pay compensation of Rs. _______________;</li>
<li>Award cost of litigation;</li>
<li>Pass any other order deemed fit in the interest of justice.</li>
</ol>

<table style="width: 100%; margin-top: 30px;">
<tr>
<td style="width: 50%;"><strong>Place:</strong> _______________<br><strong>Date:</strong> _______________</td>
<td style="text-align: right;"><strong>COMPLAINANT</strong><br>({name})</td>
</tr>
</table>

<p style="margin-top: 30px;"><strong>VERIFICATION:</strong></p>
<p>I, {name}, do hereby verify that the contents of the above complaint are true and correct to my knowledge and belief.</p>
</div>
""",

    "poa": """
<div style="font-family: Arial; padding: 20px; max-width: 800px;">
<h2 style="text-align: center; border-bottom: 2px solid #333;">GENERAL POWER OF ATTORNEY</h2>

<p>KNOW ALL MEN BY THESE PRESENTS:</p>

<p>I, <strong>{name}</strong>, S/o / D/o / W/o <strong>{father_name}</strong>, aged about ____ years, residing at <strong>{address}</strong>, hereinafter referred to as the "PRINCIPAL" (which expression shall include his/her heirs, executors, administrators and assigns) of the ONE PART;</p>

<p>DO HEREBY APPOINT AND CONSTITUTE:</p>

<p><strong>{opposite_party}</strong>, residing at _______________, hereinafter referred to as the "ATTORNEY" (which expression shall include his/her heirs, executors, administrators and assigns) of the OTHER PART;</p>

<p>AS my true and lawful Attorney to do and execute all or any of the following acts, deeds and things on my behalf:</p>

<ol style="line-height: 2;">
<li>To appear before any authority, court, tribunal or forum on my behalf.</li>
<li>{details}</li>
<li>To sign, execute and present all applications, documents, papers as may be necessary.</li>
<li>To receive payments and give valid receipts.</li>
<li>To do all other acts as may be necessary for the purposes mentioned above.</li>
</ol>

<p>AND I hereby agree to ratify and confirm all that my said Attorney shall lawfully do or cause to be done by virtue of these presents.</p>

<p><strong>IN WITNESS WHEREOF,</strong> I have hereunto set my hand on this _____ day of _____________, 20____.</p>

<table style="width: 100%; margin-top: 40px;">
<tr>
<td style="width: 50%;"><strong>WITNESSES:</strong><br><br>1. _______________<br><br>2. _______________</td>
<td style="text-align: right;"><strong>PRINCIPAL</strong><br><br>({name})</td>
</tr>
</table>

<p style="margin-top: 40px; text-align: center;"><strong>ACCEPTED</strong></p>
<p style="text-align: center;">I accept the above Power of Attorney.</p>
<p style="text-align: right;"><strong>ATTORNEY</strong><br>({opposite_party})</p>
</div>
"""
}

@app.post("/generate-document")
def generate_document(req: DocumentRequest):
    doc_type = req.doc_type.lower()
    
    if doc_type not in DOCUMENT_TEMPLATES:
        return {
            "success": False,
            "error": "Invalid document type",
            "available_types": list(DOCUMENT_TEMPLATES.keys())
        }
    
    template = DOCUMENT_TEMPLATES[doc_type]
    
    # Extract subject from details (first line or first 50 chars)
    subject = req.details.split('\n')[0][:50] if req.details else "Legal Matter"
    
    # Generate document
    document = template.format(
        name=req.name or "_______________",
        father_name=req.father_name or "_______________",
        address=req.address or "_______________",
        details=req.details or "_______________",
        opposite_party=req.opposite_party or "_______________",
        police_station=req.police_station or "_______________",
        date_of_incident=req.date_of_incident or "_______________",
        witnesses=req.witnesses or "_______________",
        subject=subject
    )
    
    return {
        "success": True,
        "document_type": doc_type,
        "document_html": document,
        "instructions": {
            "fir": "Print this and submit to the concerned Police Station. Keep a copy for yourself.",
            "affidavit": "Get this notarized from a Notary Public or Oath Commissioner.",
            "legal_notice": "Send via Registered Post AD. Keep postal receipt and copy.",
            "rti": "Submit with Rs.10 fee via IPO/DD. Keep acknowledgment.",
            "bail": "File through your lawyer in the appropriate court.",
            "complaint_consumer": "File online at edaakhil.nic.in or submit to Consumer Forum.",
            "poa": "Get this registered at Sub-Registrar office for immovable property matters."
        }.get(doc_type, "Consult a lawyer before using this document.")
    }

@app.get("/document-types")
def get_document_types():
    return {
        "available_documents": [
            {"type": "fir", "name": "FIR (First Information Report)", "description": "Police complaint for cognizable offenses"},
            {"type": "affidavit", "name": "General Affidavit", "description": "Sworn statement for various purposes"},
            {"type": "legal_notice", "name": "Legal Notice", "description": "Formal notice before legal action"},
            {"type": "rti", "name": "RTI Application", "description": "Right to Information request"},
            {"type": "bail", "name": "Bail Application", "description": "Application for bail under CrPC"},
            {"type": "complaint_consumer", "name": "Consumer Complaint", "description": "Complaint under Consumer Protection Act"},
            {"type": "poa", "name": "Power of Attorney", "description": "Authorization to act on behalf"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
