# ruff: noqa
QUESTIONS = {
    "Environmental": [
        {
            "report_question": "What environmental goals does this document describe?",
            "prompt": """
## What environmental goals does this document describe?
Extract and analyze all environmental goals described in the document, including:

### Emissions and climate:
* Specific greenhouse gas reduction targets with baseline years
* Scope 1, 2, and 3 emissions coverage
* Science-based targets alignment details
* Energy efficiency goals with metrics
* Renewable energy adoption targets

### Resource management:
* Water usage reduction goals with specific metrics
* Waste reduction and recycling targets
* Raw material sourcing commitments
* Circular economy initiatives with measurable outcomes
* Resource efficiency metrics and deadlines

### Biodiversity and ecosystems:
* Land use and restoration targets
* Species protection commitments
* Habitat conservation goals
* Environmental impact reduction metrics
* Ecosystem services preservation plans

### Implementation framework:
* Specific milestone dates
* Investment commitments
* Measurement methodologies
* Verification processes
* Progress tracking mechanisms

Please identify any environmental goals that:
* Lack specific numerical targets
* Have undefined timelines
* Missing baseline measurements
* Need verification methods
* Have unclear scope definitions
""",
        },
        {
            "report_question": "What beneficial environmental claims does the company make?",
            "prompt": """
## What beneficial environmental claims does the company make?
Please identify and analyze all environmental claims made by the company, including:
* Specific quantifiable metrics or targets (e.g., CO2 reduction goals, waste reduction numbers)
* Time periods for these commitments
* Current progress against stated goals
* Third-party verification or certification of claims
* Supporting evidence or methodology used to measure impact

Please note any environmental claims that lack specific metrics or verification. For claims with numerical targets, include baseline years and target completion dates.
        """,
        },
        {
            "report_question": "What potential environment greenwashing can you identify that should be fact checked?",
            "prompt": """
## What potential environment greenwashing can you identify that should be fact checked?
Analyze the company's environmental claims for potential greenwashing indicators by examining:

### Quantitative verification:
* Compare stated environmental metrics against industry standard measurements
* Identify any missing baseline data or calculation methodologies
* Flag claims using non-standard or proprietary measurement methods

### Timeline accuracy:
* Check for vague or distant target dates without interim milestones
* Identify any missed previous environmental commitments
* Compare progress rates against stated goals

### Scope definition:
* Examine whether environmental claims cover all operations or select facilities
* Identify any excluded business units or geographical regions
* Check if supply chain impacts are included in environmental calculations

### Documentation gaps:
List environmental claims lacking third-party verification
Flag any missing emissions scopes (1, 2, or 3) in carbon reporting
Note absence of standardized reporting frameworks (GRI, SASB, TCFD)

Please cite specific examples where claims require additional verification or appear inconsistent with available data.
        """,
        },
        {
            "report_question": "What environmental regulations, standards or certifications can you identify in the document?",
            "prompt": """
## What environmental regulations, standards or certifications can you identify in the document?
Identify and categorize all environmental regulations, standards, and certifications mentioned in the document, including:

### Regulatory compliance:
* Mandatory environmental regulations at local, national, and international levels
* Current compliance status and any noted violations or penalties
* Regulatory bodies providing oversight
* Reporting requirements and submission frequencies

### Voluntary standards:
* Industry-specific environmental standards being followed
* Implementation status and coverage scope
* Expiration or renewal dates of certifications
* Entities responsible for verification

### Certification details:
* Full names and versions of current certifications
* Certification bodies and their accreditation status
* Audit frequency and most recent verification dates
* Geographic or operational scope of certifications
* Any noted gaps in certification coverage

### Performance metrics:
* Specific requirements under each standard/certification
* Current performance against required thresholds
* Any variances or exemptions granted
* Monitoring and reporting protocols in place

Please note any expired certifications, pending renewals, or areas where required certifications appear to be missing.
        """,
        },
    ],
    "Social": [
        {
            "report_question": "What social goals does this document describe?",
            "prompt": """
## What social goals does this document describe?
Analyze all social goals and commitments described in the document, including:

### Workforce initiatives:
* Specific diversity, equity, and inclusion targets with deadlines
* Employee training and development programs with participation metrics
* Worker safety objectives with quantifiable measures
* Labor rights commitments and verification methods
* Compensation and benefits targets

### Community impact:
* Quantified community investment goals
* Specific beneficiary populations with reach metrics
* Local employment or procurement targets
* Community engagement program metrics
* Timeline for community-focused initiatives

### Supply chain responsibility:
* Supplier code of conduct requirements
* Human rights due diligence processes
* Fair labor practice verification methods
* Supplier diversity targets
* Audit frequencies and coverage

### Implementation details:
* Baseline measurements for each goal
* Specific target dates and milestones
* Current progress metrics
* Responsible parties or oversight mechanisms
* Independent verification methods

Please note any social goals lacking specific metrics, timelines, or verification methods.
""",
        },
        {
            "report_question": "What beneficial societal claims does the company make?",
            "prompt": """
## What beneficial societal claims does the company make?
Identify and analyze all societal benefit claims made by the company, including:

### Economic impact claims:
* Job creation numbers with timeframes
* Local economic contribution metrics
* Tax contribution data
* Supply chain economic impacts
* Investment in local infrastructure

### Social value claims:
* Specific beneficiary populations with reach metrics
* Healthcare or education access improvements
* Poverty reduction initiatives with metrics
* Quality of life improvements with measurements
* Technology access or digital inclusion data

### Innovation claims:
* Research and development investments
* Patents or technological advances
* Societal problem solutions
* Access to essential services
* Knowledge transfer initiatives

### Verification elements:
* Independent assessment methods
* Measurement methodologies
* Baseline comparisons
* Progress tracking mechanisms
* Third-party validations

Please note any societal benefit claims that:
* Lack quantifiable metrics
* Have undefined measurement methods
* Missing impact assessments
* Need independent verification
* Make broad generalizations without evidence
""",
        },
        {
            "report_question": "What potential societal social-washing can you identify that should be fact checked?",
            "prompt": """
## What potential societal social-washing can you identify that should be fact checked?
Analyze the company's societal benefit claims for potential social-washing indicators by examining:

### Impact measurement:
* Compare stated social metrics against recognized industry standards
* Identify claims using non-standard measurement methods
* Flag impact numbers without clear calculation methodologies
* Note any missing baseline data
* Check for selective reporting of positive outcomes

### Beneficiary verification:
* Examine how beneficiary numbers are calculated
* Check for double-counting across programs
* Identify undefined or vague beneficiary groups
* Verify claimed reach in target communities
* Review evidence of sustained impact

### Investment claims:
* Compare stated investments against company revenues/profits
* Check for restatements of existing spending
* Identify bundled numbers that inflate impact
* Verify additionality of social investments
* Review actual disbursement of promised funds

### Implementation gaps:
* List claims lacking independent verification
* Note missing stakeholder feedback
* Flag initiatives without clear governance
* Identify discontinued programs still being promoted
* Check for misalignment between claims and actions

Please cite specific examples where:
* Claims appear inconsistent with available data
* Impact measurement needs verification
* Benefits may be overstated
* Evidence is primarily anecdotal
* Long-term outcomes are unclear
""",
        },
        {
            "report_question": "What societal regulations, standards or certifications can you identify in the document?",
            "prompt": """
## What societal regulations, standards or certifications can you identify in the document?
Identify and analyze all societal regulations, standards, and certifications mentioned in the document, including:

### Labor and workplace:
* Employment law compliance status
* Workplace safety certifications
* Equal opportunity compliance
* Labor rights standards
* Working conditions certifications

### Human rights compliance:
* Human rights frameworks adopted
* Modern slavery compliance
* Child labor prevention standards
* Indigenous rights protections
* Conflict minerals certifications

### Social responsibility standards:
* ISO social responsibility certifications
* SA8000 or similar standards
* Fair trade certifications
* Social accountability frameworks
* Community engagement standards

### Verification details:
* Certification validity periods
* Auditing bodies and frequencies
* Scope of certifications
* Geographic coverage
* Non-compliance incidents

For each identified item, note:
* Current compliance status
* Expiration/renewal dates
* Coverage limitations
* Audit findings
* Missing required certifications
* Areas needing verification
""",
        },
    ],
    "Governance": [
        {
            "report_question": "What governance goals does this document describe?",
            "prompt": """
## What governance goals does this document describe?
Analyze all governance goals and commitments described in the document, including:

### Board structure and oversight:
* Board composition targets with deadlines
* Independence requirements
* Diversity objectives with metrics
* Committee structure goals
* Succession planning frameworks

### Risk management:
* Specific risk oversight mechanisms
* Compliance program targets
* Internal control objectives
* Audit frequency requirements
* Incident response protocols

### Ethics and transparency:
* Anti-corruption program metrics
* Whistleblower protection goals
* Disclosure requirements
* Reporting frequency targets
* Stakeholder engagement frameworks

### Implementation details:
* Specific timeline commitments
* Measurement methodologies
* Progress tracking mechanisms
* Accountability structures
* Independent verification processes

For each goal, identify:
* Quantifiable targets
* Baseline measurements
* Implementation deadlines
* Responsible parties
* Verification methods
* Performance indicators

Please note any governance goals that lack:
* Specific metrics
* Clear timelines
* Verification processes
* Accountability measures
* Progress tracking methods
""",
        },
        {
            "report_question": "What beneficial governance claims does the company make?",
            "prompt": """
## What beneficial governance claims does the company make?
Identify and analyze all beneficial governance claims made by the company, including:

### Board effectiveness:
* Board independence metrics
* Diversity statistics and trends
* Meeting attendance rates
* Skills matrix coverage
* Committee performance measures

### Risk and compliance:
* Specific compliance achievement rates
* Risk management effectiveness metrics
* Audit findings and resolutions
* Incident response statistics
* Control effectiveness measures

### Transparency claims:
* Disclosure comprehensiveness metrics
* Reporting framework adherence
* Stakeholder engagement statistics
* Information accessibility measures
* Response times to inquiries

### Verification elements:
* Independent assessment results
* External ratings or rankings
* Peer comparison data
* Industry benchmark positions
* Third-party evaluations

For each claim, note:
* Specific measurement methods
* Comparative industry data
* Historical performance trends
* Supporting evidence
* External validation

Please identify claims that:
* Lack quantitative support
* Need independent verification
* Make broad generalizations
* Omit contextual data
* Use non-standard metrics
""",
        },
        {
            "report_question": "What potential governance greenwashing can you identify that should be fact checked?",
            "prompt": """
## What potential governance greenwashing can you identify that should be fact checked?
Analyze the company's governance claims for potential misrepresentation or overstatement by examining:

### Leadership structure claims:
* Compare stated independence metrics against regulatory definitions
* Verify board diversity statistics methodology
* Check attendance and participation calculations
* Examine executive compensation alignment claims
* Verify voting rights and shareholder power claims

### Oversight effectiveness:
* Analyze risk management performance measures
* Check audit committee independence claims
* Verify reported compliance statistics
* Examine control effectiveness metrics
* Review incident response track records

### Transparency commitments:
* Compare disclosure practices against stated policies
* Verify stakeholder engagement metrics
* Check accessibility of reported information
* Examine completeness of disclosures
* Verify timeliness of reporting

### Implementation verification:
* List governance claims lacking external validation
* Identify selective use of metrics
* Flag inconsistencies between policies and practices
* Note gaps between commitments and actions
* Check for outdated or discontinued practices still being promoted

Please cite specific examples where:
* Claims require additional verification
* Metrics appear inconsistent with industry standards
* Governance structures lack effectiveness measures
* Reporting omits material information
* Current practices contradict stated policies
""",
        },
        {
            "report_question": "What governance regulations, standards or certifications can you identify in the document?",
            "prompt": """
## What governance regulations, standards or certifications can you identify in the document?
Identify and analyze all governance regulations, standards, and certifications mentioned in the document, including:

### Regulatory compliance:
* Stock exchange listing requirements
* Securities regulations adherence
* Corporate governance codes
* Financial reporting standards
* Regulatory filing requirements

### Voluntary standards:
* Corporate governance frameworks adopted
* Industry-specific governance codes
* ESG reporting standards followed
* Ethics and compliance certifications
* Risk management standards

### Certification details:
* Certification validity periods
* Auditing organizations
* Scope of certifications
* Geographic applicability
* Renewal requirements

### Verification elements:
* Assessment methodologies
* Compliance monitoring systems
* Audit frequencies
* Independent verification processes
* Non-compliance reporting

For each requirement, note:
* Current compliance status
* Required reporting frequencies
* Coverage limitations
* Recent audit findings
* Pending regulatory changes
* Areas lacking certification
}
""",
        },
    ],
}
