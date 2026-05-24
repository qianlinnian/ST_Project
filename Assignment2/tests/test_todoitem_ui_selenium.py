import json
import os
import urllib.error
import urllib.request

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


FRONTEND_URL = os.getenv(
    "TODO_FRONTEND_URL",
    "http://127.0.0.1:8000/todo.html#/&test-list",
)
API_BASE_URL = os.getenv("TODO_API_BASE_URL", "http://127.0.0.1:5000/api")
BROWSER = os.getenv("SELENIUM_BROWSER", "chrome").lower()
HEADLESS = os.getenv("SELENIUM_HEADLESS", "0") == "1"


def api_request(method, path, payload=None):
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        API_BASE_URL + path,
        data=data,
        headers=headers,
        method=method,
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        body = response.read().decode("utf-8")
        return json.loads(body)["data"] if body else None


def reset_todos():
    todos = api_request("GET", "/todos")
    for todo in todos:
        api_request("DELETE", f"/todos/{todo['id']}")


def create_driver():
    if BROWSER == "edge":
        options = webdriver.EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        return webdriver.Edge(options=options)

    if BROWSER == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("-headless")
        return webdriver.Firefox(options=options)

    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=options)


@pytest.fixture(scope="session")
def driver():
    browser = create_driver()
    yield browser
    browser.quit()


@pytest.fixture(autouse=True)
def clean_state(driver):
    try:
        reset_todos()
    except urllib.error.URLError as exc:
        pytest.fail(f"Backend API is not available at {API_BASE_URL}: {exc}")
    driver.get(FRONTEND_URL)
    TodoPage(driver).wait_until_loaded()


@pytest.fixture
def page(driver):
    return TodoPage(driver)


class TodoPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def wait_until_loaded(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".new-todo")))
        self.wait.until(lambda d: "TODOs : test list" in d.find_element(By.ID, "todostitle").text)

    def add(self, title):
        new_todo = self.driver.find_element(By.CSS_SELECTOR, ".new-todo")
        new_todo.clear()
        new_todo.send_keys(title)
        new_todo.send_keys(Keys.TAB)
        self.wait_for_text(title)

    def add_many(self, *titles):
        for title in titles:
            self.add(title)

    def visible_items(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".todo-list li")

    def visible_count(self):
        return len(self.visible_items())

    def texts(self):
        return [item.find_element(By.CSS_SELECTOR, "label").text for item in self.visible_items()]

    def completed_flags(self):
        return ["completed" in item.get_attribute("class").split() for item in self.visible_items()]

    def active_count_text(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".todo-count").text

    def assert_visible(self, expected_texts, expected_completed=None):
        self.wait.until(lambda _: self.texts() == list(expected_texts))
        assert self.visible_count() == len(expected_texts)
        assert self.texts() == list(expected_texts)
        if expected_completed is not None:
            assert self.completed_flags() == list(expected_completed)

    def wait_for_text(self, title):
        self.wait.until(lambda _: title in self.texts())

    def wait_for_count(self, count):
        self.wait.until(lambda _: self.visible_count() == count)

    def item_by_text(self, title):
        self.wait_for_text(title)
        for item in self.visible_items():
            if item.find_element(By.CSS_SELECTOR, "label").text == title:
                return item
        raise AssertionError(f"Todo item not found: {title}")

    def toggle(self, title):
        self.item_by_text(title).find_element(By.CSS_SELECTOR, ".toggle").click()
        self.wait.until(lambda _: title in self.texts())

    def toggle_all(self):
        self.driver.find_element(By.ID, "toggle-all").click()
        self.wait.until(lambda _: all(self.completed_flags()))

    def edit(self, old_title, new_title):
        item = self.item_by_text(old_title)
        label = item.find_element(By.CSS_SELECTOR, "label")
        ActionChains(self.driver).double_click(label).perform()

        edit_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "li.editing .edit"))
        )

        # Selenium 的 Ctrl+A 在部分前端/浏览器组合下不稳定，
        # 所以这里用 JS 直接设置 value，并派发 input/change 事件。
        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            input.focus();
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            edit_input,
            new_title,
        )

        # 同时尝试 按下 Enter 键 和 失去焦点 来提交编辑，确保在各种前端实现下都能正确触发保存逻辑。
        edit_input.send_keys(Keys.ENTER)
        self.driver.execute_script("arguments[0].blur();", edit_input)

        if new_title.strip():
            self.wait.until(lambda _: new_title.strip() in self.texts())
        else:
            self.wait.until(lambda _: old_title not in self.texts())

    def delete(self, title):
        item = self.item_by_text(title)
        ActionChains(self.driver).move_to_element(item).perform()
        item.find_element(By.CSS_SELECTOR, ".destroy").click()
        self.wait.until(lambda _: title not in self.texts())

    def clear_completed(self):
        self.driver.find_element(By.CSS_SELECTOR, ".clear-completed").click()

    def filter_all(self):
        self.driver.find_element(By.CSS_SELECTOR, '.filters a[href="#/"]').click()

    def filter_active(self):
        self.driver.find_element(By.CSS_SELECTOR, '.filters a[href="#/active"]').click()

    def filter_completed(self):
        self.driver.find_element(By.CSS_SELECTOR, '.filters a[href="#/completed"]').click()


