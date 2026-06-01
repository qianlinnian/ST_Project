"""
Selenium + pytest execution for Assignment 2 Todo Item cases.
 
traceability sources:
  - exports/todoitem_optimized_test_suite.csv
  - exports/todoitem_traceability_matrix.csv
  - exports/todoitem_requirements_structured.csv
  - exports/todoitem_state_transitions.csv

Run prerequisites:
  1. Backend:  cd simpletodolist/backend && python app.py
  2. Frontend: cd simpletodolist && python -m http.server 8000
  3. Install:  pip install pytest selenium requests
  4. Run:      pytest Assignment2/tests/test_todoitem_ui_selenium_generated_from_csv.py -q -rA

Optional environment variables:
  TODO_FRONTEND_BASE_URL=http://127.0.0.1:8000/todo.html
  TODO_FRONTEND_URL_TEMPLATE=http://127.0.0.1:8000/todo.html#{filter_hash}&{list_name}
  TODO_API_BASE_URL=http://127.0.0.1:5000/api
  SELENIUM_BROWSER=chrome
  SELENIUM_HEADLESS=0|1
  WAIT_SECONDS=6

Approximation rules are intentionally explicit in code:
  - Generic boundary/partition rows from the CSV are materialized into
    deterministic concrete inputs instead of being silently collapsed.
  - Invalid-id rows use backend API evidence plus unchanged UI state because the
    page has no control for selecting a non-existent todo item.
  - Validation rows that mention "error shown" are approximated by asserting
    that invalid data is rejected and not committed. The target app exposes
    backend validation errors but does not render a visible validation message.
  - TC-173 ("list at max capacity") is approximated with the nearest enforced
    creation rejection boundary: title length 101. The backend repository only
    enforces MAX_TITLE_LENGTH = 100 and does not define list capacity.
"""

from __future__ import annotations

import csv
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

import pytest
import requests
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, NoSuchElementException, SessionNotCreatedException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


ROOT = Path(__file__).resolve().parents[1]
EXPORTS_DIR = ROOT / "exports"
OPTIMIZED_CSV = EXPORTS_DIR / "todoitem_optimized_test_suite.csv"
TRACEABILITY_CSV = EXPORTS_DIR / "todoitem_traceability_matrix.csv"
REQUIREMENTS_CSV = EXPORTS_DIR / "todoitem_requirements_structured.csv"
STATE_TRANSITIONS_CSV = EXPORTS_DIR / "todoitem_state_transitions.csv"

