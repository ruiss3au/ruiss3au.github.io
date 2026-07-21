---
title: "MRSS: Sharing 5G Spectrum with 6G"
description: "How Multi-RAT Spectrum Sharing lets operators put 6G on existing 5G spectrum without stranding their 5G investment, and why the control channel overhead number is the fight."
date: 2026-07-01
tags: ["3GPP", "RAN1", "RAN4", "6G", "Rel-20"]
featured: true
---

The 6G Radio study asks a hard commercial question before it asks any technical
one: how does an operator who has just finished paying for 5G put 6G on the air
without stranding the 5G it already sells? The answer that most of the industry
has rallied around is **MRSS, Multi-RAT Spectrum Sharing**: let a single carrier
carry both 5G New Radio (NR) and 6G radio (6GR) at the same time, with the
scheduler splitting time and frequency resources between the two on a
slot-by-slot basis.

This note tracks what MRSS is, why it is being treated as the primary migration
path, what the alternatives are, where the overhead argument comes from, and who
is on which side. It is a companion to [aNB and Xa: The 6G Base Station](/posts/anb-xa-overview/),
which covers the architecture debate at RAN3. MRSS is the RAN1 and RAN4 half of
the same migration story.

### What MRSS Is

MRSS is Dynamic Spectrum Sharing (DSS) reborn for the 5G-to-6G transition. It is
the direct descendant of LTE-NR DSS, but pointed at NR and 6GR sharing the same
band. The Centre of Excellence in Wireless Technology (CEWiT) framed the core
idea early, at RAN#109: 6G is expected to be deployed "re-using the existing 5G
mid-band (~3.5GHz) and site grid using spectrum refarming and the around 7 GHz
band," and MRSS is "a simple and efficient way of deploying 6G in the current 5G
(3.5GHz) bands"
[RP-252371](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_109/Docs/RP-252371.zip).

The key property, and the reason operators like it, is that MRSS keeps 6G
**standalone**. There is no anchor cell, no master or secondary node, no
inter-node coordination interface. One base station, one carrier, one scheduler
handing resource elements to either a 5G User Equipment (UE) or a 6G UE according
to instantaneous traffic. Ericsson's description is the cleanest: "the scheduler
assigns time/frequency resources to 5G or 6G users on a dynamic basis, based on
the instantaneous traffic situation," and to handle a wide range of 5G-to-6G
traffic ratios "the MRSS solution needs to be dynamic in both time and frequency
domains" [RP-261057](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261057.zip).

That standalone property is what separates MRSS from the aNB/Xa architecture
work. MRSS lives entirely inside one base station at the physical layer. The Xa
interface, dual connectivity, and inter-gNB aggregation live between base
stations. The two debates meet only at the migration question they both try to
answer.

### Why MRSS and Not Something Else

The 5G migration memory is doing a lot of the arguing here. Operators watched
Non-Standalone (NSA) and E-UTRA-NR Dual Connectivity (EN-DC) become a long-lived
crutch because a new core network took years to mature, and they do not want a
repeat. Vodafone made the parallel explicit at RAN#111: many operators still
carry large numbers of EN-DC users precisely because "the operators have
experienced many issues with the uptake of a new core network," and Voice over
IP Multimedia Subsystem (IMS) "also took many years." Their conclusion is to be
cautious about core dependencies and to prefer migration options that avoid them
[RP-260482](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_111/Docs/RP-260482.zip).

MRSS is attractive because it is the option that most cleanly sidesteps that
trap. A shared carrier lets 6G go standalone from day one while reusing the
mid-band the operator already owns. The alternatives all reintroduce some
version of the anchor dependency:

- **Hard spectrum refarming.** Statically carve existing 5G spectrum off for 6G.
  Simple, but it strands 5G users on whatever is left and forfeits the dynamic
  efficiency of sharing. CEWiT frames MRSS as the more efficient alternative,
  where 6G reuses the existing 5G mid-band via spectrum refarming rather than a
  static carve-out
  [RP-252371](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_109/Docs/RP-252371.zip).
- **New-band-only deployment.** Put 6G only in new bands around 7 GHz and leave
  NR untouched in mid-band. Clean, but the around 7 GHz coverage footprint is
  smaller than mid-band, so 6G looks uncompetitive outside dense areas. Vodafone
  notes that to match "low band +3.5 GHz" NR performance, the mid-band Time
  Division Duplex (TDD) likely "needs to support MRSS"
  [RP-260482](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_111/Docs/RP-260482.zip).
- **5G-6G Dual Connectivity (DC).** The explicit fallback. Vodafone warns that
  any absence of good TDD MRSS performance "is likely to encourage companies to
  propose Dual Connectivity of (mid-band) NR with (low band) 6GR master cell"
  [RP-260482](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_111/Docs/RP-260482.zip).
  CEWiT rejects the RAN-level, EN-DC-style flavor of this as "very limiting on
  the Stand-alone operation of 6G" and argues for core-level aggregation instead
  [RP-252371](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_109/Docs/RP-252371.zip).
