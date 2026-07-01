---
title: "aNB and Xa: The 6G Base Station"
date: 2026-07-01
tags: ["3GPP", "RAN3", "6G", "Rel-20"]
featured: true
---

RAN3 is building the 6G base station. It named the node **aNB**, the next
letter after eNB (4G) and gNB (5G). The horizontal interface between aNBs
is **Xa**, the next letter after X2 and Xn. The naming was adopted at
RAN3#131 in Gothenburg (February 2026) and codified in TR 38.760-3, the 6G
RAN architecture study. What follows tracks what has been agreed, what is
still open, and who is driving each thread.

## The Naming Convention

```
3G: Node B
4G: eNB (evolved Node B)  — X2 interface
5G: gNB                    — Xn interface
6G: aNB                    — Xa interface
```

## What Has Been Agreed

RAN3#131 (Feb 2026, Gothenburg) adopted the Xa terminology and established
Higher Layer Split (HLS) as the baseline, carrying the Central Unit /
Distributed Unit (CU/DU) separation forward from 5G.

RAN3#131bis (Mar 2026) produced the first substantive working assumption
(WA) driven by Nokia
[R3-261317](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131bis/Docs/R3-261317.zip):

> Working assumption: For connectivity services, the Xa interface is a
> point-to-point interface between the endpoints; a point-to-point logical
> interface should be feasible even in the absence of a physical direct
> connection between the endpoints. For Further Study: new services.

Nokia argued point-to-point (P2P) is the right first choice: it is proven
for latency critical services and avoids the complexity of Service-Based
Architecture (SBA) inside the RAN.
Ericsson, Huawei, LG, InterDigital, Ofinno, China Telecom, Rakuten Mobile,
and CATT all contributed. No company dissented. Xa is P2P.

RAN3#132 (May 2026, Dalian) consolidated. Nokia reaffirmed P2P
[R3-262284](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262284.zip).
Qualcomm entered with a new dimension: what interface type for new services
such as AI/ML data collection?
[R3-262168](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262168.zip).
This is the wedge for allowing non-P2P modes on Xa for AI/ML use cases.

The current baseline captures these general principles for Xa in
TR 38.760-3:

1. Direct interface between peer aNBs
2. P2P for connectivity services
3. Control Plane / User Plane (CP/UP) separation carried forward from 5G
4. RNL/TNL separation (Radio Network Layer and Transport Network Layer independent)
5. Reliable signalling transmission on the control plane
6. All deployment scenarios (HLS, co-located, disaggregated RAN)
7. Extensibility for future enhancements

## P2P vs SBI: The RAN-CN Interface

Xa between aNBs is settled as P2P. The aNB-to-core interface is not.
Agenda 10.3 in RAN3 is a live fight over whether the 6G RAN-CN interface
stays P2P (evolved NGAP, the 5G model) or adopts SBI (service-based
architecture, the 5G core model). The decision shapes whether the aNB is
an evolved gNB or a new architectural entity.

### What P2P means for the aNB

In 5G, the gNB talks to one core entity: the Access and Mobility Management
Function (AMF). Every other interaction (Session Management Function for
sessions, Location Management Function for positioning, Ambient IoT Function
for Ambient IoT) is relayed through it. Adding a new function means revising
the NG Application Protocol (NGAP) and updating every gNB. The positioning
function required new NGAP procedures piggybacked through the AMF. The
Ambient IoT function needed its own bolt-on connection.

P2P advocates (Ericsson, Nokia) argue the model is proven.
Ericsson [R3-260467](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260467.zip):
RNL/TNL separation with an evolved NGAP, where new functions are added as
elementary procedures instead of new interfaces. Qualcomm led a multi-company
P2P evaluation [R3-260063](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260063.zip)
with operators T-Mobile, Verizon, NTT Docomo, Boost, Jio, FiberCop, Charter,
Telstra, and Google co-sponsoring.

CATT's evaluation at RAN3#132 [R3-262126](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262126.zip)
found P2P wins on deployment maturity and latency but loses on extensibility:
"P2P option is leveraged for RAN-CN interface through 2G to 5G. Multiple
deployment scenarios such as many-to-many are supported through additional
elementary procedures defined with each new feature."

### What SBI means for the aNB

SBI turns the aNB into a service producer and consumer on the core's bus.
Instead of routing everything through the AMF, the aNB discovers and talks
directly to AMF, SMF, an AI-training network function (NF), a sensing-fusion
NF, and a policy NF without an intermediary.

Seoul National University [R3-260136](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260136.zip)
argued the necessity: "6G evolves into a multi-service platform supporting
AI/ML, Integrated Sensing and Communication (ISAC), and cloud-native
deployments. These services necessitate RAN interactions with diverse Core
Network Functions beyond traditional AMF anchoring." They continued
[R3-260139](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260139.zip):
"Relying on legacy Control Plane and User Plane architectures introduces
significant intrinsic protocol bottlenecks and procedural latencies."

