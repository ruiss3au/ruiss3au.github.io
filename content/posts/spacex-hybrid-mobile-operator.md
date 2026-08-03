---
title: "Why SpaceX Still Needs a Terrestrial Mobile Network"
description: "How handset link budgets, beam capacity, and the EchoStar spectrum package shape a possible Starlink mobile network."
date: 2026-08-03
tags: ["Starlink", "NTN", "D2D", "Mobile Networks", "Spectrum"]
featured: true
---

SpaceX's agreement to acquire EchoStar spectrum creates the foundation for a
much larger Starlink direct-to-device (D2D) system. It does not remove the two
physical constraints that separate satellite coverage from a terrestrial
mobile network: the uplink power of an ordinary phone and the amount of traffic
that can be carried per square kilometre.

Satellite D2D can supply wide-area reach and low-duty-cycle service. A
terrestrial radio access network (RAN) is needed for dense traffic and reliable
indoor coverage. Wholesale roaming could connect the two without requiring
SpaceX to build a national site grid from the outset. That combination would
amount to a hybrid mobile network operator (MNO), although SpaceX has not
announced such a network.

### Coverage and Capacity Are Different Problems

A national mobile service has to operate across traffic densities that differ
by several orders of magnitude. A highway dead zone may contain a few active
phones across hundreds of square kilometres. A city cell may carry hundreds of
simultaneous sessions inside one square kilometre. The same radio architecture
is not efficient at both extremes.

The key difference is **spatial reuse**. A terrestrial operator can transmit on
the same frequency from many sufficiently separated sites. When a city needs
more capacity, it can split cells and add sites near demand. A satellite beam
can reuse spectrum in other beams, but its serving area and interference
geometry are much larger and move with the constellation. Capacity cannot be
placed at street level with the same granularity.

The resulting SpaceX network would not be a satellite system replacing mobile
base stations. It would be one service platform selecting among owned
terrestrial cells, a roaming partner, and Starlink D2D according to coverage
and load.

### The Uplink From an Ordinary Phone

The downlink benefits from the satellite's available transmit power and large
antenna array. The reverse link begins with a battery-powered handset whose
effective isotropic radiated power (EIRP) is around 23 dBm in the reference
case. That is about 200 milliwatts before antenna directionality is accounted
for.

For frequency `f` in GHz and range `d` in km, free-space path loss is

```text
FSPL [dB] = 92.45 + 20 log10(f) + 20 log10(d)
```

At 2 GHz and 550 km, the loss is approximately 153.3 dB. At the same frequency
over a 10 km terrestrial path, it is approximately 118.5 dB. The satellite path
therefore begins about 34.8 dB behind, before accounting for low satellite
elevation, building penetration, foliage, or body loss. The spaceborne antenna
has to recover much of that deficit.

The carrier-to-noise-density ratio is

```text
C/N0 = EIRP + G/T - L - k
```

where `G/T` is the satellite receiver figure of merit, `L` is total loss,
and `k = -228.6 dBW/K/Hz`. For a receiver bandwidth `B`,

```text
C/N = C/N0 - 10 log10(B)
```

The Third Generation Partnership Project (3GPP) study
[TR 38.821](https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf)
shows how narrow the margin can be. Its S-band handset cases use a 23 dBm EIRP,
a 360 kHz uplink allocation, clear sky, 30-degree elevation, and a 3 dB
shadowing margin.

| 3GPP study case | Path loss | Satellite `G/T` | `C/N` over 360 kHz |
|---|---:|---:|---:|
| 600 km, receiver set 1 | 159.1 dB | 1.1 dB/K | 2.8 dB |
| 1,200 km, receiver set 1 | 164.5 dB | 1.1 dB/K | -2.6 dB |
| 600 km, receiver set 2 | 159.1 dB | -4.9 dB/K | -3.2 dB |
| 1,200 km, receiver set 2 | 164.5 dB | -4.9 dB/K | -8.6 dB |

These are study results, not decoding thresholds. Whether the Physical Uplink
Shared Channel (PUSCH), Physical Uplink Control Channel (PUCCH), or random
access preamble closes depends on coding, repetition, reference signals,
receiver implementation, interference, and the required block error rate. The
table does show that orbital geometry and satellite receive performance can
move the link from positive to negative carrier-to-noise ratio.

