# Air Canvas 🎨

A real-time virtual drawing application built using Python, OpenCV, and MediaPipe. Air Canvas allows users to draw on a virtual canvas using hand gestures captured through a webcam.

The application uses hand tracking to detect finger movements and translate them into drawing actions. Users can select colors, draw in the air, save their drawings, and view saved images through a gallery.

## Features

- **Real-Time Hand Tracking:** Detects hand landmarks using MediaPipe.
- **Air Drawing:** Draw on a virtual canvas using your index finger.
- **Color Selection:** Choose different drawing colors using hand gestures.
- **Eraser:** Erase drawings using the eraser option.
- **Save Drawings:** Save your canvas as PNG images.
- **Drawing Gallery:** View saved drawings in a separate gallery application.
- **Image Navigation:** Navigate between saved drawings.
- **Image Deletion:** Delete unwanted drawings from the gallery.
- **SQLite Database:** Store drawing information such as filename, creation date, color, and mode.
- **Keyboard Controls:** Clear the canvas and exit the application using keyboard shortcuts.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- SQLite

## Project Structure

```text
Air-Canvas/
│
├── main.py                 # Main Air Canvas application
├── database.py             # SQLite database operations
├── gallery.py              # Saved drawing gallery
│
├── utils/
│   └── hand_utils.py       # Hand gesture detection
│
├── drawings/               # Saved drawing images
├── screenshots/             # Project screenshots
│
├── requirements.txt         # Python dependencies
├── .gitignore              # Files excluded from Git
├── README.md               # Project documentation
└── LICENSE                 # Project license
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/saliankishan/Air-Canvas.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Navigate to the project directory

```bash
cd Air-Canvas
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows Command Prompt:

```bash
venv\Scripts\activate
```

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## How to Run

### Start the Air Canvas application

```bash
python main.py
```

The application opens the webcam and allows you to draw using hand gestures.

### Open the drawing gallery

After saving drawings, open a separate terminal in the project directory and run:

```bash
python gallery.py
```

The gallery displays saved PNG drawings and provides navigation and deletion controls.

## Controls

### Hand Gestures

| Gesture | Action |
|---|---|
| Index finger up | Draw on the canvas |
| Index and middle fingers up | Select a color |
| Thumb gesture | Save the drawing |

### Keyboard Controls

| Key | Action |
|---|---|
| C | Clear the canvas |
| Ctrl + Z | Undo |
| Q | Quit the application |

### Gallery Controls

| Key | Action |
|---|---|
| A | Previous image |
| D | Next image |
| X | Delete current image |
| Q | Exit gallery |
| ESC | Exit gallery |

## How It Works

1. OpenCV captures video from the webcam.
2. MediaPipe detects hand landmarks.
3. The application identifies finger positions.
4. Hand gestures determine whether the user is drawing, selecting a color, or saving.
5. Drawing movements are rendered on a virtual canvas.
6. Saved drawings are stored as PNG images.
7. SQLite stores drawing metadata.
8. The gallery allows users to view and manage saved drawings.

## Database

The application uses SQLite to maintain drawing information.

The database stores:

- Drawing ID
- Filename
- Creation date and time
- Color
- Mode

The database is initialized automatically when the main application starts.

## Requirements

- Python 3
- Webcam
- Windows, Linux, or macOS
- Required Python packages listed in `requirements.txt`

A working webcam is required for real-time hand tracking.

## Future Enhancements

- Improve undo functionality.
- Add more drawing colors.
- Improve canvas controls.
- Add a more advanced drawing interface.
- Improve application path handling.
- Add additional hand gesture interactions.

## Author

Developed as a Python computer vision project.
