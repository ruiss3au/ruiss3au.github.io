---
title: "RAN4#120bis: Waveform gains depend on resource allocation"
description: "October liaison evidence on waveform gains, beamforming, channel prediction and sensing feasibility."
date: 2026-10-16
tags: ["3GPP", "RAN4", "Rel-20", "6G"]
weight: 190
featured: true
llm: generated
---

RAN4 reported that low peak-to-average-power-ratio waveforms offer their largest transmit-power gains in outer resource-block allocations, where out-of-band emission constraints are stricter. Inner allocations generally show smaller gains. Its outgoing liaison from Jeju, South Korea, on 12-16 October 2026 asks RAN1 to include these results in 6G waveform evaluation [R1-2609005](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609005.zip).

This report covers RAN4#120bis through outgoing liaison statements forwarded to November's RAN1#127. The company-specific waveform-results attachment and the full meeting contribution record were not reviewed. The letters establish working-group observations and requests; they do not establish individual company positions.

## Waveform power gains depend on where transmission occurs

RAN4's reply on uplink frequency-domain spectrum shaping identifies outer physical-resource-block allocations as the main setting where low peak-to-average-power-ratio waveforms yield transmit-power improvements. It attributes that distinction to stricter out-of-band emission constraints. Inner allocations generally offer more modest gains because the baseline already has greater emission margin [R1-2609005](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609005.zip).

The letter also warns that a reference baseline may already permit power boosting relative to the indicated power class. A relative waveform gain therefore cannot simply be read as extra output power over the nominal class in every allocation. The attached company-specific evaluations were not reviewed for this report, and no company ranking or universal gain is inferred.

RAN4 allows consideration of redefined error-vector-magnitude equalizer spectrum-flatness requirements for candidate waveforms. It asks that receiver-performance impact also be considered in RAN1's net-gain evaluation. New requirements, if agreed, would be introduced in Release 21. [R1-2609005](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609005.zip).

## Coherence and wake-up operation retain open requirements

For coherent uplink multiple-input multiple-output transmission, RAN4 considers existing New Radio requirements a starting point for up to four transmit ports. It continues studying possible updates and side conditions, while leaving detailed amplitude and phase error modeling to RAN1. It requests feedback on reasons to change the existing requirements for 6G [R1-2609007](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609007.zip).

Power saving creates a different timing question. In its reply on wake-up signals and connected-mode discontinuous reception, RAN4 says the measurement cycle used to define delay requirements can equal or exceed the configured wake-up/reception cycle. Exact 6G radio-resource-management delay requirements remain for the work-item phase. [R1-2609006](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609006.zip).

## Prediction quality is also a channel-model question

RAN4 describes a study that predicts a target cell's layer-three received power using measurements on other frequency layers, with the target cell not co-sited with a measured cell. Under its stated stochastic channel-model assumptions, prediction accuracy was worse than the existing inter-frequency measurement-accuracy requirement [R1-2609010](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609010.zip).

Its proposed explanation is insufficient correlation between non-collocated sites in the model. RAN4 identifies alternative modeling approaches, including map-based ray tracing, and asks RAN1 which assumptions and procedures can be reused or need alignment. It plans to continue the study while awaiting feedback.

## Digital beamforming remains a complementary model

For 6G Frequency Range 2, RAN4 keeps analog beamforming as the baseline for requirements development. It studies a complementary digital-beamforming analytical model, with any later digital-specific requirements envisaged as optional device capabilities if agreed in a subsequent work-item phase [R1-2609011](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609011.zip).

The model considers deriving spatial filters from simultaneous observations across antenna branches during one downlink reference-signal occasion, given timing, configuration and sufficient received-signal quality. It also considers weights derived from channel estimates without restriction to a predefined codebook, and up to two spatial layers. RAN4 asks RAN1 to assess the implications for physical-layer procedures and specifications.

## A network sensing target is not a single-radio test

The sensing liaison identifies a mismatch in responsibility: the sensing performance indicators in Technical Report 38.914 apply at network level, while RAN4 can define and test radio-frequency performance for a single base station. It plans to study single-base-station feasibility and coexistence as a baseline [R1-2609012](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609012.zip).

A simplified mapping between single-node signal quality and network sensing performance, potentially through a fusion gain or scaling factor, remains undecided. RAN4 asks RAN1 for guidance. The letter states that RAN4 has not decided whether to use this approach.

RAN4 requests RAN1 feedback on waveform receiver penalties, channel-model correlation, digital-beamforming procedures and the mapping from network sensing targets to single-base-station tests. Its next meeting is listed for Calgary on 16-20 November [R1-2609005](https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_127/Docs/R1-2609005.zip).
