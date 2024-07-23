from dotenv import load_dotenv

load_dotenv()

import os
import math
import random
import json
import openai

SYSTEM_MESSAGE = '''Give me the following information about each word as a list of JSON objects:

1. definition (string)
2. example (string): Example sentense that demonstrates how to use the word
3. part_of_speech (string): Part of speech of the word, eg verb, adjective, etc
4. pronounciation (string)

The output must be a list of JSON objects. Here's an example:

```json
[
    {
        "word": "Candid",
        "definition": "...",
        "example": "...",
        "part_of_speech": "...",
        "pronounciation": "..."
    },
    ...
]
```
'''

WORDS = [
    'Peculiar', 'Aticulate', 'Superfluous', 'Controversy', 'Diminish', 'Intrepid', 'Prodigious', 'Coherent', 'Disdain', 'Enigma', 'Extricate', 'Hypocrisy', 'Capitulate', 'Deft', 'Frivolous', 'Grandious', 'Imperative', 'Opaque', 'Paradox', 'Relinquish', 'Fathom', 'Indomitable', 'Lament', 'Acquaintence', 'Adversary', 'Archaic', 'Laudable', 'Propencity', 'Substantiate', 'Abundance', 'Penchant', 'Permeate', 'Controversy', 'Sagacious', 'Abolish', 'Amend', 'Concur', 'Eccentric', 'Exemplary', 'Imminent', 'Inevitable', 'Lucrative', 'Placid', 'Reclusive', 'Vindicate', 'Alleviate', 'Dubious', 'Ostentatious', 'Pragmatic'

]

def test_defn(start_index, end_index):
    path = './vocab/vocab_cody.json'
    defn = []

    with open(path, 'r') as file:
        defn = json.load(file)

    for _ in range(math.ceil((end_index - start_index) * 2)):
        i = random.randint(0, (end_index - start_index) or len(defn))
        word = defn[start_index + i]
        print(f'\n\nWhat is the definition of {word["word"]}?')
        input()
        print(word['definition'])
        print(word['example'])
        print(word['part_of_speech'])
        input()

def _call_openai(client, words: list[str]) -> str:
    completion = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': SYSTEM_MESSAGE},
            {'role': 'user', 'content': '\n'.join(words)},
        ],
    )
    return completion.choices[0].message.content

def _extract_json(content: str) -> str:
    start_index = content.index('```json') + len('```json')
    end_index = content[start_index:].index('```') + start_index
    return content[start_index:end_index]

def _process_result(content: str):
    res = _extract_json(content)
    return json.loads(res)

def generate_defn():
    client = openai.OpenAI()

    cumulative_result = []

    for i in range(math.ceil(len(WORDS) / 10)):
        words = WORDS[i * 10:(i + 1) * 10]
        openai_result = _call_openai(client, words)
        result = _process_result(openai_result)
        cumulative_result += result

    print(json.dumps(cumulative_result, indent=2))

def main():
    test_defn(0, 70)
    #generate_defn()

if __name__ == '__main__':
    main()
