# Audit-compare — Comprehensive Checklist

Scan BOTH codebases against every dimension. Cite file:line for every observation. Don't skip a dimension because it "looks fine" — verify.

## 0. Product intent and adoption fit

- Apply [Planpro's product-research lens](contracts/product-research.md) to the target project.
- Identify the user/problem, desired outcome, guardrail, operating model, and explicit architectural trade-offs.
- For every proposed adoption, state the product outcome, evidence, added complexity, operational burden, reversibility, and cheapest validation.
- Reject patterns that are impressive in the reference but misaligned with the target's needs.

## 1. Code patterns & conventions

- Naming consistency (files, types, functions, variables)
- File/module organization — single-responsibility vs god-files
- Repeated logic that should be shared (DRY opportunities)
- Error handling style — consistent? swallowed? typed?
- Idiomatic use of the language (vs carrying over patterns from another stack)
- Comment quality — explanatory of *why*, not *what*

## 2. Performance & efficiency

- Hot paths — algorithmic complexity, needless allocations
- Caching strategies (memoization, response caching, layered caches)
- Async/concurrency patterns — parallelism vs serialization, batching
- Database/query patterns — N+1, missing indexes, eager vs lazy load
- Lazy initialization, startup time, cold-path cost
- Resource pooling (connections, threads, objects)

## 3. Memory & resource management

- Allocation patterns — reuse vs churn, buffer sizing
- Lifecycle management — ownership, RAII, dispose patterns
- Leak vectors — unclosed handles, lingering references, event listeners
- Backpressure — what happens when queues/buffers fill
- Streaming vs materializing — large payloads, files, responses

## 4. Error handling & resilience

- Error taxonomy — typed errors, sentinel vs exception vs Result
- Recovery strategies — retry, circuit breakers, dead-letter queues
- Partial failure handling — what happens when one step in a pipeline fails
- Validation — where, how strict, fail-fast vs collect-all
- Observability of errors — structured logging, correlation IDs, stack preservation

## 5. Security

- Input validation at trust boundaries
- Authn/authz checks — where, how enforced, bypass paths
- Secret handling — hardcoded, env, rotation, leakage in logs
- Dependency vulnerabilities — pinned versions, audit tools
- Attack surface — unnecessary endpoints, exposed internals, default-deny

## 6. Testing strategy

- Coverage of critical paths (not just line coverage)
- Test pyramid — unit/integration/e2e balance
- Test independence — shared state, ordering dependencies
- Fakes vs mocks vs real dependencies (contract tests)
- Property-based / fuzz testing where applicable
- Test performance — can the suite run in under a minute?

## 7. API & interface design

- Consistency of public interfaces (naming, arity, return shapes)
- Versioning strategy — breaking vs additive changes
- Error contracts — predictable codes/shapes to consumers
- Pagination / streaming for large result sets
- Documentation — is the interface self-describing?

## 8. Dependency hygiene

- Unnecessary dependencies — vendored or reimplemented elsewhere
- Version pinning and update cadence
- Transitive dependency risk
- Duplicate functionality across deps (two HTTP clients, two loggers)
- Build-time vs runtime deps clearly separated

## 9. Observability & operations

- Logging — structured, leveled, contextual
- Metrics — what's measured, what should be
- Tracing — request-scoped, cross-service where applicable
- Health checks & readiness probes
- Debuggability — can you reconstruct a production failure from artifacts?

## 10. Architecture & module boundaries

- Coupling — do modules talk through clean interfaces or directly?
- Direction of dependencies (deps point inward/downward, no cycles)
- Replaceability — could you swap one module for another without rippling?
- Configuration vs code — secrets, env, feature flags
- Where the feature should naturally live in this project (vs where reference put it)
