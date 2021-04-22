_kSheets = "sheets"
_kDocumentId = "documentId"
_kSpreadsheet = "spreadsheet"
_kStart = "start"
_kEnd = "end"

_kDefault = "default"

def _a1Notation (start, end, spreadsheet):
    '''Returns the A1 notation for the given start and end ranges, and an optional spreadsheet name'''
    a1 = f"{start}:{end}"
    if spreadsheet.strip():
        a1 = f"{spreadsheet}!{a1}"
    return a1

def _getRange(sheetsSettings):
    '''Returns the sheet range to download from the settings object in A1 notation'''
    return _a1Notation(sheetsSettings[_kStart], sheetsSettings[_kEnd], sheetsSettings.get(_kSpreadsheet, ""))

def _downloadData (sheets, sheetsSettings):
    '''Downloads and returns the raw spreadsheet data, whose range is specified by the settings'''

    # We need to make sure we download row 1, as this contains the translations' language names
    ranges = [_a1Notation("1", "1", sheetsSettings.get(_kSpreadsheet, "")), _getRange(sheetsSettings)]

    result = sheets.values().batchGet(spreadsheetId=sheetsSettings[_kDocumentId],
        ranges=ranges).execute()
    
    # If returned valueRanges does not exist or is empty, return empty array
    if "valueRanges" not in result or not result["valueRanges"]: return []
    valueRanges = result["valueRanges"]
    header = valueRanges[0].get("values", [])
    values = valueRanges[1].get("values", [])

    print (f"Downloaded {len(values)} translations from Google Sheets...")

    return header + values 

def _mapTranslations (raw) -> dict[str, dict[str, str]]:
    '''Given the raw spreadsheet data, creates a dictionary which maps localization keys to language-specific location data
    
    For instance, to get the translation of the key "test.key" for the spreadsheet language called "Spanish" one would use:

        _mapTranslations(raw)["test.key"]["Spanish"]
    '''
    
    translations = {}

    headers = raw[0] # List of languages

    for i in range(1, len(raw)):
        row = raw[i]

        # If this row is empty or if there is no key assigned to it, ignore it
        if not row or not row[0].strip(): continue

        languages = {}

        for j in range (1, len(headers)):
            # Go through translations one by one and parse them

            language = headers[j].strip()
            if not language: continue # No language for this index, skip

            translation = row[j] if j < len(row) else ""
            languages[language] = translation
            
        translations[row[0].strip()] = languages

    return translations

def _getLanguageSet (data):
    '''Gets the set of languages in this spreadsheet from the raw data'''
    header = data[0]
    languages = set()
    for i in range(1, len(header)):
        lang = header[i].strip()
        if not lang: continue
        languages.add(lang)
    return languages

class Translations:
    '''
    Helper class that encapsulates translation data downloaded from Google Sheets.
    '''

    def __init__(self, sheets, settings):
        '''Creates a translations object and downloads the translation data from Google Sheets'''
        self._settings = settings
        self._sheetsSettings = settings[_kSheets]
        self._sheets = sheets

        data = _downloadData(self._sheets, self._sheetsSettings)
        self._mapping = _mapTranslations(data)

        self.languages = _getLanguageSet(data)
        self.defaultLanguage = settings[_kDefault]

        if (self.defaultLanguage not in self.languages):
            print(f"Warning: Default language '{self.defaultLanguage}' in settings.json is not one of the languages specified by the Google Sheets spreadsheet.")

    def get(self, key: str, lang: str) -> str:
        '''
        Given a localization key and a language name (exactly as it appears on the spreadsheet),
        returns the translation of the key into the given language.
            
        If no key exists, returns the key name.
            
        If no translation exists for this language, returns default language translation.
        '''

        if key not in self._mapping:
            print (f"WARING: No translations found for key '{key}'. Using key name instead...")
            return key

        translations = self._mapping[key]
        if lang not in translations or not translations[lang]:
            print (f"WARNING: No {lang} translation found for key '{key}'. Using the '{self.defaultLanguage}' translation instead...")
            return translations[self.defaultLanguage]

        return translations[lang]

    def hasKey (self, key: str) -> bool:
        '''Returns a true if a translation for key exists, and false otherwise'''
        return key in self._mapping
