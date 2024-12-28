# 11copy

A simple, modern backup tool built with Python and CustomTkinter. 11copy provides an easy way to keep directories in sync with a clean, user-friendly interface.

## Features

- Modern, clean user interface with dark/light mode support
- Incremental backup (only copies changed or new files)
- Real-time progress tracking
- Preserves file metadata
- Remembers last used directories
- Path collision detection
- Windows path length handling
- System theme integration

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
```bash
pip install customtkinter
```
3. Download the `11copy.py` file

## Usage

Run the application:
```bash
python 11copy.py
```

### Basic Operation:

1. Select source directory using the "Browse" button or by typing the path
2. Select target directory using the "Browse" button or by typing the path
3. Click "Start Backup" to begin the backup process

The application will:
- Remember your last used directories
- Only copy files that are new or modified
- Show progress during the backup
- Prevent backing up into source directory
- Handle long path names automatically

### Features:

- **Smart Copy**: Only copies files that have changed or don't exist in the target
- **Progress Tracking**: Shows real-time progress of the backup operation
- **Theme Support**: Includes dark/light mode toggle
- **Directory Memory**: Saves your last used directories in config.json
- **Error Handling**: Provides clear error messages for common issues

## Technical Details

The application uses:
- CustomTkinter for the modern UI
- JSON for configuration storage
- Python's built-in file handling libraries
- Incremental backup strategy

Configuration is stored in `config.json` in the same directory as the application.

## Limitations

- No compression
- No encryption
- Single direction sync (source → target)
- Windows path length limit of 260 characters applies

## Error Messages

Common error messages and their meaning:
- "Target directory cannot be inside source directory": Prevents recursive backup situations
- "Path too long": File path exceeds Windows 260 character limit
- "Source directory does not exist": The specified source directory is invalid

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use and modify for your own projects.
