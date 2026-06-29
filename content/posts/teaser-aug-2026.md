---
title: "Teaser: August 2026 Meetings"
date: 2026-06-22
tags: ["3GPP"]
featured: true
---

RAN1#126 and RAN4#120 are expected in August 2026 (exact dates TBC). These
will be the first meetings after the Rel-20 feature freeze at RAN#112 in
Singapore, which means the psychological shift from "finish the release" to
"start the next one" will be complete. Rel-21 studies begin, and the
unresolved questions that were deferred past Rel-20 will resurface.

## What to Watch

### 6G Radio Waveform (FS_6G_Radio)

RAN1#125 left us with a narrow set: OFDM as baseline, OTFS as the leading
high-mobility optional waveform, and UFMC as a mixed-numerology candidate.
But no formal down-select happened. RAN1#126 is where the evaluation
framework meets the deadline pressure: companies that have been running
simulations against the agreed channel models since RAN1#123 will start
pressing for decisions.

**Watch for**: The first waveform consolidation proposal - likely from OPPO
or Nokia - attempting to collapse the candidate list to OFDM + one optional
waveform. Expect Ericsson to push for OFDM-only as the mandatory baseline
with optional enhancements defined at a higher layer. HiSilicon (Huawei)
has been quiet on waveforms since RAN1#122; if they re-enter with a
proposal, it reshapes the dynamics.

**Companies to track**: OPPO (evaluation leadership, multiple waveform
papers at RAN1#123-125), Nokia (AI-native PHY framing), Ericsson
(pragmatic OFDM baseline), HiSilicon (silent lately, may re-engage).

### AI/ML Air Interface Architecture

This is the unresolved question that survived Rel-20. Nokia's AI-native
vision (AI as the default processing paradigm, classical as fallback) vs
the cautious camp (Ericsson, Qualcomm, Apple: AI as optional UE capability)
was explicitly deferred past RAN#112. OPPO's modular middle path (mandatory
baseline + optional AI layer) is the compromise that kept the specification
moving without resolving the architecture.

**Watch for**: Rel-21 study proposals that frame the architecture question
in new terms. The industry may try to avoid refighting the same battle by
splitting the problem: separate study items for AI channel estimation (closer
to Nokia's position) and AI beam management (closer to the cautious camp's
comfort zone). Case 0 (CSI compression) succeeded because it was scoped
narrowly; expect attempts to replicate that formula.

**Companies to track**: Nokia (will bring a Rel-21 AI-native study proposal),
Ericsson (will counter-propose a UE-capability-framework approach), OPPO
(modular design, likely to emerge as neutral broker), Qualcomm (implementation-
cost arguments for IoT device tiers).

### Spectrum Aggregation and Gothia-cell

OPPO introduced the Single Cell Multi-Carrier concept at RAN1#122 in
Bangalore (July 2025). It was nicknamed the "Gothia-cell" at RAN4#118 in
Gothenburg, and vivo filed a detailed analysis at RAN4#119 in Dalian. The
concept - a cell that aggregates multiple spectrum blocks across non-contiguous
carriers - is a 6G enabler for operators with fragmented spectrum
holdings. It is early-stage, not yet a formal work item, and has no
RAN1 design counterpart beyond RAN1#125 contributions.

**Watch for**: vivo bringing a more detailed framework to RAN4#120,
potentially including evaluation assumptions and simulation parameters.
Ericsson and Nokia have not yet engaged directly; if they bring counter-
proposals, it means the concept is gaining traction. If they stay silent,
it may be too early. The critical test is whether vivo can get it onto the
agenda of a joint RAN1/RAN4 session or a RAN1 liaison statement.

**Companies to track**: vivo (originator, will push forward), Ericsson
(potential alternative framework, focused on carrier aggregation
evolution), Nokia (spectrum aggregation through multi-carrier 6G design).

### 7-24 GHz mmWave Framework (FR2-2 / FR3)

The channel models were defined at RAN1#125. Now the hard part begins:
RAN4#120 will see the first RF requirement proposals for devices operating
in the 7-24 GHz range. Beam sweeping overhead is the dominant bottleneck.
Companies that have been working on FR2 (mmWave, 24-52 GHz) will bring
their experience; companies that have not will struggle to catch up.

**Watch for**: Initial BS and UE RF requirement proposals - transmitter
power, ACLR, EVM, receiver sensitivity - for candidate bands around 7 GHz
and 13-15 GHz. The debate will center on how many antenna elements are
mandatory (steers the beam sweeping overhead) and whether Relaxed 6G
device categories with fewer antennas should be allowed.

**Companies to track**: Ericsson (FR2 deployment experience), Nokia (hardware
platforms across bands), Qualcomm (modem/antenna integration cost),
HiSilicon (massive MIMO at higher frequencies).

### NR NTN and GNSS-Resilient Operation

