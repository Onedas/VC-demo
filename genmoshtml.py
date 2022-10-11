#!/usr/bin/env python3

from jinja2 import FileSystemLoader, Environment

import os
import glob
import yaml


def gen_naturalness_rows():
    ret = []

    sources = sorted(glob.glob('data/source/*.wav'))
    proposed = 'data/proposed'
    aga = 'data/again'
    ada = 'data/adain'
    vq = 'data/vqvc'
    au = 'data/autovc'

    with open('MOSLink/Naturalness/google_forms.yaml') as f:
        surveys = yaml.load(f, Loader=yaml.SafeLoader)

    idx = 0
    for src in sources:
        src_basename = os.path.basename(src).split('.')[0]
        for tgt in sources:
            if src == tgt:
                continue
            tgt_basename = os.path.basename(tgt).split('.')[0]
            idx += 1
            row = (
                idx,
                src,
                os.path.join(proposed, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(aga, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(ada, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(vq, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(au, f'{src_basename}_to_{tgt_basename}.wav'),
                surveys.get(idx, None)
            )
            ret.append(row)
    return ret


def gen_similarity_rows():
    ret = []

    sources = sorted(glob.glob('data/source/*.wav'))

    proposed = 'data/proposed'
    aga = 'data/again'
    ada = 'data/adain'
    vq = 'data/vqvc'
    au = 'data/autovc'

    with open('MOSLink/Similarity/google_forms.yaml') as f:
        surveys = yaml.load(f, Loader=yaml.SafeLoader)

    idx = 0
    for src in sources:
        src_basename = os.path.basename(src).split('.')[0]
        for tgt in sources:
            if src == tgt:
                continue
            tgt_basename = os.path.basename(tgt).split('.')[0]
            idx += 1
            row = (
                idx,
                tgt,
                os.path.join(proposed, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(aga, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(ada, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(vq, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(au, f'{src_basename}_to_{tgt_basename}.wav'),
                surveys.get(idx, None)
            )
            ret.append(row)
    return ret


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    naturalness_rows = gen_naturalness_rows()
    similarity_rows = gen_similarity_rows()

    html = template.render(
        naturalness_rows=naturalness_rows,
        similarity_rows=similarity_rows,
    )
    print(html)


if __name__ == "__main__":
    main()
