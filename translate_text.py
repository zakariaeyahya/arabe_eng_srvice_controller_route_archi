from seamless_translator import SeamlessTranslator

translator = SeamlessTranslator()

def translate_text(text, src_lang, tgt_lang):
    return translator.translate_text(text, src_lang, tgt_lang)