#!/usr/bin/env python3
"""Convert all zh-TW wiki md files from simplified/mixed text to Traditional Chinese (Taiwan).

Pipeline per file:
  1. Split into segments: frontmatter / fenced code / inline code / prose.
     - fenced code & inline code are NEVER touched (code correctness > wording).
  2. Prose + frontmatter values: apply glossary zh-CN->zh-TW term map first,
     then OpenCC s2tw (chars) — s2twp phrases already covered by glossary for
     domain terms; s2twp is still used as base converter for common phrases.
  3. Write back only when changed; print per-file stats.
"""
import re, glob, sys
from opencc import OpenCC

ROOT = '/home/yopitek/Project/yupitek-wiki/i18n/zh-TW/docusaurus-plugin-content-docs/current'
cc = OpenCC('s2twp')

# glossary from docs/99-admin/translation-glossary.md (zh-CN -> zh-TW)
GLOSSARY = {
    '接入点': '存取點',
    '监听模式': '監聽模式',
    '数据包注入': '封包注入',
    '网卡适配器': '無線網卡',
    '驱动程序': '驅動程式',
    '固件升级': '韌體更新',
    '固件更新': '韌體更新',
    '固件': '韌體',
    '故障排查': '疑難排解',
    '兼容性矩阵': '相容性矩陣',
    '快速入门': '快速入門',
    '无线网卡': 'Wi-Fi 無線網卡',
}
GLOSS_KEYS = sorted(GLOSSARY, key=len, reverse=True)

FENCE = re.compile(r'(```.*?```|~~~.*?~~~)', re.S)
INLINE = re.compile(r'(`[^`\n]+`)')
FM = re.compile(r'\A---\n(.*?)\n---\n', re.S)


def apply_glossary(t: str) -> str:
    for k in GLOSS_KEYS:
        t = t.replace(k, GLOSSARY[k])
    return t


def convert_segment(seg: str) -> str:
    out = []
    last = 0
    for m in INLINE.finditer(seg):
        out.append(cc.convert(apply_glossary(seg[last:m.start()])))
        out.append(m.group(0))          # inline code untouched
        last = m.end()
    out.append(cc.convert(apply_glossary(seg[last:])))
    return ''.join(out)


def convert_file(path: str):
    src = open(path, encoding='utf-8').read()
    parts, segs = [], []           # parts: ('text'|'fence', content)
    pos = 0
    for m in FENCE.finditer(src):
        if m.start() > pos:
            parts.append(('text', src[pos:m.start()]))
        parts.append(('fence', m.group(0)))
        pos = m.end()
    if pos < len(src):
        parts.append(('text', src[pos:]))

    changed_chars = 0
    for kind, content in parts:
        if kind == 'fence':
            continue
        new = convert_segment(content)
        if new != content:
            changed_chars += sum(1 for a, b in zip(content, new) if a != b) + abs(len(content) - len(new))
            content = new
        parts[parts.index((kind, content))] if False else None
    # rebuild
    out = []
    idx = 0
    # simpler: rebuild by replacing text parts sequentially
    res = src
    # redo properly (we mutated copies above); do it cleanly:
    pieces = []
    pos = 0
    for m in FENCE.finditer(src):
        pieces.append(convert_segment(src[pos:m.start()]))
        pieces.append(m.group(0))
        pos = m.end()
    pieces.append(convert_segment(src[pos:]))
    res = ''.join(pieces)
    if res != src:
        open(path, 'w', encoding='utf-8').write(res)
    return changed_chars


def main():
    files = sorted(glob.glob(f'{ROOT}/**/*.md', recursive=True))
    total_files, total_delta = 0, 0
    for f in files:
        d = convert_file(f)
        if d:
            total_files += 1
            total_delta += d
            rel = f.split('/current/')[1]
            print(f'{d:5d} {rel}')
    print(f'\nconverted={total_files}/{len(files)} files, approx_char_diff={total_delta}')


if __name__ == '__main__':
    main()
