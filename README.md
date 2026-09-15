# ST131Finder

A single-file web tool that assigns clade and subclade to *Escherichia coli* ST131 assemblies.
Everything runs in the browser — sequence data never leaves the machine. The only external
resource the page requests is a web-font stylesheet, fetched once at load; it works offline
without it, using system fonts.

▶ **Run it now, no installation:** https://toyotakasato.github.io/st131finder/

Every isolate is reported under each of the five studies that define ST131 population
structure, so a result can be quoted in whichever nomenclature a manuscript uses.

| Study | Nomenclature |
|---|---|
| Price LB et al. *mBio* 2013;4:e00377-13 | H30 / H30R / H30Rx |
| Petty NK et al. *PNAS* 2014;111:5694 | clades A / B / C |
| Ben Zakour NL et al. *mBio* 2016;7:e00347-16 | B0 / B1–B5, C0, the intermediate clade |
| Stoesser N et al. *mBio* 2016;7:e02162-15 | C1 / C2 |
| Matsumura Y et al. *AAC* 2017;61:e00179-17 | C0 / C1-nM27 / C1-M27 / C2 |

## Output

| Section | Content |
|---|---|
| Clade | A / B0 / B1 / B / C0/C3 / C1-M27 / C1-nM27 / C2 / Unclassified / non-ST131 |
| In silico PCR | The seven Table 1 primer pairs plus the *aer* SNP assay, the O25b *pabB* PCR and the Johnson *fimH*/*ybbW*/*rfb*/*fliC*/*plsB*/*nupC* assays, with product sizes and primer alignments |
| MLST | Achtman scheme, seven allele numbers and the ST |
| Lineage | The isolate's label under each of the five studies above, with a note on what each label means |
| fimH | *fimH*30 / 22 / 27 / 35 / 41 by allele-specific PCR |
| Serotype | O and H antigens from allele matching plus the *rfb* and *pabB* PCRs |
| QRDR | GyrA 83/87 and ParC 80/84 |
| Resistance genes | ResFinder panel — β-lactamases, PMQR, aminoglycoside, sulfonamide and others, with percent identity |

**Download CSV** and **Download JSON** save the whole run to disk; **Show as text** opens the
same content for copy-paste when a viewer blocks downloads. A clade C isolate negative for
both C1 and C2 is reported as **C0/C3** — the position Ben Zakour et al. defined as C0, the
ancestor of C1 and C2, from which Matsumura et al. later split C3. The assay cannot separate
C0 from C3, and the result says so.

## Version and provenance

**v1.3.0, built 2026-08-28.** v1.3.0 derives the Price label (H30 / H30R / H30Rx) from the clade
rather than from the *ybbW* and *fimH*30 markers, since Stoesser et al. report that C1 and C2
correspond to H30R and H30Rx; across 333 assemblies this changed the label of five clade C2 isolates
and altered no other output. v1.2.0 accepts an isolate as ST131 when either the region 19 amplicon or
in silico MLST supports it, correcting a defect in which a region 19 amplicon lost to assembly
fragmentation overrode an exact seven-locus ST131 profile; across 333 assemblies this changed the output
of one isolate and of no other, and specificity on 132 non-ST131 isolates was unchanged. v1.1.0 added the
*plsB* and *nupC* assays and reports clade B as B0 or B1, a strictly additive change affecting no call
outside clade B. v1.0.1 renamed the tool from its working name and changed the export file names; the reference database is unchanged and the diff over the hashed algorithm region is four
lines, all of them export labels. All published validation figures were generated with **v1.0.0**
(algorithm `b2c66eaded…`, file `434d2d1cb0…`) and were reproduced byte for byte by v1.0.1. The
algorithm and the reference database are otherwise fixed; any change to either requires a new version.

| Component | sha256 |
|---|---|
| `st131finder-v1.3.0.html` | `97114e1c8e6b9b7106a8f9699125ea0bcbf93e073f3e2f2478953a57b3a52ab0` |
| algorithm source (v1.3.0) | `c775cb3c1f9b275e5b89bd4d8bc5c2d883decb84cd9af4ce34c9e6b8fa5cf76d` |
| `db.json` reference database | `89e9166a635090c044669978cc47568d73595e044e403542b7ceb9a6f3f2479a` |
| release file (v1.0.0, validated) | `434d2d1cb0941db6130aefe2da6f8cbf5cbabcad979c27a49955056dfe3da41f` |
| algorithm source (v1.0.0, validated) | `b2c66eaded52ebe38896961dd2cce4d26ec32e1312e02c49efebb3e78e41f1c7` |

The version and both component hashes are printed at the foot of the page and written into
every CSV and JSON export, so any result can be traced to the build that produced it. The
build is byte-for-byte reproducible: `python3 build_release.py` from the same `app.html` and
`db.json` reproduces the file hash exactly (gzip timestamps are pinned to zero for this
reason). Verify a copy with `shasum -a 256 st131finder-v1.3.0.html`.

**Development and validation.** Version 1.0.0 was finalised against 200 whole-genome-sequenced
isolates from Maeda et al. (*Antimicrob Agents Chemother* 2026;70:e00007-26), which served as
the **development set** — two corrections were made after inspecting those results (the fimH
reporting rule and the MLST seed set). Figures obtained on that collection therefore describe
development performance, not independent validation. An independent validation set, analysed
without further changes to this frozen build, is required before performance is reported as
such.

## Reading the results

The most recently analysed isolate appears at the top, so a long batch reads newest first.
Each card carries its run number: analysing A, B, C puts C at the top with run number 03.
When two or more isolates are loaded, a run summary table sits above the cards in the same order.

Browsers hand over multi-file selections in an unpredictable order, so files are sorted by
name (numeric-aware) before analysis. Analysis order, run numbers and display order therefore
always agree.

## How a band is called

The published primers are allele-specific and carry deliberate internal mismatches — the
clade C forward primer, for example, mismatches every template four bases from its 3′ end.
Exact matching is therefore the wrong test. A product is called when:

1. the 3′-terminal base matches exactly (the discriminating SNP sits there),
2. no more than two mismatches occur anywhere in the primer, and
3. the product falls within 25 bp of the expected size.

These thresholds were calibrated on three sequenced isolates spanning clades B and C1-M27,
with no false positives and no false negatives.

## Deployment

One file, no server.

**Run the hosted copy** — https://toyotakasato.github.io/st131finder/ — nothing to install.

**Locally / offline** — download `st131finder-v1.3.0.html` and double-click it. The reference
database is embedded, so no network access is needed.

**Host your own copy on GitHub Pages** — put a byte-identical copy of the release file at the
repository root named `index.html`, then set Settings → Pages to branch `main`, folder
`/ (root)`. The tool is then served at `https://<user>.github.io/<repo>/` with no running costs
and nothing to maintain.

## Requirements

Current Chrome, Edge, Firefox or Safari. Uses `DecompressionStream` (Safari 16.4+).
About 3–4 seconds per 5 Mb genome. File size 1.29 MB including all reference data.

## Reference data

- PubMLST *Escherichia coli* #1 (Achtman) scheme — retrieved August 2026
- ResFinder — retrieved August 2026
- ECTyper O- and H-antigen allele set — retrieved August 2026
- O25b: *pabB* PCR of Clermont et al. 2008, *J Antimicrob Chemother* 61:1024

Databases are embedded in the HTML as gzip + Base64. To refresh them, rebuild `db.json`
and swap the Base64 payload in the `<script id="dbz">` block.

## Cross-framework consistency

Because these frameworks rest on different markers, the tool checks them against each
other and warns when they disagree — for example when *fimH*30 is positive but the clade
assay calls B, or when a C2 isolate lacks the *ybbW* SNP, as Matsumura et al. reported for
one genome. Clade C isolates normally carry *fimH*30, but alternative alleles occur, so the
clade call is never inferred from *fimH* and vice versa.

## Assay sources

- Johnson JR, Johnston BD, Porter SB, et al. *Microbiol Spectr* 2022;10:e01064-22 — *fimH*, *ybbW*, *rfb* and *fliC* primers
- Banerjee R, Johnston B, Lohse C, et al. *Antimicrob Agents Chemother* 2013;57:6385 — H30Rx *ybbW* SNP
- Clermont O, Dhanji H, Upton M, et al. *J Antimicrob Chemother* 2008;61:1024 — O25b *pabB* PCR

## Limitations

- Clade B is reported as B0 or B1 only when the *plsB* or *nupC* amplicon is recovered; a *plsB*-negative assembly with no *nupC* band is reported as clade B with the subclade undetermined. Ben Zakour et al. resolved clade B proper into five subclades (B1–B5); the assay separates B0 from the rest but cannot resolve B1 from B2–B5, and the B1 label follows Johnson et al.
- An isolate is accepted as ST131 on either the region 19 amplicon or an exact seven-locus MLST profile, so a fragmented region 19 locus no longer costs the clade call.
- In draft assemblies an amplicon that straddles a contig boundary is scored negative. When M27PP1 is negative but the *aer* SNP assay is positive, the isolate is still called C1-M27 and a warning explains why.
- The Price et al. label is derived from the clade assignment, not from the *ybbW* marker. A clade C2 isolate is reported as H30Rx even when the *ybbW* SNP is absent, and the result records that absence; 2 of 42 C2 genomes in the validation collection lacked the marker.
- These are in silico calls, not a guarantee of what a gel will show. Confirm clade assignment by core-genome phylogeny for epidemiological work.
- Research use. Not intended for diagnostic purposes.
