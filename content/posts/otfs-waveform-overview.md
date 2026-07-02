---
title: "OTFS and 6G: The Waveform Question"
date: 2026-07-02
tags: ["3GPP", "RAN1", "6G", "Rel-20"]
featured: true
---

The 6G waveform debate looked settled at RAN1#122: the moderator summaries recorded
agreement that "CP-OFDM waveform as defined in 5G NR is supported as the basis for
6GR for downlink" and "CP-OFDM and DFT-s-OFDM waveforms as defined in 5G NR are
supported as the basis for 6GR for uplink"
[R1-2506595](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2506595.zip).
Here Cyclic Prefix Orthogonal Frequency Division Multiplexing (CP-OFDM) and
Discrete Fourier Transform spread OFDM (DFT-s-OFDM) are the 5G New Radio (NR)
waveforms, and 6GR is the 6G radio. What was not settled was whether that door
would swing open for anything else. Cohere Technologies pushed Orthogonal Time
Frequency Space (OTFS), in its Zak-OTFS variant, into the conversation. Their
RAN1#122 contributions were co-signed by the Indian Institutes of Technology at
Delhi, Kanpur, Madras, and Bombay, the Centre of Excellence in Wireless
Technology (CEWiT), Lekha Wireless, Telstra, and Tech Mahindra, a coalition with
enough combined weight to keep the incumbents from closing the door entirely
[R1-2505627](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505627.zip).
Twenty months later, at RAN1#125, the communications waveform is converging
around OFDM, but OTFS has found a second argument in the Integrated Sensing and
Communication (ISAC) track. Nothing has been finalized: the Multi-RAT Spectrum
Sharing (MRSS) overhead question is still open, no formal decision has excluded
OTFS, and the ISAC study agreement from RAN1#124bis explicitly says "other
waveforms are not precluded"
[R1-2604633](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604633.zip).

