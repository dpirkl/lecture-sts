import deepl
from utils import AUTH_KEY

# DeepL API documentation:  https://www.deepl.com/docs-api/

# The authentication key for the DeepL API. Specified in another file.


class DeepLTranslator:
    """Translator Object using the DeepL API.

        Args:

            target_lang (str): The target language for the translation.
                For example:
                    'EN':       english,
                    'EN-GB':    british english,
                    'EN-US':    american english,
                    'DE':       german.

            source_lang (str): The language of the original text. DeepL automatically detects the language, if no value is provided for this parameter.
                (default is None)

            formality (str): The formality of the translated text.
                These are the options (from the DeepL API documentation):
                    'default'
                    'more':         for a more formal language
                    'less':         for a more informal language
                    'prefer_more':  for a more formal language if available, otherwise fallback to default formality
                    'prefer_less':  for a more informal language if available, otherwise fallback to default formality
                (default is 'default')

        """

    translator: deepl.Translator
    formality: str
    target_lang: str
    source_lang: str

    def __init__(self, target_lang: str = 'EN-US', source_lang: str = None, formality: str = 'default'):
        self.translator = deepl.Translator(AUTH_KEY)
        self.target_lang = target_lang
        self.source_lang = source_lang
        self.formality = formality

    def translate(self, text: str) -> str:
        """Translate the given text.

        Args:
            text (str): The text to translate.

        Returns:
            str: The translated text.
        """

        if self.source_lang is not None:
            result = self.translator.translate_text(text, target_lang=self.target_lang, source_lang=self.source_lang,
                                                    formality=self.formality)
        else:
            result = self.translator.translate_text(text, target_lang=self.target_lang, formality=self.formality)

        return result.text
