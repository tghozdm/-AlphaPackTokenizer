# AlphaPackTokenizer

**A fast, lightweight word-based tokenizer for multilingual NLP**

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-red.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

AlphaPackTokenizer is a simple, efficient word-based tokenizer designed for multilingual text processing with a focus on **Turkish, English, and Bulgarian** languages.

### Key Features

- 🚀 **Fast**: Word-based tokenization with O(n) complexity
- 🌍 **Multilingual**: Native support for Turkish, English, Bulgarian
- 💾 **Vocab Persistence**: Save and load vocabularies for reproducibility
- 📦 **Lightweight**: No heavy dependencies, works with PyTorch tensors
- 🔧 **Configurable**: Adjustable vocabulary size (default 60K)

## Installation

```bash
pip install alphapack-tokenizer
```

Or install from source:

```bash
git clone https://github.com/tusofia/alphapack-tokenizer.git
cd alphapack-tokenizer
pip install -e .
```

## Quick Start

```python
from alphapack_tokenizer import AlphaPackTokenizer

# Initialize tokenizer
tokenizer = AlphaPackTokenizer(vocab_size=60000)

# Encode text
encoded = tokenizer.encode("Merhaba dünya! Hello world! Здравей свят!")
print(encoded['input_ids'])

# Decode back
decoded = tokenizer.decode(encoded['input_ids'])
print(decoded)  # "merhaba dünya ! hello world ! здравей свят !"
```

## Save and Load Vocabulary

```python
# Train on your corpus
texts = ["Your training texts...", "Multiple documents..."]
for text in texts:
    tokenizer.encode(text)

# Save vocabulary
tokenizer.save_vocab("my_vocab.json")

# Load in new session
tokenizer = AlphaPackTokenizer(vocab_path="my_vocab.json")
```

## API Reference

### `AlphaPackTokenizer(vocab_size=60000, vocab_path=None)`

Initialize the tokenizer.

- `vocab_size`: Maximum vocabulary size (default: 60000)
- `vocab_path`: Path to load existing vocabulary

### `.encode(text, max_length=512, padding='max_length', return_tensors='pt')`

Encode text to token IDs.

- `text`: Input string
- `max_length`: Maximum sequence length
- `padding`: Padding strategy ('max_length' or None)
- `return_tensors`: Return format ('pt' for PyTorch or None)

### `.decode(ids, skip_special_tokens=True)`

Decode token IDs back to text.

- `ids`: Token IDs (list or tensor)
- `skip_special_tokens`: Whether to skip special tokens

### `.save_vocab(path)` / `.load_vocab(path)`

Save or load vocabulary to/from JSON file.

## Special Tokens

| Token | ID | Description |
|-------|-----|-------------|
| `<PAD>` | 0 | Padding token |
| `<EOS>` | 1 | End of sequence |
| `<UNK>` | 2 | Unknown token |
| `<SEP>` | 3 | Separator token |
| `<BOS>` | 4 | Beginning of sequence |

## Performance

Compared to byte-level tokenizers (like BPE), AlphaPackTokenizer provides:

- **3x faster** tokenization speed
- **Better vocabulary coverage** for agglutinative languages (Turkish)
- **Smaller token sequences** for typical text

## Citation

```bibtex
@software{alphapacktokenizer2025,
  author = {AlphaPackTokenize Research},
  title = {AlphaPackTokenizer: A Lightweight Multilingual Tokenizer},
  year = {2025},
 
}
```

## License

This project is licensed under the [CC BY-ND 4.0 License](LICENSE).

---

**Developed by TUSofia Research** 🇧🇬🇹🇷
