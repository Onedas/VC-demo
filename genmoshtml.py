#!/usr/bin/env python3
import random
from jinja2 import FileSystemLoader, Environment
import os
import glob
import yaml
import soundfile as sf


def gen_naturalness_rows():
    ret = []
    logs = {}

    sources = sorted(glob.glob('data/source/*.wav'))
    proposed = 'data/proposed'
    aga = 'data/again'
    ada = 'data/adain'
    vq = 'data/vqvc'
    au = 'data/autovc'

    with open('metas/MOSLink/Naturalness/google_forms.yaml') as f:
        surveys = yaml.load(f, Loader=yaml.SafeLoader)

    idx = 0
    for src in sources:
        src_basename = os.path.basename(src).split('.')[0]
        for tgt in sources:
            if src == tgt:
                continue
            tgt_basename = os.path.basename(tgt).split('.')[0]
            idx += 1
            audios = [src,
                      os.path.join(proposed, f'{src_basename}_to_{tgt_basename}.wav'),
                      os.path.join(aga, f'{src_basename}_to_{tgt_basename}.wav'),
                      os.path.join(ada, f'{src_basename}_to_{tgt_basename}.wav'),
                      os.path.join(vq, f'{src_basename}_to_{tgt_basename}.wav'),
                      os.path.join(au, f'{src_basename}_to_{tgt_basename}.wav')
                      ]
            random.shuffle(audios)

            row = [idx,
                   *audios,
                   surveys.get(idx, None)]

            ret.append(row)
            logs[idx] = audios

    with open('metas/MOSLink/Naturalness/audio_logs.yaml', 'w+') as f:
        yaml.dump(logs, f, allow_unicode=True)
    return ret


def gen_similarity_rows():
    ret = []
    logs = {}

    sources = sorted(glob.glob('data/source/*.wav'))

    proposed = 'data/proposed'
    aga = 'data/again'
    ada = 'data/adain'
    vq = 'data/vqvc'
    au = 'data/autovc'

    with open('metas/MOSLink/Similarity/google_forms.yaml') as f:
        surveys = yaml.load(f, Loader=yaml.SafeLoader)

    idx = 0
    for src in sources:
        src_basename = os.path.basename(src).split('.')[0]
        for tgt in sources:
            if src == tgt:
                continue
            tgt_basename = os.path.basename(tgt).split('.')[0]
            idx += 1
            audios = [os.path.join(proposed, f'{src_basename}_to_{tgt_basename}.wav'),
                      os.path.join(aga, f'{src_basename}_to_{tgt_basename}.wav'),
                      os.path.join(ada, f'{src_basename}_to_{tgt_basename}.wav'),
                      os.path.join(vq, f'{src_basename}_to_{tgt_basename}.wav'),
                      os.path.join(au, f'{src_basename}_to_{tgt_basename}.wav')]
            random.shuffle(audios)

            row = [idx,
                   tgt,
                   *audios,
                   surveys.get(idx, None)]

            ret.append(row)
            logs[idx] = audios

    with open('metas/MOSLink/Similarity/audio_logs.yaml', 'w+') as f:
        yaml.dump(logs, f, allow_unicode=True)
    return ret


def rescaling_audios():
    sources = sorted(glob.glob('data/source/*.wav'))
    proposed = 'data/proposed'
    aga = 'data/again'
    ada = 'data/adain'
    vq = 'data/vqvc'
    au = 'data/autovc'

    idx = 0
    for src in sources:
        src_basename = os.path.basename(src).split('.')[0]
        for tgt in sources:
            if src == tgt:
                continue
            tgt_basename = os.path.basename(tgt).split('.')[0]
            idx += 1
            audios = [
                # src,
                os.path.join(proposed, f'{src_basename}_to_{tgt_basename}.wav'),
                # os.path.join(aga, f'{src_basename}_to_{tgt_basename}.wav'),
                # os.path.join(ada, f'{src_basename}_to_{tgt_basename}.wav'),
                # os.path.join(vq, f'{src_basename}_to_{tgt_basename}.wav'),
                # os.path.join(au, f'{src_basename}_to_{tgt_basename}.wav')
                      ]
            for audio in audios:
                wav, sr = sf.read(audio)
                rescale_wav = wav * 1/max([wav.max(), -wav.min()])
                sf.write(audio, rescale_wav, sr)

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    # rescaling_audios()
    naturalness_rows = gen_naturalness_rows()
    similarity_rows = gen_similarity_rows()

    html = template.render(
        naturalness_rows=naturalness_rows,
        similarity_rows=similarity_rows,
    )
    print(html)


if __name__ == "__main__":
    main()
