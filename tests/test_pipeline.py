import pytest
from src.video_audio import download_video, extract_audio
from src.model import classify_accent, MODEL_OPTIONS


def test_download_and_extract(tmp_path):
    # This is a placeholder test; replace URL with a stable small test video
    test_url = "https://sample-videos.com/video123/mp4/240/big_buck_bunny_240p_1mb.mp4"
    video_path = download_video(test_url, str(tmp_path))
    wav_path = tmp_path / "audio.wav"
    extract_audio(video_path, str(wav_path))
    assert wav_path.exists()


@pytest.mark.parametrize("model_key", list(MODEL_OPTIONS.keys()))
def test_classify_placeholder(model_key):
    # Placeholder: audio file must be provided for real test
    wav_path = "tests/sample.wav"
    label, confidence = classify_accent(wav_path, model_key)
    assert isinstance(label, str)
    assert isinstance(confidence, float)
