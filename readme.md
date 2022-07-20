# MIDI preprocessing to avoid time signature changes

Scans a given folder for MIDI files and creates MIDI snippets without time signature changes. Each time the time signature within a MIDI file changes the file is split.

## Installation

This Script was implemented on python version `3.8.10`. To install required dependencies just run:
```
pip install -r requirements.txt
```

## Usage

To split all MIDI files of the folder `<midi-folder>` run:
```
python3 main.py --midi-folder <midi-folder>
```

If only some time signatures are accepted it is possible to restrict the output to a set of time signatures e.g. `4/4`, `2/4`, `3/4` and `6/8` with:
```
python3 main.py --midi-folder <midi-folder> --accepted-time-signatures "4/4" "2/4" "3/4" "6/8"
```

To use another output folder than `output/` you can give an alternative path with the argument `--save-folder`.
