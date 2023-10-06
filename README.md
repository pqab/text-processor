# Text processor

## Setup

Setup venv

```bash
pyenv which python3
.../python3 -m venv env
```

Set your shell to use the venv paths for Python by activating the virtual environment

```bash
source env/bin/activate
```

If you want to stop using the virtual environment and go back to your global Python, you can deactivate it:

```bash
deactivate
```

Ref: <https://cloud.google.com/python/docs/setup>

## Run

Setup input in input folder

```bash
python3 main.py
```

### Input

```text
└── input
    ├── input.env
    ├── extract_html
    │   ├── input.html
    │   └── extract_html.env
    ├── extract_csv
    │   └── input.csv
    ├── google_text_to_speech
    │   ├── service_account_key.json
    │   └── google_text_to_speech.env
    ├── google_drive_upload
    │   ├── service_account_key.json
    │   └── google_drive_upload.env
    └── replace_text
        └── input.txt
```

#### input/input.env

Config to define which input type, processors to use, etc...

| VARIABLE   | DESCRITPION                                                | AVAILABLE VALUE                                              |
| ---------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| processors | List of processors to be used in ordering (comma separtor) | extract_html<br>extract_csv<br>google_drive_upload<br>google_text_to_speech<br>replace_text |

### extract_html processor

Required inputs:

- input.html
- extract_html.env

Example:

***processor input***

input.html

```html
<p>Random paragraph <span id="text-cantonese-1" class="extract_text">Text 1</span></p>

<table>
    <thead>
        <tr>
            <th>Random Title</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Random text 1 - <span id="text-mandarin-2" class="extract_text">Text 2</span></td>
        </tr>
        <tr>
            <td>Random text 2- <span id="text-cantonese-3" class="extract_text">Text 3</span></td>
        </tr>
    </tbody>
</table>
```

extract_html.env

| VARIABLE     | DESCRITPION                                        | EXAMPLE      |
| ------------ | -------------------------------------------------- | ------------ |
| element_name | The element name to be extracted                   | span         |
| class_name   | The class name of the element name to be extracted | extract_text |

***processor output***

```python
dict(
    'text-cantonese-1', 'Text 1',
    'text-mandarin-2', 'Text 2',
    'text-cantonese-3', 'Text 3'
)
```

### extract_csv processor

Required inputs:

- input.csv

Example:

***processor input***

input.csv

```csv
id,value
text-1,"Text 1"
text-2,"Text 2"
text-3,"Text 3"
```

***processor output***

```python
dict(
    'text-cantonese-1', 'Text 1',
    'text-mandarin-2', 'Text 2',
    'text-cantonese-3', 'Text 3'
)
```

### google_text_to_speech processor

Required inputs:

- service_account_key.json
- google_text_to_speech.env

Example:

***processor input***

service_account_key.json

<https://cloud.google.com/docs/authentication/use-service-account-impersonation>

google_text_to_speech.env

<https://cloud.google.com/text-to-speech/docs/voices>

| VARIABLE                           | DESCRITPION                                                         | EXAMPLE            |
| ---------------------------------- | ------------------------------------------------------------------- | ------------------ |
| supported_languages                | The list of supported language                                      | cantonese,mandarin |
| <supported_language>_language_code | The language to be used in the TTS api for the supported language   | yue-HK             |
| <supported_language>_name          | The voice name to be used in the TTS api for the supported language | yue-HK-Standard-A  |

***processor output***

assumed the output from the previous processor

```python
dict(
    'text-cantonese-1', 'Text 1',
    'text-mandarin-2', 'Text 2',
    'text-cantonese-3', 'Text 3'
)
```

it will convert the text to audio file 1 by 1 using the google text-to-speech api, and map to the audio output path

```python
dict(
    'text-cantonese-1', 'output/google_text_to_speech/text-cantonese-1.mp3',
    'text-mandarin-2', 'output/google_text_to_speech/text-mandarin-2.mp3',
    'text-cantonese-3', 'output/google_text_to_speech/text-cantonese-3.mp3'
)
```

### google_drive_upload processor

Required inputs:

- service_account_key.json
- google_drive_upload.env

Example:

***processor input***

google_text_to_speech.env

| VARIABLE    | DESCRITPION                                       | EXAMPLE                           |
| ----------- | ------------------------------------------------- | --------------------------------- |
| driveId     | The drive id of the folder to be used uploaded to | 11U0ft-85rh6AiEKYX0d29LWI9A425e1o |

***processor output***

assumed the output from the previous processor

