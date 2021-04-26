# Localization Scripts for quboga.me

This folder contains scripts and configuration files that automatically create and bake different versions of the website in other languages, effectively localizing them.

## Dependencies

* Python >=3.9.4 64-bit
* `google-api-python-client` >=2.1.0
* `google-auth-httplib2` >=0.1.0
* `google-auth-oauthlib` >=0.4.4
* `appdirs` >=1.4.4
* `beautifulsoup4` >=4.9.3
* `gitpython` >=3.1.14

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
7. Run the script: `python3 localize.py`

Note: On first run, you may be prompted for a `credentials.json` file and be required to log in to Google. This is necessary in order to access the localization data.

## Settings

Before running `localize.py`, be sure to configure `settings.json` with the localizer settings that should be used when translating the website.

Setting Name | Description | Optional
-------------|-------------|------------
`output` | Relative to the `docs` folder, the path to the directory that should contain the localized versions of the webpages.
`input` | An array of paths to HTML files that should be localized, given relative to the `docs` folder.
`default` | The language name of the default language, exactly as it appears on row `1` of the spreadsheet, for which no web pages will be generated. 
`sheets` | An object containing values necessary to download the localization data from the Google Sheets spreadsheet
`sheets.documentId` | The unique ID specifying which Google Sheets document to download the localization data from
`sheets.spreadsheet` | The name of the spreadsheet to download data from. If not present, null, or empty, uses the default (first) spreadsheet | &check;
`sheets.start` | The start of the range to download data from. Note that row `1` is a assumed to contain the language names, and should not be specified.
`sheets.end` | The end of the range to download data from. Note that row `1` is a assumed to contain the language names, and should not be specified.
`bindings` | An array of objects containing values which bind translations on the localizations spreadsheet to actual, generated web pages.
`bindings[x].spreadsheetName` | The name of this language, exactly as it appears on row `1` of the localization spreadsheet
`bindings[x].languageCode` | The Accept-Language code for this language, as specified by [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
`bindings[x].generate` | If specified and set to `false`, no website will be generated for this language. Use to prevent generating a website for a language whose translations are not yet complete | &check;
`replacements` | An array of objects, each specifying selectors that should be replaced with the given HTML | &check;
`replacements[x].id` | A CSS ID representing the element whose contents should be replaced with the given HTML
`replacements[x].src` | The path to an HTML source file whose contents will replace the given selector 
`replacements[x].remove` | Should the CSS ID of this selector be removed after replacement? Defaults to `true` | &check;
`relink` | An array of HTML attributes whose values should be relinked, that is to say, their values should be treated as paths and replaced with new paths relative to their new directory. Apply the `no-relink` attribute to an element to disable this feature.

## Translating Elements

To translate an element's inner HTML, add the `localize` tag to the element, specifying the localization key for that translation. For instance:

```html
<p localize="website.welcome">Welcome to the website!</p>
```

To translate other attributes on an element, such as `src`, pass a JSON object to the `localize` attribute, specifying a localization key for each attribute you want to translate. The JSON object should use single, not double quotes. For instance:

```html
<img src="images/image.png" localize="{'src': 'website.image'}">
```

To translate both the inner HTML **and** an attribute, specify the `text` key inside the JSON object passed to the `localize` attribute:

```html
<a href="https://www.mywebsite.com" localize="{'text': 'website.link', 'href': 'website.link.url'}">Go to the website!</a>
```

To prevent certain tags and their children from appearing in translated documents, even though they appear in the source document, mark the tag with the `no-include` attribute.