from bs4 import BeautifulSoup
import git
import os
import json
import codecs

from urllib.parse import urlparse

_kBindings = "bindings"

_kReplacements = "replacements"
_kReplacementsId = "id"
_kReplacementsSrc = "src"
_kReplacementsRemoveId = "remove"

_kInputs = "input"
_kOutput = "output"
_kRelink = "relink"

_kBindingSpreadsheet = "spreadsheetName"
_kBindingLanguageCode = "languageCode"
_kBindingGenerate = "generate"

class _Binding:
    '''A language binding specified in the settings'''
    def __init__ (self, settingsBinding):
        self.spreadsheetName = settingsBinding[_kBindingSpreadsheet]
        self.languageCode = settingsBinding[_kBindingLanguageCode]
        self.generate = settingsBinding.get(_kBindingGenerate, True)

class _BindingSet:
    '''The set of all language bindings specified in the settings'''
    def __init__(self, settings):
        bindings = settings[_kBindings]

        self.default = None
        self.bindings = []
        for settingsBinding in bindings:
            binding = _Binding(settingsBinding)

            if binding.spreadsheetName == settings["default"]:
                self.default = binding

            self.bindings.append(binding)

    def getSpreadsheetLanguages(self):
        '''Gets a collection of spreadsheet language names contained in this set'''
        langs = set()
        for binding in self.bindings:
            langs.add(binding.spreadsheetName)
        return langs

    def getBindingByCode (self, langCode):
        '''Gets a binding from an ISO language code.
        Returns None if no binding with this code could be found.'''
        for binding in self.bindings:
            if binding.languageCode.lower() == langCode.lower():
                return binding
        return None
        
    def getBindingByName (self, langName):
        '''Gets a binding from a spreadsheet language name.
        Returns None if no binding with this name could be found.'''
        for binding in self.bindings:
            if binding.spreadsheetName == langName:
                return binding
        return None

    def __iter__ (self):
        return self.bindings.__iter__()