FRONTEND_BASE_URL = os.getenv("TODO_FRONTEND_BASE_URL", "http://127.0.0.1:8000/todo.html")
FRONTEND_URL_TEMPLATE = os.getenv("TODO_FRONTEND_URL_TEMPLATE", "")
API_BASE = os.getenv("TODO_API_BASE_URL", os.getenv("API_BASE", "http://127.0.0.1:5000/api")).rstrip("/")
BROWSER = os.getenv("SELENIUM_BROWSER", os.getenv("BROWSER", "chrome")).lower()
HEADLESS = os.getenv("SELENIUM_HEADLESS", os.getenv("HEADLESS", "0")) == "1"
WAIT_SECONDS = float(os.getenv("WAIT_SECONDS", "6"))
INVALID_TODO_ID = 999999
DEFAULT_CHROME_BINARY = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
CHROME_BINARY = Path(os.getenv("SELENIUM_CHROME_BINARY", str(DEFAULT_CHROME_BINARY)))
CHROME_PROFILE_ROOT = Path(
    os.getenv(
        "SELENIUM_CHROME_PROFILE_ROOT",
        str(Path(tempfile.gettempdir()) / "codex-selenium-profiles"),
    )
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


@dataclass(frozen=True)
class CaseRecord:
    test_case_id: str
    suite_id: str
    suite_name: str
    requirement_id: str
    requirement_text: str
    coverage_id: str
    coverage_description: str
    technique: str
    precondition: str
    test_data: str
    steps: str
    expected_result: str
    priority: str
    risk_level: str
    coverage_type: str
    plan: str
    approximation_note: str
    payload: dict[str, Any]

    @property
    def case_number(self) -> int:
        return int(self.test_case_id.split("-")[1])


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _rotate(case_number: int, options: list[Any]) -> Any:
    return options[(case_number - 1) % len(options)]


def _case_list_slug(case_id: str) -> str:
    return f"csv-{case_id.lower()}"


def _api_list_name(list_slug: str) -> str:
    return f"todos-{list_slug}"


def _build_frontend_url(list_slug: str, filter_name: str = "") -> str:
    filter_hash = f"/{filter_name}" if filter_name else "/"
    if FRONTEND_URL_TEMPLATE:
        return FRONTEND_URL_TEMPLATE.format(
            list_name=list_slug,
            filter_name=filter_name,
            filter_hash=filter_hash,
        )
    # Include a query component tied to the list so Selenium navigation becomes a
    # real page load instead of a fragment-only hash change. The app reads the
    # list name from the hash on initial load and does not rebind storage on
    # later hash-only transitions.
    return f"{FRONTEND_BASE_URL}?list={quote(list_slug, safe='')}#{filter_hash}&{list_slug}"


def api_request(method: str, path: str, *, expected: tuple[int, ...] = (200, 201), **kwargs: Any) -> requests.Response:
    response = requests.request(method, f"{API_BASE}{path}", timeout=5, **kwargs)
    if response.status_code not in expected:
        raise AssertionError(f"{method} {path} returned {response.status_code}: {response.text}")
    return response


def api_delete_list(list_name: str) -> None:
    response = requests.delete(f"{API_BASE}/lists/{quote(list_name, safe='')}", timeout=5)
    if response.status_code not in (200, 404):
        raise AssertionError(f"DELETE /lists/{list_name} returned {response.status_code}: {response.text}")


def api_list_todos(list_name: str, *, status: str = "all") -> list[dict[str, Any]]:
    response = api_request("GET", f"/todos?list={quote(list_name, safe='')}&status={quote(status, safe='')}")
    return response.json()["data"]


def api_create_todo(list_name: str, title: str) -> dict[str, Any]:
    response = api_request("POST", f"/todos?list={quote(list_name, safe='')}", json={"title": title})
    return response.json()["data"]


def api_set_completed(list_name: str, todo_id: int, completed: bool) -> dict[str, Any]:
    response = api_request(
        "PATCH",
        f"/todos/{todo_id}/complete?list={quote(list_name, safe='')}",
        json={"completed": completed},
    )
    return response.json()["data"]


def api_get_todo_response(list_name: str, todo_id: int, *, expected: tuple[int, ...] = (200, 404)) -> requests.Response:
    return api_request("GET", f"/todos/{todo_id}?list={quote(list_name, safe='')}", expected=expected)


def api_update_todo_response(list_name: str, todo_id: int, title: str, *, expected: tuple[int, ...] = (200, 400, 404)) -> requests.Response:
    return api_request(
        "PUT",
        f"/todos/{todo_id}?list={quote(list_name, safe='')}",
        expected=expected,
        json={"title": title},
    )


def api_toggle_todo_response(list_name: str, todo_id: int, completed: bool, *, expected: tuple[int, ...] = (200, 400, 404)) -> requests.Response:
    return api_request(
        "PATCH",
        f"/todos/{todo_id}/complete?list={quote(list_name, safe='')}",
        expected=expected,
        json={"completed": completed},
    )


def api_delete_todo_response(list_name: str, todo_id: int, *, expected: tuple[int, ...] = (200, 404)) -> requests.Response:
    return api_request("DELETE", f"/todos/{todo_id}?list={quote(list_name, safe='')}", expected=expected)




def _make_chrome_driver(profile_dir: Path):
    if not CHROME_BINARY.exists():
        raise RuntimeError(f"Chrome binary not found: {CHROME_BINARY}")
    profile_dir.mkdir(parents=True, exist_ok=True)
    options = webdriver.ChromeOptions()
    options.binary_location = str(CHROME_BINARY)
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--remote-debugging-port=0")
    options.add_argument(f"--user-data-dir={profile_dir}")
    return webdriver.Chrome(options=options)


def make_driver(profile_dir: Path):
    if BROWSER != "chrome":
        raise RuntimeError(
            f"This script only supports Chrome. "
            f"Received SELENIUM_BROWSER={BROWSER!r}."
        )
    try:
        return _make_chrome_driver(profile_dir)
    except (SessionNotCreatedException, WebDriverException) as exc:
        raise RuntimeError(
            f"Chrome WebDriver startup failed. "
            f"binary={CHROME_BINARY} profile={profile_dir} headless={HEADLESS}"
        ) from exc


class BrowserSession:
    def __init__(self):
        CHROME_PROFILE_ROOT.mkdir(parents=True, exist_ok=True)
        self.profile_dir = Path(tempfile.mkdtemp(prefix="chrome-codex-", dir=str(CHROME_PROFILE_ROOT)))
        self.driver = make_driver(self.profile_dir)

    def restart(self) -> webdriver.Remote:
        try:
            self.driver.quit()
        except Exception:
            pass
        self.driver = make_driver(self.profile_dir)
        return self.driver

    def close(self) -> None:
        try:
            self.driver.quit()
        except Exception:
            pass
        shutil.rmtree(self.profile_dir, ignore_errors=True)


class TodoPage:
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_SECONDS)

    def open(self, list_slug: str, filter_name: str = "") -> "TodoPage":
        self.driver.get("about:blank")
        self.driver.get(_build_frontend_url(list_slug, filter_name))
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".new-todo")))
        expected_heading = f"TODOs : {list_slug.replace('-', ' ')}"
        self.wait.until(lambda _: self.driver.find_element(By.CSS_SELECTOR, "#todostitle").text.strip() == expected_heading)
        return self

    def reload(self) -> None:
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".new-todo")))

    def all_items(self) -> list[Any]:
        return self.driver.find_elements(By.CSS_SELECTOR, ".todo-list li")

    def wait_for_item_count(self, expected_minimum: int = 1) -> list[Any]:
        self.wait.until(lambda _: len(self.all_items()) >= expected_minimum)
        return self.all_items()

    def item_at(self, index: int = 0):
        self.wait.until(lambda _: len(self.all_items()) > index)
        return self.all_items()[index]

    def visible_items(self) -> list[Any]:
        return [item for item in self.all_items() if item.is_displayed()]

    def labels(self, *, visible_only: bool = True) -> list[str]:
        items = self.visible_items() if visible_only else self.all_items()
        return [item.find_element(By.CSS_SELECTOR, "label").text for item in items]

    def completed_flags(self, *, visible_only: bool = False) -> list[bool]:
        items = self.visible_items() if visible_only else self.all_items()
        return ["completed" in (item.get_attribute("class") or "").split() for item in items]

    def selected_filter(self) -> str:
        selected = self.driver.find_element(By.CSS_SELECTOR, ".filters .selected")
        return selected.text.strip().lower()

    def item_count_text(self) -> str:
        return self.driver.find_element(By.CSS_SELECTOR, ".todo-count").text.strip()

    def footer_visible(self) -> bool:
        return self.driver.find_element(By.CSS_SELECTOR, ".footer").is_displayed()

    def main_visible(self) -> bool:
        return self.driver.find_element(By.CSS_SELECTOR, ".main").is_displayed()

    def create_via_ui(self, title: str) -> None:
        input_box = self.driver.find_element(By.CSS_SELECTOR, ".new-todo")
        input_box.click()
        input_box.send_keys(Keys.CONTROL, "a")
        input_box.send_keys(Keys.BACKSPACE)
        if title:
            input_box.send_keys(title)
        input_box.send_keys(Keys.TAB)

    def select_filter(self, filter_name: str) -> None:
        target = filter_name.lower()
        anchors = self.driver.find_elements(By.CSS_SELECTOR, ".filters a")
        for anchor in anchors:
            if anchor.text.strip().lower() == target:
                anchor.click()
                self.wait.until(lambda _: self.selected_filter() == target)
                return
        raise NoSuchElementException(f"Filter '{filter_name}' not found")

    def toggle_item(self, index: int = 0) -> None:
        item = self.item_at(index)
        item.find_element(By.CSS_SELECTOR, "input.toggle").click()

    def toggle_all(self) -> None:
        self.driver.find_element(By.CSS_SELECTOR, "label[for='toggle-all']").click()

    def clear_completed(self) -> None:
        self.driver.find_element(By.CSS_SELECTOR, ".clear-completed").click()

    def delete_item(self, index: int = 0) -> None:
        item = self.item_at(index)
        ActionChains(self.driver).move_to_element(item).perform()
        button = item.find_element(By.CSS_SELECTOR, ".destroy")
        button.click()

    def enter_edit_mode(self, index: int = 0):
        label = self.item_at(index).find_element(By.CSS_SELECTOR, "label")
        ActionChains(self.driver).double_click(label).perform()
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".todo-list li.editing .edit")))

    def single_click_label(self, index: int = 0) -> None:
        self.item_at(index).find_element(By.CSS_SELECTOR, "label").click()

    def edit_submit(self, index: int, new_title: str) -> None:
        input_box = self.enter_edit_mode(index)
        input_box.send_keys(Keys.CONTROL, "a")
        input_box.send_keys(Keys.BACKSPACE)
        if new_title:
            input_box.send_keys(new_title)
        input_box.send_keys(Keys.ENTER)

    def edit_escape(self, index: int, draft_title: str) -> None:
        input_box = self.enter_edit_mode(index)
        input_box.send_keys(Keys.CONTROL, "a")
        input_box.send_keys(Keys.BACKSPACE)
        if draft_title:
            input_box.send_keys(draft_title)
        input_box.send_keys(Keys.ESCAPE)


