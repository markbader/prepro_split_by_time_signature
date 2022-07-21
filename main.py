from sys import stderr
from typing import List

import argparse
from pathlib import Path
import multiprocessing as mp

from miditoolkit.midi.parser import MidiFile as BaseMidiFile
from miditoolkit.midi.containers import TimeSignature

argument_parser = argparse.ArgumentParser(description='')

argument_parser.add_argument('--midi-folder', type=Path, default='datasets/midi/', help="Folder containing the midi files.")
argument_parser.add_argument('--save-folder', type=Path, default='output/', help="Folder to save generated transitions.")
argument_parser.add_argument('--accepted-time-signatures', nargs='+', default=['4/4', '3/4', '2/4', '6/8'])
args = argument_parser.parse_args()

args.save_folder.mkdir(parents=True, exist_ok=True)

class MidiFile(BaseMidiFile):
    def __init__(self, filename: Path, *args, **kwargs):
        super().__init__(filename=filename, *args, **kwargs)
        self.name = filename.stem


def read_midis(midi_folder: Path) -> List[MidiFile]:
    filenames = []
    for ext in ('*.mid', '*.midi'):
        filenames.extend(midi_folder.glob(ext))

    return filenames

def is_supported_ts(ts: TimeSignature, ts_list: List[str]) -> bool:
    if ts_list:
        return f'{ts.numerator}/{ts.denominator}' in ts_list
    else:
        # If no time signature is specified everything is accepted.
        return True

def split_midi(filename: Path) -> None:
    midi = MidiFile(filename)
    quarter_length = midi.ticks_per_beat
    min_length = quarter_length * 4 * 16

    for idx, ts in enumerate(midi.time_signature_changes):
        if is_supported_ts(ts, args.accepted_time_signatures):
            start = ts.time
            if len(midi.time_signature_changes) > idx + 1:
                end = midi.time_signature_changes[idx + 1].time - 1
            else:
                end = midi.max_tick
            if end - start < min_length:
                continue

            midi.dump(args.save_folder / f'{midi.name}_{idx}.mid', segment=(start, end))


def main() -> int:
    try:
        midis = read_midis(args.midi_folder)
        pool = mp.Pool(mp.cpu_count() - 1)
        print(f'Found {len(midis)} MIDI files.')
        pool.map(split_midi, midis)
        print('Processing done.')

    except KeyboardInterrupt:
        print('Aborted manually.', file=stderr)
        return 1

    except Exception as e:
        print('Aborted.', e, file=stderr)
        return 1

    return 0 #success

if __name__ == "__main__":
    main()
