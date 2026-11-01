# OpenCart System Tests (32571 Assessment Task 3)

Automated Selenium + pytest tests for https://opencart.abstracta.us/

| Test Case | Function | File |
|---|---|---|
| TC07 | F07 Add to Shopping Cart | `tests/test_tc07_add_to_cart.py` |
| TC08 | F08 Update Cart Quantity | `tests/test_tc08_update_quantity.py` |
| TC09 | F09 Remove from Cart | `tests/test_tc09_remove_from_cart.py` |

Each file has three scenarios (`test_s1_…`, `test_s2_…`, `test_s3_…`). Page objects live in `pages/`.

## Setup (Windows)

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Requires Google Chrome; Selenium Manager downloads the matching ChromeDriver automatically.

## Run

```
.venv\Scripts\python.exe -m pytest                 # all tests, visible Chrome
.venv\Scripts\python.exe -m pytest -m tc07         # one test case
set HEADLESS=1 && .venv\Scripts\python.exe -m pytest   # headless
```

Outputs:
- `reports/report.html` – HTML report (failure screenshots embedded)
- `screenshots/<test name>/NN_<step>.png` – step-by-step screenshots
