# 11copy

A modern file synchronization tool built with Python and CustomTkinter. 11copy provides easy and reliable file synchronization with validation capabilities.

## Features

- Fast and reliable file copying
- Two-way synchronization option
- File validation using MD5 checksums
- Modern, clean user interface
- Dark/light mode support
- Real-time progress tracking
- Incremental backup (only copies changed files)
- Smart path handling
- Configuration persistence

## Installation

1. Ensure Python 3.7+ is installed
2. Install required dependency:
```bash
pip install customtkinter
```
3. Download `11copy.py`

## Usage

Run the application:
```bash
python 11copy.py
```

### Basic Operation:

1. Select source directory using "Browse" or enter path
2. Select target directory using "Browse" or enter path
3. Configure sync options:
   - Two-way sync: Enable to sync files in both directions
   - Validate copies: Enable to verify file integrity
4. Click "Start Backup" to begin

### Sync Modes:

- **One-way sync** (default)
  - Copies newer files from source to target
  - Does not delete any files
  - Preserves target-only files

- **Two-way sync**
  - Synchronizes files in both directions
  - Copies newer files to either location
  - Does not delete any files
  - Safe bidirectional updates

### Validation:

When enabled, validation:
- Calculates MD5 checksums of files
- Verifies integrity of copied files
- Validates existing files
- Shows validation progress
- Reports any mismatches

### Features in Detail:

- **Smart Copy**
  - Only copies new or modified files
  - Preserves file metadata
  - Handles long paths
  - Prevents recursive copying

- **Progress Tracking**
  - Shows current operation
  - Displays file counts
  - Indicates sync direction
  - Real-time status updates

- **UI Features**
  - Dark/light mode toggle
  - Clear status messages
  - Directory memory
  - Progress bar

## Configuration

Settings are stored in `config.json`:
- Last used source directory
- Last used target directory

## Technical Details

- Built with Python 3.7+
- Uses CustomTkinter for modern UI
- MD5 for file validation
- Non-destructive operations
- Handles paths up to 260 characters

## Limitations

- No file compression
- No encryption
- Doesn't delete files
- Windows path length limit (260 chars)

## Common Messages

- "No files need updating": All files are synchronized
- "Validating files...": Checking file integrity
- "Copying files...": Transferring new/modified files
- "→": Source to target direction
- "←": Target to source direction (in two-way mode)

## Error Messages

- "Target directory cannot be inside source directory": Prevents recursive copying
- "Path too long": File path exceeds Windows limit
- "Validation failed": File integrity check failed
- "Source directory does not exist": Invalid source path

## Contributing

Issues and pull requests are welcome!

## License

MIT License - free to use and modify
