from sys import stderr
from typing import List

import argparse
from pathlib import Path

from miditoolkit.midi.parser import MidiFile as BaseMidiFile
from miditoolkit.midi.containers import TimeSignature

class MidiFile(BaseMidiFile):
    def __init__(self, filename: Path, *args, **kwargs):
        super().__init__(filename=filename, *args, **kwargs)
        self.name = filename.stem


def read_midis(midi_folder: Path) -> List[MidiFile]:
    filenames = []
    for ext in ('*.mid', '*.midi'):
        filenames.extend(midi_folder.glob(ext))

    return filenames

def is_supported_ts(ts: TimeSignature) -> bool:
    if f'{ts.numerator}/{ts.denominator}' in ('4/4', '3/4', '2/4', '6/8'):
        return True
    return False

def main(midi_folder: Path, save_folder: Path) -> int:
    try:
        midis = read_midis(midi_folder)
        print(f'Found {len(midis)} MIDI files.')
        for i, filename in enumerate(midis):
            print(f'Process file {i}/{len(midis)}', end='\r', flush=True)
            midi = MidiFile(filename)
            for idx, time_signature in enumerate(midi.time_signature_changes):
                if is_supported_ts(time_signature):
                    start = time_signature.time
                    if len(midi.time_signature_changes) > idx + 1:
                        end = midi.time_signature_changes[idx + 1].time - 1
                    else:
                        end = midi.max_tick
                    if end <= start:
                        continue

                    midi.dump(save_folder / f'{midi.name}_{idx}.mid', segment=(start, end))

    except KeyboardInterrupt:
        print('Aborted manually.', file=stderr)
        return 1

    except Exception as e:
        print('Aborted.', e, file=stderr)
        return 1

    return 0 #success

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('--midi-folder', type=Path, default='datasets/midi/', help="Folder containing the midi files.")
    argument_parser.add_argument('--save-folder', type=Path, default='generated_transitions', help="Folder to save generated transitions.")
    args = argument_parser.parse_args()

    args.save_folder.mkdir(parents=True, exist_ok=True)

    main(args.midi_folder, args.save_folder)
