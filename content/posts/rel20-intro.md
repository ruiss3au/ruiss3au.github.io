---
title: "Tracking and Understanding 3GPP RAN1 and RAN4 Meetings"
date: 2026-06-05
tags: ["3GPP"]
---
Mobile communications is one of my main areas of interest. 3GPP has established as the main standardization body for mobile communications and that is where the latest 5G standards have been defined.
The work on the 5G Advanced releases are wrapping up and 3GPP is preparing to start the 6G work. I would like to watch closely the standardization work of this new system, especially what happens in the radio access network. But before that, I have to understand what has happened in the previous releases.
To this end, I am starting a blog post series on the RAN1 and RAN4 work on 3GPP Release 20. I will highlight the main points discussed in the most important
work items in each meeting where Rel-20 was discussed. I hope that such a series is a good way to start the work in this blog.

In this first post, I would like to begin with a quick summary of what happened in Rel. 19 and what was expected to be done in Rel. 20. I would also like to be clear about the methodology I am using to document this. I have basically built a knowledge base of 3GPP tdocs and I interact with it through LLMs. So beware that the analysis here might contain plain mistakes.

## Table of Contents

- [The Transition From Rel-19 to Rel-20](#the-transition-from-rel-19-to-rel-20)
  - [MIMO Phase 5](#mimo-phase-5-nr_mimo_ph5-core)
  - [Duplex Evolution (SBFD)](#duplex-evolution-nr_duplex_evo-core)
  - [AI/ML for Air Interface](#aiml-for-air-interface-nr_aiml_air-core)
  - [Network Energy Savings](#network-energy-savings-netw_energy_nr_enh-core)
  - [Low-Power Wake-Up Signal](#low-power-wake-up-signal-nr_lpwus-core)
  - [NTN Phase 3](#ntn-phase-3-nr_ntn_ph3-core)
  - [Integrated Sensing and Communication](#integrated-sensing-and-communication-fs_sensing_nr)
  - [Ambient IoT](#ambient-iot-fs_ambient_iot_solutions-ambient_iot_solutions-core)
  - [EN-DC RF Phase 4](#en-dc-rf-phase-4-nr_endc_rf_ph4-core)
  - [Carrier Aggregation and SUL](#carrier-aggregation-and-supplementary-uplink-nr_cadc_sul_r19-core)
  - [IoT over NTN](#iot-over-ntn-iot_ntn_ph3-core)
  - [NR Mobility Phase 4](#nr-mobility-phase-4-nr_mob_ph4-core)
  - [XR Phase 3](#xr-phase-3-nr_xr_ph3-core)
  - [RRM Phase 5](#rrm-phase-5-nr_rrm_ph5-core)
  - [Low-Band CA via Switching](#low-band-carrier-aggregation-via-switching-nr_lbca_sw-core)
- [What Changed in Rel-20](#what-changed-in-rel-20)
- [Release 20 Status](#release-20-status)
- [What This Blog Series Covers](#what-this-blog-series-covers)

# The Transition From Rel-19 to Rel-20

Rel-19 was a refinement cycle for 5G-Advanced (Rel-18). RAN1 and RAN4 delivered
major enhancements across the radio stack. Key achievements in the most active work/study items are summarized in the following sections.

### MIMO Phase 5 (NR_MIMO_Ph5-Core)

MIMO has evolved through multiple 3GPP releases. Rel-15 established the NR
MIMO baseline: up to 32 antenna ports, Type I and Type II codebooks, and basic
beam management. Rel-16 (eMIMO) added multi-TRP transmission for reliability
and introduced low-overhead CSI reporting. Rel-17 (FeMIMO) tackled multi-beam
operation at FR2 with unified TCI framework, enabling beam indication across
multiple channels from a single control message. Rel-18 (MIMO evolution DL/UL)
scaled massive MIMO to 64T64R configurations, enhanced SRS-based beam
management for high-mobility scenarios, and introduced AI/ML-based CSI
prediction studies.

Rel-19 MIMO Phase 5 addressed the remaining challenges that earlier phases left
open: coherent joint transmission from multiple TRPs where Rel-16/17 only
supported non-coherent schemes, 32-port CSI-RS codebooks for FR1 massive MIMO
deployments exceeding the previous 16-port limit, unified TCI framework
extensions for seamless beam switching across component carriers [R1-2400105,
R1-2400728], and CSI enhancements for high Doppler scenarios up to 500 km/h. The central technical
challenge was inter-site phase coherence across non-colocated TRPs, which
requires tight fronthaul synchronization. Ericsson and Nokia pushed for
practical implementations using Xn-based coordination rather than ideal
fronthaul, arguing that sub-microsecond synchronization between sites was not
deployable at scale and that inter-site phase noise would degrade coherent
combining gain to negligible levels. Samsung and Qualcomm advocated for more
aggressive multi-panel UE designs and ideal-fronthaul CJT, pointing to
laboratory demonstrations showing 30-40% throughput gain with phase-coherent
multi-TRP [R1-2401437, R1-2400753, R1-2400957]. The fight was a proxy for a broader industry split: operators and
infrastructure vendors (Ericsson, Nokia) prioritized deployability over
theoretical gains, while chipset and device vendors (Samsung, Qualcomm) pushed
the envelope on what UEs could support. Huawei and HiSilicon contributed mostly
to multi-TRP CSI framework and codebook extensions, staying neutral on the
fronthaul debate while ensuring their massive MIMO portfolio would benefit
from any outcome. The specification landed as a compromise: Xn-based non-coherent
JT as baseline with optional extensions for ideal-fronthaul deployments.

### Duplex Evolution (NR_duplex_evo-Core)

Sub-band full duplex (SBFD) became the flagship Rel-19 feature. The motivation
was clear: TDD spectrum is underutilized because operators cannot transmit and
receive simultaneously. SBFD allows a gNB to transmit on one sub-band while
receiving on another within the same TDD carrier, doubling spectral efficiency
in principle without requiring paired FDD spectrum.

The challenges were substantial. Cross-link interference (CLI) between gNBs
sharing adjacent sub-bands, and self-interference at the gNB between its own
transmitter and receiver, had to be measured, reported, and mitigated. New slot
formats were needed where the gNB transmits DL and receives UL on different
frequency resources simultaneously. UE complexity increases because UEs must
handle new scheduling constraints: a UE can be scheduled for DL on one sub-band
while its neighbor is scheduled for UL on an adjacent sub-band, creating
adjacent-channel interference that existing receiver filters cannot handle.

Ericsson and Nokia led the RAN1 specification of SBFD slot formats and resource
allocation. Huawei and HiSilicon drove the CLI measurement framework and
self-interference cancellation requirements. Qualcomm pushed for dynamic
TDD/SBFD switching to allow operators to toggle between modes based on traffic.
Samsung contributed to UE RF requirements for SBFD-aware adjacent channel
selectivity.

The most striking shift was Ericsson and Nokia's position. During the Rel-18
study phase and early Rel-19 scoping, both companies were vocal critics of
SBFD, particularly on base station radio aspects. Their argument: self-
interference cancellation at gNB transmit power levels (up to 200 W per
antenna port) was not practically achievable with the ACLR and EVM
requirements needed for NR, and dynamic TDD with fast slot adaptation already
captured most of the duplexing gain without requiring new hardware. Huawei and
CMCC, supported by Chinese operators with large TDD deployments, pushed the
study item through [R4-2409177, R4-2409178].

Once SBFD became a formal work item, Ericsson and Nokia pivoted from opposition
to specification leadership. Rather than letting competitors define the
requirements unilaterally, they drove the BS RF conformance framework:
in-channel blocking requirements for SBFD (TS 38.104), OTA spatial emission
limits, ACLR and EVM targets for simultaneous DL/UL transmission, and BS
receiver sensitivity under self-interference [R4-2507728, R4-2507639]. The
pattern is classic 3GPP:
you lose the vote on whether to study something, you lead the specification to
ensure it is practical and deployable. The result is that SBFD requirements
now reflect European operator constraints on hardware feasibility rather than
the more aggressive Chinese proposals that initially defined the work item.

### AI/ML for Air Interface (NR_AIML_air-Core)

AI/ML entered the 3GPP physical layer specification for the first time in
Rel-19. The motivation: classical signal processing algorithms for CSI
compression, beam management, and positioning hit diminishing returns as MIMO
array sizes grew and deployment scenarios became more complex. AI/ML offers
the promise of learning optimal parameterizations from deployment data rather
than hand-crafting them.

Three use cases were prioritized [R1-2400165, R1-2400795, R1-2400171, R1-2400166]. CSI compression with autoencoders, using
neural networks to encode the channel state at the UE and decode it at the gNB,
potentially replacing the Type-II codebook which scales poorly beyond 32 ports.
AI-assisted beam prediction in both temporal and spatial domains, predicting
the best beam from past measurements, reducing the overhead of beam sweeping.
Neural network-based positioning enhancement, improving accuracy beyond
classical time-difference-of-arrival methods using learned environment models.

The main challenges: defining a lifecycle management framework (model
registration, activation, deactivation, and fallback to classical algorithms),
ensuring interoperability between UE and gNB implementations from different
vendors, and managing UE complexity since AI inference adds compute cost
[R1-2400797, R1-2401006, R1-2503239].

The deepest fight in Rel-19 was not technical but philosophical: should 3GPP
standardize AI/ML model architectures, or only the interfaces around them?
Ericsson and Qualcomm argued for UE-side model ownership: each vendor ships
proprietary models, 3GPP standardizes only the activation/deactivation
signaling, training data interfaces, and performance requirements. This
preserves vendor differentiation and allows rapid iteration [R1-2400172,
R1-2401435]. Nokia and Huawei pushed for standardized model architectures, particularly for the
autoencoder-based CSI compression, arguing that without a common encoder-
decoder layout, interoperability between different UEs and gNBs is impossible
and operators face a multivendor nightmare. Apple sided with Ericsson and
Qualcomm, prioritizing implementation simplicity and opposing anything that
mandated on-device AI inference for all device classes.

The fight intensified when it became clear that Rel-19 would only deliver
the framework, not the architectures. Huawei, Nokia, and CMCC pushed to
resolve the architecture question in Rel-19 rather than deferring to Rel-20.
Ericsson and Qualcomm successfully argued that premature standardization of
AI models, before the technology had matured and before real deployment data
existed, would lock the industry into suboptimal designs. The compromise:
Rel-19 specified the lifecycle management framework and use case definitions;
the architecture question was deferred to Rel-20, where it remains the single
most contentious issue in RAN1. The RAN#112 plenary in June 2026 is expected
to make a binding decision on the scope.

### Network Energy Savings (Netw_Energy_NR_enh-Core)

Operators demanded concrete gNB power reduction targets: 30% at medium load
and up to 50% at low load compared to the Rel-18 baseline. These targets were
set in a dedicated RAN workshop and drove the scope of the normative work
[R1-2400176, R1-2400335].

Rel-19 delivered three key mechanisms. Dynamic SSB periodicity adaptation
allows the gNB to reduce always-on synchronization signal transmissions from
every 20 ms to every 160 ms during low-load periods, cutting idle-mode power
by approximately 40%. Cell DTX/DRX with UE assistance enables the gNB to enter
deep sleep during periods with no active UEs, waking only when a UE signals
activity through a low-power wake-up receiver. On-demand SIB1 transmission
triggers system information broadcast only when needed, reducing periodic
broadcast overhead.

RAN4 specified RF requirement relaxations for energy-saving modes: looser
transmit power accuracy during DTX, relaxed adjacent channel leakage ratio
during low-power states, and reduced measurement reporting requirements during
DRX. Nokia dominated this work item with 86 proposal TDocs, nearly ten
times the output of Ericsson (9) and CMCC (9). This asymmetry created tension:
Nokia effectively drove the technical direction, while Ericsson and CMCC,
despite setting the original energy-saving targets, played supporting roles in
the specification phase [R1-2505060]. The dynamic reflected a strategic bet: Nokia had
invested heavily in energy-efficient hardware and saw the Rel-19 normative
work as a competitive differentiator for their AirScale base station portfolio.
Operators like CMCC, despite pushing the original KPIs, delegated the detailed
specification work to the vendors who would implement it.

### Low-Power Wake-Up Signal (NR_LPWUS-Core)

A separate low-power wake-up receiver (LP-WUR) was specified [R1-2400962,
R1-2401023], allowing the UE to power down its main receiver chain and listen only on a low-complexity
wake-up radio. The LP-WUS waveform was designed to match Msg3 PUSCH
performance: approximately 3-5 dB worse than paging PDCCH but with the WUR
consuming roughly 1% of the main receiver power, a ~100x reduction in idle-
mode UE power consumption, extending battery life for IoT and wearable devices
from days to weeks [R2-2404996]. The main challenge was coexistence: the LP-WUS signal
must be detectable while the main receiver is off, so it uses a simpler
modulation (OOK, on-off keying) that lacks the processing gain of NR PDCCH.
Nokia and Ericsson drove the LP-WUS waveform design [R1-2500113, R1-2400962] and pushed for mandatory
LP-WUR support across all device classes, arguing that network-level energy
savings cannot be achieved without widespread UE participation. Apple
pushed back hard, advocating that LP-WUR should be optional for mid-range and
low-end devices to minimize bill-of-materials cost and antenna complexity. The
debate mirrored the earlier 5G EN-DC mandatory support fight: infrastructure
vendors wanted every UE to support the feature for network efficiency; device
vendors wanted to segment the market. Samsung contributed simulation results
for LP-WUS coverage in rural scenarios, supporting the Nokia/Ericsson position
with technical evidence. The compromise landed as mandatory support for premium
device categories and optional for reduced-capability devices, a classic 3GPP
resolution to a classic industry conflict.

### NTN Phase 3 (NR_NTN_Ph3-Core)

Non-terrestrial networks progressed through three phases. Rel-17 (NTN
Solutions) established the basic framework: transparent payload architecture
where the satellite acts as a relay, initial channel models for LEO at 600 km
and GEO at 35,786 km, and feasibility of NR over satellite links with up to
280 ms one-way delay. Rel-18 (NTN enhanced) added GNSS-based UE positioning for
satellite access, HARQ process extensions beyond 16 processes to handle the
long RTT, and support for S-band (2 GHz) and Ka-band (20-30 GHz).

Rel-19 NTN Phase 3 addressed the hardest deployment challenges [R1-2400843,
R1-2400977, R1-2400132]. UE timing pre-compensation for LEO Doppler shifts, a LEO satellite at 600 km moves at
7.5 km/s, creating up to +-48 kHz Doppler shift at 2 GHz that must be
compensated at the UE to maintain synchronization. Retuning time requirements
for satellite beam switching as the satellite moves and the UE transitions
between beams every few seconds. HARQ process count extensions for the full
LEO round-trip time including feeder link delay. UE Power Class 3 for NTN
handheld operation (23 dBm), making satellite direct-to-handset feasible
without a dedicated satellite phone. RAN4 defined reference sensitivity for
S-band NTN, adjacent channel selectivity with satellite Doppler, and co-
existence with terrestrial NR in shared S-band spectrum.

Ericsson and Qualcomm led timing pre-compensation and HARQ design. Huawei and
HiSilicon drove UE power class specifications and Doppler compensation
algorithms. THALES, as NTN rapporteur, coordinated the channel model work and
regulatory alignment.

The tension in NTN was between traditional vendors and satellite operators.
SpaceX and AST SpaceMobile pushed for aggressive direct-to-handset
requirements: mandatory NTN support in all 5G UEs, relaxed Doppler tolerance
to accommodate diverse LEO constellations, and shared S-band spectrum with
terrestrial NR [R1-2604543, R4-2522419]. Their argument: without mandatory support, the NTN ecosystem
would fragment and never reach the scale needed for emergency services and
rural coverage. Apple, Samsung, and most UE vendors pushed back, arguing that
adding satellite-capable RF front-ends to every device would increase cost,
power consumption, and antenna complexity for a feature most users would never
access. The fight echoed the Rel-15 mmWave debate: should network-driven
features be mandatory for all devices? THALES mediated between the camps,
ensuring the channel models accommodated both aggressive and conservative
deployment assumptions. The compromise was Power Class 3 for NTN as an
optional UE capability, with the understanding that the mandate question would
return in Rel-20.

### Integrated Sensing and Communication (FS_Sensing_NR)

Rel-19 was the first time 3GPP studied whether 5G NR signals could be reused
for radar-like sensing: detecting objects, measuring velocity, and imaging
environments using the same reference signals already transmitted for
communication [R1-2400529, R1-2400648, R1-2401455]. The study item (FS_Sensing_NR) evaluated waveform designs,
particularly whether NR CSI-RS and SRS could serve dual purposes, and studied
sensing resolution trade-offs.

A fundamental architecture split emerged immediately. Ericsson drove the study
with the vision of network-as-a-sensor for industrial automation and autonomous
vehicles, proposing monostatic sensing: the gNB transmits and receives its own
sensing signals, simplifying synchronization but limiting coverage to the
cell radius. Huawei also favored monostatic, optimized for their integrated
gNB product line. Nokia and Qualcomm pushed for multi-static configurations
using multiple TRPs, arguing that distributed sensing nodes could achieve
better angular resolution and cover blind spots, at the cost of complex
inter-site synchronization of sensing measurements. The debate was a preview of
6G sensing architecture: centralized (gNB-only, simpler but range-limited)
versus distributed (multi-node, higher resolution but harder to standardize).

The study established feasibility for sub-meter range resolution using existing
NR waveforms, a key threshold for industrial applications, but left the
architecture question unresolved. Deferred to FS_Sensing_NR_bis in Rel-20, it
remains an open fight between the integrated gNB approach (Ericsson, Huawei)
and the distributed sensing approach (Nokia, Qualcomm).

### Ambient IoT (FS_Ambient_IoT_solutions, Ambient_IoT_Solutions-Core)

Ambient IoT envisions devices that harvest energy from ambient RF, light, or
vibration rather than using batteries, a paradigm shift from the 10-year
battery life targets of NB-IoT to truly maintenance-free operation. The study
item evaluated device architectures: tag-based (passive backscatter, similar
to RFID but at cellular range) and self-powered active devices with energy
storage capacitors [R1-2400075, R1-2400076]. RAN1 studied modulation schemes
for backscatter communication, waveform design for the carrier wave that
powers the tag, and coexistence with NR signals in shared spectrum.

Ericsson drove the study from the start, contributing the evaluation
assumptions, device architectures, and physical layer design framework
[R1-2400078, R1-2400079]. Nokia pushed for reader sensitivity requirements
that would enable warehouse-scale deployments, while Huawei focused on outdoor
range extension for agricultural and logistics use cases. The main debate
was indoor versus outdoor prioritization: indoor supporters (Ericsson, Nokia)
wanted factory automation first, while Asian operators pushed for outdoor
agricultural IoT. The compromise split the work into separate indoor and
outdoor study items in Rel-20.

### EN-DC RF Phase 4 (NR_ENDC_RF_Ph4-Core)

While not a flashy new feature, EN-DC RF requirements enable the practical
deployment of 5G non-standalone architectures: LTE anchor plus NR secondary
cell. Phase 4 addressed advanced antenna configurations, specifically 3T6R
and 4T6R antenna switching for SRS sounding across multiple UE antennas
[R1-2403834, R1-2403990]. These configurations allow UEs to switch their
transmit chains across up to 6 receive antennas, improving uplink MIMO
performance and coverage in NSA networks.

The work was procedural rather than contentious, with most major vendors
contributing measurement results and configuration proposals. Qualcomm
pushed for 4T6R as the high-end configuration; Apple and Samsung sought to
keep 3T6R as the practical baseline to limit RF front-end complexity. The
specification landed with both options, tiered by device category.

### Carrier Aggregation and Supplementary Uplink (NR_CADC_SUL_R19-Core)

Rel-19 extended carrier aggregation to 4 and 5 band combinations (BCS4 and
BCS5), a significant step from the previous 3-band limit [R4-2411255,
R4-2411323]. This enables operators to aggregate spectrum across low-band
(600-900 MHz), mid-band (1.8-2.6 GHz), and high-band (3.5 GHz) simultaneously
for peak data rates exceeding 4 Gbps. Supplementary Uplink (SUL) work defined
high-power UE configurations for bands where uplink is the bottleneck.

Ericsson drove the band combination definitions with detailed RF requirement
proposals, while Samsung contributed conformance test specifications. The
challenge was intermodulation: adding more bands increases the number of
intermodulation products that must be tested, exponentially growing the
conformance test burden. RAN4 defined reduced test configurations to keep
the work manageable, a long-running tension between specification
completeness and practical testability.

### IoT over NTN (IoT_NTN_Ph3-Core)

Satellite IoT addresses the coverage gap for low-rate, delay-tolerant devices
in areas without terrestrial coverage: container tracking at sea, pipeline
monitoring in remote regions, agricultural sensors in unconnected areas.
The work item focused on uplink capacity and throughput enhancement for NB-IoT
and eMTC over non-terrestrial links [R1-2400879, R1-2401195, R1-2401461].

The technical challenges were specific to narrowband IoT over satellite:
contention-based Msg3 transmissions where multiple devices may transmit on the
same resource, requiring new UL synchronization procedures for the long
propagation delay; HARQ process and timing advance extensions for LEO
scenarios where the satellite moves during the transmission; and power class
optimization for devices that must operate for years on a single battery while
compensating for the higher path loss of satellite links.

Iridium Satellite, with their existing 66-satellite LEO constellation, pushed
hard for narrowband NTN, contributing deployment parameters and operational
requirements. Qualcomm and Ericsson drove the physical layer specifications;
THALES coordinated the channel models for the NTN IoT bands.

### NR Mobility Phase 4 (NR_Mob_Ph4-Core)

Mobility enhancements focused on Layer 1/Layer 2 Triggered Mobility (LTM),
a fundamental shift from the traditional RRC-based handover. LTM enables the
network to trigger a handover via MAC CE or DCI rather than RRC
Reconfiguration, reducing interruption time from 30-50 ms to near-zero, a
critical requirement for URLLC and XR services [R1-2406860, R1-2406668].

The main debate was whether to prioritize inter-CU LTM (handover between
different centralized units, harder but the common real-world scenario) or
intra-CU LTM (same CU, simpler but limited to a single vendor deployment).
Ericsson and Nokia pushed for inter-CU as the primary scope, arguing
intra-CU-only LTM would have limited deployment relevance. Apple and Qualcomm
wanted to start with intra-CU and expand later, minimizing specification
risk. The Rel-19 outcome deferred inter-CU LTM to Rel-20.

Measurement enhancements for LTM were also specified: new measurement objects
and reporting configurations that allow the UE to measure candidate cells
during the LTM execution phase without interrupting ongoing data transmission
[R1-2406791, R1-2406861].

### XR Phase 3 (NR_XR_Ph3-Core)

Extended Reality (XR) workloads, encompassing VR, AR, and cloud-rendered
gaming, impose stringent requirements on 5G: periodic traffic bursts of
large downlink data (rendered frames) and smaller uplink data (pose/controller
information) with end-to-end latency below 10 ms. The key Rel-19 challenge was
enabling simultaneous transmission and reception of XR traffic during RRM
measurement gaps: when the UE tunes away to measure neighbor cells, the XR
flow is interrupted, causing frame drops and motion sickness [R1-2400748,
R1-2400677, R1-2400921].

Samsung and Qualcomm proposed reducing measurement gap duration and increasing
the periodicity to minimize XR interruption. Apple and Ericsson pushed for
smarter scheduling: aligning measurement gaps with XR traffic periodicity so
that gaps fall between XR bursts rather than during them. Nokia contributed
the work plan framework and measurement configurations [R1-2400922]. The
solution combined both approaches: configurable measurement gap patterns with
XR-aware scheduling restrictions, allowing operators to tune the trade-off
between mobility robustness and XR quality of experience.

### RRM Phase 5 (NR_RRM_Ph5-Core)

Radio Resource Management Phase 5 addressed practical deployment bottlenecks.
The flagship feature was fast SCell activation: reducing the delay from SCell
configuration to usable throughput from hundreds of milliseconds to tens of
milliseconds, enabling carrier aggregation to respond dynamically to traffic
bursts rather than being statically configured [R4-2408529, R4-2408439].

The technical work focused on Layer 3 measurement delay reduction for FR2-1
(mmWave): improving SSB-based measurement accuracy and reducing the
measurement period so that SCells can be activated faster based on reliable
signal quality information [R4-2407312, R4-2409150]. Apple drove the FR2-1
measurement optimizations, reflecting the importance of mmWave carrier
aggregation for their devices. Samsung and Qualcomm contributed L3 measurement
enhancements for both FR1 and FR2.

### Low-Band Carrier Aggregation via Switching (NR_LBCA_Sw-Core)

A Rel-19 study item exploring carrier aggregation across low bands (below
1 GHz) using transmit switching rather than simultaneous transmission. Low
bands provide coverage but are fragmented into narrow, non-contiguous
allocations. Simultaneous transmission across multiple low-band carriers is
impractical because the antenna separation required to avoid intermodulation
would exceed the UE form factor [R4-2500139, R4-2500405].

Switching-based CA allows the UE to rapidly toggle between low-band carriers
rather than aggregating them simultaneously, trading off peak throughput for
coverage flexibility. The study evaluated switching times, RF front-end impact,
and network signaling for dynamic carrier selection. HiSilicon proposed the
switching framework; Nokia contributed feasibility analysis; Apple drove the
UE RF requirement specifications [R4-2500215, R4-2500313]. The work was purely
a feasibility study in Rel-19, with normative specification deferred to
Rel-20.

## What Changed in Rel-20

Rel-20 is fundamentally different. The center of gravity shifted from refining
5G-Advanced to studying 6G. The work items that defined Rel-19 continued but
at reduced scale, while a new generation of study items emerged.

**FS_6G_Radio takes over.** The 6G Radio study item, entirely absent from
Rel-19, became the single most active work item in Rel-20 RAN1/RAN4 meetings
[R1-2505125, R1-2505127]. The group is defining channel models for the 7-24 GHz
range, evaluating candidate waveforms beyond OFDM (including OTFS for
high-Doppler and UFMC for mixed numerologies), studying sub-THz propagation
characteristics above 100 GHz for extreme data rates, and setting 6G KPI
targets: peak data rates exceeding 100 Gbps, sub-millisecond user plane
latency, centimeter-level positioning accuracy, and 10x spectral efficiency
improvement over NR.

**AI/ML moves to specification.** NR_AIML_air_Ph2-Core transitions from
Rel-19 feasibility studies to normative specification. Companies are now
proposing concrete AI/ML architectures. The key debate has shifted from
whether AI should be standardized at all to what scope: should model
architectures be standardized (Huawei, Nokia), or only the interfaces and
performance requirements (Qualcomm, Ericsson, Apple)?

**MIMO Phase 6 (NR_MIMO_Ph6-Core).** Multi-TRP enhancements continue into
Rel-20, targeting distributed MIMO with coherent joint transmission across
more than two TRPs, AI/ML-assisted beam management at scale for massive MIMO
arrays exceeding 128 antenna elements, and CSI enhancements for high-mobility
scenarios up to 500 km/h [R1-2505864, R1-2505576].

**Sensing goes normative (FS_Sensing_NR_bis).** The Rel-19 study established
feasibility. The Rel-20 bis study moves toward specification: defining sensing
service types (object detection, velocity measurement, environmental imaging),
sensing-specific signal designs using enhanced CSI-RS and SRS, and RAN-CN
interface procedures for sensing requests and reporting.

**NTN shifts to resilience and expansion.** FS_NR_NTN_GNSS_resilient addresses
operation when GNSS is unavailable or compromised: the UE must maintain
positioning and timing through alternative means including network-based
assistance and inertial sensors [R1-2505142, R1-2604543]. IoT_NTN_Ph4 continues
narrowband NTN for satellite IoT. Ku-band feasibility studies evaluate 12-18
GHz for higher-capacity NTN links.

**Ambient IoT becomes normative.** The Rel-19 study item splits into indoor and
outdoor work items in Rel-20 [R1-2400075, R1-2400076]. RAN4 is defining receiver
sensitivity targets for energy-harvesting devices, outdoor backscatter
modulation ranges up to 100 meters, and coexistence with NR and LTE in shared
spectrum.

**Leftover Rel-19 topics.** Several Rel-19 work items continue into Rel-20
at reduced activity: NR mobility Phase 4 (LTM enhancements, inter-CU handover),
XR Phase 3 (low-latency delivery for immersive applications), and enhanced
carrier aggregation (NR_CADC_SUL_R20_HPUE with high-power UE for supplementary
uplink).

## Release 20 Status

Release 20 is not finished yet. RAN1 and RAN4 work continues through multiple
plenary milestones. RAN#112 in June 2026 marks the 80% Stage-2 freeze;
RAN#113 in September 2026 is the final Stage-2 freeze. Stage-3 functional
freeze follows at RAN#115 in March 2027, with ASN.1 freeze and release
closure at RAN#116 in June 2027.

RAN#112 is the inflection point. Before it, the focus was feature invention:
deciding what goes into Rel-20, resolving architecture debates, and
completing study items. After it, the focus shifts to specification
completion: closing remaining issues, defining signaling and procedure
details, and converting concepts into PHY/MAC and RRC specifications. Most
feature decisions are already made; the remaining work is precision, not
direction.

After RAN#112, innovation focus increasingly shifts to Rel-21, which is
expected to be the first release with normative 6G specifications. Research
teams begin working on 6G proposals while standards engineers remain busy on
Rel-20 through RAN#115. Implementation teams may actually increase Rel-20
effort as specifications become stable enough for chipset and gNB
development.

## What This Blog Series Covers

Before tracking Rel-21 as it happens, this series reviews each of the
eleven RAN1 and RAN4 meetings where Rel-20 was discussed, from November 2024
to May 2026. Each post dissects one meeting: what topics dominated, which
companies drove the discussion, what concrete outcomes emerged, and how the
meeting moved Rel-20 forward.

