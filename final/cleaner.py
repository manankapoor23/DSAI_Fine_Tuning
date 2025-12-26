import json
import re

# Boilerplate / junk phrases to remove
JUNK_PHRASES = [
    "Image copyright",
    "SANJAY SHARMA",
    "ਫੋਟੋ ਕੈਪਸ਼ਨ",
    "Getty Images",
    "ਈਮੇਲ ਸਾਂਝਾ ਕਰੋ",
    "ਸਾਂਝਾ ਕਰੋ",
    "ਸਾਂਝਾ ਕਰਨ ਬਾਰੇ ਹੋਰ ਪੜ੍ਹੋ",
    "ਸਾਂਝਾ ਕਰਨ ਵਾਲੇ ਪੈਨਲ ਨੂੰ ਬੰਦ ਕਰੋ",
    "ਲਿੰਕ ਨੂੰ ਕਾਪੀ ਕਰੋ",
    "ਹੋਰ ਪੜ੍ਹੋ",
    "ਇਹ ਵੀ ਪੜ੍ਹੋ",
    "ਬੀਬੀਸੀ",
    "ਪੱਤਰਕਾਰ"
]


def clean_text(text):
    # Remove junk phrases
    for phrase in JUNK_PHRASES:
        text = text.replace(phrase, "")

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def format_for_llama(text):
    return (
        "<s>[INST] ਹੇਠਾਂ ਦਿੱਤੇ ਪੈਰਾ ਨੂੰ ਸਧਾਰਣ ਅਤੇ ਸਾਫ਼ ਪੰਜਾਬੀ ਵਿੱਚ ਦੁਬਾਰਾ ਲਿਖੋ। "
        "[/INST] " + text + "</s>"
    )

input_file = "/Users/manankapoor/finetune_llm/DSAI_Fine_Tuning/final/punjabi_llama2.jsonl"
output_file = "train_safe.jsonl"

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in fin:
        obj = json.loads(line)
        raw_text = obj.get("text", "").strip()

        if not raw_text:
            continue

        cleaned = clean_text(raw_text)

        # Skip very short or broken lines
        if len(cleaned) < 80:
            continue

        formatted = format_for_llama(cleaned)

        fout.write(
            json.dumps({"text": formatted}, ensure_ascii=False) + "\n"
        )

print("✅ Cleaning & formatting completed. Output saved to train_safe.jsonl")