- **Inter-RAT mobility and inter-gNB aggregation.** Single-stack UEs handing
  over or Time Division Multiplexing (TDM)-switching between 5G and 6G, or
  Carrier Aggregation (CA) and multi-Transmission Reception Point (multi-TRP)
  across gNBs. Samsung raised MRSS together with inter-RAT mobility at RAN4#117
  [R4-2521089](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_117/Docs/R4-2521089.zip).

The through-line: MRSS pays its cost in radio efficiency at the physical layer,
while the DC-flavored alternatives pay in architectural complexity and core
dependency, which is the NSA-to-Standalone (SA) cost operators are trying not to
pay twice.

### Where the Overhead Comes From

The whole MRSS bet hinges on one number: how much spectrum does 6G burn just to
be present on a 5G carrier? If it is small, MRSS wins. If it is large, the
industry drifts back toward Dual Connectivity. This is why RAN#111 tasked RAN1
with an overhead assessment feeding into the RAN#113 checkpoint, and why the
argument is now the hottest thread in the migration debate.

The overhead is not signalling or interface overhead. It is air-interface
overhead: the cost of two systems' always-on transmissions coexisting in one
carrier. Ericsson splits it in two
[RP-261057](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261057.zip):

**Static overhead, the always-on tax.** 6G must broadcast its own Synchronization
Signal Block (SSB) and system information (System Information Block 1, SIB1, and
other SIBs) regardless of how many 6G UEs are attached, on top of the 5G
equivalents. Ericsson computes this as very small, roughly 1 percent, since the
sync and broadcast signals are a light footprint.

**Dynamic overhead, the control channel fight.** This is the contested part, and
it is all about the Physical Downlink Control Channel (PDCCH) and the Physical
Uplink Control Channel (PUCCH). If 5G and 6G use incompatible Control Resource
Set (CORESET), search space, and hashing designs, then 6G needs its own separate
control region, costing on the order of a full Orthogonal Frequency Division
Multiplexing (OFDM) symbol per slot. Ericsson calls that outcome "clearly
undesirable" and argues the opposite: align the Control Channel Element (CCE)
sizes and reuse the 5G hashing function so that "transmitting a 6G PDCCH would be
(almost) identical to transmitting a 5G PDCCH," driving the added overhead close
to zero. The catch Ericsson concedes is that reusing 5G's hashing inherits 5G's
PDCCH blocking behaviour, which may push toward a modified but "sufficiently
compatible" 6G hashing function
[RP-261057](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261057.zip).

Huawei's independent assessment lands in a similar place from a different angle,
measuring NR's own control footprint: PDCCH is about 7.7 percent of downlink and
PUCCH about 13.2 percent of uplink resources, but "with dynamic sharing of
PDCCH and PUCCH resources between NR and 6GR, PDCCH and PUCCH overheads in MRSS
is comparable to NR-only and 6GR-only deployments." Huawei goes further and
argues MRSS can be net positive for the 5G UEs sharing the carrier, using 6G
channel property information to improve NR Channel State Information (CSI),
claiming cell-edge Precoding Matrix Indicator (PMI) gains scaling with load
[RP-261193](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261193.zip).

The operators are less sanguine. The joint operator contribution taken into
RAN1#125 by Vodafone, Orange, and Deutsche Telekom reviewed Qualcomm's control
channel analysis and concluded that, depending on how many OFDM symbols the 5G
CORESET occupies, "more than 20% overhead is expected for 6GR" if control
resources are not shared. Their proposed remedy is a specific tool: two-stage
Downlink Control Information (DCI), where the first stage schedules a second
stage placed to avoid the 5G allocation, letting the 6G control channel "occupy
fewer resources in the 5G control region if the resources configured for this
region are agreed to be shared with 6G"
[R1-2604915](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604915.zip).

So the spread on the table is wide: vendors say 1 to 2 percent with careful
design, operators say north of 20 percent if the control region is not shared.
The number is not yet settled, and the RAN1 template collecting company inputs
before RAN#113 is where it will converge or fracture.

### The Design Levers

Three RAN1 threads exist to drive the overhead down:

**Frame and slot alignment.** T-Mobile, Nokia, and Ericsson argue that reusing
the NR frame structure as the 6G baseline is "important for efficient MRSS,"
because aligned slot and Resource Block (RB) boundaries make the scheduler's job
of interleaving 5G and 6G far cheaper
[R1-2508857](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_123/Docs/R1-2508857.zip).
RAN1#122bis duly agreed that 6GR takes the NR frame structure, 12 subcarriers per
resource block, 10 ms radio frames, and NR symbol durations as the starting
point.

**Two-stage DCI.** The operator-favoured mechanism above, letting 6G control fit
around a shared 5G CORESET rather than demanding its own symbol
[R1-2604915](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604915.zip).

**Shared random access and reference signals.** Ericsson proposes sharing
Physical Random Access Channel (PRACH) time-frequency resources with different
preamble sequences to tell 5G and 6G apart, and configuring 5G Zero-Power
Channel State Information Reference Signal (ZP-CSI-RS) to protect 6G CSI-RS, so
neither the uplink access nor the reference signals cost extra
[RP-261057](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261057.zip).

