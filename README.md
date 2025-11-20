# FakeRest Book API Test - With Python language and PyTest Framework Automation
This project repository contains an API test automation framework for the **Books** endpoints of [FakeRestAPI] (https://fackerestapi.azurewebsites.net).

It is using:
- **Python laguage**
- **PyTest Framework**
- **request "method/librarie"** for HTTP calls
- **pytest-html** for Test reports
- **Github Actions** for CI - Pipelines call

# Project Structure
This project is structured based on the best pratices of test framework, for automation tests

```text
source/
    client_api/
        config.py       # That is prviding API configuration (URL base)
        book_client.py  # Is a reusable BookClient and more Book model details
tests/
    conferencetests.py  # Is that an fixture for (client, config, payload)
    book_api_test.py    # Providing tests case with happy path and edge cases
.github/
    workflows/
        test-api.yaml   # Actions from GitHub to CI Pipelines
requirements.txt        # Providing all the the configuration for pytest and python instalation
pytest.ini              # Configuration for initializing all the process
README.md               # All instructions about the project and execution