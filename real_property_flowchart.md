# REAL PROPERTY DECISION TREES

*ASCII flowcharts for quick analysis. Follow yes/no branches to conclusion.*

---

## 1. ESTATE IDENTIFICATION FROM GRANTING LANGUAGE

```
Does language convey present possession?
├── YES: Present Estate
│   ├── Is it "for life"? → LIFE ESTATE
│   ├── Does it say "forever" or "heirs"? → FEE SIMPLE ABSOLUTE
│   └── Conditional language present?
│       ├── "So long as" → FEE SIMPLE DETERMINABLE
│       ├── "But if" → FEE SIMPLE SUBJECT TO CONDITION SUBSEQUENT
│       └── "Provided that" + third party → EXECUTORY LIMITATION
└── NO: Future Interest
    ├── Benefits original grantor? → REVERSION
    ├── Benefits third party after life estate? → REMAINDER
    └── Springs on condition? → EXECUTORY INTEREST
```

**Quick Rules:**
- "To A" = present possession
- "Then to B" = future interest
- Automatic termination = determinable/executory
- Manual reentry needed = subject to condition subsequent

---

## 2. DO BURDENS/BENEFITS RUN WITH THE LAND?

```
Is it a covenant/servitude?
├── YES: Check Elements
│   ├── Intent to run? → NO → Doesn't run
│   ├── Notice to successors? → NO → Doesn't run
│   ├── Touches and concerns the land? → NO → Doesn't run
│   └── Privity present?
│       ├── Real covenant? → Vertical privity required
│       └── Equitable servitude? → No privity needed
│       └── Common scheme implied? → Run IRIS test (Intent, Restrictive, Inquiry/record/actual notice, Same scheme)
└── NO: Is it an easement?
    ├── Appurtenant easement? → YES → Runs with dominant estate
    ├── In gross easement? → NO → Doesn't run (personal)
    └── License? → NO → Revocable, doesn't run
```

**IRIS Quick Check for Implied Servitudes:**
- **I**ntent to bind all lots?
- **R**estrictive promise (negative use)?
- **I**nquiry/actual/record notice to successor?
- **S**ame scheme across subdivision?

If all boxes checked → enforce via injunction.

**Quick Rules:**
- Real covenants: Intent + Notice + Touch & Concern + Vertical Privity
- Equitable servitudes: Intent + Notice + Touch & Concern (no privity needed)
- Easements: Appurtenant = runs; In gross = doesn't; License = never

---

## 3. WHO WINS UNDER RECORDING ACTS?

```
Which recording statute applies?
├── RACE statute? → First to record wins
│   └── (No notice inquiry)
├── NOTICE statute? → Bona fide purchaser wins
│   └── (Notice defeats protection)
└── RACE-NOTICE (majority)?
    ├── Bona fide purchaser? → NO → Prior recorded wins
    └── No notice of prior interest? → YES → BFP wins
        └── Recorded timely? → YES → BFP wins
```

**Quick Rules:**
- Race: Record first, win
- Notice: No notice + value + good faith = win
- Race-notice: Record first + no notice = win

---

## 4. EASEMENT CREATION METHODS

```
How was easement created?
├── Written agreement? → EXPRESS EASEMENT
│   └── Specify appurtenant vs in gross
├── Implied from circumstances?
│   ├── Prior use existed? → IMPLIED BY PRIOR USE
│   └── Landlocked without access? → EASEMENT BY NECESSITY
├── Adverse use for statutory period?
│   ├── Hostile + actual + exclusive + continuous? → PRESCRIPTIVE EASEMENT
│   └── Open and notorious? → YES (presumption of hostility)
└── Estoppel?
    ├── Promissory reliance? → ESTOPPEL EASEMENT
    └── (Requires detrimental reliance)
```

**Quick Rules:**
- Express: Must be in writing
- Implied: Strict necessity required
- Prescription: HATE elements (Hostile, Actual, exclusive, continuous)
- Estoppel: Promise + reliance + inequity to deny

---

## 11. COMMON SCHEME SERVITUDE ANALYSIS

