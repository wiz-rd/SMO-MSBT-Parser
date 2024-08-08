import random
from googletrans import Translator

def translate(string: list[str]) -> list[str]:

    
    # List of languages to translate to
    languages = ["af","sq","am","ar","hy","az","eu","bn","bs","bg","ca","ceb","zh-CN","zh-TW","co","hr","cs","da","nl",
                 "en","eo","et","fi","fr","fy","gl","ka","de","el","gu","ht","ha","haw","iw","hi","hmn","hu","is","id","ga",
                 "ja","jw","kn","kk","km","ko","ku","lo","lv","lt","lb","mk","mg","ms","ml","mt","mi","mr","mn","ne","no","ny",
                 "ps","fa","pl","pt","pa","ro","ru","sm","gd","sr","st","sn","sd","si","sk","sl","so","es","sw","sv",
                 "tl","tg","ta","te","th","tr","uk","ur","uz","vi","cy","xh","yi","yo","zu"]
    
    # Initialize translator
    translator = Translator()
    
    translated_strings = []
    
    # Translate each string individually
    for text in string:
        translated_text = text
        
        # Translate the string 60 times into random languages
        for _ in range(60):
            target_language = random.choice(languages)
            print(f"Translating '{translated_text}' to {target_language}")
            translated_text = translator.translate(translated_text, dest=target_language).text
        
        # Finally translate the string back to English
        print(f"Translating final version back to English")
        translated_text = translator.translate(translated_text, dest="en").text
        
        translated_strings.append(translated_text)
    
    return translated_strings