It also explains the current service boundary. T-Mobile's
[T-Satellite documentation](https://www.t-mobile.com/support/coverage/satellite-support)
confirms that supported phones can transmit messages and selected application
data. It recommends outdoor operation with a clear view of the sky and warns
that service may be unavailable inside buildings. A functioning two-way link
and poor terrestrial-style coverage probability can both be true.

### What the EchoStar Spectrum Changes

The Federal Communications Commission (FCC) approved the staged transfer to
SpaceX of 40 MHz of paired Advanced Wireless Services 4 (AWS-4), 10 MHz of
paired AWS H-block, and between 5 and 15 MHz of unpaired AWS-3 spectrum. The
[FCC order](https://docs.fcc.gov/public/attachments/DA-26-471A1.pdf) describes
approximately 65 MHz in total.

For a link budget, that total is misleading. The paired portion provides 25 MHz
in each direction when the uplink and downlink frequencies are counted
separately. Uplink and downlink megahertz are not interchangeable, and the
unpaired AWS-3 block has a different role subject to the applicable service
rules.

More importantly, a 25 MHz uplink license does not mean that one handset should
transmit across 25 MHz. With fixed total EIRP, increasing the occupied bandwidth
from the 360 kHz reference allocation to 5 MHz raises the receiver noise by

```text
10 log10(5,000 / 360) = 11.4 dB
```

That would consume far more margin than the reference link has. A D2D scheduler
instead concentrates the phone's power into narrow resource blocks and uses
coding or repetitions to accumulate energy. Additional licensed spectrum lets
the satellite schedule more narrowband users simultaneously. It increases
aggregate capacity, but it does not improve an individual phone's EIRP,
building penetration, or low-elevation margin.

This distinction is central to the EchoStar transaction. The spectrum package
can materially increase D2D concurrency without making the radio link behave
like a terrestrial cell.

### Capacity per Square Kilometre

The first-order downlink capacity density of one usable radio footprint can be
written as

```text
CA = B * eta * Nreuse / A
```

where `B` is bandwidth in MHz, `eta` is net spectral efficiency in
bit/s/Hz, `Nreuse` is the number of simultaneous sectors or equivalent
reuse units, and `A` is the serving area in square kilometres. The result is
Mbit/s/km².

Using the same equation for several radio footprints gives the following
order-of-magnitude comparison. These are scenarios, not a Starlink network
forecast.

| Radio footprint | Assumptions | Resource capacity | Capacity density |
|---|---|---:|---:|
| First-generation D2D | 5 MHz, 0.6 bit/s/Hz, 10,000 km² | 3 Mbit/s | 0.0003 Mbit/s/km² |
| Expanded D2D | 25 MHz, 1.2 bit/s/Hz, 10,000 km² | 30 Mbit/s | 0.003 Mbit/s/km² |
| Optimistic D2D | 50 MHz, 2 bit/s/Hz, 5,000 km² | 100 Mbit/s | 0.02 Mbit/s/km² |
| Rural terrestrial macro | 3 sectors, 20 MHz, 2 bit/s/Hz, 300 km² | 120 Mbit/s | 0.4 Mbit/s/km² |
| Mid-band terrestrial macro | 3 sectors, 100 MHz, 3 bit/s/Hz, 50 km² | 900 Mbit/s | 18 Mbit/s/km² |

The first D2D row is anchored to an independent
[measurement study](https://arxiv.org/pdf/2506.00283) of the initial Starlink
Direct to Cell system, which observed a 5 MHz carrier and estimated about
3 Mbit/s per beam under the measured outdoor conditions. The remaining rows
show the effect of bandwidth, efficiency, serving area, and terrestrial
sectorization.

Even the optimistic D2D case remains 20 times below the rural macro scenario
and 900 times below the mid-band macro in capacity per unit area. The exact
ratios will change with beam design, interference coordination, scheduler load,
and the number of simultaneously visible satellites. The reason for the gap
remains: terrestrial capacity scales through small serving areas and repeated
use of the same spectrum.

### From Beam Capacity to Busy-Hour Demand

Capacity density becomes more intuitive when translated into supported
population. Let adoption be 40 percent, the simultaneously active fraction be
`p`, and the rate per active user be `r`. The maximum population density is

```text
Dmax = CA / (0.4 * p * r)
```

For light data, assume 1 percent of subscribers are active at 1 Mbit/s. For
broadband-like demand, assume 5 percent are active at 5 Mbit/s.

| Radio scenario | Light data | Broadband-like demand |
|---|---:|---:|
| First-generation D2D | 0.075 people/km² | 0.003 people/km² |
| Expanded D2D | 0.75 people/km² | 0.03 people/km² |
| Optimistic D2D | 5 people/km² | 0.2 people/km² |
| Rural terrestrial macro | 100 people/km² | 4 people/km² |
| Mid-band terrestrial macro | 4,500 people/km² | 180 people/km² |

These are not coverage limits. A beam can cover a city while heavily
rate-limiting or queueing its users. They are busy-hour capacity limits under
the stated traffic model. Messaging works across much higher population
densities because both the duty cycle and payload are small. Sustained mobile
broadband does not.

A satellite service can therefore be commercially valuable without becoming
the primary radio layer in a city. Emergency messages, low-duty application
data, and coverage-gap service consume little average capacity. Video and
ordinary broadband traffic consume the shared beam quickly.

### Where Each Access Network Fits

Taken together, the two calculations define the boundaries of a hybrid
network. The uplink budget rules out satellite D2D as a substitute for indoor
and cell-edge coverage. A partner's low-band network can provide that coverage
without waiting for SpaceX to acquire low-band licenses and build thousands of
sites.

The capacity calculation rules out using satellite beams for the bulk of urban
traffic. Mid-band terrestrial cells are better suited to that job because the
same frequencies can be reused from site to site. SpaceX would only need to own
those cells where traffic volume makes wholesale capacity more expensive than
running the local RAN. In sparse areas, the calculation reverses: a wide
satellite beam is useful precisely because there is too little demand to justify
a terrestrial site.

The handset would therefore use an owned terrestrial cell where available,
roam onto a partner network across the wider terrestrial footprint, and fall
back to Starlink after terrestrial coverage ends. A common mobile core would
have to preserve authentication, policy, charging, addressing, and session
state as the access path changes. Satellite is one access network within the
service, not a replacement for the terrestrial core and RAN.

### What Remains to Be Built

The EchoStar deal supplies spectrum, not a deployed RAN. EchoStar reported in
its first-quarter 2026
[Form 10-Q](https://www.sec.gov/Archives/edgar/data/1415404/000110465926058150/sats-20260331x10q.htm)
that its cloud-native Open Radio Access Network (Open RAN) had been
decommissioned and carried no customer traffic by 15 November 2025.

Turning spectrum into terrestrial service still requires:

- low-band licenses or a roaming partner for wide-area and indoor coverage;
- mid-band radios and a dense site grid for urban capacity;
- towers, rooftops, power, fiber or microwave backhaul, and site permits;
- a production mobile core connected to both terrestrial and non-terrestrial
  access;
- mobility, authentication, policy, charging, emergency calling, lawful
  intercept, roaming, operations support, and business support systems;
- handset band support, certification, and network selection logic.

### Build, Roam, or Buy?

July reporting from
[Semafor](https://www.semafor.com/article/07/29/2026/spacex-looks-to-compete-with-the-carriers)
and
[Light Reading](https://www.lightreading.com/5g/spacex-might-build-and-buy-its-way-to-a-terrestrial-wireless-network-report)
says SpaceX has explored an MNO agreement, spectrum acquisitions, selective
construction, and carrier acquisitions. The reporting relies partly on unnamed
sources, SpaceX did not confirm a deployment plan, and the alternatives should
not be treated as a decision.

Against the radio and infrastructure requirements above, the alternatives are
not equivalent. A nationwide greenfield build duplicates infrastructure in
places where roaming is cheaper. A pure mobile virtual network operator (MVNO)
arrangement leaves all dense-area economics under an incumbent's control.
Buying a national carrier imports a complete footprint but also its debt,
legacy systems, and operating structure.

Selective terrestrial construction plus roaming fits the engineering boundary
best. Starlink can carry low-traffic services beyond terrestrial coverage, a
partner can supply national low-band and indoor service, and SpaceX can build
mid-band cells where traffic density makes wholesale capacity expensive.
Spectrum and sites can then be added market by market when ownership costs less
than roaming.

SpaceX can increase D2D capacity with spectrum, larger satellite apertures,
more beams, and more satellites. None of those changes gives an ordinary phone
more uplink power or gives a satellite beam the spatial reuse of a dense cell
grid. Those two constraints are why a technically credible Starlink mobile
operator is a hybrid network, not a satellite-only one.
