---
title: "SpaceX's terrestrial ambitions meet the interference test"
description: "What the August 3GPP documents establish about SpaceX's terrestrial spectrum work, satellite coexistence and the small-cell hypothesis."
date: 2026-08-24
lastmod: 2026-09-06
tags: ["3GPP", "SpaceX", "Starlink", "NTN", "Small Cells"]
featured: true
draft: true
---

Could a Starlink terminal become a cellular site? The attractive part of that
idea is easy to picture: an installed location with power and a satellite
backhaul connection, serving nearby phones through a small terrestrial radio.
The difficult part starts when those phones must coexist with other mobile
networks, move outside that site's coverage, and remain manageable as part of
one service. A terminal footprint and a cellular network solve different
operational problems.

The August 2026 standards record gives us a better way to examine the idea.
SpaceX is advancing terrestrial LTE and NR band requirements while proposing
how satellite interference and terrestrial-to-satellite handover should be
tested. The most revealing issue is a procedural condition connecting them:
the related satellite band proposal can be revisited after sufficient progress
and conclusions in the coexistence study. A model of interference at an
ordinary terrestrial phone has become part of the route through the standards
process
[RP-261531](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261531.zip),
[R4-2612133](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2612133.zip).

This article treats terminal-mounted small cells as a deployment hypothesis.
The primary documents establish SpaceX's radio and spectrum work. They do not
establish a particular announced terminal product or a completed small-cell
architecture. That boundary lets us ask a more useful question: which of the
technical obstacles to a hybrid service is SpaceX actually trying to remove?

## Table of contents