def test_tc066_add_valid_item_from_empty_list(page):
    page.add("Buy milk")

    page.assert_visible(["Buy milk"], [False])
    assert page.active_count_text() == "1 item left"


def test_tc067_toggle_item_completed(page):
    page.add("item 1")

    page.toggle("item 1")

    page.assert_visible(["item 1"], [True])
    assert page.active_count_text() == "0 items left"


def test_tc068_edit_item_title_to_non_empty(page):
    page.add("item 1")

    page.edit("item 1", "Buy eggs")

    page.assert_visible(["Buy eggs"], [False])


def test_tc069_edit_item_title_to_empty_removes_item(page):
    page.add("item 1")

    page.edit("item 1", "")

    page.wait_for_count(0)
    assert page.texts() == []


def test_tc070_delete_single_item(page):
    page.add_many("item 1", "item 2")

    page.delete("item 1")

    page.assert_visible(["item 2"], [False])


def test_tc071_toggle_all_to_completed(page):
    page.add_many("item 1", "item 2", "item 3")

    page.toggle_all()

    page.assert_visible(["item 1", "item 2", "item 3"], [True, True, True])
    assert page.active_count_text() == "0 items left"


def test_tc072_filter_active_only_shows_incomplete_items(page):
    page.add_many("active item", "completed item")
    page.toggle("completed item")

    page.filter_active()

    page.assert_visible(["active item"], [False])
    assert page.active_count_text() == "1 item left"


def test_tc073_filter_completed_only_shows_completed_items(page):
    page.add_many("active item", "completed item")
    page.toggle("completed item")

    page.filter_completed()

    page.assert_visible(["completed item"], [True])


def test_tc074_clear_completed_keeps_active_items(page):
    page.add_many("active item", "done item")
    page.toggle("done item")

    page.clear_completed()
    page.wait.until(lambda _: page.texts() == ["active item"])

    page.assert_visible(["active item"], [False])
    assert page.active_count_text() == "1 item left"


def test_invalid_blank_and_whitespace_input_are_ignored(page):
    new_todo = page.driver.find_element(By.CSS_SELECTOR, ".new-todo")
    new_todo.send_keys("   ")
    new_todo.send_keys(Keys.TAB)

    short_wait = WebDriverWait(page.driver, 0.5)
    with pytest.raises(TimeoutException):
        short_wait.until(lambda _: page.visible_count() == 1)
    assert page.visible_count() == 0


def test_filter_round_trip_preserves_completed_state(page):
    page.add_many("todo active", "todo done")
    page.toggle("todo done")

    page.filter_completed()
    page.assert_visible(["todo done"], [True])
    page.filter_active()
    page.assert_visible(["todo active"], [False])
    page.filter_all()
    page.assert_visible(["todo active", "todo done"], [False, True])

def test_toggle_item_completed_and_active(page):
    page.add("item 1")

    page.toggle("item 1")
    page.assert_visible(["item 1"], [True])
    assert page.active_count_text() == "0 items left"

    page.toggle("item 1")
    page.assert_visible(["item 1"], [False])
    assert page.active_count_text() == "1 item left"