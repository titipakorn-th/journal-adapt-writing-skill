#!/usr/bin/env python3
"""Check that a revised section kept every protected token of the original.

Protected: citations, cross-references, labels, footnotes, math, and numbers.
Usage: python3 check_preserved.py ORIGINAL REVISED   (exit 1 on any difference)
       python3 check_preserved.py --selftest
"""
import re
import sys
from collections import Counter

BRACED_CMD = re.compile(r"\\(cite\w*|citep|citet|ref|eqref|autoref|[cC]ref|label|footnote)\*?(\[[^\]]*\])*\{")
MATH = re.compile(
    r"\$\$.+?\$\$|\$[^$\n]+\$|\\\[.+?\\\]|\\\(.+?\\\)"
    r"|\\begin\{(equation|align|gather|multline|eqnarray|split)\*?\}.+?\\end\{\1\*?\}",
    re.S,
)
MD_CITE = re.compile(r"\[@[^\]]+\]|\[\d+(?:\s*[,\u2013-]\s*\d+)*\]")
NUMBER = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)*%?")


def _braced_end(text, start):
    depth = 1
    i = start
    while i < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0) if text[i - 1] != "\\" else 0
        i += 1
    return i


def protected_tokens(text):
    tokens = Counter()
    spans = []
    for m in BRACED_CMD.finditer(text):
        end = _braced_end(text, m.end())
        spans.append((m.start(), end))
    for pattern in (MATH, MD_CITE):
        spans += [m.span() for m in pattern.finditer(text)]
    spans.sort()
    kept, last_end = [], -1
    for s, e in spans:
        if s >= last_end:
            kept.append((s, e))
            last_end = e
    for s, e in kept:
        tokens[" ".join(text[s:e].split())] += 1
    rest = "".join(" " if any(s <= i < e for s, e in kept) else ch for i, ch in enumerate(text))
    tokens.update(NUMBER.findall(rest))
    return tokens


def diff(original, revised):
    a, b = protected_tokens(original), protected_tokens(revised)
    return a - b, b - a


def _selftest():
    orig = r"We find a 12.5% drop \citep[p.~3]{smith2020} in $\tau_t$ (see \ref{tab:1})\footnote{Data {from} 2019.}."
    missing, added = diff(orig, orig.replace("We find", "We show"))
    assert not missing and not added, "pure rewording passes"
    missing, added = diff(orig, orig.replace("12.5%", "13%"))
    assert missing == Counter({"12.5%": 1}) and added == Counter({"13%": 1}), "changed number caught"
    missing, _ = diff(orig, orig.replace(r"\citep[p.~3]{smith2020}", ""))
    assert missing == Counter({r"\citep[p.~3]{smith2020}": 1}), "dropped citation caught"
    missing, _ = diff(orig, orig.replace("{from}", "{for}"))
    assert len(missing) == 1 and "footnote" in next(iter(missing)), "footnote edit caught"
    missing, _ = diff(orig, orig.replace(r"\tau_t", r"\tau"))
    assert missing == Counter({r"$\tau_t$": 1}), "math edit caught"
    missing, added = diff("Results [@doe2021] show 3 effects.", "Results [@doe2021] show three effects.")
    assert missing == Counter({"3": 1}) and not added, "markdown cite kept, spelled-out number flagged"
    print("selftest ok")


def main(argv):
    if argv[1:] == ["--selftest"]:
        _selftest()
        return 0
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        original = f.read()
    with open(argv[2], encoding="utf-8") as f:
        revised = f.read()
    missing, added = diff(original, revised)
    for label, tokens in (("MISSING", missing), ("ADDED", added)):
        for tok, n in sorted(tokens.items()):
            print(f"{label} x{n}: {tok}")
    if missing or added:
        return 1
    print("OK: all protected tokens preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
