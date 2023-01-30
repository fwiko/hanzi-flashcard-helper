# Hanzi Flashcard Helper

Help to batch create Chinese (Mandarin) flashcards for Anki.

## Generating Reading Cards

Generate "reading cards" from a list of Hanzi phrases, translating each word into Pinyin (拼音) and English. Used to test recognition of Hanzi characters.

### Command

```
python main.py <input_file> read
```

### Input File

```text
请问，你叫什么名字？
...
```

### Output File

```
请问，你叫什么名字？	qǐng-wèn，nǐ-jiào-shén-me-míng-zì？ Excuse me, what's your name?
...
```

## Generating Cloze (Fill-in-the-Blank) Cards

Generate "cloze cards" from a list of sentences, with braces {} used to indicate the location of clozes. On Anki, the user will be prompted to enter the full text, filling in the blank - this is useful for testing grammar and character knowledge.

### Command

```
python main.py <input_file> cloze
```

### Input FileW

```
他的电话号码多少？
...
```

### Output File

```
他的电话{{c1::号}}{{c1::码}}多少？  他的电话号码多少？	tā-de-diàn-huà-{{c1::hào}}-{{c1::mǎ}}-duō-shǎo？	What's his phone number?
...
```

## Generating Writing Cards

Generate "writing cards" from a list of Hanzi characters, using [strokeorder.info](http://strokeorder.info) to fetch the IDs of GIFs outlining the stroke order of each character. When the card is viewed in Anki, the GIFs are automatically displayed.

### Command

```
python main.py <input_file> write
```

### Input File

```
我
...
```

### Output File

```
wǒ 我 28304
...
```
