# ClaimTrace Label Guide

## Purpose

This document defines the labels used to evaluate Chinese e-commerce advertising claims. Labels are assigned manually before the final test is run.

## Ground-truth labels

### high_risk

The claim contains a clearly prohibited, absolute or strongly misleading expression, or closely matches a confirmed enforcement case.

Examples include unsupported expressions such as "国家级", "最高级", "销量第一" or guaranteed medical effects.

### evidence_needed

The claim may be acceptable only if the seller can provide adequate and verifiable supporting evidence.

Examples include performance comparisons, price claims, sales rankings or product-effect claims that depend on supporting records.

### low_risk

The claim does not contain an obvious risky expression and does not require special supporting evidence under the limited project scope.

This label does not mean legal approval.

## System abstention

### insufficient_evidence

This is a system output, not a ground-truth label.

The system returns this result when the retrieved evidence is too weak to support a reliable assessment. The claim must then be sent for human review.

The system must not return low_risk when retrieval evidence is below the selected threshold.