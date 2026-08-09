# Prose Humanizer Reference

## Contents

- [Humanization standard](#humanization-standard)
- [Voice calibration](#voice-calibration)
- [Pattern taxonomy](#pattern-taxonomy)
- [False positives and human signals](#false-positives-and-human-signals)
- [Structured-file protections](#structured-file-protections)
- [User-facing source inventory](#user-facing-source-inventory)
- [Marketing and landing-page mode](#marketing-and-landing-page-mode)
- [SEO-aware rewriting](#seo-aware-rewriting)
- [Broad and high-stakes review](#broad-and-high-stakes-review)
- [Rewrite and verification procedure](#rewrite-and-verification-procedure)
- [Artifact schemas](#artifact-schemas)
- [Worked examples](#worked-examples)
- [Quality matrix](#quality-matrix)
- [Foundation and maintenance](#foundation-and-maintenance)

## Humanization standard

Humanization improves the relationship between a real writer and a real reader. It is not a filter that mechanically removes punctuation or replaces a list of words.

A successful rewrite:

- preserves information, claims, uncertainty, intent, and scope while allowing paragraph and sentence shape to change;
- uses concrete source detail and direct constructions where they improve meaning;
- matches audience, medium, and author voice;
- varies cadence naturally rather than manufacturing punchlines;
- removes formulaic inflation, filler, and fake authority;
- retains technical terms, brand language, personality, and formatting that serve the reader;
- leaves code, markup, data, and behavior intact;
- can conclude that a passage already sounds human and should remain unchanged.

“Human-written” is not synonymous with casual, quirky, imperfect, short, or opinionated. Neutral reference prose can be the correct human voice.

## Voice calibration

When a user provides a sample, record:

| Dimension | Evidence to notice |
|---|---|
| Sentence rhythm | Typical range, deliberate fragments, long/short alternation |
| Vocabulary | Plain versus technical, contractions, repeated preferred terms |
| Paragraphing | Dense argument, short web blocks, narrative buildup, list use |
| Openings and transitions | Direct starts, connective phrases, questions, scene setting |
| Punctuation | Parentheses, colons, dashes, semicolons, quotation style |
| Personality | Humor, skepticism, warmth, authority, mixed feelings, restraint |
| Register | Casual, editorial, technical, academic, policy, marketing |
| Deliberate irregularities | Repetition, sentence fragments, slang, unusual capitalization |

Match observed habits rather than normalizing them. A sample may justify punctuation or structures that generic detectors often flag. Factual and structural safety still outrank voice imitation.

Without a sample, use approved neighboring prose and the content's job. Do not infer a personal identity, demographic, dialect, or lived experience from weak evidence.

## Pattern taxonomy

Use this table diagnostically. Change a passage when patterns cluster and harm meaning, credibility, or voice. Do not run a global substitution list.

| # | Pattern | Diagnostic | Editing move |
|---|---|---|---|
| 1 | Inflated significance | Ordinary facts are framed as historic, pivotal, or symbolic | State the concrete fact and supported consequence |
| 2 | Notability dumping | Media names, awards, or follower counts substitute for relevance | Keep only evidence with contextual value |
| 3 | Superficial participle analysis | Trailing `-ing` phrases pretend to explain meaning | Remove them or state the real causal relationship |
| 4 | Generic promotional language | Superlatives and atmospheric praise lack product evidence | Name the capability, mechanism, or observed result |
| 5 | Vague authority | “Experts” or “reports” appear without an identifiable source | Name the source or remove the attribution/claim |
| 6 | Formulaic challenge/future sections | A stock obstacle paragraph resolves into optimism | Keep sourced constraints and concrete next actions |
| 7 | AI-coded vocabulary clusters | Abstract prestige words recur without precision | Prefer the clearest ordinary or domain-specific term |
| 8 | Avoiding `is`, `are`, or `has` | “Serves as,” “features,” and “boasts” inflate simple facts | Use direct copulas when they are clearer |
| 9 | Negative parallelism | “Not just X, but Y” or trailing “no guessing” performs contrast | State the positive claim and relationship directly |
| 10 | Forced triples | Ideas are padded into groups of three for cadence | Use the natural number of items |
| 11 | Synonym cycling | One entity receives needless alternate names | Repeat the clearest established term |
| 12 | False ranges | “From X to Y” joins items that are not a real continuum | Name the actual topics or stages |
| 13 | Hidden actors and fragments | Passive or subjectless copy obscures who acts | Name the actor when it improves clarity |
| 14 | Dash dependence | Dashes repeatedly carry structure or manufactured emphasis | Use the author's punctuation habits or restructure |
| 15 | Mechanical bolding | Emphasis decorates predictable nouns or every list lead | Keep emphasis only where scanning truly needs it |
| 16 | Inline-header list boilerplate | Every bullet begins with a bold label and restatement | Use prose or a list whose items add information |
| 17 | Automatic title case | Headings use title case without brand/editorial reason | Follow the surrounding style and author preference |
| 18 | Decorative emoji | Icons manufacture energy or label routine sections | Keep only meaningful, voice-consistent symbols |
| 19 | Quote-style normalization | Typography is changed merely because a detector dislikes it | Preserve source/editorial rules unless asked |
| 20 | Chatbot residue | Offers to continue, praise, or assistant framing enter content | Start with the actual content and remove correspondence |
| 21 | Cutoff or gap filler | Missing knowledge becomes disclaimer paragraphs or guesses | State a precise known limitation or omit the passage |
| 22 | Sycophancy | Praise and agreement replace useful content | Respond or write directly |
| 23 | Filler phrases | Wordy constructions add no meaning | Use the shorter accurate construction |
| 24 | Stacked hedging | Multiple qualifiers obscure the intended confidence | Keep the one qualifier that matches evidence |
| 25 | Generic positive ending | The piece closes with unspecific optimism | End on the final concrete fact, decision, or action |
| 26 | Uniform compound hyphenation | Every compound is treated identically regardless of grammar/style | Follow grammatical position and project style |
| 27 | Authority theater | “The real question” or “at its core” pretends at revelation | State the claim and supporting reason |
| 28 | Signposting announcement | “Let's explore” delays the content it announces | Begin with the substance |
| 29 | Heading restatement | A one-line paragraph repeats the heading before detail begins | Delete the warm-up and retain meaningful content |
| 30 | Diff-anchored prose | Current documentation narrates that something “was added” | Describe how the current system behaves |
| 31 | Manufactured staccato | Runs of tiny sentences stage drama without clarity | Combine related ideas and restore natural rhythm |
| 32 | Aphorism formula | “X is the language/currency/architecture of Y” replaces explanation | State the concrete relationship |
| 33 | Fake-candid opener | “Honestly?” or “Here's the thing” performs intimacy | Say the actual answer directly |

Names and numbers in examples, quotations, titles, and discussions of these patterns are secondhand text. Do not rewrite the quoted object merely because it contains a watched phrase.

## False positives and human signals

Do not flag these alone:

- Correct grammar, consistent style, formal vocabulary, or complex formatting.
- A mixed casual and technical register.
- One transition word, em dash, curly quote, short sentence, rhetorical question, or group of three.
- Letter salutations and sign-offs.
- Unsourced prose, which may be weak evidence but does not prove AI authorship.
- Text whose exact style predates or intentionally imitates a known source.

Preserve strong human signals:

- specific, unusual, source-supported detail;
- unresolved tension or mixed feelings;
- an opinion the writer can explain;
- varied sentence lengths and nonuniform paragraph rhythm;
- genuine asides, corrections, and domain idioms;
- time- and community-specific references appropriate to the audience;
- purposeful repetition and recurring vocabulary;
- restraint, including the choice not to dramatize a point.

When in doubt, compare pattern clusters with the voice sample and reader outcome. Over-editing authentic prose is a failure.

## Structured-file protections

### Markdown and MDX

Eligible by default: headings, paragraphs, list prose, blockquotes when paraphrase is authorized, table cell prose, captions, and visible link labels.

Protect by default: frontmatter keys and structured values, fenced/inline code, URLs, anchors, reference IDs, imports/exports, JSX expressions, component names/props, directives, shortcode syntax, generated API signatures, and exact quotations/citations.

Run the repository's Markdown/MDX parser or docs build when available. Verify heading anchors and relative links after heading edits.

### HTML

Eligible: visible text nodes, headings, labels, descriptions, alt text, titles, validation, and accessible names when their meaning remains accurate.

Protect: element/attribute structure, IDs, classes, `data-*`, scripts, styles, URLs, form names/values, ARIA relationships, template tokens, microdata/RDFa attributes, and JSON-LD shape. Parse or render after edits.

### JSX and TSX

Eligible: literal child text and user-visible string props such as labels, descriptions, empty states, errors, tooltips, alt text, and metadata.

Protect: imports, identifiers, component/prop names, expressions, conditions, event handlers, keys, route values, analytics IDs, test IDs, types, translation keys, interpolation, and whitespace whose rendering is intentional. Preserve apostrophe/quote escaping and JSX entity behavior.

Run formatter, typecheck, lint, tests, build, and rendered assertions applicable to the touched components.

### Templates and localization

Eligible: user-visible prose surrounding tokens.

Protect: delimiters, variables, filters, conditions, loops, HTML escaping, ICU plural/select syntax, printf-style specifiers, email headers, and localization keys. Preserve every placeholder exactly and verify each locale or template compiler affected.

Do not rewrite translated locales independently unless the user requests translation/localization work. Humanize the source locale and flag downstream localization impact.

### JSON YAML and structured data

Treat as out of scope by default. User-visible values may be edited only with an exact schema-aware scope and a parser/serializer or validation gate. Never rename keys or reformat unrelated data.

## User-facing source inventory

For a site or application, search broadly and classify narrowly. Candidate locations include:

- route/page components and content modules;
- Markdown/MDX/docs sources;
- localization catalogs and template files;
- email, notification, onboarding, help, error, empty, loading, and success copy;
- metadata, Open Graph descriptions, alt text, captions, tooltips, and ARIA labels;
- CMS seed content, fixtures, or JSON only when they are canonical user-facing sources.

Create an inventory with `ELIGIBLE`, `PROTECTED`, `REVIEW REQUIRED`, or `OUT OF SCOPE`. A search match is not authorization to rewrite it. Exclude generated output, vendored code, lockfiles, build artifacts, snapshots not explicitly in scope, and third-party text.

## Marketing and landing-page mode

Marketing copy has a legitimate persuasive job. Do not transform it into encyclopedic prose merely because promotional language appears.

Preserve:

- approved audience and conversion intent;
- exact product and category terminology;
- supportable enthusiasm, contrast, and brand personality;
- clear benefit framing tied to a real mechanism;
- outcome-specific CTA labels and necessary urgency/proof.

Challenge:

- superlatives, universals, guarantees, urgency, scarcity, numbers, comparisons, and social proof without sources;
- abstract claims that hide the product;
- interchangeable slogans, forced triples, and “future is bright” endings;
- confident benefits that exceed the documented mechanism.

Embedded callers must supply an approved claims source. Return an unresolved ambiguity instead of making the copy smoother by strengthening it.

## SEO-aware rewriting

SEO context changes the fidelity surface, not the humanization goal. Copy should still sound natural; it must also remain inside the approved page ownership and intent contract.

### Context hierarchy

Use, in order:

1. SEO owner/intent/claim constraints explicitly supplied by the current caller.
2. The exact approved `seo-strategy` landing or editorial brief and portfolio row.
3. `seo-content` brief validation, claim ledger, and content receipt for one asset.
4. `landing-page` message map and SEO plan for a conversion page.
5. Foundation/Setup evidence only through approved upstream pointers.
6. Inference from current copy, labelled unverified and never used to broaden intent.

Do not search for volume or competitors merely to humanize copy. Do not invoke provider tooling or treat term repetition as an ownership signal.

### Preserve versus rewrite

| SEO-aware element | Default handling |
|---|---|
| Primary page owner, cluster, search intent, user job | Preserve exactly as a semantic constraint |
| Protected winners and overlap exclusions | Preserve; reject copy that creates competing scope |
| Product/entity/category terminology | Preserve approved meaning; vary only when terminology evidence permits |
| Material claims, comparisons, statistics, citations | Preserve evidence, attribution, scope, certainty, dates, and units |
| Title, H1, headings, description, visible schema text | Rewrite only inside the approved intent and claim boundary |
| URL, canonical, robots/index posture, sitemap state, JSON-LD shape | Protected; outside prose-only mutation |
| Internal-link destinations | Protected |
| Internal anchor labels | Eligible only when destination, relationship, and owner intent remain clear |
| Alt text and captions | Eligible when accessibility meaning and entity accuracy remain intact |
| Keyword repetition | No preservation quota; use the clearest natural terminology without erasing necessary domain terms |

### SEO fidelity audit

After rewriting, verify:

- the page still answers the same search/user job and does not broaden into an adjacent cluster;
- title, H1, description, headings, summary, and CTA promises remain mutually consistent;
- no source qualifier, comparison scope, number, date, entity, citation, or update signal changed;
- primary/supporting page roles and internal-link relationships remain legible;
- exact-match repetition was not replaced with vague synonyms that weaken domain accuracy;
- natural variation did not introduce an unapproved keyword, claim, or audience;
- anchors remain truthful descriptions of their destinations;
- heading edits do not break generated anchors or inbound references;
- structured-data-visible text remains consistent with rendered copy;
- the final copy does not promise rankings, traffic, product outcomes, or authority it cannot prove.

If the existing copy conflicts with the approved page-specialist brief or governing SEO opportunity, report the contradiction. Humanization cannot choose which source should win or treat a Strategy opportunity as page-level copy authority.

## Broad and high-stakes review

Review-before-write applies when:

- scope spans a site, docs set, localization catalog, or many templates;
- the source of truth or user-facing/canonical file is ambiguous;
- rewrites may change brand voice or product positioning materially;
- legal, policy, privacy, medical, safety, security, financial, pricing, guarantee, regulated, or accessibility-critical meaning is involved;
- exact quotations, compliance language, contractual language, or approved claims dominate the text.

Create `HUMANIZED.md` with representative or complete candidate content as appropriate. Show the user:

1. Scope and files affected.
2. Voice and editing posture.
3. Representative before/after deltas without reproducing sensitive or very long sources.
4. Claim, legal, placeholder, and structural risks.
5. Exact overwrite boundary.

Approval must name the candidate or unchanged rule set. A material later change requires delta confirmation.

## Rewrite and verification procedure

### Unit loop

1. Read the whole logical unit and its neighbors.
2. Mark protected facts, terms, placeholders, links, and syntax.
3. Record voice evidence.
4. Identify pattern clusters and false positives.
5. Draft while preserving all information.
6. Audit lingering formulaic or generated qualities.
7. Audit new facts, stronger certainty, dropped qualifiers, and changed meaning.
8. Audit syntax and structure.
9. Revise and compare the final result with source.

### File loop

1. Apply changes through a syntax-aware edit where practical.
2. Parse/format the file.
3. Run focused tests or docs checks.
4. Inspect the diff for non-prose edits.
5. Render representative output when copy affects layout, accessibility, or interaction.
6. Log evidence and self-judgment.

### Integrated loop

1. Re-read the full page/document flow rather than isolated strings.
2. Check terminology and voice consistency across files.
3. Verify CTA, error/recovery, navigation, heading, and cross-reference coherence.
4. Run the complete applicable project gate.
5. Reconcile every quality dimension and remaining waiver.

## Artifact schemas

### SCOPE.md

Headings: `Invocation`, `Audience and purpose`, `Source authority`, `Voice evidence`, `Eligible prose`, `Protected structures`, `Risk and approval`, `Project gates`, `Boundaries`.

### PROGRESS.md

```md
## 2026-01-01T12:00:00Z — DONE — Humanize onboarding empty states

- Scope: `src/onboarding/...`
- Fidelity: capabilities and CTA outcomes unchanged
- Structure: JSX parse and placeholders preserved
- Evidence: focused tests, typecheck, rendered empty/error states
- I am satisfied this step is complete because the copy reads naturally in context, every source claim and placeholder matches, and all applicable gates pass.
```

### REWRITE-REPORT.md

Headings: `Scope`, `Voice baseline`, `Pattern clusters`, `Intentional traits preserved`, `Representative decisions`, `Factual and claim fidelity`, `Structural protections`, `Changed files or sections`, `Unchanged or skipped`, `Remaining concerns`.

### QUALITY-REPORT.md

Headings: `Quality report`, `Fidelity evidence`, `Structural and project evidence`, `Rendered or reader-flow evidence`, `Deviations and waivers`, `Final integrated verification`, `Final status`.

## Worked examples

### Technical documentation

Before:

> This powerful capability serves as a crucial cornerstone of the platform, enabling developers to seamlessly manage retries.

After:

> The retry queue lets developers inspect failed jobs and run them again.

The rewrite keeps the mechanism and actor, removes unsupported significance and “seamlessly,” and uses direct verbs.

### Product marketing

Before:

> Unlock a revolutionary workflow that transforms the way your team collaborates.

After when the source proves shared review but not transformation:

> Review drafts together before anything is published.

This remains persuasive because the product action and control are concrete.

### JSX with protected behavior

Before:

```tsx
<EmptyState
  title="Your incredible journey starts here"
  actionLabel="Get started"
  onAction={() => router.push('/imports/new')}
/>
```

Eligible rewrite:

```tsx
<EmptyState
  title="Import your first file"
  actionLabel="Choose a file"
  onAction={() => router.push('/imports/new')}
/>
```

The route, component, prop names, expression, and structure remain unchanged. The new copy is valid only if importing a file is the verified action.

### Intentional voice preserved

Source:

> The setup is fussy. I wish it weren't, but hiding that would waste your time.

Leave it unless the requested voice conflicts. The mixed feeling and direct warning are human and useful.

## Quality matrix

| Dimension | Minimum evidence |
|---|---|
| Factual fidelity | Claim-by-claim comparison; no new or strengthened facts |
| Meaning and completeness | Source information and qualifiers preserved or approved cuts recorded |
| Voice and audience | Sample/neighbor evidence plus full-flow read |
| Naturalness | Cluster-based audit and final cadence pass |
| Structural safety | Parser/format plus placeholder, link, identifier, markup comparison |
| User experience | Labels, actions, errors, recovery, headings, accessibility meaning remain coherent |
| Code health | Applicable type, lint, test, build, and rendered checks |
| Documentation health | Applicable docs build, links, anchors, examples, and navigation |
| Scope discipline | Final diff contains only authorized prose and generated artifacts |
| SEO fidelity when applicable | Approved owner, intent, protected winners, claims, headings/metadata meaning, citations, and link responsibilities preserved |
| Privacy | No sensitive source content copied into reports or chat unnecessarily |
| Rollback | Version-control diff or explicit candidate preserves recoverability |

Final status for each dimension is `VERIFIED`, `NOT APPLICABLE`, or `WAIVED` with explicit provenance. `UNKNOWN` cannot remain at completion.

## Foundation and maintenance

This skill is an original Gremlin Skills adaptation of `blader/humanizer`, which is licensed under MIT and derives its detection approach from Wikipedia's community-maintained observations of AI-writing patterns. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

The adaptation adds Gremlin work artifacts, direct/embedded composition, safe source-code editing, broad/high-stakes approval gates, project verification, marketing-intent preservation, quality evidence, and standalone execution. Maintain the no-fabrication, voice-calibration, cluster/false-positive, and draft-audit-final foundations when updating the taxonomy.
