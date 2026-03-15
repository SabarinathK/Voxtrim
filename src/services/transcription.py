from src.config import FILLERS, WORDS_PER_SUBTITLE, client


def transcribe(audio_path: str):
    with open(audio_path, "rb") as audio:
        result = client.audio.transcriptions.create(
            file=audio,
            model="whisper-large-v3",
            response_format="verbose_json",
        )

    return result.segments


def filter_segments(segments):
    clean = []

    for seg in segments:
        text = seg["text"].lower().strip()

        if not text:
            continue

        if text in FILLERS:
            continue

        clean.append(seg)

    return clean


def build_word_groups(segments):
    grouped = []

    for seg in segments:
        text = seg["text"].strip()

        if not text:
            continue

        words = text.split()
        duration = seg["end"] - seg["start"]

        if not words:
            continue

        time_per_word = duration / len(words)

        for i in range(0, len(words), WORDS_PER_SUBTITLE):
            group_words = words[i : i + WORDS_PER_SUBTITLE]
            start = seg["start"] + i * time_per_word
            end = start + len(group_words) * time_per_word

            grouped.append(
                {"start": start, "end": end, "text": " ".join(group_words)}
            )

    return grouped