There is also a waveform sideshow. Cohere Technologies used the MRSS requirement
to argue for its Zak-Orthogonal Time Frequency Space (Zak-OTFS) waveform at
RAN1#122, both clarifying the MRSS requirement for 6G waveforms
[R1-2505627](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505627.zip)
and proposing Zak-OTFS as the vehicle to support it
[R1-2505628](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505628.zip),
while Boost Mobile weighed in on efficient 5G-6G sharing
[R1-2505919](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505919.zip).
The frame-structure agreement, keeping the NR waveform as baseline, has so far
kept these proposals at the margins.

### RAN4: Scope and Coexistence

RAN4 owns the Radio Frequency (RF) and coexistence side, and its debate has been
about scope more than overhead. The peak was RAN4#117, where the feature drew a
broad field. Apple pressed on scope with a discussion paper and a liaison
statement on 6GR MRSS
[R4-2520666](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_117/Docs/R4-2520666.zip),
[R4-2520667](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_117/Docs/R4-2520667.zip),
and later brought the scope question up to the plenary at RAN#110. There Apple
argued two boundaries: that MRSS should cover only 5G-6G sharing and exclude
coexistence with Narrowband IoT (NB-IoT) and enhanced Machine-Type Communication
(eMTC) ("if NB-IoT/eMTC and 6G are deployed in adjacent channels, it is not
MRSS"), and that whether NR Non-Terrestrial Network (NTN) plus 6G Terrestrial
Network (TN) sharing belongs in MRSS at all needs a RAN decision
[RP-253439](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_110/Docs/RP-253439.zip).

The NTN thread was pushed by the satellite camp: ViaSat, Thuraya, and Terrestar
gave views on the NTN aspects of the MRSS study
[R4-2520748](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_117/Docs/R4-2520748.zip).
OPPO [R4-2521452](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_117/Docs/R4-2521452.zip),
ZTE and Sanechips [R4-2521753](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_117/Docs/R4-2521753.zip),
Institute for Information Industry (III) and National Taiwan University (NTU) on
system parameters
[R4-2521891](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_117/Docs/R4-2521891.zip),
and Chunghwa Telecom Laboratories (CHTTL) on scenarios
[R4-2522132](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_117/Docs/R4-2522132.zip)
all contributed initial views. The thread continued at RAN4#118 with Xiaomi,
Apple, OPPO [R4-2601427](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_118/Docs/R4-2601427.zip),
and ZTE [R4-2601850](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_118/Docs/R4-2601850.zip),
and at RAN4#119 with a notable CHTTL contribution on enabling 5G-6G MRSS on
existing NR base station hardware
[R4-2607160](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_119/Docs/R4-2607160.zip),
the hardware-reuse question that decides whether MRSS is a software upgrade or a
forklift.

### The TDD Problem

The one place operators are visibly nervous is TDD. Existing LTE-NR DSS
deployments have mostly been in Frequency Division Duplex (FDD) bands, and
Vodafone points out that "many operators (and perhaps, RAN vendors) have little
or no experience of DSS operation in TDD bands." Since the commercially important
mid-band at 3.5 GHz is TDD, MRSS has to work there, and Vodafone wants both TDD
and FDD MRSS performance evaluated before the migration decision
[RP-260482](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_111/Docs/RP-260482.zip).
This is exactly the gap where, if the answer disappoints, Dual Connectivity comes
back through the door.

### Company Positions

| Position | Companies |
|----------|-----------|
| Overhead is small (1-2%), MRSS viable | Ericsson, Huawei |
| Overhead large (>20%) unless control shared, needs two-stage DCI | Vodafone, Orange, Deutsche Telekom, Bouygues Telecom, Telecom Italia, AT&T, BT |
| Scope discipline: 5G-6G only, exclude NB-IoT/eMTC | Apple |
| NTN sharing should be in scope | ViaSat, Thuraya, Terrestar |
| Frame reuse as MRSS enabler | T-Mobile, Nokia, Ericsson |
| Alternative waveform for MRSS | Cohere Technologies |
| Hardware reuse feasibility | CHTTL |
| Architecture-level migration (CN aggregation) | CEWiT |

### The Bet in One Sentence

MRSS is the industry's attempt to migrate to 6G without repeating NSA-to-SA, by
trading a few percent of physical-layer efficiency for standalone 6G on existing
spectrum. Whether that trade holds depends on one unresolved number, the control
channel overhead in TDD, and the answer is due at RAN#113 in September 2026.

### What to Watch

1. **The overhead number.** RAN1 is collecting company inputs into a template
   before RAN#113. Watch whether the vendor 1-2 percent figure or the operator
   20 percent figure prevails, and whether TDD is evaluated separately.
2. **Two-stage DCI.** Whether the operator-backed control channel mechanism gets
   adopted as the MRSS tool or stays a general 6G feature.
3. **RAN4 scope decisions.** NB-IoT/eMTC exclusion and the NR NTN plus 6G TN
   question both need RAN guidance.
4. **TDD MRSS performance.** The gap most likely to reopen the Dual Connectivity
   debate if the numbers disappoint.
5. **Hardware reuse.** Whether MRSS runs on deployed NR base station hardware or
   demands new radios, which decides its real-world migration cost.
