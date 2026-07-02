# Git Migration Plan — jjainsurance.com website

Two phases. Phase A is zero-risk (nothing about deploys changes). Phase B is
optional and only after Phase A feels routine.

## Phase A — version history only (do this now, ~15 min, zero deploy risk)

The deploy command stays exactly `npx wrangler deploy`. Git just records
history so every deploy is diffable and reversible.

From a real Windows terminal:

```
cd C:\Website
git init -b main
git add -A
git commit -m "Baseline: site as deployed 2026-07-02 (post-audit)"
```

Then create a PRIVATE repo on github.com (e.g. `jja-website`), and:

```
git remote add origin https://github.com/<your-user>/jja-website.git
git push -u origin main
```

**New finish-work ritual** (replaces nothing, adds one step):

1. `python predeploy_check.py`   ← must say PASS
2. `git add -A && git commit -m "what changed"`
3. `npx wrangler deploy`
4. `python checkpoint.py`

To see what changed before deploying: `git diff`. To roll back a bad edit:
`git checkout -- <file>` (before commit) or `git revert` (after).

## Phase B — auto-deploy on push (later, only when wanted)

Cloudflare **Workers Builds** can deploy the `jjainsurance` Worker
automatically on every push to `main` (Dashboard → Workers → jjainsurance →
Settings → Build). Because it uses the same `wrangler.jsonc` (same worker
name, same assets directory), the deployed artifact is identical to a manual
deploy — no URL, header, or SEO impact.

Prerequisites before enabling:
- Phase A routine (every deploy has a matching commit).
- Decide whether predeploy_check should run in CI (Workers Builds can run a
  build command — `python predeploy_check.py` — and abort on failure, which
  makes broken deploys impossible even if the local step is skipped).

Until Phase B, do NOT connect the repo to any auto-deploy — manual
`npx wrangler deploy` remains the only deploy path.
