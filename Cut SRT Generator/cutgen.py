import re
from pathlib import Path

# ---------------- CONFIG ----------------
OUTPUT_FILE = Path.home() / "Desktop" / "cuts.srt"

INCLUDE_INITIAL_CUT = True   # creates 00:00:00,000 --> 00:00:01,000
INITIAL_CUT_DURATION = 1.0  # seconds
FPS = 29.97  # for frame-accurate timing
# ---------------------------------------


def parse_time(t):
    """
    Parses time strings like:
    :24      -> 00:00:24.000
    1:04     -> 00:01:04.000
    10:12    -> 00:10:12.000
    """
    if t.startswith(":"):
        minutes = 0
        seconds = int(t[1:])
    else:
        minutes, seconds = map(int, t.split(":"))

    return minutes * 60 + seconds


def seconds_to_srt_time(seconds):
    # Snap to nearest frame for 29.97 fps accuracy
    frame = round(seconds * FPS)
    seconds = frame / FPS
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def extract_ranges(text):

    pattern = r"([0-9:]+)\s*to\s*([0-9:]+)"
    matches = re.findall(pattern, text)
    return [(parse_time(start), parse_time(end)) for start, end in matches]


def write_srt(ranges, output_path):
    index = 1
    lines = []

    if INCLUDE_INITIAL_CUT:
        lines.extend([
            str(index),
            f"{seconds_to_srt_time(0)} --> {seconds_to_srt_time(INITIAL_CUT_DURATION)}",
            "CUT",
            ""
        ])
        index += 1

    for start, end in ranges:
        lines.extend([
            str(index),
            f"{seconds_to_srt_time(start)} --> {seconds_to_srt_time(end)}",
            "CUT",
            ""
        ])
        index += 1

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    print("Enter cut instructions:")

    user_input = input("> ").strip()

    ranges = extract_ranges(user_input)

    if not ranges:
        print("No valid cut ranges found. Exiting.")
        return

    write_srt(ranges, OUTPUT_FILE)
    print(f"\nSRT file successfully created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