def _create_seed(list_name: str, *, titles: list[str], completed_indexes: set[int] | None = None) -> list[dict[str, Any]]:
    completed_indexes = completed_indexes or set()
    todos: list[dict[str, Any]] = []
    for idx, title in enumerate(titles):
        todo = api_create_todo(list_name, title)
        if idx in completed_indexes:
            todo = api_set_completed(list_name, todo["id"], True)
        todos.append(todo)
    return todos


def _wait_for_backend_count(page: TodoPage, list_name: str, expected: int) -> None:
    page.wait.until(lambda _: len(api_list_todos(list_name)) == expected)


def _wait_for_backend_titles(page: TodoPage, list_name: str, expected_titles: list[str]) -> None:
    page.wait.until(lambda _: [todo["title"] for todo in api_list_todos(list_name)] == expected_titles)


def _wait_for_single_backend_todo(page: TodoPage, list_name: str) -> dict[str, Any]:
    page.wait.until(lambda _: len(api_list_todos(list_name)) == 1)
    todos = api_list_todos(list_name)
    assert len(todos) == 1, f"Expected exactly one todo in {list_name}, found {len(todos)}"
    return todos[0]


def _build_case_plan(row: dict[str, str], requirement_text: str, coverage_description: str) -> tuple[str, str, dict[str, Any]]:
    case_id = row["test_case_id"]
    case_number = int(case_id.split("-")[1])
    requirement_id = row["requirement_id"]
    test_data = _normalize_text(row.get("test_data"))
    expected_result = _normalize_text(row.get("expected_result"))
    lowered_coverage = coverage_description.lower()

    if requirement_id == "REQ-STATE-MODEL":
        coverage_id = row["coverage_id"]
        if coverage_id == "COV-STATE-TR-001":
            return "state_toggle_to_completed", "", {}
        if coverage_id == "COV-STATE-TR-002":
            return "state_toggle_to_active", "", {}
        if coverage_id == "COV-STATE-TR-003":
            return "state_enter_edit_active", "", {}
        if coverage_id == "COV-STATE-TR-004":
            return "state_enter_edit_completed", "", {}
        if coverage_id == "COV-STATE-TR-005":
            return "state_edit_save_active", "", {"new_title": "updated title"}
        if coverage_id == "COV-STATE-TR-006":
            return "state_edit_empty_delete", "", {}
        if coverage_id == "COV-STATE-TR-007":
            return "state_escape_from_edit_active", "", {}
        if coverage_id == "COV-STATE-TR-008":
            return "state_escape_from_edit_completed", "", {}
        if coverage_id == "COV-STATE-TR-009":
            return "state_delete_active", "", {}
        if coverage_id == "COV-STATE-TR-010":
            return "state_delete_completed", "", {}
        if coverage_id == "COV-STATE-TR-011":
            return "state_toggle_all_completed", "", {}
        if coverage_id == "COV-STATE-TR-012":
            return "state_toggle_all_active", "", {}
        if coverage_id == "COV-STATE-TR-013":
            return "state_clear_completed", "", {}

    if requirement_id == "REQ-TODO-001":
        if case_id == "TC-173":
            return (
                "create_reject_overlength",
                "Approximation: the app has no list-capacity constraint, so TC-173 is executed with the nearest enforced creation rejection boundary: title length 101.",
                {"title": "X" * 101},
            )
        if "rule 2" in test_data.lower() or "rejected" in expected_result.lower():
            return (
                "create_reject_empty",
                "Approximation: the false-branch condition is executed with an empty/whitespace title because the UI exposes title validity but not an explicit list-exists toggle.",
                {"title": "   "},
            )
        return (
            "create_success",
            "Approximation: generic positive creation rows are concretized into deterministic non-empty title boundaries.",
            {"title": _rotate(case_number, ["a", "csv generated todo", "X" * 100])},
        )

    if requirement_id == "REQ-TODO-002":
        if case_id in {"TC-149", "TC-150", "TC-151"}:
            raw = {"TC-149": " ", "TC-150": " " * 100, "TC-151": " " * 101}[case_id]
            return (
                "trim_whitespace_invalid_outcome",
                "Approximation: these whitespace-only trimming rows assert the trimmed input is not committed; edit-delete semantics are covered explicitly by REQ-TODO-008 cases.",
                {"title": raw},
            )
        if "rule 2" in test_data.lower():
            return (
                "create_success",
                "Approximation: the false branch of 'has leading/trailing whitespace' is executed with an already-trimmed title and must save unchanged.",
                {"title": "already-trimmed"},
            )
        if case_id in {"TC-161", "TC-167"}:
            return "trim_edit_save", "", {"original": "seed title", "new_title": "  edited with spaces  "}
        return "trim_create_save", "", {"title": _rotate(case_number, ["  spaced  ", "  another spaced title  ", "  trim-me-please  "])}

    if requirement_id == "REQ-TODO-003":
        if case_id == "TC-157":
            return (
                "create_success",
                "Approximation: the false branch of the empty-after-trim condition is represented by a valid non-empty title.",
                {"title": "valid-after-trim"},
            )
        if case_id == "TC-172":
            return (
                "validation_no_invalid_commit_combined",
                "Approximation: the app has no visible validation banner, so this case combines invalid create rejection and invalid edit non-commit/deletion checks.",
                {},
            )
        return "create_reject_empty", "Approximation: 'error shown' is executed as 'invalid data not committed' because the app does not render a validation message.", {"title": "   "}

    if requirement_id == "REQ-TODO-004":
        if case_id == "TC-152":
            return "edit_save_valid_100", "", {"new_title": "Y" * 100}
        if case_id == "TC-153":
            return "edit_reject_overlength", "", {"new_title": "Y" * 101}
        if case_id == "TC-159":
            return (
                "edit_save_valid_100",
                "Approximation: the false branch of 'title length > 100' is represented with the exact upper valid boundary (100 characters).",
                {"new_title": "Z" * 100},
            )
        return "create_reject_overlength", "Approximation: 'error shown' is executed as 'invalid data not committed' because the app does not render a validation message.", {"title": "Z" * 101}

    if requirement_id == "REQ-TODO-005":
        if case_id == "TC-174":
            return "toggle_roundtrip", "", {}
        if "rule 2" in test_data.lower():
            return (
                "toggle_missing_item",
                "Approximation: the false branch is executed through the backend API with a sentinel non-existent todo id because the UI cannot point at a missing item.",
                {},
            )
        return "toggle_single", "", {"initial_completed": False}

    if requirement_id == "REQ-TODO-006":
        if case_id == "TC-077":
            return (
                "enter_edit_single_click_noop",
                "Approximation: the null-id boundary is represented by a single click, which preserves the label state because double-click is the required trigger.",
                {},
            )
        if case_id in {"TC-097", "TC-124"}:
            return (
                "enter_edit_missing_item",
                "Approximation: the missing-item branch is executed through backend existence checks plus unchanged UI state because the page cannot enter edit mode for a non-existent todo.",
                {},
            )
        return "enter_edit_existing", "", {"initial_completed": case_number % 2 == 0}

    if requirement_id == "REQ-TODO-007":
        if case_id == "TC-081":
            return (
                "edit_missing_item",
                "Approximation: the max-integer id boundary is executed through the backend API with a sentinel non-existent todo id and must leave the list unchanged.",
                {"new_title": "unreachable-title"},
            )
        if case_id == "TC-094":
            return "edit_save_valid_100", "", {"new_title": "E" * 100}
        if case_id == "TC-095":
            return "edit_reject_overlength", "", {"new_title": "E" * 101}
        if case_id in {"TC-099", "TC-101", "TC-107", "TC-115"}:
            return (
                "edit_empty_delete",
                "Approximation: the invalid/false-branch update rows use the concrete alternate app behavior for invalid edited titles: trimming to empty deletes the todo.",
                {"new_title": "   ", "initial_completed": False},
            )
        return "edit_save_valid", "", {"new_title": _rotate(case_number, ["edited title", "edited again", "updated title"]), "initial_completed": case_number % 2 == 0}

    if requirement_id == "REQ-TODO-008":
        return "edit_empty_delete", "", {"new_title": _rotate(case_number, ["", "   ", " " * 5]), "initial_completed": case_number % 2 == 0}

    if requirement_id == "REQ-TODO-009":
        return "edit_escape_cancel", "", {"initial_completed": case_number % 2 == 0, "draft_title": "draft that must be reverted"}

    if requirement_id == "REQ-TODO-010":
        if case_id in {"TC-068", "TC-073"}:
            return (
                "delete_missing_item",
                "Approximation: the false/missing-id branch is executed through the backend API with a sentinel non-existent todo id.",
                {},
            )
        return "delete_existing", "", {"initial_completed": case_number % 2 == 0}

    if requirement_id == "REQ-TODO-011":
        if case_id in {"TC-005"}:
            return (
                "toggle_all_empty_noop",
                "Approximation: 'list exists' false cannot be selected directly in this page, so the closest UI-observable branch is an empty current list and a safe no-op.",
                {},
            )
        if case_id in {"TC-025"}:
            return "toggle_all_active", "", {}
        if case_id in {"TC-176"}:
            return "toggle_all_completed", "", {"mixed_seed": True}
        target = "completed" if case_number % 2 else "active"
        return (
            f"toggle_all_{target}",
            "Approximation: generic 'specified status' rows are deterministically split between complete-all and activate-all to cover both allowed bulk actions.",
            {},
        )

    if requirement_id == "REQ-TODO-012":
        if case_id == "TC-131":
            return (
                "filter_empty_safe",
                "Approximation: to exercise an empty filtered result in a UI that hides filters on a totally empty list, seed one active item, switch to Completed, and verify the filtered result is empty.",
                {"filter_name": "completed"},
            )
        filter_name = _rotate(case_number, ["all", "active", "completed"])
        return (
            "filter_view",
            "Approximation: generic filter rows are deterministically rotated across All, Active, and Completed so each exported abstract row has a concrete filter target.",
            {"filter_name": filter_name},
        )

    if requirement_id == "REQ-TODO-013":
        if case_id in {"TC-031", "TC-033"}:
            return (
                "clear_completed_noop",
                "Approximation: the false branch of 'there are completed items' is executed with an all-active list and must remain unchanged.",
                {},
            )
        return "clear_completed_existing", "", {}

    raise AssertionError(f"Unhandled requirement mapping for {requirement_id}: {requirement_text} / {lowered_coverage}")