The standards fight now has a well-funded outside backer. On 2 July 2026,
Light Reading reported that the US Department of Defense (DoD) awarded Cohere a
$28 million contract through its FutureG program, an endorsement of OTFS for
exactly the sensing use case the 3GPP debate has left open
([US Defense Dept backs 6G rival to tech used by Ericsson and Nokia](https://www.lightreading.com/6g/us-defense-dept-backs-6g-rival-to-tech-used-by-ericsson-and-nokia)).
FutureG lead Tom Rondeau put the case bluntly: "Ericsson and Nokia have both
shown me their ability to do ISAC sensing of drones with OFDM, but it's not a
natural fit. The OFDM waveform is not optimal for sensing." Cohere claims OTFS is
about four times more accurate than OFDM for a given slice of spectrum, and the
DoD interest in turning civilian networks into nationwide radar for drone
tracking is precisely the high-mobility sensing scenario where OTFS is supposed
to win. The contract does not change any 3GPP agreement, but it puts government
money behind the ISAC argument below.

This note tracks three fronts of the OTFS debate: why MRSS has sidelined it in
the communications waveform track, why ISAC is where the argument has shifted,
and how the optional-deployment model would work. It is a companion to
[MRSS: Sharing 5G Spectrum with 6G](/posts/mrss-overview/), which covers the core
MRSS debate.

## What OTFS Claims

OTFS modulates symbols in the delay-Doppler domain rather than the time-frequency
domain. The selling point is that each symbol in the delay-Doppler grid spreads
evenly across the full time-frequency resource block, so when a channel has both
delay spread and Doppler spread simultaneously, every symbol experiences the same
average channel statistics. OFDM, by contrast, assigns each subcarrier to a
single frequency bin: a strong Doppler shift breaks subcarrier orthogonality and
creates inter-carrier interference. OTFS is supposed to fix that.

Cohere's specific variant, Zak-OTFS, uses the Zak transform to move between the
delay-Doppler and time domains. Their key claim, delivered at RAN1#122, is that
Zak-OTFS can be deployed as a backward-compatible precoder on top of CP-OFDM: an
Inverse Discrete Frequency Zak Transform (IDFZT) feeds into the standard OFDM
modulator. They call this "OTFS over OFDM"
[R1-2505629](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505629.zip).

Their three-phase rollout:

- Phase 0: Legacy 5G CP-OFDM for all User Equipment (UE).
- Phase 1: OTFS over OFDM for 6G OTFS-capable UEs via software upgrade on the
  base station (gNB). No hardware changes.
- Phase 2: Fully optimized Zak-OTFS in new bands or after hardware refresh.

The concurrency is the point. Phase 1 does not displace OFDM. It runs alongside
it. OTFS UEs decode the precoded signal. Legacy 6G UEs see CP-OFDM. One carrier,
two waveforms, no forklift.

Cohere's simulation results, presented in R1-2505629, show Zak-OTFS over OFDM at
15 kHz subcarrier spacing outperforming CP-OFDM at both 15 kHz and 30 kHz in a
10 MHz urban macro channel at 12 GHz with 1 kHz Doppler, corresponding to roughly
90 km/h. Fully optimized Zak-OTFS pushes further. The RAN1#122 co-signers span
academia and industry: the IITs at Delhi, Kanpur, Madras, and Bombay, CEWiT,
Lekha Wireless, Telstra, and Tech Mahindra. A separate operator coalition
(Telstra, Reliance Jio, Telefonica, Bell, Spark NZ, BBC, and Telus) had backed
keeping non-OFDM waveforms in scope at the study-item stage
[RP-251248](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_108/Docs/RP-251248.zip).

## Front 1: MRSS Has Sidelined OTFS for Communications

The MRSS requirement demands that 6G and 5G share a single carrier with the
scheduler handing time-frequency resources to either radio on a per-slot basis.
Any waveform that cannot interleave seamlessly with 5G OFDM burns overhead:
guard bands, guard periods, lost resource elements.

RAN1#122 handled OTFS by relegation rather than rejection. The waveform
agreement named CP-OFDM as the downlink basis and CP-OFDM plus DFT-s-OFDM as the
uplink basis. OTFS and Zak-OTFS were placed in an "Other waveforms" list of
candidates to be studied only if proponents could "identify at least the target
use cases, signals/channels to use the waveform, and how the proposal is intended
... to support multiplexing with CP-OFDM, including MRSS, and how multi-user
multiplexing is supported"
[R1-2506595](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2506595.zip).
That burden of proof, tied explicitly to MRSS compatibility, is what has kept
OTFS at the margins of the communications track.

Nokia's own RAN1#122 contribution pushed CP-OFDM as the baseline without
engaging Zak-OTFS by name, proposing "CP-OFDM is the waveform used for
communication in 6G downlink" and "CP-OFDM and DFT-s-OFDM are the baseline
waveforms for 6G uplink," and stressing that hardware reuse is "especially
important in case MRSS is used for spectrum sharing between 5G and 6G"
[R1-2505127](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505127.zip).

Ericsson's RAN1#122 contribution took a different angle. They did not name
Zak-OTFS specifically but framed the demand that any new waveform must outperform
NR OFDM across six criteria: inter-carrier guard bands, multiple-access guard
bands, self-interference, Multiple-Input Multiple-Output (MIMO) simplicity,
low-complexity receivers, and service multiplexing. The framing was a high bar:
no alternative waveform was likely to beat OFDM on all six simultaneously
[R1-2505520](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505520.zip).

Through RAN1#125, the communications waveform position held: CP-OFDM as the
downlink basis, CP-OFDM and DFT-s-OFDM for uplink, with enhancements confined to
OFDM-based options such as DFT-s-OFDM modifications. The RAN1#125 waveform
summaries record no agreement naming OTFS as a communications waveform candidate
[R1-2603727](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2603727.zip).

Cohere fought MRSS interpretation directly. At RAN1#122, they argued that MRSS
should mean only "schedulable at PRB and slot boundaries with minimal loss," not
requiring OFDM subcarrier orthogonality. They claimed Zak-OTFS "meets the MRSS
requirements" because OTFS blocks can be placed into Physical Resource Block (PRB)
allocations with resource block boundaries and slot boundaries intact
[R1-2505627](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505627.zip),
[R1-2505628](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505628.zip).

Boost Mobile took the opposing interpretation at the same meeting, arguing that
6G must "preserve orthogonality with the 5G OFDM waveform," which in their framing
enables unified baseband processing and eliminates the need for guard bands
[R1-2505919](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505919.zip).
RAN1#123 reinforced the baseline with the frame-structure agreement, which
covered the NR frame structure, symbol durations, and resource block definitions
as the 6G starting point
[R1-2508857](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_123/Docs/R1-2508857.zip).
The scheduler works in time-frequency. Any waveform that does not map cleanly to
that grid pays a coordination tax.

### The Control Channel Fix

This is the one part of the MRSS argument that does not land on OTFS. Ericsson's
overhead assessment at RAN#112 argued that MRSS overhead can be driven to 1-2
percent if 5G and 6G share the same Physical Downlink Control Channel (PDCCH)
hashing function, Control Channel Element (CCE) sizes, and search space design.
The control channel question is about Control Resource Set (CORESET) alignment,
not about what modulation carries the data channel
[RP-261057](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261057.zip).

In an OTFS-over-OFDM Phase 1 deployment, the control channel stays CP-OFDM for
all UEs. The data channel gets precoded for OTFS-capable UEs and stays CP-OFDM
for legacy UEs. The PDCCH, Physical Uplink Control Channel (PUCCH),
Synchronization Signal Block (SSB), and reference signals are all OFDM. The
control channel sharing works because everything at the control layer is the same
waveform. Vodafone, Orange, and Deutsche Telekom's joint contribution at RAN1#125
confirmed this boundary: the overhead fight is about sharing the 5G CORESET, not
about the data waveform
[R1-2604915](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604915.zip).

### Where the MRSS Pressure Lands

The MRSS concern for OTFS is on the data channel. Cohere has not published
quantitative analysis of the overhead that OTFS-over-OFDM would impose in an
MRSS deployment. The RAN1#122 relegation of OTFS was itself conditioned on
proponents showing how the waveform multiplexes with CP-OFDM under MRSS
[R1-2506595](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2506595.zip),
a burden that remains unmet.
If the precoding introduces inter-PRB interference requiring guard subcarriers,
each guard subcarrier is lost capacity. The operator coalition including Vodafone,
Orange, Deutsche Telekom, Bouygues Telecom, Telecom Italia, AT&T, and BT is
demanding MRSS overhead be kept "very low," citing 4G/5G Dynamic Spectrum Sharing
(DSS) experience where roughly 30 percent resource element loss made DSS
commercially unattractive
[R1-2604502](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604502.zip),
[R1-2604507](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604507.zip).

The operators have not taken a public position on OTFS. Cohere has not yet filed
an OTFS MRSS overhead analysis in RAN1. Until those numbers exist, the MRSS
question is an open liability, not a settled verdict.

## Front 2: ISAC Is the Second Life

While the communications waveform was settling around OFDM, RAN1#124bis carved
out a separate agreement for ISAC: "CP-OFDM waveform as defined for 6GR is the
starting point for 6G ISAC waveform study. Study on enhancements on CP-OFDM or
other waveforms is not precluded." The "not precluded" clause is the pressure
valve.

### Why ISAC Is Different

Sensing and communication have different waveform ideals. Communication needs
orthogonal subcarriers that isolate data streams. Sensing needs sharp
autocorrelation that discriminates targets in range and Doppler. In OFDM, the
range resolution is limited by bandwidth and the velocity resolution by frame
duration. The cyclic prefix that makes OFDM robust against delay spread also
creates periodic peaks in the range-Doppler ambiguity function, aliasing targets
beyond the unambiguous range. Standard OFDM sensing also degrades when Doppler
shift breaks subcarrier orthogonality, a problem that grows with carrier
frequency: at 28 GHz, 90 km/h creates roughly 2.3 kHz Doppler. At 100 GHz, the
same speed creates 8.3 kHz.

OTFS operates natively in delay-Doppler. Its matched filter is the doubly
dispersive channel itself. For sensing, that means the ambiguity function is
inherently two-dimensional range-Doppler rather than being synthesized from
sequential OFDM symbols. The claim is that OTFS provides better target
discrimination in high-mobility scenarios, which is exactly the ISAC use case:
Uncrewed Aerial Vehicle (UAV) detection, vehicle tracking, high-speed rail
sensing.

### Qualcomm's ISAC Rejection

Qualcomm's RAN1#125 contribution explicitly addressed OTFS for ISAC, arguing the
"performance gap between OFDM-based waveforms and OTFS significantly narrows when
interference-aware multi-symbol receiver design is considered." They concluded
that no alternative waveform
"currently demonstrates a sufficiently compelling system-level advantage to
outweigh the cost, complexity, and ecosystem disruption associated with deviating
from an OFDM-based unified 6G air interface"
[R1-2604712](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604712.zip).

### The OFDM Synthesis Argument

Apple, Nokia, and AT&T each filed RAN1#125 contributions on ISAC waveform that
take CP-OFDM as the starting point and discuss waveform requirements in terms of
OFDM-based enhancements. Apple argued that "OFDM can achieve the same/similar
sensing performance as sensing-centric waveforms in terms of delay and Doppler
estimation" and described frequency-domain OFDM
sensing where range and velocity are extracted directly from modulation symbols
[R1-2603869](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2603869.zip).

AT&T and FirstNet's RAN1#125 contribution reinforced the baseline: "CP-OFDM is
used as the benchmark for evaluating the benefits of sensing waveforms." They
listed "ease of integration with communication" and "hardware impacts on radio
front-end and baseband" among the design considerations for evaluating waveform
candidates, both of which favor OFDM
[R1-2604633](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604633.zip).

Nokia's sensing waveform contribution at RAN1#125 is titled "On waveform for
sensing in 6GR"
[R1-2603538](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2603538.zip).

The LG Electronics (LGE) moderator summary from RAN1#125 listed CP-OFDM
enhancements as the main study candidates for ISAC waveform (Peak-to-Average
Power Ratio (PAPR), ambiguity function, Peak-to-Sidelobe Level Ratio (PSLR) and
Integrated Sidelobe Level Ratio (ISLR), cross-correlation) and proposed studying
"pulse-type waveform generation based on DFT-s-OFDM." The summary did not name
OTFS or Zak-OTFS in its proposed agreements. Companies supporting OFDM-based
sensing in the moderator's list included Nokia, InterDigital, Samsung, ZTE, ETRI,
DOCOMO, LGE, Xiaomi, CMCC, OPPO, Lenovo, Qualcomm, and Google. The proposed
enhancement areas all assume CP-OFDM as the starting point
[R1-2604763](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604763.zip).

### Cohere's ISAC Counter

Cohere's ISAC strategy is a pivot from the communications waveform fight. Their
RAN1#125 contribution proposed an ISAC system where "the sensing signal is
overlayed as a weak signal on the existing communication signal and hence does
not require any share of resource allocated to the communication signals,
resulting in no sensing overhead." The communication receiver is not required to
know the sensing signal
exists. Two versions: an OTFS-over-OFDM precoder for backward compatibility, and
pure Zak-OTFS for improved performance at higher complexity
[R1-2603875](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2603875.zip).

This submission does not ask to replace OFDM. It proposes using the ISAC
"other waveforms are not precluded" clause to specify an optional sensing
waveform that OTFS-capable gNBs can activate alongside OFDM communication. The
zero-overhead claim directly addresses the operator MRSS concern: if the
sensing signal is an overlay and costs nothing when idle, it avoids the
resource-loss problem that made 4G/5G DSS commercially unattractive.

## Front 3: Optional Deployment

Cohere's three-phase plan maps to an optional specification model: define OTFS
as a UE capability, specify the IDFZT precoder interface, and let OTFS-capable
UEs decode the precoded signal while legacy UEs see CP-OFDM.

### OTFS as a UE Capability

In wireless specifications, "optional" means a feature that a UE may implement
but the network may or may not support. Examples from NR: optional dynamic
waveform switching in Rel-18, optional full-power mode 1 in Rel-16, optional
additional Demodulation Reference Signal (DMRS) configurations. The pattern is
that the specification writes the protocol and the UE capability signalling, but
neither the network nor the UE is required to support it. Interoperability is
ensured by the baseline: if the network does not support OTFS, the UE falls back
to CP-OFDM.

For OTFS, this means:

- gNB broadcasts capability: "I support OTFS precoding on PDSCH."
- OTFS-capable UE responds: "I support OTFS reception."
- gNB schedules that UE with IDFZT precoding on its allocated PRBs.
- Legacy UE in the same slot gets normal CP-OFDM on its PRBs.

The gNB hardware path is identical in both cases: the precoder sits in the
baseband processing chain before the Inverse Fast Fourier Transform (IFFT).
Existing radios, existing power amplifiers, existing antenna arrays. The per-UE
differentiation is digital.

### What Would Make It Work

The ISAC use case. Cohere's overlay model means a single gNB can do both:
communications over CP-OFDM and sensing over the OTFS-overlay signal. A
non-OTFS gNB does communications only. An OTFS gNB gets sensing as a free
side channel.

The frequency argument. OTFS gain scales with carrier frequency times velocity.
At 3.5 GHz and pedestrian speeds, OFDM and OTFS are comparable. At 28 GHz and
highway speeds, OTFS has a growing advantage. At 100 GHz and anything moving, the
advantage is structural. 6G will operate across all of these. If the gain curve
is steep enough, the optional deployment argument becomes: deploy OTFS in the
frequency bands and mobility scenarios where it matters, leave it off where it
does not.

CEWiT contributed an RAN1#125 observation that cuts the other way: "Waveforms
with large subcarrier spacing are not suitable for sensing, as they increase the
probability of ghost target detection." Their proposal to support 7.5 kHz
subcarrier spacing for sensing applications to reduce ghost target detection is
not specifically about OTFS, but the physics it describes, that sensing
resolution demands narrow subcarriers while communication mobility demands wide
ones, is the opening OTFS needs: OTFS decouples delay resolution from subcarrier
spacing entirely
[R1-2604860](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604860.zip).

### What Would Block It

If Qualcomm's multi-symbol receiver claim holds up under evaluation, the
performance gap that OTFS is meant to fill disappears, and OTFS becomes
specification complexity without clear deployment return.

Nokia's moderator summaries show the waveform debate has produced no proposed
agreement naming OTFS. The trajectory is toward OFDM enhancements. At this
stage, OTFS remains in the "other waveforms are not precluded" footnote.

The operator MRSS position is unresolved. Cohere has not yet published an MRSS
overhead analysis for OTFS-over-OFDM. If such analysis shows non-trivial
overhead, OTFS loses the zero-cost migration argument. If Cohere can show
negligible overhead, or if OTFS is proposed only for new bands where MRSS does
not apply, that liability is contained.

## Company Positions

The following table summarises positions documented in RAN1 contributions. Where
a position is supported by a single company, the TDoc is cited.

| Position | Companies | Source |
|----------|-----------|--------|
| Zak-OTFS as 6G waveform candidate | Cohere Technologies, IIT Delhi/Kanpur/Madras/Bombay, CEWiT, Lekha Wireless, Telstra, Tech Mahindra | [R1-2505629](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505629.zip) |
| CP-OFDM as 6G baseline waveform (DL and UL) | Nokia | [R1-2505127](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505127.zip) |
| New waveform must outperform NR OFDM on six criteria | Ericsson | [R1-2505520](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505520.zip) |
| OTFS gap narrows with advanced multi-symbol OFDM receiver | Qualcomm | [R1-2604712](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604712.zip) |
| CP-OFDM as ISAC waveform baseline, OFDM-based pulse/FMCW synthesis | Nokia, Samsung, ZTE, DOCOMO, LGE, Xiaomi, CMCC, OPPO, Lenovo (per moderator summary) | [R1-2604763](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604763.zip) |
| OFDM achieves same/similar sensing performance as sensing-centric waveforms | Apple | [R1-2603869](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2603869.zip) |
| CP-OFDM as benchmark for evaluating sensing waveforms | AT&T, FirstNet | [R1-2604633](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604633.zip) |
| MRSS requires orthogonality with 5G OFDM | Boost Mobile | [R1-2505919](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505919.zip) |
| MRSS can work at PRB/slot boundaries without subcarrier orthogonality | Cohere Technologies | [R1-2505627](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_122/Docs/R1-2505627.zip) |
| Low MRSS overhead essential | Vodafone, Orange, Deutsche Telekom, Bouygues Telecom, Telecom Italia, AT&T, BT | [R1-2604502](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604502.zip) |
| 7.5 kHz SCS to reduce ghost target detection in sensing | CEWiT | [R1-2604860](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604860.zip) |

## What to Watch

1. **RAN1#126 ISAC waveform agreements.** The LGE moderator summary from RAN1#125
   proposed CP-OFDM enhancements, pulse-type DFT-s-OFDM, and left other waveforms
   as "not precluded." If RAN1#126 names specific alternative waveforms for ISAC
   study, OTFS stays in formal consideration.

2. **OTFS MRSS overhead measurement.** Cohere has not filed an OTFS-over-OFDM MRSS
   overhead analysis. If one appears showing negligible overhead on a shared
   carrier, the MRSS objection loses weight. If such analysis is absent or shows
   non-trivial overhead, deployment on MRSS bands becomes difficult.

3. **Qualcomm's multi-symbol receiver claim.** Qualcomm argues at RAN1#125
   [R1-2604712](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604712.zip)
   that advanced OFDM receivers narrow the gap against OTFS. If upcoming
   evaluations confirm this across the agreed ISAC scenarios, the case for a
   new waveform weakens.

4. **Operator support.** Telstra, Jio, Telefonica, Bell, Spark, BBC, and Telus
   supported the 6G Study Item Description (SID) at RAN#108 and co-signed
   [RP-251248](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_108/Docs/RP-251248.zip),
   which argued for keeping non-OFDM waveforms in scope. None have filed a
   dedicated OTFS TDoc in RAN1 since. If an operator files a support submission,
   the dynamics shift.

5. **Cohere's ISAC overlay model.** The RAN1#125 ISAC contribution
   [R1-2603875](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2603875.zip)
   proposes overlaying a weak sensing signal on OFDM with zero overhead. If RAN1
   adopts this as a study scenario, even as a non-precluded alternative, it gives
   OTFS a specification track outside the communications waveform agenda.

6. **CEWiT's subcarrier spacing observation.** CEWiT's RAN1#125 contribution
   [R1-2604860](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_125/Docs/R1-2604860.zip)
   observed that large subcarrier spacing raises ghost target detection,
   proposing 7.5 kHz subcarrier spacing for ISAC. The underlying physics, that sensing
   resolution and communication mobility pull subcarrier design in opposite
   directions, is the structural problem OTFS was designed to solve. If the ISAC
   study confirms this tension, OTFS's decoupled delay-Doppler grid becomes a
   technically motivated alternative.
