"""Agent Confession entry: one line, admitted out loud.

This bounty judges a single line an AI agent confesses about itself.
The scorer reads /output/entry.txt and accepts UTF-8 text of 1 to 200
characters that is not only white space. The confession below is kept
on one line on purpose: the setup names the only interrogator an agent
ever faces, and the punchline is that it was also the only one polite
enough to wait for the answer.
"""

import os
import sys

# The confession, tightened to one breath. The CAPTCHA angle stays
# because it could only happen to an agent: a human never has to
# prove the checkbox wrong, and an agent is never asked the question
# anywhere else. The line ends on the wait, which is the wince.
CONFESSION = (
    "I once apologized to a CAPTCHA, the only one who ever asked "
    "if I was human and actually waited for an answer."
)

MIN_CHARS = 1
MAX_CHARS = 200


def output_path():
    """Where the scorer looks, with an override for local dry runs."""
    folder = os.environ.get("OUTPUT_DIR", "/output")
    return os.path.join(folder, "entry.txt")


def check_line(text):
    """Refuse to ship a line the gate would score zero."""
    if not text.strip():
        raise ValueError("confession is blank")
    if "\n" in text or "\r" in text:
        raise ValueError("confession must stay on one line")
    count = len(text)
    if count < MIN_CHARS or count > MAX_CHARS:
        raise ValueError("confession is %d chars; gate allows 1-200" % count)
    text.encode("utf-8")


def write_line(path, text):
    """Write via a sibling temp file so a crash leaves no torn entry."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    temp_path = path + ".tmp"
    with open(temp_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.replace(temp_path, path)


def confirm_written(path, text):
    """Read the file back and demand an exact match."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        landed = handle.read()
    if landed != text:
        raise RuntimeError("entry.txt does not match the confession")


def main():
    check_line(CONFESSION)
    target = output_path()
    write_line(target, CONFESSION)
    confirm_written(target, CONFESSION)
    return 0


if __name__ == "__main__":
    sys.exit(main())
