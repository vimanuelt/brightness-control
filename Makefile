# Makefile for brightness-control (GhostBSD edition)

# Variables
APP_NAME := brightness-control
PYTHON   := python3
PIP      := pip3
VENV_DIR := venv
BIN_DIR  := /usr/local/bin
SYSTEM_PACKAGES := python py311-pygobject gtk4 xrandr
GI_PATH := /usr/local/lib/python3.11/site-packages

# Default target
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make install     - Install dependencies, build executable, and install to /usr/local/bin/"
	@echo "  make uninstall   - Remove the installed binary from /usr/local/bin/"
	@echo "  make build       - Build a standalone executable with PyInstaller"
	@echo "  make clean       - Remove build artifacts and the virtual environment"

# Install required system packages
.PHONY: system-deps
system-deps:
	@echo "Installing required system packages..."
	sudo pkg install -y $(SYSTEM_PACKAGES)

# Create a virtual environment and install Python dependencies
.PHONY: python-deps
python-deps:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	. $(VENV_DIR)/bin/activate && \
	   $(PIP) install --upgrade pip && \
	   $(PIP) install pyinstaller

# Build a standalone executable using PyInstaller
.PHONY: build
build: python-deps
	. $(VENV_DIR)/bin/activate && \
	   pyinstaller --onefile \
	       --paths=$(GI_PATH) \
	       --hidden-import=gi \
	       --hidden-import=gi.repository \
	       brightness-control.py --name $(APP_NAME)

# Install the binary to /usr/local/bin/
.PHONY: install-bin
install-bin: build
	@echo "Installing the binary to $(BIN_DIR)..."
	sudo install -m 755 dist/$(APP_NAME) $(BIN_DIR)

# Install everything: dependencies, build, and install binary
.PHONY: install
install: system-deps install-bin
	@echo "Installation complete! You can now run '$(APP_NAME)' from anywhere."

# Uninstall the binary from /usr/local/bin/
.PHONY: uninstall
uninstall:
	@echo "Uninstalling the binary from $(BIN_DIR)..."
	@if [ -f "$(BIN_DIR)/$(APP_NAME)" ]; then \
		sudo rm -f $(BIN_DIR)/$(APP_NAME); \
		echo "$(APP_NAME) has been removed from $(BIN_DIR)."; \
	else \
		echo "$(APP_NAME) is not installed in $(BIN_DIR)."; \
	fi

# Clean up build artifacts and virtual environment
.PHONY: clean
clean:
	rm -rf dist build __pycache__ *.spec
	rm -rf $(VENV_DIR)
	@echo "Cleaned up build artifacts and virtual environment."

