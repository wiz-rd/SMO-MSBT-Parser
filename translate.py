import random
from googletrans import Translator

def translate(string: list[str]) -> list[str]:
    COUNT = 60
    
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
        
        # Translate the string into random languages COUNT times
        for _ in range(COUNT):
            target_language = random.choice(languages)
            print(f"Translating '{translated_text}' to {target_language}")
            translated_text = translator.translate(translated_text, dest=target_language).text
        
        # Finally translate the string back to English
        print(f"Translating final version back to English")
        translated_text = translator.translate(translated_text, dest="en").text
        
        translated_strings.append(translated_text)
    
    return translated_strings

if __name__ == "__main__":
    # testing it to make sure it works
    test_strings = [
        "This is a test message, yes? I sure hope it isn't a cowboy or cobweb.",
        "Why I'll be darned, if it isn't yet another landlubber.",
        "Hi! How did you get here so quickly? I thought you were a burst of lightning for a second there."
    ]

    outputs = translate(test_strings)

    print("+" * 10, "Final results:", "+" * 10)
    print("Original messages:")
    print(*test_strings, sep="\n")
    print("-" * 20)
    print("Translated messages:")
    print(*outputs, sep="\n")
