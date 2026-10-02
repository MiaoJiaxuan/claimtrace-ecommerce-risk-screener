# Workflow illustration

`claimtrace-evidence-flow.svg` depicts a claim moving through case retrieval to a screening result or human review. The illustration uses local vector shapes with no external image, font or logo dependencies. The bilingual interface supplies its accessible description.

## English case display

`case-summaries-en.json` provides English display titles and summaries for all 30 records in `data/sources.csv`, keyed by case ID. These are project summaries, not official English case titles. The interface preserves the original Chinese text in expandable source cards. Retrieval, model inputs, citation validation and saved evaluation records use the original corpus.
