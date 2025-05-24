import os
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from transformers import AutoFeatureExtractor, AutoModelForAudioClassification, pipeline
from speechbrain.inference import EncoderClassifier
from speechbrain.inference.interfaces import foreign_class


# Available models:
MODEL_OPTIONS = {
    'dima806': 'dima806/speech-accent-classification',
    'speechbrain': 'Jzuluaga/accent-id-commonaccent_ecapa',
    'xlsr': "warisqr7/accent-id-commonaccent_xlsr-en-english"
    # 'Jzuluaga_xlsr': "Jzuluaga/accent-id-commonaccent_xlsr-en-english"
}


def load_accent_classifier(model_key: str = 'dima806'):
    if model_key not in MODEL_OPTIONS:
        raise ValueError(f"Unsupported model key {model_key}. Choose from {list(MODEL_OPTIONS.keys())}")

    model_name = MODEL_OPTIONS[model_key]

    if model_key == 'dima806':
        extractor = AutoFeatureExtractor.from_pretrained(model_name)
        model = AutoModelForAudioClassification.from_pretrained(model_name)
        return pipeline(task="audio-classification",
                        model=model,
                        feature_extractor=extractor,
                        return_all_scores=False
                        )
    elif model_key == 'speechbrain':
        return EncoderClassifier.from_hparams(source=model_name,
                                              savedir="pretrained_models/accent-id-commonaccent_ecapa"
                                              )
    elif model_key == 'xlsr':
        return foreign_class(source=model_name,
                             pymodule_file="custom_interface.py",
                             classname="CustomEncoderWav2vec2Classifier"
                             )
    elif model_key == 'Jzuluaga_xlsr':
        return foreign_class(source=model_name,
                             pymodule_file="custom_interface.py",
                             classname="CustomEncoderWav2vec2Classifier"
                             )
    else:
        pass


def classify_accent(wav_path: str, model_key: str = 'dima806', classifier=None) -> tuple[str, float]:

    if classifier is None:
        classifier = load_accent_classifier(model_key)

    try:
        if model_key == 'dima806':
            result = classifier(wav_path)[0]
            label = result['label']
            confidence = result['score'] * 100
        else:
            result = classifier.classify_file(wav_path)
            label = result[3][0]
            confidence = result[1][0] * 100
    except Exception as e:
        # Fallback or log error
        label, confidence = 'error', 0.0
        print(f"Warning: classification failed: {e}")
    return label, confidence
