# Gremlin Skills catalog

These pages explain when each promoted skill is useful, what authority it has, what it produces, and how it relates to adjacent workflows. Registry-owned fields are generated; the surrounding guidance remains curated.

<!-- BEGIN GENERATED:SKILL-INDEX -->
### Engineering

| Skill | Purpose | Authority |
|---|---|---|
| [audit-compare](audit-compare.md) | Audit a reference project's codebase against an existing project to propose optimizations — unique code patterns, efficiencies, memory management, smart strategies, and more. | read-only |
| [audit-plan](audit-plan.md) | Audit one or more reference projects and create a proposal for a new project implementation — rewrites, ports, or combinations of features from multiple projects into one new codebase. | read-only |
| [brainstormpro](brainstormpro.md) | Audit a codebase through the lens of a user's outcome, propose distinct evidence-grounded ideas with trade-offs and validation experiments, let the user choose, and hand the approved proposal to Planpro or Goalpro. | read-only |
| [compact-history](compact-history.md) | Audits, verifies, summarizes, and archives accumulated agent-work history while preserving unfinished initiatives and extracting actionable follow-up work. | executor |
| [documentation-audit](documentation-audit.md) | Deeply audits project documentation, verifies it against implementation and history, classifies drift and implementation state, and produces a Goalpro-ready cleanup and restructuring plan. | read-only |
| [feature-clone](feature-clone.md) | Extract a feature from an existing app into transposable documentation — a stack-agnostic spec plus reference-implementation notes — that lets another agent implement the same feature in a different project. | read-only |
| [feature-goal](feature-goal.md) | Drive implementation of a feature from a Feature Clone stage using a Plan→Do→Verify loop with Jira-style acceptance criteria, looping until every criterion is met. | executor |
| [goalpro](goalpro.md) | Relentlessly drive toward a goal from a plan or instruction set through a Plan→Do→Verify loop with Jira-style acceptance criteria, looping until every criterion is met. | executor |
| [migratepro](migratepro.md) | Rewrite an existing codebase in a new stack one module at a time, keeping the app shippable throughout. | executor |
| [planpro](planpro.md) | Take a simple feature request, do a deep dive on the existing codebase, and write a detailed phased plan with project-specific implementation notes. | read-only |
| [releasepro](releasepro.md) | Prepare a release by classifying changes, selecting a repository-compatible version, verifying the exact release state, updating release artifacts, committing, tagging, and optionally pushing exact refs. | executor |
| [restructure](restructure.md) | Reorganize a project's filesystem to be coherent and logical — aligning naming, locations, and module boundaries to detected conventions plus language/framework best practices. Includes a minor opportunistic refactor pass (splits, re-homing functions) required by the moves. | executor |
| [testpro](testpro.md) | Audits an existing test suite and, only when improvement is explicitly requested or approved, builds missing test infrastructure and closes gaps through a Plan→Do→Verify loop. | hybrid |
| [workspacepro](workspacepro.md) | Audits and codifies a master software workspace containing multiple related repositories, shared knowledge, references, utilities, and agent guidance, then produces a detailed Goalpro-ready reorganization plan. | read-only |

### Experience