def load_case_records() -> list[CaseRecord]:
    optimized_rows = _read_csv(OPTIMIZED_CSV)
    traceability_rows = _read_csv(TRACEABILITY_CSV)
    requirement_rows = _read_csv(REQUIREMENTS_CSV)

    traceability_by_case = {row["test_case_id"]: row for row in traceability_rows}
    requirement_text_by_id = {row["requirement_id"]: row["requirement_text"] for row in requirement_rows}

    records: list[CaseRecord] = []
    for row in optimized_rows:
        trace = traceability_by_case[row["test_case_id"]]
        requirement_text = requirement_text_by_id.get(
            row["requirement_id"],
            _normalize_text(trace.get("requirement_text")) or "State transition model coverage case",
        )
        coverage_description = _normalize_text(trace.get("coverage_description"))
        plan, approximation_note, payload = _build_case_plan(row, requirement_text, coverage_description)
        records.append(
            CaseRecord(
                test_case_id=row["test_case_id"],
                suite_id=row["suite_id"],
                suite_name=row["suite_name"],
                requirement_id=row["requirement_id"],
                requirement_text=requirement_text,
                coverage_id=row["coverage_id"],
                coverage_description=coverage_description,
                technique=row["technique"],
                precondition=row["precondition"],
                test_data=_normalize_text(row.get("test_data")),
                steps=row["steps"],
                expected_result=row["expected_result"],
                priority=row["priority"],
                risk_level=row["risk_level"],
                coverage_type=row["coverage_type"],
                plan=plan,
                approximation_note=approximation_note,
                payload=payload,
            )
        )
    assert len(records) == 169, f"Expected 169 optimized cases, found {len(records)}"
    return records


