import os

DFLT_GRAZE_ROOTDIR = os.path.expanduser('~/graze')


def convert_all_mp3s_to_wav(rootdir=DFLT_GRAZE_ROOTDIR, verbose=True):
    from py2store import filt_iter, dig
    from graze import Graze
    import re
    import os
    import subprocess

    GrazedMp3s = filt_iter(Graze, filt=lambda x: 'podbean' in x and x.endswith('.mp3'))
    mp3s = GrazedMp3s(rootdir)
    list(mp3s)

    mp3_p = re.compile('.mp3$')
    for k in mp3s:
        mp3_filepath = dig.inner_most_key(mp3s, k)
        wav_filepath = mp3_p.sub('.wav', mp3_filepath)
        if not os.path.isfile(wav_filepath):
            if verbose:
                print(mp3_filepath)
            output = subprocess.run(f'sox {mp3_filepath} {wav_filepath}'.split(' '))
            if verbose:
                print(output)
                print("")


if __name__ == '__main__':
    import argh

    argh.dispatch_commands(([convert_all_mp3s_to_wav]))