```python
dict(
    'text-cantonese-1', 'output/google_text_to_speech/text-cantonese-1.mp3',
    'text-mandarin-2', 'output/google_text_to_speech/text-mandarin-2.mp3',
    'text-cantonese-3', 'output/google_text_to_speech/text-cantonese-3.mp3'
)
```

it will upload the file to google drive to the specific foler, using the key as the filename, and return the share id

```python
dict(
    'text-cantonese-1', '11Udfft-85rh6AiEsfYX0df9LWI9A425e34',
    'text-mandarin-2', '11Udfft-85rh6AiEsfYX0as9LWI9A425e12',
    'text-cantonese-3', '11Udfft-85rh6AfsffYX0d29LWI9A425e1o'
)
```

### google_drive_delete processor

Required inputs:

- service_account_key.json
- google_drive_delete.env
- input.csv

Example:

***processor input***

input.csv

```csv
1db2yIQRJh5GG2R7DkxKzWk3IQl2H0cN7
1wrrapVq35TV1aGR0Ffnq3zqNJgs7wHZw
18wuSwraNWvDmhIfTf8RJ2j9DEk-65ZS_
17P3AnkBhUl2F6pBgpt770sDGYz38rTTN
154WmBGEGaYGUGdnFbyfNGUg3xjQFjZZW
```

google_text_to_speech.env

| VARIABLE    | DESCRITPION                                       | EXAMPLE                           |
| ----------- | ------------------------------------------------- | --------------------------------- |
| driveId     | The drive id of the folder to be used uploaded to | 11U0ft-85rh6AiEKYX0d29LWI9A425e1o |

***processor output***

it will delete the file 1 by 1 from the specific folder

```python
dict(
    '1db2yIQRJh5GG2R7DkxKzWk3IQl2H0cN7', None,
    '1wrrapVq35TV1aGR0Ffnq3zqNJgs7wHZw', None,
    '18wuSwraNWvDmhIfTf8RJ2j9DEk-65ZS_', None,
    '17P3AnkBhUl2F6pBgpt770sDGYz38rTTN', None,
    '154WmBGEGaYGUGdnFbyfNGUg3xjQFjZZW', None
)
```

### replace_text processor

Required inputs:

- input.txt

Example:

***processor input***

input.txt (can be any text context)

```html
<p>Random paragraph <span id="text-cantonese-1" class="extract_text">Text 1 - {{text-1}}</span></p>

<table>
    <thead>
        <tr>
            <th>Random Title</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Random text 1 - <span id="text-mandarin-2" class="extract_text">Text 2 - {{text-2}}</span></td>
        </tr>
        <tr>
            <td>Random text 2- <span id="text-cantonese-3" class="extract_text">Text 3 - {{text-3}}</span></td>
        </tr>
    </tbody>
</table>
```

```csv
id,value
text-1,"Text 1",{{text-cantonese-1}}
text-2,"Text 2",{{text-mandarin-2}}
text-3,"Text 3",{{text-cantonese-3}}
```

***processor output***

assumed the output from the previous processor

```python
dict(
    'text-cantonese-1', '755f5be9-907a-4957-88d4-0c7527e0e104',
    'text-mandarin-2', '5abb79da-ee45-441f-ab44-ab50f3d73abf',
    'text-cantonese-3', '81f01ef3-6862-40c0-a356-5e7b0ba52a2b'
)
```

it will replace the placeholder with the text value

```html
<p>Random paragraph <span id="text-cantonese-1" class="extract_text">Text 1 - 755f5be9-907a-4957-88d4-0c7527e0e104</span></p>

<table>
    <thead>
        <tr>
            <th>Random Title</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Random text 1 - <span id="text-mandarin-2" class="extract_text">Text 2 - 5abb79da-ee45-441f-ab44-ab50f3d73abf</span></td>
        </tr>
        <tr>
            <td>Random text 2- <span id="text-cantonese-3" class="extract_text">Text 3 - 81f01ef3-6862-40c0-a356-5e7b0ba52a2b</span></td>
        </tr>
    </tbody>
</table>
```

```csv
id,value
text-1,"Text 1",755f5be9-907a-4957-88d4-0c7527e0e104
text-2,"Text 2",5abb79da-ee45-441f-ab44-ab50f3d73abf
text-3,"Text 3",81f01ef3-6862-40c0-a356-5e7b0ba52a2b
```

## Use cases

input html -> extract-html -> google-text-to-speech -> google-drive-upload -> replace-text -> output html

input csv -> extract-csv -> google-text-to-speech -> google-drive-upload -> replace-text -> output csv

input csv -> google-drive-delete