def _getDocsPath ():
    '''Gets the absolute path to the docs path'''
    git_repo = git.Repo(os.path.realpath(__file__), search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    
    return os.path.join(git_root, "docs")

def _getPath (inputPath):
    '''Gets the absolute path to inputPath, which is a path relative to the docs folder'''
    return os.path.join(_getDocsPath(), inputPath)

def _saveLocalizationScript (settings, bindings: list[_Binding]):
    '''Saves the localization.js script into the localization folder'''
    print("Saving localization.js script...")

    # Get path to localization.js
    localizationScriptPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template", "localization.js")

    # Load script into memory
    scriptContents = None
    with codecs.open(localizationScriptPath, "r", "utf-8") as file:
        scriptContents = file.read()        

    # Convert bindings list to a javascript object
    bindingsStr = map(lambda x: f'"{x.languageCode}": "/{os.path.join(settings[_kOutput], x.languageCode)}"'.replace("\\", "/"), bindings)
    languageBindings = ", ".join(bindingsStr)
    languageBindings = "{" + languageBindings + "}"
    scriptContents = scriptContents.replace(u"{{LANG}}", languageBindings)

    # Save file
    with codecs.open(os.path.join(_getPath(settings[_kOutput]), "localization.js"), "w+", "utf-8") as file:
        file.write(scriptContents)

    print("Saved localization.js script.")


class Generator:
    '''Helper class that generates and outputs localized websites'''
    def __init__ (self, translations, settings):
        self.settings = settings
        self.translations = translations
        self.bindings = _BindingSet(settings)

    def generate(self):
        # Get list of bindings for which we will generate languages
        bindings = [binding for binding in self.bindings if (binding.generate and binding != self.bindings.default)]

        print (f"Generating webpages for {', '.join([b.spreadsheetName for b in bindings])}, with default language {self.bindings.default.spreadsheetName}")

        # Get list of input files
        inputs = self.settings[_kInputs]
        badInputs = []

        # Verify that all inputs exist
        for i in range(len(inputs) - 1, -1, -1):
            absPath = _getPath(inputs[i])
            if not os.path.exists(absPath):
                badInputs.append(inputs[i])
                del inputs[i]
        
        print (f"Using {', '.join(inputs)} as input files.")
        if (len(badInputs) > 0):
            print(f"WARNING: {', '.join(badInputs)} {'were' if len(badInputs) > 1 else 'was'} specified as input, but {'these files do' if len(badInputs) > 1 else 'this file does'} not exist")

        print()

        for binding in bindings:
            outputDir = os.path.join(self.settings[_kOutput], binding.languageCode)

            print ("=======================")
            print (f"Generating {binding.spreadsheetName} webpage at {outputDir}")

            for inp in inputs:
                outputPath = os.path.join(outputDir, inp)

                print (f"Generating '{inp}' at '{outputPath}'...")

                self._generatePage(inp, outputPath, binding)

                print (f"Generated '{inp}.'")

        _saveLocalizationScript(self.settings, bindings)

    def _generatePage(self, inputPath: str, outputPath: str, binding: _Binding):
        '''
        Generates a translated webpage.

        inputPath: The path to the input file, relative to the docs folder
        outputPath: The path to the output file, relative to the docs folder
        binding: A language binding indicating which translation we are creating
        '''

        # Load input HTML into a BeautifulSoup object
        soup = None
        with codecs.open(_getPath(inputPath), 'r', "utf-8") as file:
            raw = file.read()
            soup = BeautifulSoup(raw, features="html.parser")

        # Remove unwanted elements from the soup
        self._removeNoIncludes(soup)

        # Perform any replacements on the soup
        self._replacements(soup)

        # Translate the page
        self._translate(soup, binding)

        # Relink the page
        inputDir = os.path.dirname(inputPath)
        outputDir = os.path.dirname(outputPath)
        
        if not inputDir.startswith("/"): inputDir = "/" + inputDir
        if not outputDir.startswith("/"): outputDir = "/" + outputDir

        self._relink(soup, inputDir, outputDir)

        # Save the resulting soup
        output = _getPath(outputPath)

        os.makedirs(os.path.dirname(output), exist_ok=True) # Ensure write directory exists
        with codecs.open(output, 'w+', "utf-8") as output:
            output.write(str(soup.prettify()))

    def _removeNoIncludes (self, soup: BeautifulSoup) -> BeautifulSoup:
        '''Removes elements from the soup marked with no-include'''
        elements = soup.select("[no-include]")
        for element in elements: element.decompose()

    def _replacements (self, soup: BeautifulSoup) -> BeautifulSoup:
        '''Performs any replacements on the HTML, as specified in settings.json'''

        replacements = self.settings.get(_kReplacements, [])

        for replacement in replacements:
            elementId = replacement[_kReplacementsId]
            src = _getPath(replacement[_kReplacementsSrc])
            removeId = replacement.get(_kReplacementsRemoveId, True)

            # Find elements with this id
            matchingElements = soup.select(f"#{elementId}")

            if len(matchingElements) == 0: continue

            # Load replacement HTML
            replacementSoup = None
            with codecs.open(src, 'r', "utf-8") as file:
                raw = file.read()
                replacementSoup = BeautifulSoup(raw, features="html.parser")
            
            for rootElement in matchingElements:
                for replacementElement in (replacementSoup if replacementSoup.html is None else replacementSoup.html).find_all(recursive=False):
                    rootElement.append(replacementElement)

                # Delete matching element's id if necessary
                if removeId:
                    del rootElement.attrs["id"]

        return soup
    
    def _translate(self, soup: BeautifulSoup, binding: _Binding):
        '''
        Finds all elements in the soup with a "localize" attribute and attempts to translate them into the language specified by "binding"
        '''

        # Find all elements with the "localize" attribute
        elements = soup.select("[localize]")

        for element in elements:
            value = element["localize"]

            # Begin translating
            try:
                # Try to interpret value as a json object
                translations = json.loads(value.replace("'", '"'))

                for attr, key in translations.items():
                    translated = self.translations.get(key, binding.spreadsheetName)
                    
                    if attr == "text": element.string = translated
                    else: element[attr] = translated

            except json.decoder.JSONDecodeError:
                # Interpret value as a key
                element.string = self.translations.get(value, binding.spreadsheetName)

            # Delete the localize attribute (it doesn't need to be in the final document)
            del element.attrs["localize"]

    def _relink(self, soup, inputDir, outputDir):
        '''
        Relinks elements in the soup containing relinkable tags, as specified by the "relink" setting in settings.json.

        inputDir should be the path to the directory containing the input HTML, relative to the docs folder.
        outputDir should be the path to the directory that will contain the output HTML, relative to the docs folder.
        '''

        for attr in self.settings[_kRelink]:
            # For each relinkable attribute, find all elements of this type and perform modifications

            elements = soup.select(f"[{attr}]")

            for element in elements:
                if element.has_attr("no-relink"): continue # no-relink found, don't change this element

                # Get URL that we may or may not relink
                url = element[attr]

                # If url starts with pound character (#), do not relink
                if url.startswith("#"): continue

                parseResult = urlparse(url)

                # If url has a network location or a scheme (such as HTTP), don't relink, as this path is not relative
                if (parseResult.netloc or parseResult.scheme): continue

                assetPath = os.path.join(inputDir, url)

                relativePath = os.path.relpath(assetPath, start=outputDir)

                element[attr] = relativePath

        return soup
    
    