- [A terrestrial band with its own engineering case](#a-terrestrial-band-with-its-own-engineering-case)
  - [The filter matters as much as the frequency allocation](#the-filter-matters-as-much-as-the-frequency-allocation)
- [The satellite condition: protect the phone at the coverage edge](#the-satellite-condition-protect-the-phone-at-the-coverage-edge)
  - [What SpaceX wants the model to assume](#what-spacex-wants-the-model-to-assume)
  - [Why the operator positions are more complicated](#why-the-operator-positions-are-more-complicated)
- [A continuous service needs a conditional handover](#a-continuous-service-needs-a-conditional-handover)
- [What the Femto record actually establishes](#what-the-femto-record-actually-establishes)
- [The deployment questions the band work cannot answer](#the-deployment-questions-the-band-work-cannot-answer)
- [The next documents that would change the assessment](#the-next-documents-that-would-change-the-assessment)

## A terrestrial band with its own engineering case

SpaceX's terrestrial work is specific. The New Radio (NR) work-item
description, jointly sourced with Boost Mobile Network and EchoStar, defines
1915-1920 MHz uplink and 2180-2200 MHz downlink. It includes asymmetric channel
bandwidth, variable transmit/receive separation, user equipment (UE)
power-class-3 requirements and base-station requirements. Its August
rapporteur work plan describes the project as initiated at the June plenary
[RP-261570](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261570.zip),
[R4-2610141](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610141.zip).

There is parallel Long Term Evolution (LTE) work. SpaceX proposes reserving
band 116 for LTE and n116 for NR, with reuse of applicable base-station
requirements from existing bands 25/n25 and 66/n66. The identifier remains a
proposal in these papers; it should not be described as an August-approved
band assignment
[R4-2610136](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610136.zip),
[R4-2610138](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610138.zip).

This matters to the small-cell question because it demonstrates work on a
terrestrial air interface with an identifiable frequency pair and device
requirements. It does not choose the site's size, ownership or backhaul.
The same band project cannot, by itself, distinguish a consumer-hosted radio
from an operator-controlled installation. That distinction needs deployment
and architecture evidence beyond a band definition.

### The filter matters as much as the frequency allocation

SpaceX's UE paper describes treating the new uplink as a five-megahertz
extension near the n25 uplink. The resulting transition toward the n2/n25
downlink is narrower, making filter performance and protection of other
phones relevant. It proposes evaluating additional maximum power reduction
(A-MPR), the allowance for reducing transmitter power to meet additional
emission requirements. It also proposes network signaling for handling the
equivalent isotropically radiated power constraint
[R4-2610139](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610139.zip).

Murata proposes technical baselines drawn from existing terrestrial and
satellite emission treatments, with additional assessment of UE-to-UE
coexistence and receiver blocking. This is the component-level test of reuse:
an existing requirement may be a useful starting point without making every
filtering problem disappear
[R4-2610269](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610269.zip).

For a hypothetical small-cell service, the implication is straightforward.
Site availability is only one input to coverage. If some uplink allocations
require appreciable power backoff, the phone's usable link budget changes.
Neither the spectrum bandwidth nor a nominal UE power class establishes the
coverage that a deployed cell will deliver. The next useful evidence is
tested radio-frequency (RF) behavior under an agreed implementation model.

## The satellite condition: protect the phone at the coverage edge

The June plenary discussion identified a different link-budget problem on
the terrestrial receiver side. Verizon argued that modeling one interfering
satellite and a heavily interference-limited terrestrial network can miss
the vulnerability of a noise-limited coverage edge. A phone in that situation
has little margin; added unwanted satellite power may matter more than an
average-network result suggests
[RP-261531](https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261531.zip).

The study direction calls for aggregate interference from multiple satellites
and attention to those coverage edges. T-Mobile and Rogers' August paper
reports that direction as approved and reproduces the condition for
revisiting the related non-terrestrial network (NTN) band proposal. This is
an inherited June condition, not evidence that August completed the study
[R4-2612133](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2612133.zip).

The important connection is that a 6G study can affect an NR spectrum project.
The shared issue is the physical interference between deployments. A company
trying to bring satellite and terrestrial capabilities to market has reason
to engage in that modeling work even before any product architecture appears
in the standards record.

### What SpaceX wants the model to assume

SpaceX proposes a minimum unobstructed elevation angle of 28 degrees for
coexistence simulations. Its dense low-Earth-orbit example considers up to
eleven visible satellite access nodes, with further work to identify which
actually emit into the relevant adjacent channel. It also asks for discussion
of simultaneously active beams and suggests representing terrestrial coverage
edges by removing wrap-around and specifying a user-placement radius
[R4-2610133](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610133.zip).

Each assumption affects the answer. Counting every visible satellite as an
identical interferer can misrepresent a constellation's operation; omitting
relevant active satellites can understate interference. The model needs to
connect visibility, frequency use, loading and antenna patterns. SpaceX's
paper also asks for testability assessment before new adjacent-channel
leakage requirements are specified and raises a radiated-power-based metric.

The commercial significance is an inference from that technical choice.
A requirement attached to each spacecraft's transmitter and a protection
criterion attached to aggregate interference constrain a deployment in
different ways. The standards work must establish how the two relate.
The contribution does not show that RAN4 accepted SpaceX's preferred model.

### Why the operator positions are more complicated

T-Mobile and Rogers also distinguish aggregate protection from a universal
per-satellite emission limit. They propose that aggregate ground-level
protection should not automatically translate into one new transmitter
requirement, and that applicable regulatory treatment be considered. They
add a consistency demand: new coexistence requirements should apply to
legacy NTN bands with adjacent or overlapping terrestrial downlinks too
[R4-2612133](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2612133.zip).

This is more specific than a confrontation between all mobile operators and
all satellite companies. There is overlap on the distinction between a
single transmitter and the combined interference at a victim. There are
still consequential choices about model assumptions, the protection metric
and which existing bands a new rule would affect.

Ericsson separately asks how to identify the noise-limited terrestrial users,
noting that they need not be the same users as the fifth-percentile
throughput group. That question is central to whether a test protects the
coverage that a terrestrial operator worries about losing
[R4-2611464](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2611464.zip).

## A continuous service needs a conditional handover

The phone must also move between coverage layers. SpaceX proposes assuming
that a UE configured to measure an NTN neighbor activates its global
navigation satellite system (GNSS) receiver before LTE-to-NR-NTN handover
begins. It argues that position availability supports timing and Doppler
compensation and that recovering from failed handover can itself consume
power. Its proposed fallback, if no reasonable latency requirement gains
consensus, is to declare that connected-mode mobility infeasible under the
existing GNSS-dependent design
[R4-2610131](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610131.zip).

Qualcomm instead proposes preserving freedom over GNSS activation timing.
Its zero-additional-GNSS-time condition for handover requires the target NTN
cell to have been configured for measurement and a measurement reported
within the preceding five seconds. It also discusses a narrowly scoped
optional capability as an alternative for acquisition time
[R4-2612187](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2612187.zip).

Those proposals expose what a service-continuity claim would need to specify.
Does the phone have fresh positioning and measurements before losing the
terrestrial link? What happens when it does not? A transition demonstrated
under prepared conditions is not automatically representative of every
indoor exit, coverage hole or device power state. Neither paper establishes
that all such cases are solved, and this LTE handover work should not be
mistaken for a complete NR-small-cell-to-satellite mobility design.

The separate GNSS-resilient work program addresses assistance and compensation
when a device cannot rely on its own positioning. Its work plan reproduces
scope spanning random access, timing advance, frequency adjustment and
performance requirements. It is relevant future machinery, with its own
specification and testing dependencies
[R4-2612145](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2612145.zip).

## What the Femto record actually establishes

NR Femto is a relevant separate standards thread, but the available evidence
must be read at its actual level. The architecture contribution R3-255055
has a broad joint company source list. R3-261206 concerns core-network
awareness, with Huawei, CATT, Samsung, Ericsson, China Telecom, Lenovo and
Qualcomm listed jointly. R3-263243 is a later correction on that subject
[R3-255055](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_129/Docs/R3-255055.zip),
[R3-261206](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_131-bis/Docs/R3-261206.zip),
[R3-263243](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_133/Docs/R3-263243.zip).

The local copies have metadata but no extracted text. They establish the
subject and participation, not the exact architecture, an adopted signaling
procedure, or its applicability to Starlink. The reviewed primary material
does not identify a SpaceX-specific Femto solution. That is a limit of this
review, not a claim to have proved the absence of such work everywhere.

A proposed terminal-hosted cell would need an operational account of how it
joins the network, how access is controlled and how failures are handled.
Those are engineering questions for the hypothesis. They cannot be answered
by citing the title of a general Femto contribution, and should not be
presented as features already established for Starlink.

## The deployment questions the band work cannot answer

Consider two installations. One is placed by an operator where demand and
interference planning justify it, with controlled power and maintenance.
Another is placed by a customer for satellite reception, with a location and
availability governed by the customer's needs. Both might provide a transport
path for a radio, but they imply different control over coverage and service
availability. This comparison is a deployment scenario, not a description of
an announced SpaceX product.

For the customer-hosted case, terminal density would have to align with mobile
demand. A backhaul connection at one address does not establish continuous
street coverage or sufficient capacity at another. Whether users can roam
beyond those sites, whether access is public or restricted, and who restores
a failed node all affect the service. None follows from approval of a
frequency pair or a transmit-power class.

SpaceX's additional NTN work shows another part of its engineering agenda.
It challenges restrictive carrier-aggregation bandwidth combinations and
requests PC1.5 support for n252 and n256. Those are efforts to expand the
usable satellite radio framework; they do not specify a terminal-mounted
cell or show that such a cell is the intended deployment
[R4-2610132](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610132.zip),
[R4-2610135](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_120/Docs/R4-2610135.zip).

## The next documents that would change the assessment

The nearest standards checkpoint is a verified disposition of the RAN4
coexistence proposals: the model, the protected terrestrial population and
the relationship between aggregate protection and transmitter requirements.
Sufficient progress could affect the related NTN band proposal's return.
A handover disposition would clarify the conditions under which continuity
can be tested. Band-specific RF results would narrow what a handset can
actually deliver on the proposed terrestrial allocation.

A stronger small-cell conclusion requires different evidence: an explicit
deployment or architecture document joining the terrestrial radio, terminal
backhaul and network integration. It would need to explain access, mobility,
management and the failure behavior. That would turn an attractive hardware
idea into something whose standards dependencies and operational tradeoffs
could be evaluated directly.

The current record already tells an important story. SpaceX is working on
terrestrial spectrum requirements while trying to shape satellite coexistence
and mobility assumptions. The obstacles are identifiable, and so are several
of the other companies' positions. The unresolved question is which
requirements will be accepted and what deployment can meet them. The
[RAN4#120 report](/3gpp/ran4-120/) places satellite coexistence and
mobility within the wider terrestrial, AI and sensing agenda; the
[RAN1#126 report](/3gpp/ran1-126/) follows the
parallel work on radio procedures and GNSS resilience.

Evidence reviewed 6 September 2026. This replaces the earlier draft's
unverified commercial framing and overly specific Femto claims with
attributed primary-document findings. Final August RAN4 dispositions remain
an explicit gap.
