# Profile Outputs

This folder stores generated writing profiles. The `current.md` files are created after corpus ingestion and mining.

Expected outputs:

```text
profiles/author_style/current.md
profiles/journal_style/current.md
profiles/topic_style/current.md
profiles/domain_style/current.md
```

Use `profiles/domain_style/current.md` only as a legacy combined profile. New workflows should prefer:

```text
profiles/author_style/current.md
profiles/journal_style/current.md
profiles/topic_style/current.md
working/intro_reference_map.md
```

Do not paste current manuscript results into profile files. Put current facts in `working/current_manuscript_brief.md`, `working/evidence_packet.md`, or the live prompt.
