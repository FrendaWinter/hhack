# hhack
About hacking!

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

- `Domain Separation`: Every set of related components is grouped as a single entity; components can be applications, data, or other resources. Each entity will have its own domain and be assigned a common set of security attributes. For example, consider the x86 processor privilege levels: the operating system kernel can run in ring 0 (the most privileged level). In contrast, user-mode applications can run in ring 3 (the least privileged level). Domain separation is included in the Goguen-Meseguer Model.
- `Layering`: When a system is structured into many abstract levels or layers, it becomes possible to impose security policies at different levels; moreover, it would be feasible to validate the operation. Let’s consider the OSI (Open Systems Interconnection) model with its seven layers in networking. Each layer in the OSI model provides specific services to the layer above it. This layering makes it possible to impose security policies and easily validate that the system is working as intended. Another example from the programming world is disk operations; a programmer usually uses the disk read and write functions provided by the chosen high-level programming language. The programming language hides the low-level system calls and presents them as more user-friendly methods. Layering relates to Defence in Depth.
- `Encapsulation`: In object-oriented programming (OOP), we hide low-level implementations and prevent direct manipulation of the data in an object by providing specific methods for that purpose. For example, if you have a clock object, you would provide a method increment() instead of giving the user direct access to the seconds variable. The aim is to prevent invalid values for your variables. Similarly, in larger systems, you would use (or even design) a proper Application Programming Interface (API) that your application would use to access the database.
- `Redundancy`: This principle ensures availability and integrity. There are many examples related to redundancy. Consider the case of a hardware server with two built-in power supplies: if one power supply fails, the system continues to function. Consider a RAID 5 configuration with three drives: if one drive fails, data remains available using the remaining two drives. Moreover, if data is improperly changed on one of the disks, it would be detected via the parity, ensuring the data’s integrity.
- `Virtualization`: With the advent of cloud services, virtualization has become more common and popular. The concept of virtualization is sharing a single set of hardware among multiple operating systems. Virtualization provides sandboxing capabilities that improve security boundaries, secure detonation, and observance of malicious programs.

ISO/IEC 19249 teaches five design principles:

- `Least Privilege`: You can also phrase it informally as “need-to basis” or “need-to-know basis” as you answer the question, “who can access what?” The principle of least privilege teaches that you should provide the least amount of permissions for someone to carry out their task and nothing more. For example, if a user needs to be able to view a document, you should give them read rights without write rights.
- `Attack Surface Minimisation`: Every system has vulnerabilities that an attacker might use to compromise a system. Some vulnerabilities are known, while others are yet to be discovered. These vulnerabilities represent risks that we should aim to minimize. For example, in one of the steps to harden a Linux system, we would disable any service we don’t need.
- `Centralized Parameter Validation`: Many threats are due to the system receiving input, especially from users. Invalid inputs can be used to exploit vulnerabilities in the system, such as denial of service and remote code execution. Therefore, parameter validation is a necessary step to ensure the correct system state. Considering the number of parameters a system handles, the validation of the parameters should be centralized within one library or system.
- `Centralized General Security Services`: As a security principle, we should aim to centralize all security services. For example, we would create a centralized server for authentication. Of course, you might take proper measures to ensure availability and prevent creating a single point of failure.
- `Preparing for Error and Exception Handling`: Whenever we build a system, we should take into account that errors and exceptions do and will occur. For instance, in a shopping application, a customer might try to place an order for an out-of-stock item. A database might get overloaded and stop responding to a web application. This principle teaches that the systems should be designed to fail safe; for example, if a firewall crashes, it should block all traffic instead of allowing all traffic. Moreover, we should be careful that error messages don’t leak information that we consider confidential, such as dumping memory content that contains information related to other customers.

### Zero Trust

Never trust, always verify.

### Trust but verify

This principle teaches that we should always verify even when we trust an entity and its behaviour.