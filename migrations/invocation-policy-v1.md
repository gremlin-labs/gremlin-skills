# Invocation policy owner review

- Status: `approved`
- Proposal SHA-256: `0b1ac09e7a4674ca56ed4138df2735a01084d952480ba98f6a5fc61b78036e88`
- Recommendation: 24 model-visible; 12 user-only
- Public registry and host metadata match this approved matrix.
- Invocation does not grant authority; every existing approval and external-action gate remains in force.

## Matrix

| Skill | Proposed mode | Authority | Required composition | Optional complements | Rationale |
|---|---|---|---|---|---|
| `audit-compare` | **model-visible** | read-only; source never; external none | — | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `audit-plan` | **model-visible** | read-only; source never; external none | audit-compare (reference, model-visible) | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `brainstormpro` | **model-visible** | read-only; source never; external none | planpro (handoff, model-visible) | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `compact-history` | **user-only** | executor; source never; external none | — | theme-library | Housekeeping executor can relocate managed artifacts after confirmation, so the human must name it. |
| `design-direction` | **model-visible** | read-only; source never; external none | — | goalpro, planpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `design-review` | **model-visible** | read-only; source never; external none | — | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `designpro` | **model-visible** | read-only; source never; external none | — | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `documentation-audit` | **model-visible** | read-only; source never; external none | — | theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `email-lifecycle-audit` | **model-visible** | read-only; source never; external none | email-lifecycle-strategy (handoff, model-visible) | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `email-lifecycle-strategy` | **model-visible** | read-only; source never; external none | prose-humanizer (embedded, model-visible) | goalpro, planpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `feature-clone` | **model-visible** | read-only; source never; external none | — | theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `feature-goal` | **user-only** | executor; source task-scoped; external none | goalpro (reference, user-only) | theme-library | Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it. |
| `gamepro` | **user-only** | executor; source task-scoped; external none | — | theme-library | Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it. |
| `goalpro` | **user-only** | executor; source task-scoped; external none | — | theme-library | Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it. |
| `landing-page` | **model-visible** | hybrid; source after-approval; external none | prose-humanizer (embedded, model-visible), seo-strategy (context, model-visible) | theme-library, turbulencejs-integration | Page specialist begins read-only, requires exact approval before source mutation, and must remain auto-discoverable for operational pipeline routing. |
| `migratepro` | **user-only** | executor; source task-scoped; external none | — | theme-library | Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it. |
| `motion-audit` | **model-visible** | read-only; source never; external none | — | goalpro, motion-direction, planpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `motion-direction` | **model-visible** | read-only; source never; external none | — | goalpro, planpro, theme-library, turbulencejs-integration | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `onboarding-audit` | **model-visible** | read-only; source never; external none | onboarding-direction (handoff, model-visible) | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `onboarding-direction` | **model-visible** | read-only; source never; external none | prose-humanizer (embedded, model-visible) | goalpro, planpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `planpro` | **model-visible** | read-only; source never; external none | — | theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `prose-humanizer` | **model-visible** | executor; source task-scoped; external none | seo-strategy (context, model-visible) | theme-library | Bounded task-scoped transformation with no external action; useful as an explicitly embedded primitive. |
| `releasepro` | **user-only** | executor; source after-approval; external approval-required | — | theme-library | Workflow can change external state and retains a second action approval gate after explicit invocation. |
| `restructure` | **user-only** | executor; source task-scoped; external none | — | theme-library | Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it. |
| `seo-content` | **model-visible** | hybrid; source after-approval; external approval-required | prose-humanizer (embedded, model-visible), seo-strategy (context, model-visible) | seo-indexing, seo-monitor, theme-library | Page specialist begins read-only, requires exact approval before source mutation, and must remain auto-discoverable for operational pipeline routing. |
| `seo-foundation` | **model-visible** | read-only; source never; external none | — | seo-strategy, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `seo-indexing` | **user-only** | executor; source never; external approval-required | — | seo-monitor, theme-library | Workflow can change external state and retains a second action approval gate after explicit invocation. |
| `seo-monitor` | **model-visible** | read-only; source never; external none | — | theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `seo-setup` | **user-only** | executor; source after-approval; external approval-required | — | seo-foundation, theme-library | Workflow can change external state and retains a second action approval gate after explicit invocation. |
| `seo-strategy` | **model-visible** | read-only; source never; external none | — | goalpro, landing-page, seo-content, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `stripe-audit` | **model-visible** | read-only; source never; external none | — | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `testpro` | **user-only** | hybrid; source after-approval; external none | — | theme-library | Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it. |
| `theme-library` | **model-visible** | read-only; source never; external none | — | goalpro, planpro | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |
| `turbulencejs-integration` | **user-only** | executor; source task-scoped; external none | — | theme-library | Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it. |
| `turbulencejs-presentation` | **user-only** | executor; source task-scoped; external none | — | theme-library | Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it. |
| `workspacepro` | **model-visible** | read-only; source never; external none | — | goalpro, theme-library | Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action. |

## Composition meanings

- `handoff`: the upstream read-only stage may invoke the named model-visible downstream stage while preserving the same slug.
- `embedded`: the caller uses the model-visible primitive while retaining artifact ownership.
- `reference`: the caller inherits authoritative instructions or contracts; it does not implicitly invoke the dependency.
- `context`: the caller validates and preserves an upstream decision; it does not delegate its own task.
- Optional complements are discoverable integrations or handoffs, never hidden required cross-package behavior.

## Approval boundary

Approval must identify the proposal SHA above. Applying it will be a separate change that updates the canonical registry and generated Claude/Codex metadata together; partial approval is not applied silently.