```
Was there a common development plan?
├── NO → No implied servitude
└── YES → Continue
    ├── Intent to restrict ALL lots? → NO → No scheme
    └── YES
        ├── Restriction negative (limits use)? → NO → Covenant only
        └── YES
            ├── Successor had notice?
            │   ├── Actual notice? → YES → Enforce servitude
            │   ├── Record notice? → YES → Enforce servitude
            │   └── Inquiry notice (uniform appearance)? → YES → Enforce servitude
            └── NO → Buyer takes free of restriction
```

**Outcome:** If IRIS satisfied → Equitable servitude implied; remedy = injunction.

---

## 5. EASEMENT TERMINATION METHODS

```
Is easement terminated?
├── Merger of title? → YES → TERMINATED BY MERGER
├── Express release? → YES → TERMINATED BY RELEASE
├── Abandonment?
│   ├── Non-use + intent to abandon? → YES → TERMINATED
│   └── Acts inconsistent with easement? → YES → TERMINATED
├── Condemnation? → YES → TERMINATED BY EMINENT DOMAIN
└── Prescription?
    ├── Adverse use by servient owner? → YES → TERMINATED
    └── Statutory period met? → YES → TERMINATED
```

**Quick Rules:**
- Merger: Same person owns both estates
- Release: Written relinquishment
- Abandonment: Non-use + intent to abandon
- Prescription: Adverse use against easement holder

---

## 6. FIXTURE DETERMINATION

```
Is item personal property?
├── YES: Apply FIX test
│   ├── Fastened to land? → NO → REMAINS PERSONAL
│   ├── Intent to permanently improve? → NO → REMAINS PERSONAL
│   └── Removal would damage property? → NO → REMAINS PERSONAL
└── NO: Is it a trade fixture?
    ├── Commercial equipment? → YES → REMAINS PERSONAL
    └── Installed by tenant? → YES → REMOVABLE BY TENANT
```

**Quick Rules:**
- FIX: Fastened + Intent + eXtent of attachment
- Trade fixtures: Business equipment installed by tenant
- Intent controls over attachment method

---

## 7. ADVERSE POSSESSION ELEMENTS

```
Does claimant meet HATE?
├── Hostile (without permission)? → NO → NO TITLE
├── Actual physical possession? → NO → NO TITLE
├── Exclusive (no sharing with owner)? → NO → NO TITLE
└── Continuous for statutory period?
    ├── YES + color of title? → 7 YEARS
    ├── YES + no color of title? → 20 YEARS
    └── Disabilities present? → TOLLED (minority, insanity)
```

**Quick Rules:**
- HATE: Hostile, Actual, exclusive, continuous
- Color of title: Written document claiming ownership
- Tacking: Combine successive possessors' time

---

## 8. CONCURRENT OWNERSHIP TYPE

```
How many unities present?
├── All 4 unities? → JOINT TENANCY
│   ├── Married couple? → TENANCY BY ENTIRETY
│   └── Severance occurred? → NO → SURVIVORSHIP
├── Some unities missing? → TENANCY IN COMMON
└── Equal shares specified? → PRESUMPTION: TENANCY IN COMMON
```

**Quick Rules:**
- 4 Unities: Time, Title, Interest, Possession
- Joint: Right of survivorship
- Common: No survivorship, partition available

---

## 9. MORTGAGE PRIORITY

```
What type of lien?
├── Purchase money mortgage? → HIGHEST PRIORITY
│   └── (Beats all subsequent liens)
├── Construction loan? → SUPER-PRIORITY
│   └── (If recorded + funds used for construction)
└── Later lien?
    ├── Recorded first? → HIGHER PRIORITY
    └── Recorded after? → LOWER PRIORITY
```

**Quick Rules:**
- Purchase money > all juniors
- Construction loans > later liens if properly recorded
- First in time, first in right

---

## 10. TAKINGS ANALYSIS

```
Government action present?
├── Physical invasion? → PHYSICAL TAKING
│   └── → Just compensation required
├── Regulation diminishes value?
│   ├── Substantial diminution? → REGULATORY TAKING
│   ├── Nollan/Dolan factors? → ESSENTIAL NEXUS required
│   └── Rough proportionality? → YES → Valid exaction
└── Temporary taking? → COMPENSATION REQUIRED
```

**Quick Rules:**
- Physical: Always compensation
- Regulatory: Penn Central balancing test
- Exactions: Nollan/Dolan "rough proportionality"
