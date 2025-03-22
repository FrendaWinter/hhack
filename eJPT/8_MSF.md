# Metasploit framework

![Architecture](./Assets/image_10.png)

Modules:
- Exploit: Modules use for exploit target, typically paired with a payload
- Payload: Payload is the code develop by MSF and remotely executed on the target.
- Encoder: Used to encode payload in order to avoid AV detection.
- NOP: Used to ensure that payloads size are consistent, ensure payload is stable
- Auxiliary: Modules for additional functionality like enumeration, scanning

When working with MSF exploit, have 2 type of payload:
- Non-staged payload: Send to target as along with the exploit
- Staged payload: Send to the target in two part:
  - Stager: Part 1, payload use for establish a connections, and download the second part
  - Stage: Part 2, The payload execute on the target.

Meterpreter payload: is advanced multi-functional payload, use to provide attacker useful facilitates to run on target.
    - This payload execute in memory, hard to detect and trace.

MSF modules store:
    - `/usr/share/metaspoit-framework/modules`
    - For custom modules: ~/ms4/modules

## PTES

[Penetration testing execution standard](http://www.pentest-standard.org/index.php/Main_Page)

![Phases](./Assets/image_11.png)

