# ClaimTrace: Problem Statement

Miao Jiaxuan | PE6201

## Problem and user

Small Chinese e-commerce sellers need to review product advertising before publication. A prohibited-word list can catch explicit cure promises or superlatives, but it provides little evidence for interpreting claims about price, performance or product effects. Sellers without dedicated compliance support need a short, traceable review that identifies the wording at issue and points to relevant public enforcement cases.

The design draws on product-copy editing work involving a company prohibited-word list followed by supervisor review. The proposed benefit is less time spent finding relevant evidence and preparing questions for a reviewer. Seller interviews and timed observations are needed to measure that benefit.

## Proposed workflow

A seller submits one Chinese product claim. ClaimTrace runs an independent keyword baseline, retrieves related case summaries and checks whether retrieval support reaches a provisional threshold. With sufficient retrieval support, one language-model request produces a structured risk card: risk level, exact highlighted wording, reasoning, cited source and recommended next action. Weak evidence produces an abstention and a request for human review.

The application supports preparation for a publication decision. It does not verify the seller's product records or issue legal approval.

## Data and evaluation

The project uses 30 public enforcement-case summaries and 90 labelled claims, divided into 60 development and 30 locked test items. Case-derived and synthetic examples are reported separately. The rules and full pipeline are compared on the same frozen test labels.

The intended combined-class recall target is 80% for `high_risk` plus `evidence_needed`. Precision is reported alongside recall, with class counts, coverage and abstention rate. Retrieval relevance and citation support are also reviewed manually. The [final report](BUSINESS_TECHNICAL_TRADEOFF_EN.pdf) analyses the observed results, including the combined recall of 68%, missing `evidence_needed` predictions and remaining evaluation gaps.
