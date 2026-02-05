# -*- coding: utf-8 -*-
"""
AlphaPackTokenizer
==================
A fast, lightweight word-based tokenizer for multilingual NLP.
Supports Turkish, English, Bulgarian and other languages.

Copyright (c) 2025 TUSofia Research
Licensed under CC BY-ND 4.0
"""

import os
import json

__version__ = "1.0.0"
__author__ = "TUSofia Research"


class AlphaPackTokenizer:
    """
    Word-based tokenizer with vocab save/load support
    - Vocab size: configurable (default 60K)
    - Supports: Turkish, English, Bulgarian + numbers + punctuation
    - Can save/load vocab for reproducibility
    """
    
    def __init__(self, vocab_size=60000, vocab_path=None):
        """
        Initialize the tokenizer.
        
        Args:
            vocab_size: Maximum vocabulary size (default: 60000)
            vocab_path: Path to load existing vocabulary
        """
        self.vocab_size = vocab_size
        self.special_tokens = {"<PAD>": 0, "<EOS>": 1, "<UNK>": 2, "<SEP>": 3, "<BOS>": 4}
        self.word_to_id = dict(self.special_tokens)
        self.id_to_word = {v: k for k, v in self.special_tokens.items()}
        self.pad_token_id = 0
        self.eos_token_id = 1
        self.unk_token_id = 2
        self.sep_token_id = 3
        self.bos_token_id = 4
        self.next_id = len(self.special_tokens)
        self.noktalar = '.,!?;:@#$%&*+-=/()[]{}"\\'`~<>|\\^'
        
        # Load vocab if path provided
        if vocab_path and os.path.exists(vocab_path):
            self.load_vocab(vocab_path)
        else:
            print(f"[AlphaPackTokenizer] Vocab: {vocab_size}, Special: {len(self.special_tokens)}", flush=True)
    
    def _tokenize(self, text):
        """Split text into words"""
        text = text.lower().strip()
        tokens, current = [], ''
        for c in text:
            if c == ' ':
                if current: tokens.append(current)
                current = ''
            elif c in self.noktalar:
                if current: tokens.append(current)
                tokens.append(c)
                current = ''
            else:
                current += c
        if current: tokens.append(current)
        return tokens
    
    def _word_to_id(self, word):
        """Convert word to ID - sequential assignment with hash fallback"""
        if word in self.word_to_id:
            return self.word_to_id[word]
        
        # Assign new ID
        if self.next_id < self.vocab_size:
            token_id = self.next_id
            self.next_id += 1
        else:
            # Fallback to hash if vocab full
            token_id = hash(word) % (self.vocab_size - len(self.special_tokens)) + len(self.special_tokens)
        
        self.word_to_id[word] = token_id
        self.id_to_word[token_id] = word
        return token_id
    
    def encode(self, text, max_length=512, padding='max_length', return_tensors=None):
        """
        Convert text to token IDs.
        
        Args:
            text: Input string
            max_length: Maximum sequence length
            padding: Padding strategy ('max_length' or None)
            return_tensors: Return format ('pt' for PyTorch or None for list)
            
        Returns:
            Dictionary with 'input_ids' key
        """
        words = self._tokenize(text)
        ids = [self._word_to_id(w) for w in words]
        ids.append(self.eos_token_id)
        
        if len(ids) > max_length:
            ids = ids[:max_length]
        elif padding == 'max_length':
            ids += [self.pad_token_id] * (max_length - len(ids))
        
        if return_tensors == 'pt':
            try:
                import torch
                return {'input_ids': torch.tensor([ids])}
            except ImportError:
                raise ImportError("PyTorch is required for return_tensors='pt'")
        
        return {'input_ids': ids}
    
    def decode(self, ids, skip_special_tokens=True):
        """
        Convert IDs to text.
        
        Args:
            ids: Token IDs (list or tensor)
            skip_special_tokens: Whether to skip special tokens
            
        Returns:
            Decoded text string
        """
        # Handle tensor input
        try:
            import torch
            if isinstance(ids, torch.Tensor):
                ids = ids.tolist()
        except ImportError:
            pass
        
        # Handle nested lists
        if isinstance(ids, list) and len(ids) > 0 and isinstance(ids[0], list):
            ids = ids[0]
        
        words = []
        for tid in ids:
            if tid == self.eos_token_id:
                break
            if skip_special_tokens and tid in [0, 2, 3, 4]:
                continue
            word = self.id_to_word.get(tid, f"[{tid}]")
            words.append(word)
        
        return ' '.join(words)
    
    def save_vocab(self, path):
        """Save vocab to JSON file"""
        data = {
            'word_to_id': self.word_to_id,
            'id_to_word': {str(k): v for k, v in self.id_to_word.items()},
            'vocab_size': self.vocab_size,
            'next_id': self.next_id
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[AlphaPackTokenizer] Vocab saved: {path} ({len(self.word_to_id)} words)", flush=True)
    
    def load_vocab(self, path):
        """Load vocab from JSON file"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.word_to_id = data['word_to_id']
        self.id_to_word = {int(k): v for k, v in data['id_to_word'].items()}
        self.vocab_size = data.get('vocab_size', len(self.word_to_id))
        self.next_id = data.get('next_id', len(self.word_to_id))
        print(f"[AlphaPackTokenizer] Vocab loaded: {path} ({len(self.word_to_id)} words)", flush=True)
    
    def __call__(self, text, **kwargs):
        """Callable interface for encoding"""
        return self.encode(text, **kwargs)
    
    def __len__(self):
        """Return current vocabulary size"""
        return len(self.word_to_id)
    
    def get_vocab(self):
        """Return vocabulary dictionary"""
        return self.word_to_id.copy()
