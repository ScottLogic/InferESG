# ruff: noqa
QUESTIONS = {
    "Environmental": [
        {
            "report_question": "What environmental goals and claims does this document describe?",
            "prompt": """
## What environmental goals and claims does this document describe
Analyze all environmental goals and beneficial claims described in the document, including:

### Emissions and climate commitments:
* Specific greenhouse gas reduction targets with baseline years and progress
* Scope 1, 2, and 3 emissions coverage and achievements
* Science-based targets alignment and verification
* Energy efficiency goals and current performance
* Renewable energy adoption targets and progress

### Resource management:
* Water usage reduction goals and achievements
* Waste reduction and recycling targets with current status
* Raw material sourcing commitments and implementation
* Circular economy initiatives with measurable outcomes
* Resource efficiency metrics and performance data

### Biodiversity and ecosystems:
* Land use and restoration targets with progress
* Species protection commitments and achievements
* Habitat conservation goals and current status
* Environmental impact reduction metrics and results
* Ecosystem services preservation implementation

### Implementation and verification:
* Specific milestone dates and completion status
* Investment commitments and actual spending
* Measurement methodologies used
* Third-party verification processes
* Progress tracking mechanisms

For each goal and claim, identify:
* Relationship between goals and achieved results
* Supporting evidence and methodology
* Independent verification status
* Areas lacking specific metrics
* Gaps between commitments and implementation
* Timeline accuracy and progress rates

Please note any environmental goals or claims that:
* Lack quantifiable metrics
* Have undefined timelines
* Missing baseline measurements
* Need verification methods
* Have unclear scope definitions
* Show misalignment between goals and achievements
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
            "report_question": "What social goals and claims does this document describe?",
            "prompt": """
## What social goals and claims does this document describe?
Analyze all social goals and societal benefit claims described in the document, including:

### Workforce initiatives:
* Specific diversity, equity, and inclusion targets with progress metrics
* Employee development programs with participation rates and outcomes
* Worker safety objectives and achievement data
* Labor rights commitments and implementation status
* Compensation and benefits targets with current performance

### Community impact:
* Quantified community investment goals and actual spending
* Specific beneficiary populations with reach metrics and validation
* Local employment or procurement targets and achievements
* Economic contribution data with verification
* Infrastructure investment commitments and implementation

### Supply chain responsibility:
* Supplier code of conduct requirements and compliance rates
* Human rights due diligence processes and findings
* Fair labor practice verification results
* Supplier diversity targets and current status
* Audit frequencies and compliance outcomes

### Social value creation:
* Healthcare or education access improvements with metrics
* Poverty reduction initiatives with measured outcomes
* Quality of life improvements with verification data
* Technology access goals and achievement rates
* Knowledge transfer initiatives with impact measures

For each goal and claim, identify:
* Relationship between commitments and achievements
* Measurement methodologies used
* Independent verification status
* Baseline comparisons
* Progress tracking mechanisms
* Implementation timelines and current status

Please note any goals or claims that:
* Lack quantifiable metrics
* Have undefined measurement methods
* Missing impact assessments
* Need independent verification
* Show gaps between goals and achievements
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
            "report_question": "What governance goals and claims does this document describe?",
            "prompt": """
## What governance goals and claims does this document describe?
Analyze all governance goals and beneficial governance claims described in the document, including:

### Board structure and effectiveness:
* Board composition targets and current metrics
* Independence requirements and achievement rates
* Diversity objectives and current statistics
* Committee structure goals and implementation
* Meeting attendance targets and actual rates
* Skills matrix objectives and current coverage

### Risk and compliance management:
* Specific risk oversight mechanisms and performance
* Compliance program targets and achievement rates
* Internal control objectives and effectiveness measures
* Audit frequency requirements and completion rates
* Incident response protocols and implementation results

### Ethics and transparency:
* Anti-corruption program metrics and performance
* Whistleblower protection goals and implementation
* Disclosure requirements and completion rates
* Stakeholder engagement targets and achievement
* Information accessibility measures and results

### Implementation and verification:
* Timeline commitments and completion status
* Measurement methodologies used
* Progress tracking mechanisms
* Accountability structures in place
* Independent assessment results
* External ratings or benchmark positions

For each goal and claim, identify:
* Relationship between commitments and achievements
* Supporting evidence and methodology
* Comparative industry context
* Historical performance trends
* External validation status
* Implementation effectiveness

Please note any goals or claims that:
* Lack specific metrics
* Need independent verification
* Have unclear accountability measures
* Show gaps between policy and practice
* Use non-standard measurements
* Make unsubstantiated comparisons
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