| Skill | Purpose | Authority |
|---|---|---|
| [design-direction](design-direction.md) | Defines and documents an evidence-backed visual and interaction direction for a new product, major new surface, or intentional redesign before implementation. | read-only |
| [design-review](design-review.md) | Reviews a bounded UI or motion change—such as a diff, pull request, route, component, or completed implementation slice—against approved design intent, semantic tokens, component recipes, accessibility, responsive behavior, and perceptual motion quality, then returns an evidence-backed verdict. | read-only |
| [designpro](designpro.md) | Audits a web application's visual craft, design-system consistency, accessibility, token architecture, component usage, themes, and automated enforcement, then produces a detailed Goalpro-ready remediation plan. | read-only |
| [gamepro](gamepro.md) | Builds or resumes a game through visible playable milestones, from First Playable to MVP, V1, and an optional Release Candidate, using a persistent Plan→Do→Verify loop. | executor |
| [landing-page](landing-page.md) | Designs conversion-focused landing pages and optionally implements an approved preview through product-truth discovery, messaging approval, adaptive HTML previews, humanized copy, SEO, purposeful TurbulenceJS motion, and integrated verification. | hybrid |
| [motion-audit](motion-audit.md) | Audits an existing application's motion and interaction system for purpose, frequency, response, spatial continuity, interruption, gesture physics, performance, accessibility, cohesion, tokens, missed opportunities, and TurbulenceJS migration, then produces an evidence-backed remediation handoff. | read-only |
| [motion-direction](motion-direction.md) | Art-directs a TurbulenceJS-first motion language for an application, compares two or three coherent animation directions in an interactive synthetic Motion Direction Studio, and turns the approved direction into an enforceable policy for current and future pages, components, and states. | read-only |
| [onboarding-audit](onboarding-audit.md) | Audits an existing web or mobile onboarding experience against product evidence, activation goals, platform-specific UX, accessibility, trust, copy, measurement, and user-success principles, then produces a prioritized report and canonical input for Onboarding Direction. | read-only |
| [onboarding-direction](onboarding-direction.md) | Defines and documents an evidence-backed onboarding direction for web, native mobile, or cross-platform products, optimizing activation, time-to-value, user success, trust, and progressive mastery before implementation. | read-only |
| [prose-humanizer](prose-humanizer.md) | Rewrites user-facing prose to sound natural, specific, and human while preserving facts, meaning, voice, markup, and code behavior. | executor |
| [theme-library](theme-library.md) | Selects and creatively adapts bundled Gremlin palette families into product-fit theme briefs without requiring a full visual-direction exercise. | read-only |
| [turbulencejs-integration](turbulencejs-integration.md) | Selects and integrates TurbulenceJS motion into web and Electron projects, including entrypoints, visual style, intensity, accessibility, lifecycle, and verification. | executor |
| [turbulencejs-presentation](turbulencejs-presentation.md) | Plans, art-directs, builds, and verifies browser-native TurbulenceJS presentations that deliberately support 16:9 and 9:16. | executor |

### Growth

| Skill | Purpose | Authority |
|---|---|---|
| [email-lifecycle-audit](email-lifecycle-audit.md) | Audits an implemented post-signup lifecycle email system against product outcomes, campaign logic, data integrity, consent, deliverability, accessibility, copy, operations, and incremental measurement, then produces a prioritized report and canonical input for Email Lifecycle Strategy. | read-only |
| [email-lifecycle-strategy](email-lifecycle-strategy.md) | Defines and documents an evidence-backed post-signup lifecycle email strategy that advances activation, repeated value, adoption, retention, and respectful re-engagement while protecting consent, deliverability, accessibility, and inbox trust before implementation. | read-only |
| [seo-content](seo-content.md) | Executes one approved SEO content brief at a time by validating upstream ownership, researching primary sources, locking claims, drafting and humanizing copy, implementing it through project conventions, and verifying search, accessibility, build, rendering, and published behavior. | executor |
| [seo-foundation](seo-foundation.md) | Builds an evidence-backed SEO foundation by discovering and confirming business and organic competitors, inspecting their page strategies, sampling Google and Bing results, combining first-party queries with Google Ads Keyword Planner demand, and assigning keyword clusters to page owners. | read-only |
| [seo-indexing](seo-indexing.md) | Runs a guarded post-publication indexing-assistance loop that discovers new or materially updated canonical pages, verifies live crawl and index readiness, prioritizes an approved batch, requests Google indexing through supported signed-in computer use or an eligible restricted API, and records immutable receipts. | executor |
| [seo-monitor](seo-monitor.md) | Runs a read-only SEO learning loop by collecting compatible GA4, Google Search Console, Bing, crawl/index, content-receipt, and page-ownership evidence; comparing approved baselines and mature windows; protecting winners; and routing measured exceptions without reactive rewrites. | read-only |
| [seo-setup](seo-setup.md) | Establishes and verifies the technical, analytics, search-console, and keyword-research prerequisites required by an SEO program through guarded source changes, APIs, or signed-in computer use. | executor |
| [seo-strategy](seo-strategy.md) | Turns verified SEO setup and an approved competitive, keyword-demand, cluster, and page-ownership foundation into a prioritized, non-cannibalizing portfolio plan for search-targeted landing pages and editorial content. | read-only |
| [stripe-audit](stripe-audit.md) | Audits Stripe Billing and subscription implementations in Next.js applications and produces a goalpro-ready remediation package. | read-only |
<!-- END GENERATED:SKILL-INDEX -->