NR_NTN_Ph3 closed at RAN4#119 with the specification of OCC-based PUSCH
capacity enhancement and HD-FDD RedCap NTN operation. The GNSS-resilience
study (SID approved at RAN#111) has its checkpoint at RAN#113 in September
2026. RAN1#126 will be the last meeting to contribute before that checkpoint.

**Watch for**: Initial access solutions - companies will propose enhancements
to PRACH for operation without GNSS time/frequency synchronization.
THALES (rapporteur) must consolidate these into TR 38.742 before RAN#113.
The shift from transparent to regenerative payload architectures (where the
satellite processes signals on-board rather than bending the pipe) may
surface as a new dimension.

**Companies to track**: THALES (rapporteur, SID leadership), Ericsson
(PUSCH OCC leadership, downlink coverage proposals), HiSilicon (HD-FDD
RedCap NTN, capacity proposals), ESA (space infrastructure perspective),
Amazon/AWS (LEO direct-to-device, n254 channel bandwidth push).

### NR Mobility Phase 5

Apple and Lenovo's work item on LTM SCell activation improvements was
approved at RAN#111. RAN4#120 is the first meeting after approval - expect
the first set of draft CRs defining the test procedures for SCell activation
as part of LTM cell switching. The RAN1 counterpart (RAN1#126) will begin
dynamic L1 measurement configuration via MAC CE selection among pre-
configured RRC configurations.

**Watch for**: The inter-CU case - C-LTM (Conditional LTM) across CU
boundaries - which was FFS in the WID. If companies press for inclusion
at RAN1#126, it signals ambition beyond the initial scope. Apple's
design philosophy (minimize RAN1 impact, reuse Rel-19 LTM framework) will
collide with companies wanting broader enhancements.

**Companies to track**: Apple (rapporteur, design philosophy lead), Lenovo
(co-rapporteur), Ericsson (inter-CU scenarios), Nokia (RAN3 impact
assessment).

### Ambient IoT Phase 2

Huawei's revised WID (Device C with active amplification, Topology 2 with
intermediate UE reader) was approved at RAN#111. RAN1#126 will start the
normative work on the air interface for Devices 2b and C - power control,
collision handling, D2R signal design. RAN4#120 will begin the RF/RRM
requirements for active ambient IoT devices.

**Watch for**: Coexistence with NR and LTE in the same band - the most
contentious RF issue. Devices transmitting at 5 dBm peak power in bands
already occupied by macro cells. The RAN4 debate will mirror the LP-WUS
coexistence fights of Rel-19.

**Companies to track**: Huawei (rapporteur), Xiaomi (evaluation methodology
leadership), Ericsson (coexistence requirements), Qualcomm (device complexity
cost analysis).

### NR Bands, Power Classes, and RedCap Expansion

Nokia's basket WI (NR_Bands_BW_PC_BC_RedCap_R20) consolidates multiple
operator-driven requests: new channel bandwidths, HPUE for FR1, PC2 for
RedCap UEs. Approved at RAN#111, with rapporteurs from Nokia, Ericsson,
and CMCC. RAN4#120 will see the first structured wave of proposals via the
email reflector and Excel template process.

**Watch for**: The PC2 for RedCap debate - applying existing non-RedCap PC2
RF requirements to RedCap UEs on a band-agnostic basis. If companies push
for band-specific exceptions, the "band-agnostic" principle fractures.
Also watch for AWS's separate push for a 16.5 MHz channel bandwidth in n254
for LEO D2D - if it gains co-sponsors at RAN4#120, it could accelerate.

**Companies to track**: Nokia (overall rapporteur), Ericsson (channel
bandwidths rapporteur), CMCC (HPUE rapporteur), AWS (n254 16.5 MHz push),
Anterix (n106 900 MHz), Deutsche Telekom (operator requirements).

### 6G Requirements and Scenarios

TR 38.914 v0.4.1 was polished at RAN#112, effectively closing the 6G
requirements study for Rel-20 purposes. But the document will continue to
evolve through Rel-21 with new deployment scenarios, updated KPIs, and
alignment with ITU-R IMT-2030. The August meetings mark the start of that
new phase.

**Watch for**: New deployment scenarios proposed for Rel-21 - candidates
include smart factory ultra-dense deployments, maritime coverage, and
sub-THz indoor scenarios. The 6G KPI targets (60/30 bit/s/Hz peak
efficiency, 4ms/1ms latency) may be tightened based on evaluation results.

**Companies to track**: CMCC (TR 38.914 rapporteur, service-based RAN
proposal), ZTE (migration architecture, standalone 6G priority), Meta
(XR wearable device types), Xiaomi (ISAC use case selection, migration
options).

## Company Posture Changes to Monitor

**CATT and Spreadtrum** surged to the #4 and #15 positions in combined
RAN1#125 + RAN4#119 contributions. Historically mid-tier contributors,
their volume increase suggests a strategic push into Rel-21. Watch for
them co-sponsoring or leading proposals in bands/carrier aggregation and
RF requirements - areas where they have traditionally followed rather
than led.

**Apple** maintained high volume (101 contributions) but shifted focus from
NR_Mob_Ph5 (where their rapporteur role is established) to RAN4 conformance
test definitions. This is the natural evolution of a work item moving from
design to verification, but it also means Apple's RAN1 presence may diminish
in RAN1#126 as they concentrate on RAN4#120.

**vivo** at 110 contributions is punching above their historical weight,
driven largely by the Gothia-cell/spectrum aggregation push and broader
6G radio contributions. If they maintain this pace into RAN1#126, they are
positioning as a tier-1 6G contributor rather than a follower.

**Ericsson** remains the single largest contributor but their Rel-21
strategy is the open question. Will they pursue AI-native PHY (unlikely,
given their Rel-20 position) or propose an alternative 6G architecture
track? Their RAN1#126 submissions will signal their strategy.

## Bottom Line

RAN1#126 and RAN4#120 are the "what's next" meetings. The Rel-20 freeze at
RAN#112 clears the way for Rel-21 studies, and companies that deferred
ambitious proposals past the freeze (Gothia-cell, AI-native architecture,
sub-THz deployment) will bring them back. The companies that moved early
in Rel-19 (Ericsson on NTN, HiSilicon on MIMO, Nokia on AI/ML) are now
incumbents defending their positions. The companies that moved late
(Spreadtrum, CATT, vivo on spectrum aggregation) are challengers looking
for unoccupied territory. August 2026 is the opening shot of Rel-21.
