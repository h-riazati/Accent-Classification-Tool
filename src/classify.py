import argparse
import tempfile
import os
# Ensure PATH includes vendored ffmpeg
ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

from video_audio import download_video, extract_audio
from model import classify_accent, MODEL_OPTIONS
import os


def main():
    parser = argparse.ArgumentParser(description="Download video, extract audio, classify accent.")
    parser.add_argument('--url', required=True, help='Video URL (MP4 or Loom)')
    parser.add_argument('--out', default='output.wav', help='Path to save extracted WAV')
    parser.add_argument('--model', choices=list(MODEL_OPTIONS.keys()), default='dima806', help='Model to use for classification')
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Downloading video from {args.url} …")
        video_file = download_video(args.url, tmpdir)
        print(f"Extracting audio to {args.out} …")
        extract_audio(video_file, args.out)

    print(f"Classifying accent using model '{args.model}' …")
    label, confidence = classify_accent(args.out, args.model)

    # url = 'https://www.youtube.com/watch?v=PmprA_VTuKk'
    # url = 'https://www.youtube.com/watch?v=WqBZVlgORbY'
    # url = 'https://www.aparat.com/v/mlar388?discovery=1'
    # url = 'https://www.youtube.com/shorts/XcS7ih3bZzo'
    # out = 'out1.wav'
    # model = ['dima806', 'speechbrain', 'Jzuluaga_xlsr'][-1]
    #
    # with tempfile.TemporaryDirectory() as tmpdir:
    #     print(f"Downloading video from {url} …")
    #     video_file = download_video(url, tmpdir)
    #     # # video_file = r'C:\Users\\admin\AppData\Local\Temp\tmp86ta4z_h\WqBZVlgORbY.mp4'
    #     # print(f"Extracting audio to {out} …")
    #     print("Downloaded video_file path:", video_file)
    #     print("File exists?", os.path.isfile(video_file))
    #     print("Contents of tmpdir:", os.listdir(tmpdir))
    #     print(f"Extracting audio to {out} …")
    #     extract_audio(video_file, out)

    # print(f"Classifying accent using model '{model}' …")
    # label, confidence = classify_accent(out, model)
    #
    print({
        'accent': label,
        'confidence': round(confidence, 2)
    })


if __name__ == '__main__':
    main()