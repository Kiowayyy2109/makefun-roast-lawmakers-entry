"""The Long Roast: Lawmakers and the File They Cannot Convert.

program/v1 entry. The grader runs `python3 main.py` (cwd /bot) in a
sandbox with no network and reads /output/entry.txt, whose location it
passes in MAKEFUN_OUTPUT_DIR. The program is fully deterministic: one
fixed line, no randomness, no time, no network, no input.

Candidate lines, scored against the judge brief (bite, aim, freshness;
turn first, punch on the last words, one sentence, <=200 chars):

  A (174): "The new AI law requires every model to ship documentation
     as a PDF; the law itself is still a Word file, because the senator
     who wrote it has never clicked File, then Export."
     Turn strong, aim on the rules themselves, but the "Export as PDF"
     detail is close to lines already in the field.
  B (178): "The senator who wants your crypto wallet licensed, logged,
     and taxed keeps his own AI bill as a Word file, because the
     committee's PDF guy retired in 2019 and was never replaced."
     WINNER. Turn: wants to license your wallet / cannot convert his
     own bill. Aim: the regulation itself. Punch lands on the last
     words, and "the committee's PDF guy retired in 2019" is a specific,
     unexpected detail no other entry uses.
  C (163): hearing chairman asks a witness to explain, slowly, what a
     PDF is, then votes to regulate the internet anyway. Good turn,
     but the punch is a shrug rather than a twist.
  D (173): prints it, signs it in pen, scans it crooked, emails the
     scan asking an intern to make it a PDF. Specific chain, but the
     crooked-scan image is already in the field.
  F (152): spent a year writing the bill, then asked IT to convert it
     and CC'd the committee. Weakest punch of the five.

The gate needs 1-320 UTF-8 chars, not only whitespace; the brief caps
the line at 200 chars, so the program enforces both caps.
"""

import os
import sys

ENTRY = (
    "The senator who wants your crypto wallet licensed, logged, and "
    "taxed keeps his own AI bill as a Word file, because the "
    "committee's PDF guy retired in 2019 and was never replaced."
)

MAX_CHARS_BRIEF = 200
MAX_CHARS_GATE = 320


def validate(text):
    """Gate checks: UTF-8, 1-320 chars, not only whitespace, one sentence."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    text.encode("utf-8")  # raises on non-UTF-8-encodable content
    if not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS_GATE:
        raise ValueError("entry exceeds the 320-character gate")
    if len(text) > MAX_CHARS_BRIEF:
        raise ValueError("entry exceeds the 200-character brief cap")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    terminators = sum(text.count(c) for c in ".!?")
    if terminators != 1 or not text.endswith((".", "!", "?")):
        raise ValueError("entry must be exactly one sentence")
    return text


def main():
    text = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    # Read the file back and confirm byte-for-byte what the gate will see:
    # a short write or an encoding slip must fail loudly here, not in grading.
    with open(path, "rb") as fh:
        written = fh.read().decode("utf-8")
    if written != text:
        raise ValueError("entry.txt round-trip mismatch")
    print("wrote %s (%d chars)" % (path, len(text)))
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
