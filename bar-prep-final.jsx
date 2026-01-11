import React, { useState, useEffect } from 'react';
import { 
    LayoutDashboard, BookOpen, Brain, Target, Settings, Bell, Search, 
    CheckCircle2, AlertCircle, TrendingUp, Calendar, BarChart3, Flame,
    ChevronRight, ChevronDown, Menu, Scale, FileText, Users, Building2,
    Gavel, Shield, Landmark, Briefcase, Heart, Globe, Key, Layers,
    Play, Pause, RefreshCw, X, Eye, Timer, PenTool, ClipboardList,
    CheckSquare, Square, Save, ArrowLeft, GraduationCap
} from 'lucide-react';

export default function BarPrepComplete() {
    const [activeTab, setActiveTab] = useState('dashboard');
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [selectedSubject, setSelectedSubject] = useState(null);
    const [studyMode, setStudyMode] = useState(false);
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    const [showAnswer, setShowAnswer] = useState(false);
    const [sessionStats, setSessionStats] = useState({ reviewed: 0, again: 0, hard: 0, good: 0, easy: 0 });
    const [studyQueue, setStudyQueue] = useState([]);
    const [essayMode, setEssayMode] = useState(false);
    const [activeEssay, setActiveEssay] = useState(null);
    const [essayTimer, setEssayTimer] = useState(1800);
    const [timerRunning, setTimerRunning] = useState(false);
    const [essayResponse, setEssayResponse] = useState('');
    const [rubricScores, setRubricScores] = useState({});
    const [mptMode, setMptMode] = useState(false);
    const [activeMpt, setActiveMpt] = useState(null);
    const [mptTimer, setMptTimer] = useState(5400);
    const [mptTimerRunning, setMptTimerRunning] = useState(false);
    const [mptChecklist, setMptChecklist] = useState({});

    const examDate = new Date('2026-02-24');
    const daysUntilExam = Math.ceil((examDate - new Date()) / 86400000);

    useEffect(() => {
        let interval;
        if (timerRunning && essayTimer > 0) interval = setInterval(() => setEssayTimer(t => t - 1), 1000);
        return () => clearInterval(interval);
    }, [timerRunning, essayTimer]);

    useEffect(() => {
        let interval;
        if (mptTimerRunning && mptTimer > 0) interval = setInterval(() => setMptTimer(t => t - 1), 1000);
        return () => clearInterval(interval);
    }, [mptTimerRunning, mptTimer]);

    const formatTime = (s) => `${Math.floor(s/60)}:${(s%60).toString().padStart(2,'0')}`;

    // Complete Subject Data
    const subjects = {
        'Constitutional Law': {
            icon: Landmark, color: 'bg-blue-500', type: 'MBE', progress: 72, accuracy: 78,
            concepts: [
                { id: 'c1', name: 'Standing', mastery: 78, interval: 5, status: 'learning',
                  question: 'What are the Article III standing requirements?',
                  answer: '**Standing (Lujan)**\n\n1. **Injury in Fact** - Concrete, particularized, actual/imminent\n\n2. **Causation** - Fairly traceable to defendant\n\n3. **Redressability** - Favorable decision would remedy\n\n**Prudential:** No third-party standing, no generalized grievances' },
                { id: 'c2', name: 'Commerce Clause', mastery: 72, interval: 3, status: 'learning',
                  question: 'What can Congress regulate under the Commerce Clause?',
                  answer: '**Commerce Clause (Lopez)**\n\n1. **Channels** - Highways, waterways\n\n2. **Instrumentalities** - Trucks, things in commerce\n\n3. **Substantial Effects**\n   - Economic: Aggregation OK\n   - Non-economic: No aggregation\n\n**Limit:** Cannot compel commerce (NFIB)' },
                { id: 'c3', name: 'Equal Protection', mastery: 82, interval: 7, status: 'mastered',
                  question: 'What are the levels of scrutiny?',
                  answer: '**Equal Protection**\n\n**Strict:** Race, national origin\n- Compelling + narrowly tailored\n\n**Intermediate:** Sex, legitimacy\n- Important + substantially related\n\n**Rational Basis:** Everything else\n- Legitimate + rationally related' },
                { id: 'c4', name: 'First Amendment', mastery: 85, interval: 10, status: 'mastered',
                  question: 'How are speech regulations analyzed?',
                  answer: '**First Amendment**\n\n**Content-Based → Strict Scrutiny**\n\n**Content-Neutral → Intermediate**\n- TPM restrictions OK\n\n**Forums:**\n- Traditional public: highest protection\n- Designated: same while open\n- Nonpublic: reasonable + viewpoint neutral' }
            ],
            essays: [{ id: 'ce1', title: 'Commerce & Federalism', timeLimit: 30,
                prompt: 'Congress enacted: (1) Criminal pollution penalties; (2) State EPA compliance or lose highway funds; (3) State inspections required. Analyze.',
                rubric: [{ category: 'Commerce Power', maxPoints: 30 }, { category: 'Spending Power', maxPoints: 30 }, { category: 'Anti-Commandeering', maxPoints: 25 }, { category: 'Organization', maxPoints: 15 }] }]
        },
        'Contracts': {
            icon: FileText, color: 'bg-green-500', type: 'MBE', progress: 65, accuracy: 74,
            concepts: [
                { id: 'k1', name: 'Offer & Acceptance', mastery: 88, interval: 10, status: 'mastered',
                  question: 'How do acceptance rules differ under CL and UCC?',
                  answer: '**Acceptance**\n\n**Common Law - Mirror Image**\n- Must match exactly\n\n**UCC 2-207**\n- Acceptance valid with different terms\n- Between merchants: additional terms in unless material\n\n**Mailbox Rule:**\n- Acceptance: on dispatch\n- Rejection/Revocation: on receipt' },
                { id: 'k2', name: 'Consideration', mastery: 82, interval: 6, status: 'mastered',
                  question: 'What constitutes consideration?',
                  answer: '**Consideration**\n\n- Bargained-for exchange\n- Legal detriment/benefit\n\n**NOT Consideration:**\n- Past consideration\n- Pre-existing duty\n- Illusory promises\n\n**Substitutes:**\n- Promissory estoppel\n- UCC firm offer' },
                { id: 'k3', name: 'Statute of Frauds', mastery: 72, interval: 3, status: 'learning',
                  question: 'What contracts require a writing?',
                  answer: '**Statute of Frauds - MY LEGS**\n\n**M** - Marriage\n**Y** - Year (cannot perform in 1 year)\n**L** - Land\n**E** - Executor\n**G** - Goods ≥$500\n**S** - Surety\n\n**Exceptions:** Part performance, merchant confirmation, judicial admission' },
                { id: 'k4', name: 'Remedies', mastery: 78, interval: 5, status: 'learning',
                  question: 'What contract remedies are available?',
                  answer: '**Remedies**\n\n**Expectation:** Position if performed\n\n**Reliance:** Pre-contract position\n\n**Restitution:** Restore benefits\n\n**Specific Performance:** Unique goods/land\n\n**Limits:** Foreseeability, certainty, mitigation' }
            ],
            essays: [{ id: 'ke1', title: 'Battle of the Forms', timeLimit: 30,
                prompt: 'Retailer PO for 1,000 widgets. Manufacturer acknowledgment adds arbitration, warranty disclaimer. Both merchants. 900 delivered. Analyze.',
                rubric: [{ category: '2-207 Analysis', maxPoints: 30 }, { category: 'Additional Terms', maxPoints: 25 }, { category: 'Perfect Tender', maxPoints: 25 }, { category: 'Organization', maxPoints: 20 }] }]
        },
        'Criminal Law': {
            icon: Gavel, color: 'bg-red-500', type: 'MBE', progress: 81, accuracy: 82,
            concepts: [
                { id: 'cr1', name: 'Homicide', mastery: 85, interval: 8, status: 'mastered',
                  question: 'Distinguish murder and manslaughter.',
                  answer: '**Homicide**\n\n**Murder 1:** Premeditated + deliberate; Felony murder (BARRK)\n\n**Murder 2:** Intent without premeditation; Depraved heart\n\n**Voluntary Manslaughter:** Heat of passion + adequate provocation\n\n**Involuntary:** Criminal negligence' },
                { id: 'cr2', name: '4th Amendment', mastery: 78, interval: 4, status: 'learning',
                  question: 'When is a warrant required?',
                  answer: '**4th Amendment**\n\n**Katz:** Reasonable expectation of privacy\n\n**Warrant:** PC + magistrate + particularity\n\n**Exceptions - ESCAPE:**\n- Exigent circumstances\n- Search incident to arrest\n- Consent\n- Automobile\n- Plain view\n- Emergency' },
                { id: 'cr3', name: 'Miranda', mastery: 82, interval: 6, status: 'mastered',
                  question: 'When must Miranda warnings be given?',
                  answer: '**Miranda**\n\n**Trigger:** Custody + Interrogation\n\n**Custody:** Not free to leave\n**Interrogation:** Likely to elicit response\n\n**Invocation:**\n- Silence: scrupulously honor\n- Counsel: all questioning stops\n\n**Violation:** Inadmissible in case-in-chief; OK for impeachment' }
            ],
            essays: [{ id: 'cre1', title: '4th Amendment Search', timeLimit: 30,
                prompt: 'Anonymous tip about red jacket drug dealer. Officer approaches Dan, asks to search. Dan shrugs. Cocaine found. Arrest, search backpack (gun), search phone (texts), question without Miranda. Analyze.',
                rubric: [{ category: 'Consent', maxPoints: 25 }, { category: 'SITA', maxPoints: 25 }, { category: 'Riley', maxPoints: 25 }, { category: 'Miranda', maxPoints: 25 }] }]
        },
        'Evidence': {
            icon: Scale, color: 'bg-purple-500', type: 'MBE', progress: 58, accuracy: 71,
            concepts: [
                { id: 'e1', name: 'Hearsay', mastery: 85, interval: 7, status: 'mastered',
                  question: 'What is hearsay?',
                  answer: '**Hearsay (801)**\n\nOut-of-court statement for truth\n\n**NOT Hearsay:**\n- Verbal acts\n- Effect on listener\n- State of mind\n\n**801(d)(2) Admissions:**\n- Own statement\n- Adoptive\n- Agent\n- Co-conspirator' },
                { id: 'e2', name: '803 Exceptions', mastery: 70, interval: 3, status: 'learning',
                  question: 'What are the 803 exceptions?',
                  answer: '**803 Exceptions**\n\n**Present Sense:** During/immediately after\n\n**Excited Utterance:** Startling event + stress\n\n**State of Mind:** Then-existing condition\n\n**Medical:** For diagnosis/treatment\n\n**Business Records:** Regular course + near time\n\n**Public Records**' },
                { id: 'e3', name: 'Confrontation', mastery: 62, interval: 2, status: 'struggling',
                  question: 'When does Crawford bar hearsay?',
                  answer: '**Confrontation (Crawford)**\n\nBars TESTIMONIAL hearsay unless:\n- Unavailable AND\n- Prior cross-examination\n\n**Testimonial:** Police interrogations, affidavits, forensic reports\n\n**Non-testimonial:** Ongoing emergency, casual remarks, business records' }
            ],
            essays: [{ id: 'ee1', title: 'Hearsay & Character', timeLimit: 30,
                prompt: 'Dan assault trial. Prosecution: victim excited statement, police report with admission, prior conviction, reputation for violence, hospital records. Defense: testimony victim started it, victim reputation for aggression. Analyze.',
                rubric: [{ category: 'Excited Utterance', maxPoints: 20 }, { category: 'Party Admission', maxPoints: 20 }, { category: '404(b)/609', maxPoints: 20 }, { category: 'Character', maxPoints: 20 }, { category: 'Organization', maxPoints: 20 }] }]
        },
        'Real Property': {
            icon: Building2, color: 'bg-amber-500', type: 'MBE', progress: 45, accuracy: 68,
            concepts: [
                { id: 'p1', name: 'Estates', mastery: 75, interval: 4, status: 'learning',
                  question: 'What are the present estates?',
                  answer: '**Present Estates**\n\n**Fee Simple Absolute:** Complete ownership\n\n**Fee Simple Defeasible:**\n- Determinable → Possibility of reverter\n- Condition Subsequent → Right of entry\n- Executory Limitation → Executory interest\n\n**Life Estate:** For life; no waste' },
                { id: 'p2', name: 'RAP', mastery: 48, interval: 1, status: 'struggling',
                  question: 'What is the Rule Against Perpetuities?',
                  answer: '**RAP**\n\n"Must vest within 21 years after life in being"\n\n**Applies to:**\n- Contingent remainders\n- Executory interests\n- Class gifts\n\n**Traps:**\n- Fertile octogenarian\n- Unborn widow\n\n**Iowa:** USRAP 90-year wait-and-see' },
                { id: 'p3', name: 'Recording Acts', mastery: 72, interval: 3, status: 'learning',
                  question: 'What are the recording act types?',
                  answer: '**Recording Acts**\n\n**Race:** First to record\n\n**Notice:** BFP without notice wins\n\n**Race-Notice:** BFP who records first (Iowa)\n\n**Notice Types:**\n- Actual\n- Constructive (chain of title)\n- Inquiry (possession)' }
            ],
            essays: [{ id: 'pe1', title: 'Future Interests & RAP', timeLimit: 30,
                prompt: '"To Anna for life, then to children who reach 25." Anna (45) has Beth (20), Carl (18). Later has Dana. Beth and Carl reach 25. Anna dies when Dana is 8. Beth conveys to Purchaser (not recorded), then Investor (recorded, no notice). Race-notice, no RAP reform. Analyze.',
                rubric: [{ category: 'RAP', maxPoints: 30 }, { category: 'Future Interests', maxPoints: 25 }, { category: 'Recording', maxPoints: 30 }, { category: 'Organization', maxPoints: 15 }] }]
        },
        'Torts': {
            icon: Shield, color: 'bg-teal-500', type: 'MBE', progress: 70, accuracy: 79,
            concepts: [
                { id: 't1', name: 'Negligence', mastery: 88, interval: 12, status: 'mastered',
                  question: 'What are the negligence elements?',
                  answer: '**Negligence**\n\n**1. DUTY** - Reasonable care\n\n**2. BREACH** - RPP standard\n\n**3. CAUSATION**\n- Actual: but for\n- Proximate: foreseeable\n\n**4. DAMAGES** - Actual required' },
                { id: 't2', name: 'Strict Liability', mastery: 80, interval: 6, status: 'mastered',
                  question: 'When does strict liability apply?',
                  answer: '**Strict Liability**\n\n**Wild Animals:** Always\n\n**Domestic:** One-bite rule\n\n**Abnormally Dangerous:**\n- High risk\n- Cannot eliminate with care\n- Not common\n\n**Products:** Manufacturing, design, warning defects' },
                { id: 't3', name: 'Defamation', mastery: 68, interval: 2, status: 'learning',
                  question: 'What are defamation elements?',
                  answer: '**Defamation**\n\n- Defamatory statement\n- Of and concerning P\n- Publication\n- Damages\n\n**Libel:** Written (damages presumed)\n**Slander:** Spoken (special damages unless per se)\n\n**Constitutional:**\n- Public figure: actual malice\n- Private: negligence' }
            ],
            essays: [{ id: 'te1', title: 'Negligence & Causation', timeLimit: 30,
                prompt: 'Driver ran red light, hit Pedestrian. Ambulance to hospital. Doctor negligently treated, causing infection. Pedestrian has rare blood condition making infection worse. Analyze liability.',
                rubric: [{ category: 'Driver Breach', maxPoints: 20 }, { category: 'Causation', maxPoints: 30 }, { category: 'Doctor', maxPoints: 25 }, { category: 'Eggshell', maxPoints: 15 }, { category: 'Organization', maxPoints: 10 }] }]
        },
        'Civil Procedure': {
            icon: Users, color: 'bg-indigo-500', type: 'MBE', progress: 52, accuracy: 69,
            concepts: [
                { id: 'cp1', name: 'Personal Jurisdiction', mastery: 78, interval: 5, status: 'learning',
                  question: 'How is personal jurisdiction analyzed?',
                  answer: '**Personal Jurisdiction**\n\n**Traditional:** Presence, domicile, consent\n\n**Specific:**\n- Minimum contacts (purposeful availment)\n- Claim arises from contacts\n- Fair play\n\n**General:** "At home" (domicile, incorporation, PPB)' },
                { id: 'cp2', name: 'SMJ', mastery: 82, interval: 6, status: 'mastered',
                  question: 'What are the bases for federal SMJ?',
                  answer: '**Subject Matter Jurisdiction**\n\n**Federal Question:** Arises under federal law\n\n**Diversity:**\n- Complete diversity\n- Amount >$75,000\n\n**Supplemental:** Same case/controversy\n\n**Removal:** Defendant to federal; 30 days' },
                { id: 'cp3', name: 'Erie', mastery: 52, interval: 1, status: 'struggling',
                  question: 'When does Erie apply?',
                  answer: '**Erie Doctrine**\n\n**Step 1:** Federal directive?\n- FRCP: Apply if valid\n- Statute: Apply if constitutional\n\n**Step 2:** No directive - Twin aims:\n- Forum shopping\n- Inequitable administration\n\n**State:** SOL, burden of proof, choice of law' }
            ],
            essays: [{ id: 'cpe1', title: 'Jurisdiction & Erie', timeLimit: 30,
                prompt: 'P (Iowa) sues D (Nebraska corp, PPB Iowa) for $100k negligence. Iowa 2-year SOL; Nebraska 3-year. Suit filed 2.5 years after. Analyze SMJ, PJ, Erie.',
                rubric: [{ category: 'Diversity', maxPoints: 25 }, { category: 'Personal Jurisdiction', maxPoints: 25 }, { category: 'Erie', maxPoints: 30 }, { category: 'Organization', maxPoints: 20 }] }]
        },
        'Business Associations': {
            icon: Briefcase, color: 'bg-cyan-500', type: 'MEE', progress: 38, accuracy: 65,
            concepts: [
                { id: 'ba1', name: 'Partnership', mastery: 65, interval: 2, status: 'learning',
                  question: 'How is a partnership formed?',
                  answer: '**Partnership**\n\n**Formation:** 2+ persons as co-owners for profit\n- No formalities\n- Profit sharing presumption\n\n**NOT partnerships:**\n- Debt repayment\n- Wages\n- Rent' },
                { id: 'ba2', name: 'Fiduciary Duties', mastery: 58, interval: 1, status: 'struggling',
                  question: 'What fiduciary duties apply?',
                  answer: '**Fiduciary Duties**\n\n**Loyalty:**\n- No self-dealing\n- No competing\n- No usurping opportunities\n\n**Care:**\n- Good faith\n- Reasonable prudence\n\n**BJR:** Good faith, informed, rational purpose' }
            ],
            essays: [{ id: 'bae1', title: 'Partnership Duties', timeLimit: 30,
                prompt: 'A and B partners. A finds opportunity through partnership, pursues personally. Also uses partnership funds for personal expenses. Analyze.',
                rubric: [{ category: 'Duty of Loyalty', maxPoints: 35 }, { category: 'Usurping Opportunity', maxPoints: 30 }, { category: 'Remedies', maxPoints: 20 }, { category: 'Organization', maxPoints: 15 }] }]
        },
        'Trusts & Estates': {
            icon: Key, color: 'bg-rose-500', type: 'MEE', progress: 42, accuracy: 62,
            concepts: [
                { id: 'te1', name: 'Will Formalities', mastery: 70, interval: 3, status: 'learning',
                  question: 'What makes a valid will?',
                  answer: '**Will Formalities**\n\n**Attested:**\n- Writing\n- Signed by testator\n- Two witnesses\n\n**Holographic:**\n- Handwritten\n- Signed\n- No witnesses needed' },
                { id: 'te2', name: 'Trust Creation', mastery: 60, interval: 2, status: 'struggling',
                  question: 'What creates a valid trust?',
                  answer: '**Trust Creation**\n\n- Settlor with capacity\n- Intent to create\n- Trust property (res)\n- Ascertainable beneficiaries\n- Valid purpose\n\n**Default:** Revocable' }
            ],
            essays: [{ id: 'tee1', title: 'Wills & Distribution', timeLimit: 30,
                prompt: 'Will: "all to children equally." 3 children: A (predeceased, 2 kids), B (disclaimed), C (survives). Will signed by testator and one witness; second signed week later. Analyze validity and distribution.',
                rubric: [{ category: 'Formalities', maxPoints: 30 }, { category: 'Predeceased', maxPoints: 25 }, { category: 'Disclaimer', maxPoints: 25 }, { category: 'Organization', maxPoints: 20 }] }]
        },
        'Family Law': {
            icon: Heart, color: 'bg-pink-500', type: 'MEE', progress: 55, accuracy: 71,
            concepts: [
                { id: 'fl1', name: 'Property Division', mastery: 68, interval: 2, status: 'learning',
                  question: 'How is property divided in divorce?',
                  answer: '**Property Division**\n\n**Community:** Equal ownership, 50/50\n\n**Equitable Distribution:** Fair, not necessarily equal\n\n**Separate:** Before marriage, gift, inheritance\n\n**Marital:** During marriage' },
                { id: 'fl2', name: 'Child Custody', mastery: 72, interval: 3, status: 'learning',
                  question: 'What standard applies to custody?',
                  answer: '**Child Custody**\n\n**Best Interests:**\n- Child\'s wishes\n- Parents\' wishes\n- Relationships\n- Adjustment\n- Health\n- Abuse history\n\n**Types:** Legal, physical, joint, sole' }
            ],
            essays: [{ id: 'fle1', title: 'Divorce & Custody', timeLimit: 30,
                prompt: 'H (attorney, $200k) and W (homemaker) divorcing after 15 years. Assets: $500k home, H retirement $300k, W inheritance $100k. Two children 10 and 14. Analyze division, support, custody.',
                rubric: [{ category: 'Classification', maxPoints: 25 }, { category: 'Division', maxPoints: 25 }, { category: 'Support', maxPoints: 25 }, { category: 'Custody', maxPoints: 25 }] }]
        },
        'Conflict of Laws': {
            icon: Globe, color: 'bg-violet-500', type: 'MEE', progress: 28, accuracy: 58,
            concepts: [
                { id: 'col1', name: 'Choice of Law', mastery: 55, interval: 1, status: 'struggling',
                  question: 'What approaches determine applicable law?',
                  answer: '**Choice of Law**\n\n**Traditional:**\n- Torts: place of injury\n- Contracts: place of making\n\n**Modern:**\n- Interest analysis\n- Most significant relationship\n- Better rule' }
            ],
            essays: [{ id: 'cole1', title: 'Choice of Law', timeLimit: 30,
                prompt: 'P (Iowa) injured in Nebraska by D (Kansas corp). Suit in Iowa. Iowa comparative fault; Nebraska contributory negligence. Contract has Kansas choice-of-law. Analyze.',
                rubric: [{ category: 'Approach', maxPoints: 30 }, { category: 'Tort', maxPoints: 30 }, { category: 'Contract Clause', maxPoints: 25 }, { category: 'Organization', maxPoints: 15 }] }]
        },
        'Secured Transactions': {
            icon: Layers, color: 'bg-emerald-500', type: 'MEE', progress: 35, accuracy: 61,
            concepts: [
                { id: 'st1', name: 'Attachment', mastery: 60, interval: 2, status: 'learning',
                  question: 'What is required for attachment?',
                  answer: '**Attachment**\n\n1. Value given\n2. Debtor has rights in collateral\n3. Security agreement (authenticated + description) OR possession\n\n**After-acquired:** Extends to future\n**Future advances:** Covers future loans' },
                { id: 'st2', name: 'Priority', mastery: 52, interval: 1, status: 'struggling',
                  question: 'What are the priority rules?',
                  answer: '**Priority**\n\n**General:** First to file or perfect\n\n**PMSI Priority:**\n- Inventory: file + notify before possession\n- Other: 20 days to perfect\n\n**Buyers:**\n- BIOCOB takes free' }
            ],
            essays: [{ id: 'ste1', title: 'Security Interests', timeLimit: 30,
                prompt: 'Bank loaned $50k secured by "all equipment." Bank filed. Later, Seller sold equipment on PMSI credit, filing 25 days after delivery. Default. Analyze priority.',
                rubric: [{ category: 'Bank Interest', maxPoints: 25 }, { category: 'PMSI', maxPoints: 35 }, { category: '20-Day Rule', maxPoints: 25 }, { category: 'Organization', maxPoints: 15 }] }]
        }
    };

    const mptTasks = [
        { id: 'm1', title: 'Client Letter - Estate', type: 'Client Letter', timeLimit: 90, description: 'Draft letter explaining estate planning options.', skills: ['Plain language', 'Client goals', 'Recommendations', 'Format'] },
        { id: 'm2', title: 'Persuasive Brief - Suppress', type: 'Persuasive Brief', timeLimit: 90, description: 'Draft brief for motion to suppress.', skills: ['Frame issues', 'Synthesize', 'Distinguish', 'Persuade'] },
        { id: 'm3', title: 'Objective Memo - Contract', type: 'Objective Memo', timeLimit: 90, description: 'Analyze contract avoidance.', skills: ['Identify issues', 'Apply facts', 'Conclude', 'Format'] }
    ];

    const getAllConcepts = () => Object.entries(subjects).flatMap(([name, d]) => d.concepts.map(c => ({ ...c, subject: name })));
    const getDue = () => getAllConcepts().filter(c => c.interval <= 2);
    const getStruggling = () => getAllConcepts().filter(c => c.status === 'struggling');
    const getMastered = () => getAllConcepts().filter(c => c.status === 'mastered');
    const getMasteryColor = (m) => m >= 80 ? 'text-green-600' : m >= 65 ? 'text-amber-600' : 'text-red-600';
    const getStatusColor = (s) => s === 'mastered' ? 'bg-green-100 text-green-800' : s === 'learning' ? 'bg-blue-100 text-blue-800' : 'bg-red-100 text-red-800';

    const startStudy = (concepts) => { setStudyQueue(concepts); setCurrentCardIndex(0); setShowAnswer(false); setSessionStats({ reviewed: 0, again: 0, hard: 0, good: 0, easy: 0 }); setStudyMode(true); };
    const handleResponse = (r) => { setSessionStats(p => ({ ...p, reviewed: p.reviewed + 1, [r]: p[r] + 1 })); currentCardIndex < studyQueue.length - 1 ? (setCurrentCardIndex(currentCardIndex + 1), setShowAnswer(false)) : setStudyMode(false); };
    const startEssay = (e) => { setActiveEssay(e); setEssayTimer(e.timeLimit * 60); setTimerRunning(false); setEssayResponse(''); setRubricScores({}); setEssayMode(true); };
    const startMpt = (m) => { setActiveMpt(m); setMptTimer(m.timeLimit * 60); setMptTimerRunning(false); const c = {}; m.skills.forEach(s => c[s] = false); setMptChecklist(c); setMptMode(true); };

    const renderStudyMode = () => {
        const card = studyQueue[currentCardIndex];
        if (!card) return null;
        return (
            <div className="fixed inset-0 bg-slate-900 z-50 flex items-center justify-center p-4">
                <div className="w-full max-w-3xl">
                    <div className="flex justify-between items-center mb-6 text-white">
                        <button onClick={() => setStudyMode(false)} className="p-2 bg-slate-800 rounded-lg"><X size={20} /></button>
                        <div><span className="text-slate-400">{card.subject}</span> • <span>{card.name}</span></div>
                        <span className="text-slate-400">{currentCardIndex + 1}/{studyQueue.length}</span>
                    </div>
                    <div className="bg-white rounded-2xl overflow-hidden">
                        <div className="p-8 border-b"><p className="text-lg">{card.question}</p></div>
                        {showAnswer ? <div className="p-8 bg-slate-50"><pre className="whitespace-pre-wrap font-sans text-sm">{card.answer}</pre></div> : <div className="p-8 text-center"><button onClick={() => setShowAnswer(true)} className="px-8 py-3 bg-purple-600 text-white rounded-xl flex items-center space-x-2 mx-auto"><Eye size={20} /><span>Show Answer</span></button></div>}
                        {showAnswer && <div className="p-6 bg-slate-100 border-t"><p className="text-center text-sm text-slate-500 mb-4">How well did you know this?</p><div className="grid grid-cols-4 gap-3">{['again', 'hard', 'good', 'easy'].map((r, i) => <button key={r} onClick={() => handleResponse(r)} className={`py-4 rounded-xl text-white font-medium ${['bg-red-500', 'bg-orange-500', 'bg-green-500', 'bg-blue-500'][i]}`}>{r.charAt(0).toUpperCase() + r.slice(1)}</button>)}</div></div>}
                    </div>
                </div>
            </div>
        );
    };

    const renderEssayMode = () => {
        if (!activeEssay) return null;
        const total = Object.values(rubricScores).reduce((a, b) => a + b, 0);
        const max = activeEssay.rubric.reduce((a, r) => a + r.maxPoints, 0);
        return (
            <div className="fixed inset-0 bg-white z-50 flex flex-col">
                <div className="h-14 bg-slate-800 text-white flex items-center justify-between px-4">
                    <button onClick={() => setEssayMode(false)} className="p-2 hover:bg-slate-700 rounded-lg"><X size={20} /></button>
                    <span className="font-bold">{activeEssay.title}</span>
                    <div className="flex items-center space-x-3"><div className={`px-4 py-2 rounded-lg font-mono ${essayTimer < 300 ? 'bg-red-600' : 'bg-slate-700'}`}><Timer size={16} className="inline mr-2" />{formatTime(essayTimer)}</div><button onClick={() => setTimerRunning(!timerRunning)} className="p-2 bg-slate-700 rounded-lg">{timerRunning ? <Pause size={20} /> : <Play size={20} />}</button></div>
                </div>
                <div className="flex-1 flex overflow-hidden">
                    <div className="w-1/2 border-r p-6 overflow-auto bg-slate-50"><h3 className="font-bold mb-4">Question</h3><pre className="whitespace-pre-wrap font-sans text-slate-700">{activeEssay.prompt}</pre></div>
                    <div className="w-1/2"><textarea value={essayResponse} onChange={e => setEssayResponse(e.target.value)} className="w-full h-full p-6 resize-none focus:outline-none" placeholder="Begin your IRAC analysis..." /></div>
                </div>
                <div className="h-44 border-t bg-slate-50 p-4 overflow-auto">
                    <div className="flex justify-between mb-3"><h3 className="font-bold">Self-Grading</h3><span className="font-bold">{total}/{max}</span></div>
                    <div className="grid grid-cols-4 gap-3">{activeEssay.rubric.map((r, i) => <div key={i} className="bg-white rounded-lg p-3 border"><p className="text-sm font-semibold mb-2">{r.category}</p><div className="flex items-center space-x-2"><input type="number" min="0" max={r.maxPoints} value={rubricScores[r.category] || 0} onChange={e => setRubricScores({ ...rubricScores, [r.category]: Math.min(r.maxPoints, parseInt(e.target.value) || 0) })} className="w-16 px-2 py-1 border rounded text-center text-sm" /><span className="text-sm text-slate-400">/{r.maxPoints}</span></div></div>)}</div>
                </div>
            </div>
        );
    };

    const renderMptMode = () => {
        if (!activeMpt) return null;
        const done = Object.values(mptChecklist).filter(Boolean).length;
        return (
            <div className="fixed inset-0 bg-white z-50 flex flex-col">
                <div className="h-14 bg-indigo-800 text-white flex items-center justify-between px-4">
                    <button onClick={() => setMptMode(false)} className="p-2 hover:bg-indigo-700 rounded-lg"><X size={20} /></button>
                    <span className="font-bold">{activeMpt.title}</span>
                    <div className="flex items-center space-x-3"><div className={`px-4 py-2 rounded-lg font-mono ${mptTimer < 600 ? 'bg-red-600' : 'bg-indigo-700'}`}><Timer size={16} className="inline mr-2" />{formatTime(mptTimer)}</div><button onClick={() => setMptTimerRunning(!mptTimerRunning)} className="p-2 bg-indigo-700 rounded-lg">{mptTimerRunning ? <Pause size={20} /> : <Play size={20} />}</button></div>
                </div>
                <div className="flex-1 flex overflow-hidden">
                    <div className="w-1/3 border-r p-4 bg-slate-50 overflow-auto"><h3 className="font-bold mb-3">Task</h3><p className="text-sm mb-4">{activeMpt.description}</p><h4 className="font-semibold text-sm mb-2">Skills ({done}/{activeMpt.skills.length})</h4><div className="space-y-2">{activeMpt.skills.map((s, i) => <button key={i} onClick={() => setMptChecklist({ ...mptChecklist, [s]: !mptChecklist[s] })} className={`w-full p-2 rounded-lg border text-left text-sm flex items-center space-x-2 ${mptChecklist[s] ? 'bg-green-100 border-green-300' : 'bg-white'}`}>{mptChecklist[s] ? <CheckSquare size={16} /> : <Square size={16} />}<span>{s}</span></button>)}</div></div>
                    <div className="w-2/3 flex flex-col"><div className="p-4 border-b flex justify-between"><h3 className="font-bold">Your Work</h3><button className="px-3 py-1.5 bg-indigo-100 text-indigo-700 rounded-lg text-sm flex items-center space-x-1"><Save size={14} /><span>Save</span></button></div><textarea className="flex-1 p-6 resize-none focus:outline-none" placeholder="Begin drafting..." /></div>
                </div>
            </div>
        );
    };

    const renderDashboard = () => {
        const due = getDue(), struggling = getStruggling(), mastered = getMastered(), all = getAllConcepts();
        return (
            <div className="space-y-6">
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                    {[{ t: 'Days Until Exam', v: daysUntilExam, i: Calendar, c: 'text-red-600', b: 'bg-red-100' }, { t: 'Concepts Mastered', v: `${mastered.length}/${all.length}`, i: Brain, c: 'text-purple-600', b: 'bg-purple-100' }, { t: 'Due for Review', v: due.length, i: RefreshCw, c: 'text-blue-600', b: 'bg-blue-100' }, { t: 'Study Streak', v: '12 days', i: Flame, c: 'text-orange-600', b: 'bg-orange-100' }].map((s, i) => <div key={i} className="bg-white p-5 rounded-xl shadow-sm border"><div className="flex items-center justify-between"><div><p className="text-xs text-slate-500">{s.t}</p><h3 className="text-2xl font-bold text-slate-800 mt-1">{s.v}</h3></div><div className={`p-2.5 rounded-lg ${s.b}`}><s.i size={22} className={s.c} /></div></div></div>)}
                </div>
                <div className="grid grid-cols-3 gap-4">
                    <button onClick={() => startStudy(due)} className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-4 rounded-xl flex items-center justify-between group"><div className="flex items-center space-x-3"><Brain size={24} /><div className="text-left"><p className="font-bold">Review Cards</p><p className="text-sm opacity-90">{due.length} due</p></div></div><ChevronRight size={20} className="group-hover:translate-x-1 transition-transform" /></button>
                    <button onClick={() => setActiveTab('essays')} className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white p-4 rounded-xl flex items-center justify-between group"><div className="flex items-center space-x-3"><PenTool size={24} /><div className="text-left"><p className="font-bold">Practice MEE</p><p className="text-sm opacity-90">Timed essays</p></div></div><ChevronRight size={20} className="group-hover:translate-x-1 transition-transform" /></button>
                    <button onClick={() => setActiveTab('mpt')} className="bg-gradient-to-r from-indigo-500 to-violet-500 text-white p-4 rounded-xl flex items-center justify-between group"><div className="flex items-center space-x-3"><FileText size={24} /><div className="text-left"><p className="font-bold">Practice MPT</p><p className="text-sm opacity-90">90-min tasks</p></div></div><ChevronRight size={20} className="group-hover:translate-x-1 transition-transform" /></button>
                </div>
                <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white rounded-xl shadow-sm border p-5"><h3 className="font-bold text-slate-800 mb-4">MBE Subjects</h3><div className="space-y-2">{Object.entries(subjects).filter(([_, d]) => d.type === 'MBE').map(([n, d]) => <div key={n} className="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50 cursor-pointer" onClick={() => { setSelectedSubject(n); setActiveTab('subject'); }}><div className="flex items-center space-x-2"><d.icon size={16} className={d.color.replace('bg-', 'text-')} /><span className="text-sm font-medium">{n}</span></div><span className={`text-sm font-bold ${getMasteryColor(d.accuracy)}`}>{d.accuracy}%</span></div>)}
                    </div>
                    <div className="bg-white rounded-xl shadow-sm border p-5"><h3 className="font-bold text-slate-800 mb-4">MEE-Only Subjects</h3><div className="space-y-2">{Object.entries(subjects).filter(([_, d]) => d.type === 'MEE').map(([n, d]) => <div key={n} className="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50 cursor-pointer" onClick={() => { setSelectedSubject(n); setActiveTab('subject'); }}><div className="flex items-center space-x-2"><d.icon size={16} className={d.color.replace('bg-', 'text-')} /><span className="text-sm font-medium">{n}</span></div><span className={`text-sm font-bold ${getMasteryColor(d.accuracy)}`}>{d.accuracy}%</span></div>)}
                    </div>
                </div>
                {struggling.length > 0 && <div className="bg-white rounded-xl shadow-sm border p-5"><div className="flex items-center justify-between mb-4"><h3 className="font-bold text-slate-800">Focus Areas</h3><AlertCircle size={18} className="text-red-500" /></div><div className="grid grid-cols-3 gap-3">{struggling.slice(0, 6).map(c => <div key={c.id} className="p-3 rounded-lg bg-red-50 border border-red-100 cursor-pointer" onClick={() => startStudy([c])}><p className="text-sm font-semibold">{c.name}</p><p className="text-xs text-slate-500">{c.subject}</p><p className={`text-lg font-bold mt-1 ${getMasteryColor(c.mastery)}`}>{c.mastery}%</p></div>)}</div></div>}
            </div>
        );
    };

    const renderSubject = () => {
        if (!selectedSubject || !subjects[selectedSubject]) return null;
        const d = subjects[selectedSubject];
        return (
            <div className="space-y-6">
                <button onClick={() => setActiveTab('dashboard')} className="flex items-center text-slate-600 hover:text-slate-800"><ArrowLeft size={20} className="mr-2" />Back</button>
                <div className="bg-white rounded-xl shadow-sm border p-6"><div className="flex items-center space-x-4 mb-6"><div className={`p-3 rounded-xl ${d.color}`}><d.icon size={28} className="text-white" /></div><div><h2 className="text-2xl font-bold">{selectedSubject}</h2><span className="text-xs px-2 py-1 rounded-full bg-slate-100">{d.type}</span></div></div><div className="grid grid-cols-3 gap-6 text-center"><div><p className="text-3xl font-bold">{d.progress}%</p><p className="text-sm text-slate-500">Progress</p></div><div><p className={`text-3xl font-bold ${getMasteryColor(d.accuracy)}`}>{d.accuracy}%</p><p className="text-sm text-slate-500">Accuracy</p></div><div><p className="text-3xl font-bold">{d.concepts.length}</p><p className="text-sm text-slate-500">Concepts</p></div></div></div>
                <div className="bg-white rounded-xl shadow-sm border p-5"><div className="flex items-center justify-between mb-4"><h3 className="font-bold">Concepts</h3><button onClick={() => startStudy(d.concepts)} className="px-4 py-2 bg-purple-600 text-white rounded-lg text-sm flex items-center space-x-2"><Play size={14} /><span>Study All</span></button></div><div className="space-y-2">{d.concepts.map(c => <div key={c.id} className="p-3 rounded-lg bg-slate-50 border flex items-center justify-between hover:bg-slate-100 cursor-pointer" onClick={() => startStudy([c])}><div><p className="text-sm font-semibold">{c.name}</p><span className={`text-xs px-2 py-0.5 rounded-full ${getStatusColor(c.status)}`}>{c.status}</span></div><div className="text-right"><p className={`text-lg font-bold ${getMasteryColor(c.mastery)}`}>{c.mastery}%</p><p className="text-xs text-slate-400">{c.interval}d</p></div></div>)}
                </div>
                {d.essays?.length > 0 && <div className="bg-white rounded-xl shadow-sm border p-5"><h3 className="font-bold mb-4">Essays</h3><div className="space-y-3">{d.essays.map(e => <div key={e.id} className="p-4 rounded-lg bg-slate-50 border flex items-center justify-between"><div><p className="font-semibold">{e.title}</p><p className="text-xs text-slate-500">{e.timeLimit} min</p></div><button onClick={() => startEssay(e)} className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm flex items-center space-x-1"><Play size={14} /><span>Start</span></button></div>)}
                </div>}
            </div>
        );
    };

    const renderEssays = () => {
        const all = Object.entries(subjects).flatMap(([n, d]) => (d.essays || []).map(e => ({ ...e, subject: n })));
        return (
            <div className="space-y-6">
                <h2 className="text-xl font-bold">MEE Practice Essays</h2>
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-4"><div className="flex items-start space-x-3"><PenTool size={20} className="text-amber-600 mt-0.5" /><div><h3 className="font-semibold text-amber-800">MEE Strategy</h3><p className="text-sm text-amber-700">Use IRAC. 30 min per essay. Issue-spot first.</p></div></div></div>
                <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">{all.map(e => <div key={e.id} className="bg-white rounded-xl shadow-sm border overflow-hidden"><div className="p-5"><div className="flex items-center space-x-2 mb-3"><span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-1 rounded-full">{e.subject}</span><span className="text-xs text-slate-500">{e.timeLimit} min</span></div><h3 className="font-bold">{e.title}</h3></div><div className="px-5 py-3 bg-slate-50 border-t"><button onClick={() => startEssay(e)} className="w-full py-2 bg-emerald-600 text-white rounded-lg text-sm flex items-center justify-center space-x-1"><Play size={14} /><span>Start</span></button></div></div>)}
                </div>
            </div>
        );
    };

    const renderMpt = () => (
        <div className="space-y-6">
            <h2 className="text-xl font-bold">MPT Practice</h2>
            <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-4"><div className="flex items-start space-x-3"><FileText size={20} className="text-indigo-600 mt-0.5" /><div><h3 className="font-semibold text-indigo-800">MPT Strategy</h3><p className="text-sm text-indigo-700">90 min: 15 File, 20 Library, 45 writing, 10 review.</p></div></div></div>
            <div className="grid grid-cols-3 gap-4">{mptTasks.map(m => <div key={m.id} className="bg-white rounded-xl shadow-sm border overflow-hidden"><div className="p-5"><div className="flex items-center space-x-2 mb-3"><span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full">{m.type}</span><span className="text-xs text-slate-500">{m.timeLimit} min</span></div><h3 className="font-bold mb-2">{m.title}</h3><p className="text-sm text-slate-600">{m.description}</p></div><div className="px-5 py-3 bg-slate-50 border-t"><button onClick={() => startMpt(m)} className="w-full py-2 bg-indigo-600 text-white rounded-lg text-sm flex items-center justify-center space-x-1"><Play size={14} /><span>Start</span></button></div></div>)}
            </div>
        </div>
    );

    const renderContent = () => {
        switch (activeTab) {
            case 'dashboard': return renderDashboard();
            case 'subject': return renderSubject();
            case 'essays': return renderEssays();
            case 'mpt': return renderMpt();
            default: return <div className="flex items-center justify-center h-64 text-slate-400"><BookOpen size={48} className="mr-4" /><span>Under construction</span></div>;
        }
    };

    const navItems = [{ id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard }, { id: 'subjects', label: 'Subjects', icon: BookOpen }, { id: 'essays', label: 'MEE Essays', icon: PenTool }, { id: 'mpt', label: 'MPT', icon: FileText }, { id: 'analytics', label: 'Analytics', icon: BarChart3 }];

    return (
        <div className="min-h-screen flex bg-slate-50">
            {studyMode && renderStudyMode()}
            {essayMode && renderEssayMode()}
            {mptMode && renderMptMode()}
            <aside className={`fixed inset-y-0 left-0 z-40 w-56 bg-white border-r transform transition-transform lg:translate-x-0 lg:static ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                <div className="h-full flex flex-col">
                    <div className="h-14 flex items-center px-4 border-b"><div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white mr-2"><Scale size={18} /></div><span className="text-lg font-bold">BarPrep</span></div>
                    <div className="px-3 py-4 border-b"><div className="bg-gradient-to-r from-red-500 to-orange-500 rounded-lg p-3 text-white"><p className="text-xs opacity-90">Iowa Bar Exam</p><p className="text-2xl font-bold">{daysUntilExam} days</p><p className="text-xs opacity-75">February 2026</p></div></div>
                    <nav className="flex-1 py-3 px-2 overflow-auto">{navItems.map(({ id, label, icon: Icon }) => <button key={id} onClick={() => { setActiveTab(id === 'subjects' ? 'dashboard' : id); setSidebarOpen(false); }} className={`w-full flex items-center px-3 py-2 rounded-lg text-sm font-medium mb-1 ${activeTab === id ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50'}`}><Icon size={18} className="mr-2.5" />{label}</button>)}
                    </nav>
                    <div className="p-3 border-t"><div className="bg-orange-50 rounded-lg p-3 flex items-center space-x-2"><Flame size={20} className="text-orange-500" /><div><p className="text-sm font-bold">12 Day Streak!</p><p className="text-xs text-slate-500">Keep going</p></div></div></div>
                    <div className="p-3 border-t"><button className="w-full flex items-center px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50"><Settings size={18} className="mr-2.5" />Settings</button></div>
                </div>
            </aside>
            <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
                <header className="h-14 bg-white border-b flex items-center justify-between px-4">
                    <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 rounded-md text-slate-400 hover:bg-slate-100"><Menu size={20} /></button>
                    <div className="flex-1 flex justify-center lg:justify-start lg:ml-4"><div className="max-w-xs w-full relative"><div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><Search size={16} className="text-slate-400" /></div><input type="text" className="w-full pl-9 pr-3 py-1.5 border rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-blue-500" placeholder="Search..." /></div></div>
                    <div className="flex items-center space-x-3"><button className="p-1.5 rounded-full text-slate-400 hover:text-slate-500 relative"><Bell size={18} /><span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span></button><div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold">B</div></div>
                </header>
                <div className="flex-1 overflow-auto p-4 lg:p-6"><div className="max-w-6xl mx-auto">{renderContent()}</div></div>
            </main>
            {sidebarOpen && <div className="fixed inset-0 bg-slate-800 bg-opacity-50 z-30 lg:hidden" onClick={() => setSidebarOpen(false)} />}
        </div>
    );
}
