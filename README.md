# 12-Week Python Backend, AI Integration & MLOps

This repository is a build-in-public learning log. The goal is to learn backend
engineering by growing one useful product in small, reviewable steps—not by
copying a finished tutorial.

## The capstone: Learning Hub

Learning Hub is a multi-tenant API for people and teams to save learning
resources. The longer-term product will add an AI assistant and the operational
work needed to run it reliably. Each milestone should leave the code runnable,
tested, and explained.

## Repository map

- [`Week1_strict_weather/`](./Week1_strict_weather/) — structural typing and a
  pluggable weather provider exercise.
- [`Week2/`](./Week2/) — database schema and SQL practice.
- [`Week3_tenant_api/`](./Week3_tenant_api/) — early tenant API exercise.
- [`capstone/`](./capstone/) — the evolving Learning Hub application.

The curriculum source PDF is kept locally and intentionally excluded from the
public repository.

The existing week folders are kept as learning artifacts. The capstone is a
clean, runnable implementation that will reuse and improve on those ideas.

## Progress

- [x] First vertical slice: accounts, bearer-token login, workspaces, and
  workspace-scoped saved resources
- [x] Automated tests for the main flow and cross-workspace isolation
- [ ] Map each capstone milestone to the exact curriculum week and publish
  weekly learning notes
- [ ] Add resource editing/deletion and membership management
- [ ] Add the AI assistant behind a provider interface
- [ ] Add deployment, observability, evaluation, and MLOps workflows

See the [capstone guide](./capstone/README.md) for setup, API examples, and the
first learning notes.

## Build-in-public routine

For each milestone, the notes should explain:

1. What problem the feature solves.
2. What design options were considered and why one was chosen.
3. How to run and test it.
4. What is intentionally out of scope and what comes next.

This is a learning project, not a production security or deployment
certification. Before deploying it, replace development secrets, add
production-grade migrations and operational controls, and review the threat
model.
