# screening_ai/transcript_cleaner.py - Ingests list arrays of audio responses.

from screening_ai.stt_processor import clean_transcript

def process_audio_answers(audio_inputs):
    results = []
    for idx, audio in enumerate(audio_inputs):
        cleaned = clean_transcript(audio)
        results.append({
            "question_id": f"Q{idx+1}",
            "clean_text": cleaned["clean_text"],
            "confidence": cleaned["confidence"],
            "status": cleaned["status"]
        })
    return results
