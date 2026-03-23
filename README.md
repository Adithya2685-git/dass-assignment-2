Assignment 2
2024101012

Gdrive Link: 
https://drive.google.com/file/d/15G0Krmh0KzPrge73PgbEp_NKT9r4bFKu/view?usp=sharing

Folder Structure

```text
whitebox/
  code/
  diagrams/
  tests/
  report.pdf
integration/
  code/
  diagrams/
  tests/
  report.pdf
blackbox/
  tests/
  report.pdf
README.md
```

This repository assumes a local Python virtual environment at:

```bash
.venv
```


```bash
python -m venv .venv
.venv/bin/pip install pytest pylint requests
```

Whitebox

MoneyPoly Code

The `MoneyPoly` code is in:

```bash
whitebox/code/moneypoly/moneypoly
```

Run Pylint

```bash
cd whitebox/code/moneypoly/moneypoly
PYTHONPATH=. ../../../../.venv/bin/pylint main.py moneypoly/*.py
```

Run Whitebox Tests from the repository root:

```bash
.venv/bin/pytest -q whitebox/tests
```

Integration

StreetRace Manager Code implementation is in:

```bash
integration/code/streetrace_manager
```

Run StreetRace Manager
```bash
PYTHONPATH=integration/code python -m streetrace_manager
```

Run Integration Tests

```bash
.venv/bin/pytest -q integration/tests
```

Blackbox

QuickCart Server

The provided artifact is an OCI-style directory, not a tar file. To load it into Docker:

```bash
tar -C quickcart_image_x86 -cf /tmp/quickcart_image_x86.tar .
docker load -i /tmp/quickcart_image_x86.tar
docker run -d --name quickcart -p 8080:8080 quickcart:latest
```

If Docker is not running:

```bash
sudo systemctl start docker
```

Run Blackbox Tests from the repository root:

```bash
.venv/bin/pytest -q blackbox/tests
```

The tests use these environment variables if you want to override defaults:

```bash
QUICKCART_BASE_URL
QUICKCART_ROLL_NUMBER
QUICKCART_USER_ID
```

Default values used in the test scaffold are:

```bash
QUICKCART_BASE_URL=http://127.0.0.1:8080
QUICKCART_ROLL_NUMBER=2025000
QUICKCART_USER_ID=1
```
