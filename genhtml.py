#!/usr/bin/env python3

from jinja2 import FileSystemLoader, Environment

import os
import glob

def gen_oneshot_rows():
    ret = []

    melgan = sorted(glob.glob('data/melgan/*.wav'))
    pps = 'data/proposed'
    ada = 'data/adain'
    vq = 'data/vqvc'
    au = 'data/autovc'

    for src in melgan:
        src_basename = os.path.basename(src).split('.')[0]
        for tgt in melgan:
            if src == tgt:
                continue
            tgt_basename = os.path.basename(tgt).split('.')[0]
            row = (
                src_basename,
                tgt_basename,
                src, 
                tgt,
                os.path.join(pps, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(ada, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(vq, f'{src_basename}_to_{tgt_basename}.wav'),
                os.path.join(au, f'{src_basename}_to_{tgt_basename}.wav'),
            )
            ret.append(row)
    return ret

def gen_forfun_rows():
    ret = []

    srcs = sorted(glob.glob('data/forfun/source/*.wav'))
    tgts = sorted(glob.glob('data/forfun/target/*.wav'))
    pps = 'data/forfun/converted'

    for src in srcs:
        src_basename = os.path.basename(src).split('.')[0]
        for tgt in tgts:
            tgt_basename = os.path.basename(tgt).split('.')[0]
            row = (
                src_basename,
                tgt_basename,
                src, 
                tgt,
                os.path.join(pps, f'{src_basename}_to_{tgt_basename}.wav'),
            )
            ret.append(row)
    return ret

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("base.html.jinja2")

    oneshot_rows = gen_oneshot_rows()
    forfun_rows = gen_forfun_rows()

    html = template.render(
        oneshot_rows=oneshot_rows,
        forfun_rows=forfun_rows
    )
    print(html)

if __name__ == "__main__":
    main()
