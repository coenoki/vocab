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
'''

WORDS = [
    'Excerpt', 'contemplate', 'daintily', 'Apprehensive', 'meticulous', 'Ambiguous', 'Indespensable', 'Conscientious', 'Exuberant', 'Innovative', 'Illuminate', 'Punctual', 'Accentuate', 'Altercation', 'Advocate', 'Capricous', 'Debunk',
]

def test_defn(num = None):
    path = './vocab/vocab_cody.json'
    defn = []

    with open(path, 'r') as file:
        defn = json.load(file)

    while True:
        i = random.randint(0, num or len(defn))
        word = defn[i]
        print(f'\n\nWhat is the definition of {word["word"]}?')
        input()
        print(word['definition'])
        print(word['example'])
        print(word['part_of_speech'])
        input()

def generate_defn():
    client = openai.OpenAI()

    results = []

    for i in range(math.ceil(len(WORDS) / 10)):
        words = WORDS[i * 10:(i + 1) * 10]
        completion = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': SYSTEM_MESSAGE},
                {'role': 'user', 'content': '\n'.join(words)},
            ],
        )
        content = completion.choices[0].message.content

        start_index = content.index('```json') + len('```json')
        end_index = content[start_index:].index('```') + start_index
        res = content[start_index:end_index]

        defn = json.loads(res)
        results.extend(defn)

    print(json.dumps(results, indent=2))

def main():
    # test_defn(31)
    generate_defn()

if __name__ == '__main__':
    main()
