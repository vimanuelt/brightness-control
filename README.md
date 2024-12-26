# Brightness Control

`brightness-control` is a simple Python application designed for GhostBSD to adjust screen brightness using the `xrandr` utility. It provides a lightweight graphical interface built with GTK4.

---

## Features

- Adjust brightness for individual displays.
- Automatically detects connected displays.
- Lightweight and optimized for GhostBSD.

---

## Installation

Follow these steps to install and set up the application:

### Prerequisites

Ensure the following dependencies are installed on your GhostBSD system:
- `python`
- `py311-pygobject`
- `gtk4`
- `xrandr`

### Steps

1. **Clone the Repository**

   Open a terminal and run:
   ```bash
   git clone https://github.com/vimanuelt/brightness-control.git
   cd brightness-control
   ```

2. **Install the Application**

   Run the following command to install dependencies, build the application, and install the binary:
   ```bash
   make install
   ```

   This will:
   - Install the required system dependencies using `pkg`.
   - Build a standalone executable using PyInstaller.
   - Install the binary to `/usr/local/bin/`.

---

## Usage

Once installed, you can run the application from anywhere using:
```bash
brightness-control
```

### Adjusting Brightness

1. Open the application by running `brightness-control`.
2. Select a display (if multiple are connected).
3. Use the slider or input field to set the desired brightness level.

---

## Uninstallation

To remove the installed binary from your system, run:
```bash
make uninstall
```

This will delete the `brightness-control` binary from `/usr/local/bin`.

---

## Development

### Building from Source

If you want to modify the application or manually build it:
1. Clone the repository:
   ```bash
   git clone https://github.com/vimanuelt/brightness-control.git
   cd brightness-control
   ```
2. Install dependencies:
   ```bash
   make install
   ```
3. Build the executable:
   ```bash
   make build
   ```

The built executable will be located in the `dist/` directory.

### Cleaning Up

To remove build artifacts and the virtual environment:
```bash
make clean
```

---

## Troubleshooting

1. **Brightness Changes Not Applied**:
   - Ensure your display supports brightness adjustments using `xrandr`.
   - Verify the required drivers for your hardware are installed.

2. **Missing Dependencies**:
   - Reinstall the required packages:
     ```bash
     sudo pkg install python py311-pygobject gtk4 xrandr
     ```

3. **Permission Issues**:
   - Run the application as a user with sufficient permissions to manage display settings.

---

## License

This project is licensed under the **BSD 3-Clause License**. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please:
- Open an issue to report bugs or suggest features.
- Submit pull requests to improve the project.

---

## Acknowledgments

- Built with Python, GTK4, and `xrandr`.
- Designed for GhostBSD users seeking a lightweight brightness control solution.

