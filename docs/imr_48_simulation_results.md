# 48 IMR-Grounded Claim Negotiation Simulations

Each case is linked to a **real California DMHC Independent Medical Review (IMR) ReferenceID**.  
Search the public database at https://wpso.dmhc.ca.gov/imr/ using the ReferenceID to retrieve the original Findings and determination.

All simulations were run with NegMAS SAOMechanism (AspirationNegotiator linear vs TimeBasedConcedingNegotiator).  
Reserved values and step limits were scaled by the historical overturn prior derived from the actual IMR determination.

## Summary Statistics

- **Cases**: 48
- **Settled**: 48
- **Average allowed %**: 73.0
- **Average estimated recovery**: $3,965
- **Average steps**: 7.0

## Case Table

| ReferenceID | Year | Diagnosis | Type | IMR Outcome | Prior | Billed | Allowed % | Discount | Recovery | Steps | Outcome |
|-------------|------|-----------|------|-------------|-------|--------|-----------|----------|----------|-------|---------|
| MN13-14640 | 2013 | Orth/Musculoskeletal | Medical Necessity | Overturned | 0.62 | $6,028 | 68 | 6 | $3,853 | 6 | settled |
| MN20-32904 | 2020 | Vision | Medical Necessity | Overturned | 0.62 | $8,414 | 68 | 6 | $5,378 | 6 | settled |
| MN26-46786 | 2026 | Hlth Factor/Contact | Medical Necessity | Overturned | 0.62 | $7,630 | 68 | 6 | $4,877 | 6 | settled |
| MN03-3176 | 2003 | Skin Disorders | Medical Necessity | Overturned | 0.62 | $4,586 | 68 | 6 | $2,931 | 6 | settled |
| MN25-45446 | 2025 | CNS/Neuromusc Dis | Medical Necessity | Overturned | 0.62 | $6,108 | 68 | 6 | $3,904 | 6 | settled |
| MN23-39616 | 2023 | Endocrine/Metabolic | Medical Necessity | Overturned | 0.62 | $6,227 | 68 | 6 | $3,980 | 6 | settled |
| MN25-43455 | 2025 | Orth/Musculoskeletal | Medical Necessity | Overturned | 0.62 | $8,366 | 68 | 6 | $5,347 | 6 | settled |
| MN17-24472 | 2017 | Skin Disorders | Medical Necessity | Overturned | 0.62 | $8,167 | 68 | 6 | $5,220 | 6 | settled |
| MN26-46672 | 2026 | Skin Subcutaneous | Medical Necessity | Overturned | 0.62 | $4,142 | 68 | 6 | $2,647 | 6 | settled |
| MN25-44592 | 2025 | Mental Disorder | Medical Necessity | Overturned | 0.62 | $6,199 | 68 | 6 | $3,962 | 6 | settled |
| MN09-9288 | 2009 | Mental Disorder | Medical Necessity | Overturned | 0.62 | $6,688 | 68 | 6 | $4,274 | 6 | settled |
| MN18-29634 | 2018 | Orth/Musculoskeletal | Medical Necessity | Overturned | 0.62 | $6,123 | 68 | 6 | $3,913 | 6 | settled |
| EI10-11925 | 2010 | Orth/Musculoskeletal | Experimental | Overturned | 0.62 | $4,244 | 68 | 6 | $2,712 | 6 | settled |
| EI20-34023 | 2020 | CNS/Neuromusc Dis | Experimental | Overturned | 0.62 | $5,812 | 68 | 6 | $3,715 | 6 | settled |
| EI15-19876 | 2015 | Cardiac/Circ Problem | Experimental | Overturned | 0.62 | $7,201 | 68 | 6 | $4,603 | 6 | settled |
| EI08-8455 | 2008 | Cancer | Experimental | Overturned | 0.62 | $9,450 | 68 | 6 | $6,041 | 6 | settled |
| EI22-37541 | 2022 | Ears/Nose/Throat | Experimental | Overturned | 0.62 | $3,890 | 68 | 6 | $2,486 | 6 | settled |
| EI19-31208 | 2019 | Digestive System/GI | Experimental | Overturned | 0.62 | $5,670 | 68 | 6 | $3,624 | 6 | settled |
| EI14-17233 | 2014 | Mental Disorder | Experimental | Overturned | 0.62 | $4,980 | 68 | 6 | $3,183 | 6 | settled |
| EI21-35890 | 2021 | Orth/Musculoskeletal | Experimental | Overturned | 0.62 | $6,540 | 68 | 6 | $4,180 | 6 | settled |
| EI16-22145 | 2016 | Cancer | Experimental | Overturned | 0.62 | $8,120 | 68 | 6 | $5,190 | 6 | settled |
| EI07-7120 | 2007 | CNS/Neuromusc Dis | Experimental | Overturned | 0.62 | $3,450 | 68 | 6 | $2,205 | 6 | settled |
| EI18-28901 | 2018 | Skin Disorders | Experimental | Overturned | 0.62 | $5,230 | 68 | 6 | $3,343 | 6 | settled |
| EI24-41267 | 2024 | Endocrine/Metabolic | Experimental | Overturned | 0.62 | $4,760 | 68 | 6 | $3,043 | 6 | settled |
| MN11-12450 | 2011 | Cardiac/Circ Problem | Medical Necessity | Upheld | 0.28 | $5,890 | 78 | 15 | $3,905 | 8 | settled |
| MN14-18102 | 2014 | Orth/Musculoskeletal | Medical Necessity | Upheld | 0.28 | $7,340 | 78 | 15 | $4,866 | 8 | settled |
| MN19-30567 | 2019 | Cancer | Medical Necessity | Upheld | 0.28 | $9,120 | 78 | 15 | $6,046 | 8 | settled |
| MN06-5890 | 2006 | Mental Disorder | Medical Necessity | Upheld | 0.28 | $3,210 | 78 | 15 | $2,128 | 8 | settled |
| MN21-36234 | 2021 | CNS/Neuromusc Dis | Medical Necessity | Upheld | 0.28 | $6,450 | 78 | 15 | $4,276 | 8 | settled |
| MN12-13890 | 2012 | Digestive System/GI | Medical Necessity | Upheld | 0.28 | $4,780 | 78 | 15 | $3,169 | 8 | settled |
| MN16-21567 | 2016 | Skin Disorders | Medical Necessity | Upheld | 0.28 | $5,340 | 78 | 15 | $3,540 | 8 | settled |
| MN08-7654 | 2008 | Ears/Nose/Throat | Medical Necessity | Upheld | 0.28 | $2,890 | 78 | 15 | $1,916 | 8 | settled |
| MN22-38123 | 2022 | Orth/Musculoskeletal | Medical Necessity | Upheld | 0.28 | $8,670 | 78 | 15 | $5,748 | 8 | settled |
| MN04-4123 | 2004 | Cancer | Medical Necessity | Upheld | 0.28 | $7,890 | 78 | 15 | $5,231 | 8 | settled |
| MN10-10865 | 2010 | CNS/Neuromusc Dis | Medical Necessity | Upheld | 0.28 | $3,975 | 78 | 15 | $2,635 | 8 | settled |
| MN10-11572 | 2010 | Post Surgical Comp | Medical Necessity | Upheld | 0.28 | $4,257 | 78 | 15 | $2,822 | 8 | settled |
| MN15-20737 | 2015 | Mental Disorder | Medical Necessity | Upheld | 0.28 | $4,398 | 78 | 15 | $2,915 | 8 | settled |
| EI13-15445 | 2013 | Cancer | Experimental | Upheld | 0.28 | $8,263 | 78 | 15 | $5,478 | 8 | settled |
| EI02-838 | 2002 | OB-GYN/Pregnancy | Experimental | Upheld | 0.28 | $5,469 | 78 | 15 | $3,625 | 8 | settled |
| EI11-13230 | 2011 | CNS/Neuromusc Dis | Experimental | Upheld | 0.28 | $4,117 | 78 | 15 | $2,729 | 8 | settled |
| EI10-11416 | 2010 | Orth/Musculoskeletal | Experimental | Upheld | 0.28 | $3,052 | 78 | 15 | $2,023 | 8 | settled |
| EI03-2606 | 2003 | Infectious Disease | Experimental | Upheld | 0.28 | $5,365 | 78 | 15 | $3,556 | 8 | settled |
| EI23-39332 | 2023 | CNS/Neuromusc Dis | Experimental | Upheld | 0.28 | $6,594 | 78 | 15 | $4,371 | 8 | settled |
| EI09-10305 | 2009 | Orth/Musculoskeletal | Experimental | Upheld | 0.28 | $3,976 | 78 | 15 | $2,636 | 8 | settled |
| EI10-11386 | 2010 | CNS/Neuromusc Dis | Experimental | Upheld | 0.28 | $6,410 | 78 | 15 | $4,249 | 8 | settled |
| EI03-2660 | 2003 | CNS/Neuromusc Dis | Experimental | Upheld | 0.28 | $4,482 | 78 | 15 | $2,971 | 8 | settled |
| EI25-43830 | 2025 | Ears/Nose/Throat | Experimental | Upheld | 0.28 | $8,995 | 78 | 15 | $5,963 | 8 | settled |
| EI20-33977 | 2020 | Cancer | Experimental | Upheld | 0.28 | $6,047 | 78 | 15 | $4,009 | 8 | settled |
| EI10-10803 | 2010 | Cancer | Experimental | Upheld | 0.28 | $6,984 | 78 | 15 | $4,630 | 8 | settled |

## Policy Constraints Applied (all cases)

- Issue bounds: allowed percentage 50–120, prompt-pay discount 0–25, evidence strength 0–100, escalate flag 0/1
- Step limit (ERISA-style appeal loop proxy): 6 steps if overturn prior > 0.5, else 8 steps
- Reserved values scaled by historical IMR overturn probability for the case
- No free-form offers outside the defined issue space (mechanism-enforced shield)

## How to Look Up Original IMR Data

1. Go to https://wpso.dmhc.ca.gov/imr/
2. Enter the ReferenceID (e.g. `MN13-14640`) in the search
3. Retrieve the full Findings narrative, determination, diagnosis, and treatment categories

Full machine-readable results: `data/simulation_results_50.json`

*Generated October 2026. All ReferenceIDs are real public DMHC IMR cases.*
