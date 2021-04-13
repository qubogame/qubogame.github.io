# Localization Scripts for quboga.me

This folder contains scripts and configuration files that automatically create and bake different versions of the website in other languages, effectively localizing them.

## Dependencies

* Python >=3.9.4 64-bit
* `google-api-python-client` >=2.1.0
* `google-auth-httplib2` >=0.1.0
* `google-auth-oauthlib` >=0.4.4
* `appdirs` >=1.4.4

## Usage

To run the script and build the localized pages, follow these instructions:

1. Download and install [Python 3.9](https://www.python.org/downloads/release/python-394/), and be sure to add Python to your PATH
2. Open a terminal, and navigate to the `localization` directory inside this repository.
3. Create a virtual environment by running: `python3 -m venv venv`
4. Activate the virtual environment by running:
    * `source venv/bin/activate` on Bash shells
    * `venv\Scripts\activate.bat` on Windows command prompts
    * `venv\Scripts\Activate.ps1` on Windows PowerShell
5. Install all required Python packages by running: `pip install -r requirements.txt`
6. Modify any localization settings in `settings.json` as necessary (see below).
7. Run the script: `python3 localizer.py`

Note: On first run, you may be prompted for a `credentials.json` file and be required to log in to Google. This is necessary in order to access the localization data.

## Settings

Before running `localizer.py`, be sure to configure `settings.json` with the localizer settings that should be used when translating the website.

Setting Name | Description | Optional
-------------|-------------|------------
`output` | Relative to the `docs` folder, the path to the directory that should contain the localized versions of the webpages.
`default` | The language code of the default language (specified in `bindings`), for which no web pages will be generated. 
`sheets` | An object containing values necessary to download the localization data from the Google Sheets spreadsheet
`sheets.documentId` | The unique ID specifying which Google Sheets document to download the localization data from
`sheets.spreadsheet` | The name of the spreadsheet to download data from. If null or empty, uses the default (first) spreadsheet
`sheets.start` | The start of the range to download data from. Note that row `A` is a assumed to contain the language names, and should not be specified.
`sheets.end` | The end of the range to download data from. Note that row `A` is a assumed to contain the language names, and should not be specified.
`bindings` | An array of objects containing values which bind translations on the localizations spreadsheet to actual, generated web pages.
`bindings[x].spreadsheetName` | The name of this language, exactly as it appears on row `A` of the localization spreadsheet
`bindings[x].languageCode` | The Accept-Language code for this language, as specified by [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
`bindings[x].generate` | If specified and set to `false`, no website will be generated for this language. Use to prevent generating a website for a language whose translations are not yet complete | &check;
