# Plan Mapping Review

Source of truth: `Assignment2/tests/test_todoitem_ui_selenium_codex.py`

Summary:

| Metric | Value |
|---|---:|
| Total CSV cases | 169 |
| Total executable plans | 41 |
| Execution model | 169 parameterized pytest items mapped onto 41 reusable execution templates |

Interpretation:

- `plan` is an execution template, not a collapsed test case.
- Every CSV row still becomes its own `CaseRecord` and its own pytest item.
- Reuse is acceptable when cases share the same observable behavior, precondition pattern, and verdict logic.
- Risk appears when one plan mixes different requirement intents or hides an approximation. Those plans need explicit notes and review.

## Plan Review Table

| Plan | Count | Requirement scope | Why this aggregation is acceptable | Risk |
|---|---:|---|---|---|
| `clear_completed_existing` | 9 | `REQ-TODO-013` | All rows verify that completed items are removed while active items remain. Same observable behavior. | Low |
| `clear_completed_noop` | 2 | `REQ-TODO-013` | Both rows cover the false branch: no completed items exist, so nothing changes. | Low |
| `create_reject_empty` | 10 | `REQ-TODO-001`, `REQ-TODO-003` | All rows assert invalid empty-or-trimmed-empty creation is not committed. Shared verdict is "no new todo saved". | Medium |
| `create_reject_overlength` | 9 | `REQ-TODO-001`, `REQ-TODO-004` | All rows assert creation beyond length 100 is rejected. Shared verdict is "no new todo saved". | Medium |
| `create_success` | 15 | `REQ-TODO-001`, `REQ-TODO-003` | Positive creation rows share the same observable behavior: one new trimmed todo is created. Different boundaries are carried by payload. | Medium |
| `delete_existing` | 8 | `REQ-TODO-010` | All rows verify deleting an existing item from visible UI. Same behavior regardless of active/completed seed. | Low |
| `delete_missing_item` | 2 | `REQ-TODO-010` | Both rows are invalid-id approximations using backend evidence plus unchanged UI/backend state. | Medium |
| `edit_empty_delete` | 19 | `REQ-TODO-007`, `REQ-TODO-008` | All rows converge on the app's concrete behavior: editing to trimmed-empty deletes the item. Shared verdict is explicit. | Medium |
| `edit_escape_cancel` | 10 | `REQ-TODO-009` | All rows verify escape exits editing without commit and preserves prior title/state. | Low |
| `edit_missing_item` | 1 | `REQ-TODO-007` | Singleton invalid-id approximation. No aggregation risk. | Low |
| `edit_reject_overlength` | 2 | `REQ-TODO-004`, `REQ-TODO-007` | Both rows assert overlength update is rejected and prior value remains. Same verdict, different requirement origin. | Medium |
| `edit_save_valid` | 12 | `REQ-TODO-007` | All rows verify valid edit commit while preserving completed/active flag. Payload differentiates concrete title values. | Low |
| `edit_save_valid_100` | 3 | `REQ-TODO-004`, `REQ-TODO-007` | Exact upper-valid-boundary save. Same observable behavior and boundary intent. | Low |
| `enter_edit_existing` | 7 | `REQ-TODO-006` | All rows verify double-click opens edit mode for an existing item. Active/completed variants share the same trigger/result. | Low |
| `enter_edit_missing_item` | 2 | `REQ-TODO-006` | Missing-item branch is approximated via backend non-existence plus absence of editing UI. Explicitly documented. | Medium |
| `enter_edit_single_click_noop` | 1 | `REQ-TODO-006` | Singleton false-trigger approximation: single click does not enter edit mode. | Low |
| `filter_empty_safe` | 1 | `REQ-TODO-012` | Singleton approximation for empty filtered result in a UI that hides filters on a totally empty list. | Low |
| `filter_view` | 12 | `REQ-TODO-012` | All rows verify filter selection and visible-result subset. Payload rotates deterministically among `all/active/completed`. | Medium |
| `state_clear_completed` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_delete_active` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_delete_completed` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_edit_empty_delete` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_edit_save_active` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_enter_edit_active` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_enter_edit_completed` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_escape_from_edit_active` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_escape_from_edit_completed` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_toggle_all_active` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_toggle_all_completed` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_toggle_to_active` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `state_toggle_to_completed` | 1 | `REQ-STATE-MODEL` | Dedicated state transition row. | Low |
| `toggle_all_active` | 6 | `REQ-TODO-011` | All rows verify bulk transition to all-active. Shared action and verdict. | Low |
| `toggle_all_completed` | 7 | `REQ-TODO-011` | All rows verify bulk transition to all-completed. Shared action and verdict. | Low |
| `toggle_all_empty_noop` | 1 | `REQ-TODO-011` | Singleton approximation for empty-list safe no-op because toggle-all is hidden when list is empty. | Low |
| `toggle_missing_item` | 1 | `REQ-TODO-005` | Singleton invalid-id approximation using backend 404 plus unchanged state. | Low |
| `toggle_roundtrip` | 1 | `REQ-TODO-005` | Dedicated roundtrip behavior row. | Low |
| `toggle_single` | 7 | `REQ-TODO-005` | All rows verify single-item toggle from active to completed. Same behavior. | Low |
| `trim_create_save` | 2 | `REQ-TODO-002` | Both rows verify surrounding whitespace is trimmed on create and valid content remains. | Low |
| `trim_edit_save` | 2 | `REQ-TODO-002` | Both rows verify surrounding whitespace is trimmed on edit and valid content remains. | Low |
| `trim_whitespace_invalid_outcome` | 3 | `REQ-TODO-002` | All rows cover whitespace-only inputs whose trimmed result is empty; verdict is "not committed". | Medium |
| `validation_no_invalid_commit_combined` | 1 | `REQ-TODO-003` | Singleton approximation combining invalid create rejection with invalid edit non-commit/delete behavior because no visible error banner exists. | Medium |

## Plans That Need the Most Explanation in Defense

These are not necessarily wrong. They are simply the places where an examiner is most likely to ask "why did multiple cases share this plan?"

| Plan | Why it attracts questions | Defense |
|---|---|---|
| `create_reject_empty` | Mixes rows from `REQ-TODO-001` and `REQ-TODO-003`. | The shared observable contract is identical: invalid empty-or-trimmed-empty creation must not produce a saved todo. Requirement origin differs, verdict does not. |
| `create_reject_overlength` | Mixes generic invalid creation rows and explicit length-boundary rows. | The app enforces a single concrete rejection boundary at length `> 100`; all those rows map to the same executable rejection behavior. |
| `create_success` | Covers many generic positive rows with only a few concrete payloads. | The CSV rows are abstract partition/boundary records; payload rotation materializes them into deterministic valid non-empty titles while preserving one-row-one-case traceability. |
| `edit_empty_delete` | Mixes `REQ-TODO-007` invalid-edit rows and `REQ-TODO-008` explicit delete-on-empty rows. | This app's concrete behavior for trimmed-empty edit is deletion. That behavior is explicit in code and is requirement-aware rather than hidden reuse. |
| `filter_view` | Twelve rows share only three concrete filter values. | The exported rows are generic filter cases; deterministic rotation across `all/active/completed` is an explicit approximation to give every abstract row executable handling. |
| `validation_no_invalid_commit_combined` | One row combines two observable checks. | The target app has no visible validation banner, so the nearest requirement-aware execution is to prove invalid create is not saved and invalid edit likewise does not produce a committed invalid title. |

## Case-to-Plan Distribution

This section is useful when you need to prove that 169 cases still exist as distinct pytest items.

| Plan | Cases |
|---|---|
| `clear_completed_existing` | `TC-027, TC-028, TC-029, TC-030, TC-032, TC-034, TC-036, TC-038, TC-039` |
| `clear_completed_noop` | `TC-031, TC-033` |
| `create_reject_empty` | `TC-055, TC-057, TC-143, TC-144, TC-145, TC-156, TC-162, TC-163, TC-168, TC-169` |
| `create_reject_overlength` | `TC-146, TC-147, TC-148, TC-158, TC-164, TC-165, TC-170, TC-171, TC-173` |
| `create_success` | `TC-048, TC-049, TC-050, TC-051, TC-052, TC-053, TC-054, TC-056, TC-058, TC-059, TC-060, TC-061, TC-062, TC-063, TC-157` |
| `delete_existing` | `TC-064, TC-065, TC-066, TC-067, TC-069, TC-070, TC-071, TC-072` |
| `delete_missing_item` | `TC-068, TC-073` |
| `edit_empty_delete` | `TC-085, TC-086, TC-087, TC-088, TC-089, TC-090, TC-102, TC-103, TC-108, TC-109, TC-118, TC-119, TC-120, TC-121, TC-099, TC-101, TC-107, TC-115, TC-125` |
| `edit_escape_cancel` | `TC-091, TC-092, TC-093, TC-104, TC-105, TC-110, TC-111, TC-122, TC-123, TC-175` |
| `edit_missing_item` | `TC-081` |
| `edit_reject_overlength` | `TC-095, TC-153` |
| `edit_save_valid` | `TC-078, TC-079, TC-080, TC-082, TC-083, TC-084, TC-098, TC-100, TC-106, TC-114, TC-116, TC-117` |
| `edit_save_valid_100` | `TC-094, TC-152, TC-159` |
| `enter_edit_existing` | `TC-074, TC-075, TC-076, TC-096, TC-112, TC-113, TC-126` |
| `enter_edit_missing_item` | `TC-097, TC-124` |
| `enter_edit_single_click_noop` | `TC-077` |
| `filter_empty_safe` | `TC-131` |
| `filter_view` | `TC-127, TC-128, TC-129, TC-130, TC-132, TC-133, TC-134, TC-135, TC-136, TC-137, TC-138, TC-139` |
| `state_clear_completed` | `TC-026` |
| `state_delete_active` | `TC-018` |
| `state_delete_completed` | `TC-023` |
| `state_edit_empty_delete` | `TC-020` |
| `state_edit_save_active` | `TC-017` |
| `state_enter_edit_active` | `TC-016` |
| `state_enter_edit_completed` | `TC-019` |
| `state_escape_from_edit_active` | `TC-021` |
| `state_escape_from_edit_completed` | `TC-024` |
| `state_toggle_all_active` | `TC-025` |
| `state_toggle_all_completed` | `TC-022` |
| `state_toggle_to_active` | `TC-015` |
| `state_toggle_to_completed` | `TC-014` |
| `toggle_all_active` | `TC-002, TC-004, TC-006, TC-008, TC-010, TC-012` |
| `toggle_all_completed` | `TC-176, TC-001, TC-003, TC-007, TC-009, TC-011, TC-013` |
| `toggle_all_empty_noop` | `TC-005` |
| `toggle_missing_item` | `TC-044` |
| `toggle_roundtrip` | `TC-174` |
| `toggle_single` | `TC-047, TC-040, TC-041, TC-042, TC-043, TC-045, TC-046` |
| `trim_create_save` | `TC-160, TC-166` |
| `trim_edit_save` | `TC-161, TC-167` |
| `trim_whitespace_invalid_outcome` | `TC-149, TC-150, TC-151` |
| `validation_no_invalid_commit_combined` | `TC-172` |

## Bottom-Line Judgment

This mapping is acceptable from a software-testing-engineering perspective if you defend it this way:

1. The script keeps `169` distinct pytest cases and does not collapse them into `41` results.
2. The `41` plans are reusable execution templates, analogous to structured test procedures.
3. Aggregation is only accepted when the observable behavior is the same or when the approximation is explicit in code.
4. The medium-risk plans are the right places to show examiner awareness, because they are exactly where semantic over-compression could have happened if not documented.
