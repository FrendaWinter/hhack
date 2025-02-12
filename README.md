<h1>About hacking!</h1>

- [Concept](#concept)
  - [Web security](#web-security)
    - [CVE](#cve)
    - [CWE](#cwe)
    - [OWASP Top 10](#owasp-top-10)
  - [Security Principles](#security-principles)
    - [CIA](#cia)
    - [DAD](#dad)
    - [Models](#models)
      - [Bell-LaPadula Model](#bell-lapadula-model)
      - [Biba Model](#biba-model)
      - [Clark-Wilson Model](#clark-wilson-model)
    - [ISO/IEC 19249](#isoiec-19249)
    - [Zero Trust](#zero-trust)
    - [Trust but verify](#trust-but-verify)
  - [Governance \& Regulation](#governance--regulation)
    - [Information Security Governance](#information-security-governance)
    - [Information Security Regulation](#information-security-regulation)
    - [Key Benefits](#key-benefits)
    - [Information Security Frameworks](#information-security-frameworks)
  - [Governance Risk and Compliance (GRC)](#governance-risk-and-compliance-grc)

# Concept

## Web security

### CVE

- Common Vulnerabilities and Exposures,
- Is a system for identifying and cataloging known security vulnerabilities. Each CVE entry includes a unique ID and a description of the flaw.

### CWE
- CWE (Common Weakness Enumeration) is a categorization system for software and hardware weaknesses that can lead to vulnerabilities. 
- It helps identify the underlying issues that could be exploited, such as buffer overflows or improper input validation.

CWE is like a catalog, and CVE is each entry in the catalog.

### OWASP Top 10
- https://owasp.org/www-project-top-ten/

The OWASP Top 10 is a standard awareness document for developers and web application security. It represents a broad consensus about the most critical security risks to web applications.
- **Just Web Application Security Risks**

10 categories - latest 2021 - new 2025
- [A01:2021 – Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
  - CWE-425: Direct Request ('Forced Browsing')
  - CWE-862: Missing Authorization
- [A02:2021 – Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [A04:2021 – Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/)
- [A05:2021 – Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
- [A06:2021 – Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)
- [A07:2021 – Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [A08:2021 – Software and Data Integrity Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)
- [A09:2021 – Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
- [A10:2021 – Server-Side Request Forgery (SSRF)](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)

## Security Principles

### CIA

- `Confidentiality` ensures that only the intended persons or recipients can access the data.
- `Integrity` aims to ensure that the data cannot be altered; moreover, we can detect any alteration if it occurs.
- `Availability` aims to ensure that the system or service is available when needed.

### DAD 
The opposite of the CIA Triad would be the DAD Triad: Disclosure, Alteration, and Destruction.

- `Disclosure` is the opposite of `Confidentiality`. In other words, disclosure of confidential data would be an attack on confidentiality.
- `Alteration` is the opposite of `Integrity`. For example, the integrity of a cheque is indispensable.
- `Destruction/Denial` is the opposite of `Availability`.

### Models

#### Bell-LaPadula Model

The Bell-LaPadula Model aims to achieve confidentiality by specifying three rules:

- `Simple Security Property`: This property is referred to as “no read up”; it states that a subject at a lower security level cannot read an object at a higher security level. This rule prevents access to sensitive information above the authorized level.
- `Star Security Property`: This property is referred to as “no write down”; it states that a subject at a higher security level cannot write to an object at a lower security level. This rule prevents the disclosure of sensitive information to a subject of lower security level.
- `Discretionary-Security Property`: This property uses an access matrix to allow read and write operations. An example access matrix is shown in the table below and used in conjunction with the first two properties.

| Subjects  | Object A   | Object B  |
| --------- | ---------- | --------- |
| Subject 1 | Write      | No access |
| Subject 2 | Read/Write | Read      |

#### Biba Model

The `Biba Model` aims to achieve integrity by specifying two main rules:

`Simple Integrity Property`: This property is referred to as “no read down”; a higher integrity subject should not read from a lower integrity object.
`Star Integrity Property`: This property is referred to as “no write up”; a lower integrity subject should not write to a higher integrity object.

These two properties can be summarized as “read up, write down.” This rule is in contrast with the Bell-LaPadula Model, and this should not be surprising as one is concerned with confidentiality while the other is with integrity.

Biba Model suffers from various limitations. One example is that it does not handle internal threats (insider threat).

#### Clark-Wilson Model

The Clark-Wilson Model also aims to achieve integrity by using the following concepts:

- `Constrained Data Item (CDI)`: This refers to the data type whose integrity we want to preserve.
- `Unconstrained Data Item (UDI)`: This refers to all data types beyond CDI, such as user and system input.
- `Transformation Procedures (TPs)`: These procedures are programmed operations, such as read and write, and should maintain the integrity of CDIs.
- `Integrity Verification Procedures (IVPs)`: These procedures check and ensure the validity of CDIs.

More models:

- Brewer and Nash model
- Goguen-Meseguer model
- Sutherland model
- Graham-Denning model
- Harrison-Ruzzo-Ullman model

### ISO/IEC 19249

ISO/IEC 19249 lists five architectural principles:

- `Domain Separation`: Every set of related components is grouped as a single entity; components can be applications, data, or other resources. 
  - Each entity will have its own domain and be assigned a common set of security attributes.
- `Layering`: When a system is structured into many abstract levels or layers, it becomes possible to impose security policies at different levels; moreover, it would be feasible to validate the operation.
- `Encapsulation`: In object-oriented programming (OOP), we hide low-level implementations and prevent direct manipulation of the data in an object by providing specific methods for that purpose.
- `Redundancy`: This principle ensures availability and integrity. 
  - If one in two power supply fails, the system continues to function. Or Consider a RAID 5 configuration with three drives: if one drive fails, data remains available using the remaining two drives. 
  - Moreover, if data is improperly changed on one of the disks, it would be detected via the parity, ensuring the data’s integrity.
- `Virtualization`: Virtualization provides sandboxing capabilities that improve security boundaries, secure detonation, and observance of malicious programs.

ISO/IEC 19249 teaches five design principles:

- `Least Privilege`: You should provide the least amount of permissions for someone to carry out their task and nothing more.
- `Attack Surface Minimization`: Every system has vulnerabilities that an attacker might use to compromise a system. Some vulnerabilities are known, while others are yet to be discovered. These vulnerabilities represent risks that we should aim to minimize.
  - For example, in one of the steps to harden a Linux system, we would disable any service we don’t need.
- `Centralized Parameter Validation`: Many threats are due to the system receiving input. Invalid inputs can be used to exploit vulnerabilities in the system. Therefore, parameter validation is a necessary step to ensure the correct system state. 
  - Considering the number of parameters a system handles, the validation of the parameters should be centralized within one library or system.
- `Centralized General Security Services`: As a security principle, we should aim to centralize all security services.
- `Preparing for Error and Exception Handling`: Whenever we build a system, we should take into account that errors and exceptions do and will occur.

### Zero Trust

Never trust, always verify.

### Trust but verify

This principle teaches that we should always verify even when we trust an entity and its behavior.

## Governance & Regulation

- `Governance`: Managing and directing an organization or system to achieve its objectives and ensure compliance with laws, regulations, and standards.
- `Regulation`: A rule or law enforced by a governing body to ensure compliance and protect against harm.
- `Compliance`: The state of adhering to laws, regulations, and standards that apply to an organization or system.

### Information Security Governance

Governance's processes:

- `Strategy`: Developing and implementing a comprehensive information security strategy that aligns with the organization's overall business objectives.
- `Policies and procedures`: Preparing policies and procedures that govern the use and protection of information assets.
- `Risk management`: Conduct risk assessments to identify potential threats to the organization's information assets and implement risk mitigation measures.
- `Performance measurement`: Establishing metrics and key performance indicators (KPIs) to measure the effectiveness of the information security governance program.
- `Compliance`: Ensuring compliance with relevant regulations and industry best practices.

### Information Security Regulation

- Information security regulation refers to legal and regulatory frameworks that govern the use and protection of information assets. 
- Regulations are designed to protect sensitive data from unauthorized access, theft, and misuse. Compliance with regulations is typically mandatory and enforced by government agencies or other regulatory bodies. 
- Examples of information security regulations/standards include 
  - The General Data Protection Regulation (GDPR)
  - Payment Card Industry Data Security Standard (PCI DSS)
  - Personal Information Protection and Electronic Documents Act (PIPEDA), and many more.

### Key Benefits

The following are the benefits of implementing governance and regulation:
- More Robust Security Posture
- Increased Stakeholder Confidence
- Regulatory Compliance
- Better alignment with business objectives
- Informed decision-making
- Competitive advantage

### Information Security Frameworks

The information security framework provides a comprehensive set of documents that outline the organisation's approach to information security and governs how security is implemented, managed, and enforced within the organisation. This mainly includes:

- `Policies`: A formal statement that outlines an organization's goals, principles, and guidelines for achieving specific objectives.
- `Standards`: A document establishing specific requirements or specifications for a particular process, product, or service.
- `Guidelines`: A document that provides recommendations and best practices (non-mandatory) for achieving specific goals or objectives.
- `Procedures`: Set of specific steps for undertaking a particular task or process.
- `Baselines`: A set of minimum security standards or requirements that an organization or system must meet.

Steps used to develop:
- `Identify the scope and purpose`: Determine what the document will cover and why it is needed
- `Research and review`: Research relevant laws, regulations, industry standards, and best practices to ensure your document is comprehensive and up-to-date. Review existing policies, procedures, and other documents to avoid duplicating efforts or contradicting existing guidance.
- `Draft the document`: Develop an outline and start drafting the document, following best practices for writing clear and concise. Ensure the document is specific, actionable, and aligned with the organization's goals and values.
- `Review and approval`: Have the document reviewed by stakeholders, such as subject matter experts, legal and compliance teams, and senior management
- `Implementation and communication`: Communicate the document to all relevant employees and stakeholders, and ensure they understand their roles and responsibilities in implementing it. Develop training and awareness programs to ensure the document is understood and followed.
- `Review and update`: Periodically review and update the document to ensure it remains relevant and practical. Monitor compliance and adjust the document based on feedback and changes in the threat landscape or regulatory environment.

## Governance Risk and Compliance (GRC)
