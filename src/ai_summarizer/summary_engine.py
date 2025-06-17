import re
from typing import List, Dict
from transformers import pipeline

class SummaryEngine:
    def __init__(self):
        # Load multilingual summarization model
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )
        
        # Myanmar-specific rules
        self.myanmar_filters = [
            (r'[\u1000-\u109F]+', 'MYANMAR_TEXT')
        ]

    def detect_language(self, text: str) -> str:
        """Detect if text contains Myanmar characters"""
        for pattern, _ in self.myanmar_filters:
            if re.search(pattern, text):
                return "my"
        return "en"

    def summarize(self, text: str, ratio: float = 0.3) -> Dict:
        """Core summarization function"""
        lang = self.detect_language(text)
        
        if lang == "my":
            return self._summarize_myanmar(text, ratio)
        else:
            return self._summarize_english(text, ratio)

    def _summarize_english(self, text: str, ratio: float) -> Dict:
        """Summarize English/international text"""
        max_length = int(len(text.split()) * ratio)
        result = self.summarizer(text, max_length=max_length)
        return {
            "language": "en",
            "summary": result[0]['summary_text'],
            "original_length": len(text),
            "summary_length": len(result[0]['summary_text'])
        }

    def _summarize_myanmar(self, text: str, ratio: float) -> Dict:
        """Custom Myanmar text summarization"""
        # Implement your Myanmar-specific logic here
        sentences = self._split_myanmar_sentences(text)
        summary = " ".join(sentences[:3])  # Simple first-3-sentences approach
        
        return {
            "language": "my",
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "notes": "Basic Myanmar summarization"
        }

    def _split_myanmar_sentences(self, text: str) -> List[str]:
        """Basic Myanmar sentence splitter"""
        return [s.strip() for s in re.split(r'[။၏\?\!]', text) if s.strip()]
