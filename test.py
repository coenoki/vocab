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
    "persistent",
    "perspective",
    "predicament",
    "allegiance",
    "allude",
    "alternate",
    "analyze",
    "assert",
    "assess",
    "attribute",
    "bias",
    "brevity",
    "clarify",
    "collide",
    "compromise",
    "concise",
    "conform",
    "context",
    "contradict",
    "coordinate",
    "correlate",
    "credible",
    "dedicate",
    "deficiency",
    "derive",
    "devote",
    "dilemma",
    "distinguish",
    "diverge",
    "dominate",
    "emphasis",
    "emulate",
    "equate",
    "establish",
    "ethics",
    "excerpt",
    "exemplify",
    "exhibit",
    "explanation",
    "feasible",
    "formulate",
    "heritage",
    "illustrate",
    "imply",
    "juvenile",
    "kinetic",
    "legitimate",
    "liberate",
    "lucrative",
    "manipulate",
    "magnitude",
    "mandatory",
    "mediate",
    "meticulous",
    "motive",
    "negligent",
    "notable",
    "notion",
    "novel",
    "objective",
    "obligate",
    "obsolete",
    "omniscient",
    "optimize",
    "origin",
    "paradox",
    "parameter",
    "persuade",
    "phenomenon",
    "plausible",
    "potential",
    "precede",
    "predominant",
    "prejudice",
    "preliminary",
    "presume",
    "priority",
    "proclaim",
    "proficient",
    "proportion",
    "prosper",
    "protocol",
    "qualitative",
    "quantitative",
    "recession",
    "relevant"
]

def test_defn(start_index, end_index):
    path = './vocab/vocab_cody.json'
    defn = []

    with open(path, 'r') as file:
        defn = json.load(file)

    for _ in range(min(100, math.ceil((end_index - start_index) * 2))):
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
    test_defn(137, 165)
    # generate_defn()

if __name__ == '__main__':
    main()
