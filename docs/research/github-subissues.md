# GitHub sub-issues and dependencies for maps

Resolves [ticket #12](https://github.com/saiashirwad/skills/issues/12) for [map #1](https://github.com/saiashirwad/skills/issues/1). Researched 2026-09-30 using GitHub documentation and authenticated, read-only `gh api` probes on `saiashirwad/skills`. Ticket assignment/comment/closure are workflow actions, not experiments.

## Answer and recommended contract

Use native sub-issues for **map → topic → ticket**, and native `blocked_by` relationships for prerequisites. GitHub supports 100 children per parent and eight levels of nested sub-issues. REST and GraphQL expose progress and dependency summaries. A small, fixed-depth map can be fetched in one GraphQL request and filtered locally; there is no verified all-in-one server-side frontier search. In this repository, the tempting `-is:blocked` search returned blocked issues. [S1–S4; probes below]

Recommended frontier predicate: a runnable ticket is `OPEN`, has zero assignees, and has `issueDependenciesSummary.blockedBy == 0`. **Do not use `totalBlockedBy == 0`: closed prerequisites remain linked.** Also apply the application's ticket-kind/leaf rule, not just this predicate, so maps/topics are not accidentally dispatched. Recheck before assigning; discovery is not an atomic claim. [S3–S4; P2–P4]

For study review dates, use a machine-readable ISO date in the issue body as the portable baseline and compare it locally. Labels are good for categories, not date-range arithmetic. Organization issue fields now support date values and search ranges, but this repository is user-owned and its `issueFieldValues` query failed. Do not require that feature in a core intended to work in arbitrary repositories. Project date fields are another option, with an explicit project setup requirement. [S5–S7; P5]

## Capabilities and limits

| Need | Finding | Source |
| --- | --- | --- |
| Hierarchy | Up to **100 sub-issues per parent**, **eight levels of nested sub-issues**; map/topic/ticket comfortably fits. | S1 |
| Parent and cross-repository links | REST can read the parent, add/remove children and reprioritize them. `replace_parent` replaces a child's current parent; model this as one parent, not multiple parents. The add endpoint requires child and parent to have the **same repository owner**; do not assume arbitrary cross-owner maps. | S2 |
| Progress | REST `sub_issues_summary` has `total`, `completed`, `percent_completed`; GraphQL has `subIssuesSummary { total completed percentCompleted }`. The live map returned 14, 2, 14. | S2, S4; P1–P3 |
| Dependency direction | For issue A blocked by B, operate on A's `dependencies/blocked_by` and pass B's issue ID. Reverse `dependencies/blocking` is readable. | S3 |
| Active vs historical dependencies | REST `blocked_by` / GraphQL `blockedBy` is the active blocker count; `total_blocked_by` / `totalBlockedBy` includes open and closed issues. Live #6 had zero active blockers but one retained closed prerequisite (#4). | S3, S4; P2 |
| Dependency writes | REST supports add/remove blocked-by links; live GraphQL schema exposes `addBlockedBy` and `removeBlockedBy`. | S3, S4 |
| Relationship IDs | REST path uses repository issue **number**, but add/remove relationship bodies use numeric issue **ID**, not that number. GraphQL mutations use node IDs; obtain them from API responses rather than constructing them. | S2–S4 |
| Pagination | REST relationship lists default to 30, max 100 per page. GraphQL connections expose cursors; every returned connection must be checked for more pages. | S2–S4 |
| Reopening | Live GraphQL schema exposes `reopenIssue(input: {issueId: ...})`; input requires the issue node ID. Reopening is supported, but it is a separate scheduling action, not a native review-date timer. | S4; P6 |

**Boundaries not established:** the retrieved dependency documentation does not state a maximum dependency count or cycle/depth constraints. No destructive limit tests were run. The current map is flat, so recursive progress aggregation, cancellation (`not_planned`) counting, automatic parent close/reopen behavior, and re-blocking after reopening a prerequisite were not experimentally established. Do not promise a leaf-weighted progress percentage or automatic parent state propagation; calculate/report leaf progress explicitly if required. The eight-level wording above is GitHub's wording, not a tested root-inclusive off-by-one interpretation. [S1–S4]

## Querying the frontier in one call

### Flat parent: one REST request works, with local filtering

This exact read-only command returned `[6]` during the experiment:

```sh
gh api 'repos/saiashirwad/skills/issues/1/sub_issues?per_page=100' \
  --jq '[.[] | select(.state == "open" and (.assignees|length) == 0 and .issue_dependencies_summary.blocked_by == 0) | .number]'
```

The endpoint returns child issues with their summaries and assignees, so no per-child dependency requests are necessary just to decide readiness. It fetches **direct children**, not the whole descendant tree. [S2; P1, P4]

### Two levels beneath the map: one GraphQL request, local filtering

The following shape was executed successfully against #1 (also selecting labels and parent links in the probe). Its nested child lists were empty because the existing map is flat. It retrieves enough data for map/topic/ticket readiness without fetching every prerequisite. [S4; P3]

```graphql
query {
  repository(owner: "saiashirwad", name: "skills") {
    issue(number: 1) {
      number
      subIssuesSummary { total completed percentCompleted }
      subIssues(first: 100) {
        pageInfo { hasNextPage endCursor }
        nodes {
          number
          state
          assignees(first: 1) { totalCount }
          issueDependenciesSummary { blockedBy totalBlockedBy }
          subIssues(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              number
              state
              assignees(first: 1) { totalCount }
              issueDependenciesSummary { blockedBy totalBlockedBy }
            }
          }
        }
      }
    }
  }
}
```

Run with `gh api graphql -f query='...'`. For cross-repository maps also select `id`, `url`, and `repository { nameWithOwner }`; an issue number alone is not globally unique. The application should inspect all `pageInfo` values and fail/re-fetch rather than silently truncate. A fixed selection is not arbitrary recursion: extend the selection for deeper maps or traverse in bounded batches. Large nested requests remain subject to GraphQL resource limits; this experiment only validates the small current map, not a fully populated 100×100 hierarchy. [S2, S4]

Live introspection showed `subIssues` only takes cursor/pagination arguments, while `blockedBy`/`blocking` additionally take `orderBy`; no state/assignee/blocked filter arguments were exposed on these connections. Thus **one network request plus local filtering** is the supported conclusion, not one server-filtered recursive query. [S4; P3]

### Search is not a verified substitute

These REST searches were actually run:

```sh
gh api --method GET search/issues \
  -f q='repo:saiashirwad/skills is:issue is:open no:assignee -is:blocked' \
  -f per_page=100 --jq '{total_count,incomplete_results,numbers:[.items[].number]}'
# total_count: 6; incomplete_results: false; numbers: [8,7,6,5,3,1]

gh api --method GET search/issues \
  -f q='repo:saiashirwad/skills is:issue is:open no:assignee is:blocked' \
  --jq '{total_count,numbers:[.items[].number]}'
# total_count: 0; numbers: []
```

Yet #3, #5, #7 and #8 had active blockers in REST/GraphQL. This is direct evidence that these searches cannot implement readiness in this environment; a successful HTTP response does not validate qualifier semantics. Search also included the map itself. No verified transitive-map search qualifier was found in the retrieved search documentation. Prefer relationship traversal and summary checks. [S5; P1–P4]

## Labels, fields, and review dates

- **Labels:** searchable using `label:`, with documented AND/OR combinations. `label:"wayfinder:grilling"` returned `[8,7,6,5,3,2]` in REST search. Labels are also readable in GraphQL `labels` and REST issue objects. [S2, S5; P5]
- **Organization issue fields:** current docs describe organization-defined text, number, single-select and **date** fields, with up to 25 fields per organization. Filtering docs explicitly show `field."target date":>=2026-03-01`; a configured review-date field could use the same date-comparison approach. This is not merely free text in the issue body. [S6–S7]
- **API field access:** REST issue schemas include `issue_field_values`, and the live GraphQL `Issue` schema exposes `issueFieldValues`. But querying `issueFieldValues(first:25){totalCount}` on #12 failed twice with a GitHub internal execution error; the REST projection on #1 yielded null. The owner was confirmed as `User`, not `Organization`. Field-value retrieval and date-range REST/GraphQL search were **not validated on a populated field** here. [S2, S4; P5]
- **Project fields are different:** project-scoped values can differ for the same issue in different projects, whereas organization issue fields live on the issue. GraphQL exposes `projectItems`, and `ProjectV2ItemFieldDateValue.date` exists in the live schema; #12 had no project items. Adding a project is an optional product decision, not a prerequisite for hierarchy/dependencies. [S4, S7; P5–P6]
- **Portable recommendation:** keep one `review_on: YYYY-MM-DD` value in an agreed body section; fetch `body` with the issue, parse strictly, and compare dates locally for `study-due`. Search labels to narrow candidates, but scan closed review tickets too. This is a proposed convention, not a GitHub date-field feature. Decide timezone and overdue semantics in the study scheduler.

## Read-only evidence ledger

Snapshots were taken on 2026-09-30 while other jobs were assigning/closing tickets, so counts are historical, not assertions about today's live frontier.

| Probe | Request / result |
| --- | --- |
| P1 | `gh api repos/saiashirwad/skills/issues/1` and `gh api 'repos/saiashirwad/skills/issues/1/sub_issues?per_page=100'`: map summary 14 total / 2 completed / 14%; children #2–#15. #3 active blockers 1; #5 2 active / 3 total; #7 2; #8 1. |
| P2 | `gh api repos/saiashirwad/skills/issues/6/dependencies/blocked_by`: retained #4, `state: closed`, `state_reason: completed`; #6 summary 0 active / 1 total. |
| P3 | Nested GraphQL query above, with `parent {number}` and `labels(first:10){nodes{name}}`: succeeded, all direct children's parent was #1, map `hasNextPage: false`, nested lists empty; summary matched REST. `__type(name:"Issue")` confirmed relationship fields and their arguments. |
| P4 | REST local frontier filtering returned only #6; search experiments returned the inconsistent results reproduced above. |
| P5 | Label search returned six matching issues. GraphQL `owner {__typename}` was `User`; #12 `projectItems.totalCount` was 0. Isolated `issueFieldValues` retry failed at `2026-09-30T12:19:39Z`, request identifier `80DD:0BD7:4CE0845:5184A6A:6ABCFE5B`. |
| P6 | GraphQL introspection confirmed mutations `addSubIssue`, `removeSubIssue`, `reprioritizeSubIssue`, `addBlockedBy`, `removeBlockedBy`, `reopenIssue`; `ReopenIssueInput.issueId`; and `ProjectV2ItemFieldDateValue.date`. No mutations were executed as research tests. |

Introspection reproduction examples:

```sh
gh api graphql -f query='{ __type(name:"Issue") { fields { name description args { name } } } }'
gh api graphql -f query='{ a:__type(name:"IssueDependenciesSummary") { fields {name description} } b:__type(name:"SubIssuesSummary") { fields {name description} } }'
gh api graphql -f query='{ __type(name:"ReopenIssueInput") { inputFields {name description} } }'
```

An initial request with three introspected `fields` selections was rejected with `INTROSPECTION_LIMIT_EXCEEDED`; splitting it into requests with at most two succeeded. This is a tooling detail, not a hierarchy-depth limit.

## Primary sources

- **S1:** [GitHub Docs: Adding sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues) — hierarchy, count and nesting limits.
- **S2:** [GitHub REST: Sub-issues](https://docs.github.com/en/rest/issues/sub-issues) — routes, IDs, same-owner restriction, pagination and issue response schema.
- **S3:** [GitHub REST: Issue dependencies](https://docs.github.com/en/rest/issues/issue-dependencies) and [creating issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies) — relationship direction, reads and writes.
- **S4:** [GitHub GraphQL API](https://api.github.com/graphql), authenticated schema introspection and read-only repository queries recorded above. This is the primary source for exact current schema names; the documentation mutations URL redirected to a generic reference page during this research, so it was not used as evidence for mutation details.
- **S5:** [GitHub Docs: Searching issues and pull requests](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests) — state, labels, assignment and metadata searches.
- **S6:** [GitHub Docs: Filtering and searching issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests#filtering-by-issue-fields) — field filter syntax and date comparisons.
- **S7:** [GitHub Docs: Managing issue fields in your organization](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-fields-in-your-organization) — field scope/types/limits and distinction from project fields.