CASES = load_case_records()


def _case_id(case: CaseRecord) -> str:
    return f"{case.test_case_id}[{case.requirement_id}|{case.coverage_id}|{case.plan}]"


@pytest.fixture(scope="session")
def browser_session():
    session = BrowserSession()
    yield session
    session.close()


def _prepare_case_page(driver: webdriver.Remote, case: CaseRecord) -> tuple[TodoPage, str, str]:
    list_slug = _case_list_slug(case.test_case_id)
    list_name = _api_list_name(list_slug)
    api_delete_list(list_name)
    page = TodoPage(driver)
    return page, list_slug, list_name


def _execute_case_once(driver: webdriver.Remote, case: CaseRecord) -> None:
    page, list_slug, list_name = _prepare_case_page(driver, case)
    plan = case.plan
    data = case.payload

    if plan == "create_success":
        page.open(list_slug)
        before = api_list_todos(list_name)
        page.create_via_ui(data["title"])
        _wait_for_backend_count(page, list_name, len(before) + 1)
        todos = api_list_todos(list_name)
        assert todos[-1]["title"] == data["title"].strip()
        assert todos[-1]["title"] in page.labels(visible_only=False)
        return

    if plan == "create_reject_empty":
        page.open(list_slug)
        before = api_list_todos(list_name)
        page.create_via_ui(data["title"])
        page.reload()
        assert api_list_todos(list_name) == before
        return

    if plan == "create_reject_overlength":
        page.open(list_slug)
        before = api_list_todos(list_name)
        page.create_via_ui(data["title"])
        page.reload()
        assert api_list_todos(list_name) == before
        return

    if plan == "trim_create_save":
        page.open(list_slug)
        page.create_via_ui(data["title"])
        _wait_for_backend_count(page, list_name, 1)
        todos = api_list_todos(list_name)
        assert todos[0]["title"] == data["title"].strip()
        return

    if plan == "trim_edit_save":
        _create_seed(list_name, titles=[data["original"]])
        page.open(list_slug)
        page.edit_submit(0, data["new_title"])
        _wait_for_backend_titles(page, list_name, [data["new_title"].strip()])
        assert page.labels(visible_only=False) == [data["new_title"].strip()]
        return

    if plan == "trim_whitespace_invalid_outcome":
        page.open(list_slug)
        before = api_list_todos(list_name)
        page.create_via_ui(data["title"])
        page.reload()
        assert api_list_todos(list_name) == before
        return

    if plan == "validation_no_invalid_commit_combined":
        page.open(list_slug)
        page.create_via_ui("   ")
        page.reload()
        assert api_list_todos(list_name) == []
        _create_seed(list_name, titles=["keep-me"])
        page.reload()
        page.edit_submit(0, "   ")
        _wait_for_backend_count(page, list_name, 0)
        return

    if plan == "toggle_single":
        todo = _create_seed(list_name, titles=["toggle me"])[0]
        page.open(list_slug)
        page.toggle_item(0)
        page.wait.until(lambda _: len(api_list_todos(list_name)) == 1 and api_list_todos(list_name)[0]["completed"] is True)
        updated = _wait_for_single_backend_todo(page, list_name)
        assert updated["id"] == todo["id"]
        assert updated["completed"] is True
        return

    if plan == "toggle_roundtrip":
        _create_seed(list_name, titles=["toggle twice"])
        page.open(list_slug)
        page.toggle_item(0)
        page.wait.until(lambda _: len(api_list_todos(list_name)) == 1 and api_list_todos(list_name)[0]["completed"] is True)
        page.toggle_item(0)
        page.wait.until(lambda _: len(api_list_todos(list_name)) == 1 and api_list_todos(list_name)[0]["completed"] is False)
        return

    if plan == "toggle_missing_item":
        _create_seed(list_name, titles=["existing"])
        page.open(list_slug)
        before = api_list_todos(list_name)
        response = api_toggle_todo_response(list_name, INVALID_TODO_ID, True, expected=(404,))
        assert response.status_code == 404
        assert api_list_todos(list_name) == before
        return

    if plan == "enter_edit_existing":
        completed = bool(data["initial_completed"])
        _create_seed(list_name, titles=["editable"], completed_indexes={0} if completed else set())
        page.open(list_slug)
        input_box = page.enter_edit_mode(0)
        assert input_box.get_attribute("value") == "editable"
        return

    if plan == "enter_edit_single_click_noop":
        _create_seed(list_name, titles=["single-click"])
        page.open(list_slug)
        page.single_click_label(0)
        assert page.driver.find_elements(By.CSS_SELECTOR, ".todo-list li.editing .edit") == []
        return

    if plan == "enter_edit_missing_item":
        _create_seed(list_name, titles=["present"])
        page.open(list_slug)
        before = api_list_todos(list_name)
        response = api_get_todo_response(list_name, INVALID_TODO_ID, expected=(404,))
        assert response.status_code == 404
        assert page.driver.find_elements(By.CSS_SELECTOR, ".todo-list li.editing .edit") == []
        assert api_list_todos(list_name) == before
        return

    if plan == "edit_save_valid":
        completed = bool(data["initial_completed"])
        _create_seed(list_name, titles=["before"], completed_indexes={0} if completed else set())
        page.open(list_slug)
        page.edit_submit(0, data["new_title"])
        _wait_for_backend_titles(page, list_name, [data["new_title"]])
        saved = _wait_for_single_backend_todo(page, list_name)
        assert saved["completed"] is completed
        return

    if plan == "edit_save_valid_100":
        _create_seed(list_name, titles=["before"])
        page.open(list_slug)
        page.edit_submit(0, data["new_title"])
        _wait_for_backend_titles(page, list_name, [data["new_title"]])
        assert len(_wait_for_single_backend_todo(page, list_name)["title"]) == 100
        return

    if plan == "edit_reject_overlength":
        todo = _create_seed(list_name, titles=["before"])[0]
        page.open(list_slug)
        before = api_list_todos(list_name)
        response = api_update_todo_response(list_name, todo["id"], data["new_title"], expected=(400,))
        assert response.status_code == 400
        assert api_list_todos(list_name) == before
        assert page.labels(visible_only=False) == ["before"]
        return

    if plan == "edit_missing_item":
        _create_seed(list_name, titles=["before"])
        page.open(list_slug)
        before = api_list_todos(list_name)
        response = api_update_todo_response(list_name, INVALID_TODO_ID, data["new_title"], expected=(404,))
        assert response.status_code == 404
        assert api_list_todos(list_name) == before
        return

    if plan == "edit_empty_delete":
        completed = bool(data.get("initial_completed"))
        _create_seed(list_name, titles=["to-delete"], completed_indexes={0} if completed else set())
        page.open(list_slug)
        page.edit_submit(0, data["new_title"])
        _wait_for_backend_count(page, list_name, 0)
        assert page.labels(visible_only=False) == []
        return

    if plan == "edit_escape_cancel":
        completed = bool(data["initial_completed"])
        _create_seed(list_name, titles=["original"], completed_indexes={0} if completed else set())
        page.open(list_slug)
        page.edit_escape(0, data["draft_title"])
        page.wait.until(lambda _: len(api_list_todos(list_name)) == 1 and api_list_todos(list_name)[0]["title"] == "original")
        todo = _wait_for_single_backend_todo(page, list_name)
        assert todo["title"] == "original"
        assert todo["completed"] is completed
        return

    if plan == "delete_existing":
        completed = bool(data["initial_completed"])
        _create_seed(list_name, titles=["remove-me"], completed_indexes={0} if completed else set())
        page.open(list_slug)
        page.delete_item(0)
        _wait_for_backend_count(page, list_name, 0)
        return

    if plan == "delete_missing_item":
        _create_seed(list_name, titles=["kept"])
        page.open(list_slug)
        before = api_list_todos(list_name)
        response = api_delete_todo_response(list_name, INVALID_TODO_ID, expected=(404,))
        assert response.status_code == 404
        assert api_list_todos(list_name) == before
        return

    if plan == "toggle_all_completed":
        if data.get("mixed_seed"):
            _create_seed(list_name, titles=["a", "b", "c"], completed_indexes={1})
        else:
            _create_seed(list_name, titles=["a", "b", "c"])
        page.open(list_slug)
        page.toggle_all()
        page.wait.until(lambda _: all(todo["completed"] for todo in api_list_todos(list_name)))
        assert all(page.completed_flags())
        return

    if plan == "toggle_all_active":
        _create_seed(list_name, titles=["a", "b", "c"], completed_indexes={0, 1, 2})
        page.open(list_slug)
        page.toggle_all()
        page.wait.until(lambda _: all(not todo["completed"] for todo in api_list_todos(list_name)))
        assert not any(page.completed_flags())
        return

    if plan == "toggle_all_empty_noop":
        page.open(list_slug)
        assert api_list_todos(list_name) == []
        assert page.main_visible() is False
        assert page.footer_visible() is False
        return

    if plan == "filter_view":
        _create_seed(list_name, titles=["active one", "completed one", "active two"], completed_indexes={1})
        page.open(list_slug)
        page.select_filter(data["filter_name"])
        visible = page.labels()
        if data["filter_name"] == "all":
            assert visible == ["active one", "completed one", "active two"]
        elif data["filter_name"] == "active":
            assert visible == ["active one", "active two"]
        else:
            assert visible == ["completed one"]
        assert page.selected_filter() == data["filter_name"]
        return

    if plan == "filter_empty_safe":
        _create_seed(list_name, titles=["active only"])
        page.open(list_slug)
        page.select_filter(data["filter_name"])
        assert page.labels() == []
        assert page.selected_filter() == data["filter_name"]
        assert api_list_todos(list_name, status="completed") == []
        return

    if plan == "clear_completed_existing":
        _create_seed(list_name, titles=["active", "done one", "done two"], completed_indexes={1, 2})
        page.open(list_slug)
        page.clear_completed()
        _wait_for_backend_titles(page, list_name, ["active"])
        remaining = api_list_todos(list_name)
        assert [todo["title"] for todo in remaining] == ["active"]
        assert all(not todo["completed"] for todo in remaining)
        return

    if plan == "clear_completed_noop":
        _create_seed(list_name, titles=["still active"])
        page.open(list_slug)
        before = api_list_todos(list_name)
        assert api_list_todos(list_name) == before
        completed = api_list_todos(list_name, status="completed")
        assert completed == []
        clear_buttons = page.driver.find_elements(By.CSS_SELECTOR, ".clear-completed")
        assert clear_buttons == [] or all(not button.is_displayed() for button in clear_buttons)
        return

    if plan == "state_toggle_to_completed":
        _create_seed(list_name, titles=["stateful"])
        page.open(list_slug)
        page.toggle_item(0)
        page.wait.until(lambda _: len(api_list_todos(list_name)) == 1 and api_list_todos(list_name)[0]["completed"] is True)
        return

    if plan == "state_toggle_to_active":
        _create_seed(list_name, titles=["stateful"], completed_indexes={0})
        page.open(list_slug)
        page.toggle_item(0)
        page.wait.until(lambda _: len(api_list_todos(list_name)) == 1 and api_list_todos(list_name)[0]["completed"] is False)
        return

    if plan == "state_enter_edit_active":
        _create_seed(list_name, titles=["active-edit"])
        page.open(list_slug)
        assert page.enter_edit_mode(0).get_attribute("value") == "active-edit"
        return

    if plan == "state_enter_edit_completed":
        _create_seed(list_name, titles=["completed-edit"], completed_indexes={0})
        page.open(list_slug)
        assert page.enter_edit_mode(0).get_attribute("value") == "completed-edit"
        return

    if plan == "state_edit_save_active":
        _create_seed(list_name, titles=["before"])
        page.open(list_slug)
        page.edit_submit(0, data["new_title"])
        _wait_for_backend_titles(page, list_name, [data["new_title"]])
        assert _wait_for_single_backend_todo(page, list_name)["completed"] is False
        return

    if plan == "state_edit_empty_delete":
        _create_seed(list_name, titles=["delete-me"])
        page.open(list_slug)
        page.edit_submit(0, "")
        _wait_for_backend_count(page, list_name, 0)
        return

    if plan == "state_escape_from_edit_active":
        _create_seed(list_name, titles=["restore-me"])
        page.open(list_slug)
        page.edit_escape(0, "draft")
        page.wait.until(lambda _: len(api_list_todos(list_name)) == 1 and api_list_todos(list_name)[0]["title"] == "restore-me")
        assert _wait_for_single_backend_todo(page, list_name)["completed"] is False
        return

    if plan == "state_escape_from_edit_completed":
        _create_seed(list_name, titles=["restore-completed"], completed_indexes={0})
        page.open(list_slug)
        page.edit_escape(0, "draft")
        page.wait.until(lambda _: len(api_list_todos(list_name)) == 1 and api_list_todos(list_name)[0]["title"] == "restore-completed")
        assert _wait_for_single_backend_todo(page, list_name)["completed"] is True
        return

    if plan == "state_delete_active":
        _create_seed(list_name, titles=["delete-active"])
        page.open(list_slug)
        page.delete_item(0)
        _wait_for_backend_count(page, list_name, 0)
        return

    if plan == "state_delete_completed":
        _create_seed(list_name, titles=["delete-completed"], completed_indexes={0})
        page.open(list_slug)
        page.delete_item(0)
        _wait_for_backend_count(page, list_name, 0)
        return

    if plan == "state_toggle_all_completed":
        _create_seed(list_name, titles=["one", "two"])
        page.open(list_slug)
        page.toggle_all()
        page.wait.until(lambda _: all(todo["completed"] for todo in api_list_todos(list_name)))
        return

    if plan == "state_toggle_all_active":
        _create_seed(list_name, titles=["one", "two"], completed_indexes={0, 1})
        page.open(list_slug)
        page.toggle_all()
        page.wait.until(lambda _: all(not todo["completed"] for todo in api_list_todos(list_name)))
        return

    if plan == "state_clear_completed":
        _create_seed(list_name, titles=["active", "completed"], completed_indexes={1})
        page.open(list_slug)
        page.clear_completed()
        _wait_for_backend_titles(page, list_name, ["active"])
        return

    raise AssertionError(f"Unhandled plan {plan} for {case.test_case_id}")


def execute_case(browser_session: BrowserSession, case: CaseRecord) -> None:
    try:
        _execute_case_once(browser_session.driver, case)
    except InvalidSessionIdException:
        _execute_case_once(browser_session.restart(), case)


@pytest.mark.parametrize("case", CASES, ids=_case_id)
def test_todoitem_cases_generated_from_csv(browser_session: BrowserSession, case: CaseRecord):
    """
    Single entry point so every optimized CSV record remains individually traceable.

    Traceability fields kept on each parameterized case:
      - test_case_id
      - requirement_id
      - coverage_id
      - suite_id
    """

    execute_case(browser_session, case)
