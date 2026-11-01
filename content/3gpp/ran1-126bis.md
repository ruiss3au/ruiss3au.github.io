---
title: "RAN1#126bis: RAN1 asks RAN4 to revisit reference-signal power limits"
description: "An October liaison-based report on sensing, reference-signal power and cross-group measurement questions."
date: 2026-10-16
tags: ["3GPP", "RAN1", "Rel-20", "6G"]
weight: 180
featured: true
llm: generated
---

RAN1 asked RAN4 to revisit guidance on reference-signal power boosting for 6G at its 12-16 October 2026 meeting in Jeju, South Korea. The request returns to a transmitter problem identified in earlier work: boosting a reference signal can require a more linear power amplifier or reduced output power [R4-2630005](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_121/Docs/R4-2630005.zip).

This report follows RAN1's outgoing liaison statements, available as incoming documents for November's RAN4#121. It covers the requests preserved in their text. Missing agreement tables and company contributions prevent a full account of the meeting's decisions and disagreements.

## Reference-signal power is a transmitter question

Channel-state information reference signals (CSI-RS) help a receiver characterize the radio channel. RAN1 asked RAN4 whether earlier guidance on boosting their power needs updating for 6G. The liaison recalls historical advice: boosting by 9 decibels could introduce power-amplifier nonlinearity, requiring a more linear transmitter or reduced radio output power. Those observations are explicitly prior guidance, not a newly agreed 6G limit [R4-2630005](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_121/Docs/R4-2630005.zip).

RAN1 asks whether the earlier guidance still applies. The letter contains no updated RAN4 answer.

## Compensation depends on measurement accuracy

A second liaison concerns joint downlink and uplink channel-state acquisition. RAN1 describes a use case in which the device supplies assistance information for network-side compensation of sounding reference-signal power imbalance. It asks RAN4 what accuracy is achievable when measuring received-power differences between device receive ports or port groups using CSI-RS [R4-2630006](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_121/Docs/R4-2630006.zip).

The agreement block referenced in the letter is absent from the extracted text. No numerical accuracy target or signaling format can be recovered from this source.

## Ambient devices need a defined reader measurement

For ambient Internet of Things devices, the reader is the radio endpoint that a device must select. RAN1's liaison asks RAN4 to choose between alternatives and define the measured bandwidth for reader-to-device reference-signal received power. The extracted letter reproduces RAN2's position that reader selection and reselection use that measurement, subject to RAN1 and RAN4 decisions [R4-2630007](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_121/Docs/R4-2630007.zip).

The letter also records that support for reader reselection does not imply that every active device supports inter-frequency reselection. It says the frequency-priority mechanism used in New Radio cell reselection is not reused for these active devices. The alternatives themselves are not preserved in the extracted agreement block, so this report does not describe their technical differences.

## Pairing identifiers remain outside RAN1 scope

For artificial intelligence and machine learning in the physical layer, RAN1 replied to RAN2 about life-cycle management of two-sided models. It reported no issue with the cited RAN2 agreement and working assumption. It also placed the number of pairing-identifier values for inter-vendor collaboration Direction C outside its scope, and said RAN1 was not expected to specify those values [R4-2630008](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_121/Docs/R4-2630008.zip).

The detailed Direction C agreement block is missing from the extraction. The visible response establishes the scope decision but does not describe how devices or networks exchange pairing identifiers.

## Sensing assumptions are not emission requirements

RAN1 supplied information for European Conference of Postal and Telecommunications Administrations studies in 3.4-3.8 GHz, while stating that it had not studied emission aspects or defined a common sensing-signal power spectral density. It also said the parameters supplied for sensing-performance evaluation did not themselves establish radio-frequency requirements or verified feasibility [R4-2630004](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_121/Docs/R4-2630004.zip).

For 6G sensing evaluations, the letter records two interference options: omit interference or model it explicitly. RAN1 will collect simulation results for both. It also states that sensing resolution, sensing-service latency and refresh rate were not considered as performance metrics or requirements in these evaluations.

RAN1 requested RAN4 responses on power boosting, receive-port measurement accuracy and ambient-device measurement bandwidth. The letter lists RAN1#127 in Calgary on 16-20 November as its next meeting [R4-2630005](https://www.3gpp.org/ftp/tsg_ran/WG4_Radio/TSGR4_121/Docs/R4-2630005.zip).
