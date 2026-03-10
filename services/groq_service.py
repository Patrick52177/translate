import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

SUPPORTED_LANGUAGES = {
    'mg': 'Malagasy',
    'fr': 'French',
    'en': 'English',
    'es': 'Spanish',
    'ar': 'Arabic',
    'zh': 'Chinese (Mandarin)',
    'de': 'German',
    'pt': 'Portuguese',
}

def detect_language(text: str) -> str:
    """Détecte automatiquement la langue d'un texte"""
    codes = ', '.join(SUPPORTED_LANGUAGES.keys())
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"""You are a language detector.
Detect the language of the given text and respond with ONLY one of these codes: {codes}
Respond with ONLY the code, nothing else."""
            },
            {"role": "user", "content": text}
        ],
        max_tokens=5,
        temperature=0.1
    )
    detected = response.choices[0].message.content.strip().lower()
    if detected not in SUPPORTED_LANGUAGES:
        return 'fr'
    return detected

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Traduit un texte d'une langue vers une autre"""
    source_name = SUPPORTED_LANGUAGES.get(source_lang, source_lang)
    target_name = SUPPORTED_LANGUAGES.get(target_lang, target_lang)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"""You are an expert translator specializing in multiple languages including Malagasy.
Translate the following text from {source_name} to {target_name}.
Rules:
- Provide ONLY the translation, no explanations
- Keep the same tone and style
- Preserve formatting and punctuation
- For Malagasy, use standard Merina dialect
- For Arabic, use Modern Standard Arabic
- For Chinese, use Simplified Chinese"""
            },
            {"role": "user", "content": text}
        ],
        max_tokens=1000,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()