Deutsche Telekom, with Qualcomm, FiberCop, T-Mobile, Jio, and Tejas Network,
explored architectural directions for SBI [R3-260114](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260114.zip).
The operator push is driven by slicing: if the RAN is an equal peer on the
service bus, operators can orchestrate a slice end-to-end without the AMF as
a single point of RAN integration.

Xiaomi contributed both P2P [R3-260107](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260107.zip)
and SBI [R3-260108](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260108.zip)
analyses in parallel. They describe two SBI architectures: Full SBA
(replace all legacy protocols with SBI, aligned with cloud-native vision but
high migration cost) and Hybrid (retain P2P for latency-critical mobility
while introducing SBI for new capabilities).

### Protocol stacks under evaluation

For P2P, three options are captured in TR 38.760-3:

| Option | Transport | Source |
|--------|-----------|--------|
| 1 | SCTP (Stream Control Transmission Protocol, 5G legacy) | InterDigital [R3-260067](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260067.zip) |
| 2 | QUIC-based | Qualcomm/InterDigital |
| 3 | HTTP/3-based | (new at RAN3#131) |

For SBI, two options:

| Option | Stack | Source |
|--------|-------|--------|
| 1 | TCP + HTTP/2 | (traditional) |
| 2 | QUIC + HTTP/3 | InterDigital [R3-260066](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260066.zip) |

CATT's evaluation at RAN3#132 [R3-262125](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262125.zip)
analyzes the two SBI variants for connectivity services. TCP/HTTP2 carries
session state per connection. QUIC/HTTP3 decouples streams from connections,
which matters when a single aNB needs concurrent sessions with multiple core
functions during a failover.

### The strategic fault line

The debate is not primarily technical. Both can carry control-plane
messages. The question is who controls the architecture:

- P2P camp (Ericsson, Nokia): preserve the clean RAN/CN boundary with a thin,
  stable interface. The aNB is an evolution of the gNB. Adding new services
  means new procedures on the proven interface.

- SBI camp (CMCC, Deutsche Telekom, Seoul National, Qualcomm operators): the
  5G AMF-centric architecture was designed before AI/ML and sensing were
  first-class 6G workloads. Routing everything through one CN anchor creates
  a bottleneck for data that is neither pure user plane nor pure control
  plane. The aNB must be an equal peer on the core service bus.

- Hybrid (OPPO, Xiaomi, CATT): P2P for connectivity and mobility
  (latency-critical, well-understood), SBI for AI/ML, sensing, and new
  services. OPPO [R3-260090](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131/Docs/R3-260090.zip):
  "During the migration of core network from 4G to 5G, one of the important
  evolutions was to transit to service-based architecture. Now, in 6G,
  whether to extend SBA to RAN-CN interface or not needs to be further
  studied."

### Evaluation timeline

RAN3 agreed at #131bis that the evaluation should be a single table comparing
P2P and SBI on deployment, migration, latency, scalability, security, and new
services [CATT R3-262126](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262126.zip).
Results feed into the milestone at RAN#113 (September 2026).

## Key Documents

| TDoc | Title | Company | Meeting |
|------|-------|---------|---------|
| [R3-261317](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131bis/Docs/R3-261317.zip) | Baseline Agreements for Xa Interface | Nokia | #131bis |
| [R3-261285](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131bis/Docs/R3-261285.zip) | Considerations on Xa interface between aNBs | Tejas Network | #131bis |
| [R3-261374](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131bis/Docs/R3-261374.zip) | About Xa interface | Ericsson | #131bis |
| [R3-262168](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262168.zip) | Aspects of 6G Xa interface | Qualcomm | #132 |
| [R3-262284](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262284.zip) | Baseline Agreements for Xa Interface | Nokia | #132 |
| [R3-262347](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262347.zip) | Xa interface between aNBs for connectivity | Tejas Network | #132 |
| [R3-261202](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131bis/Docs/R3-261202.zip) | Further discussion on Xa interface | Huawei | #131bis |
| [R3-262401](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_132/Docs/R3-262401.zip) | Discussions on 6G Xa interface principles | LG | #132 |

## What to Watch at RAN3#133 (Aug 2026, Maastricht)

1. New services interface decision. Qualcomm will press to resolve the
   "For Further Study: new services" status on Xa with a proposal for AI/ML
   data collection.

2. Xa protocol stack selection. The P2P transport layer choice between SCTP,
   QUIC, and HTTP/3.

3. RAN-CN interface evaluation results. The comparison table (P2P vs SBI on
   deployment, migration, latency, scalability, security, new services) may
   reach a working assumption ahead of the RAN#113 checkpoint.

4. Hybrid model traction. Whether OPPO/Xiaomi/CATT's proposal (P2P for
   mobility, SBI for AI/sensing) gains broad support.

5. aNB functional split. HLS is assumed baseline. The question is whether
   anyone proposes a new split point beyond Option 2 from 5G.
