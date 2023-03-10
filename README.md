# OS3C (Open Source Security Auditor/Checker)

---

OS3C is an open-source security testing tool for websites. Its primary focus is to help website owners and developers ensure the security and compliance of their websites. This tool is built with the ease of maintainability and extensibility in mind.

---

## Usage

---

To run OS3C, you need to use the `run.py` script and specify the target URL using the `-u` or `--url` option.

```sh
python3 run.py -u https://www.example.com
```

or if you have poetry installed:

- Install the dependencies

```sh
poetry install
```

- Run with poetry

```sh
poetry run python ./run.py -u https://www.example.com 
```

---

## Project Status
This project is currently under heavy development.

---

## Current To-Dos:
- Develop a user-friendly interface (potentially web based)
- Support session based request.
- Enable saving of progress.
- Allow testing of dynamically loaded pages.

---

## Callbacks/Modules
- Implemented
	- Email extractor.
	- Phone number extractor.
- Yet to be implemented
	- SQLi detector.
	- XSS detector.
	- ...

---

## Contributing

---

If you are interested in contributing to the development of OS3C, please get in touch! We welcome contributions of all kinds, including bug reports, feature requests, and pull requests.

---

## DISCLAIMER
This tool is not intended to be used for illegal or malicious purposes. The creators and contributors of OS3C are not responsible for any misuse of the tool. Please use OS3C in accordance with all applicable laws and ethical principles.
