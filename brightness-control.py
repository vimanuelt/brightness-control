#!/usr/bin/env python3

import gi
import subprocess
import os
from tempfile import NamedTemporaryFile

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, Gdk

class BrightnessControl:
    def __init__(self):
        self.brightness = 0
        self.gamma = 1.0  # Default gamma value
        self.video_outputs = self.detect_video_outputs()  # Detect multiple video outputs
        self.video_output = self.video_outputs[0] if self.video_outputs else None
        self.brightness = self.get_brightness() or 0.99  # Set initial brightness
        self.gamma = self.get_gamma() or 1.0  # Set initial gamma

    def run(self):
        app = Gtk.Application(application_id="com.example.brightness-control")
        app.connect("activate", self.on_activate)
        app.run()

    def on_activate(self, app):
        window = self.new_window(app)
        window.set_title("Brightness and Contrast Control")
        window.set_default_size(300, 400)  # Increased window size to fit additional controls

        with NamedTemporaryFile(delete=False, suffix=".css") as css_file:
            css_file.write(b"""
            window {
                background-color: #f5f5f5;
            }
            label {
                font-size: 16px;
                padding: 5px;
                color: #000000;
            }
            button {
                padding: 10px;
                font-size: 16px;
                color: #ffffff;
                background-color: #007acc;
                border-radius: 5px;
                border: none;
            }
            button:hover {
                background-color: #005f9e;
            }
            scale trough {
                background-color: #e0e0e0;
            }
            scale slider {
                background-color: #007acc;
            }
            """)
            css_file_name = css_file.name

        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(Gio.File.new_for_path(css_file_name))

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Main container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)

        # Gtk.DropDown for selecting video output
        video_list = Gtk.StringList.new(self.video_outputs)
        self.output_dropdown = Gtk.DropDown(model=video_list)

        # Set the first active output
        if self.video_outputs:
            self.output_dropdown.set_selected(0)

        self.output_dropdown.set_size_request(150, -1)
        self.output_dropdown.connect("notify::selected", self.on_output_changed)

        # Video output label
        vbox.append(Gtk.Label(label="Select Device:"))
        vbox.append(self.output_dropdown)

        # Current brightness label
        self.brightness_label = self.new_label(f"Brightness: {int(self.brightness * 100)}%")
        vbox.append(self.brightness_label)

        # Brightness control with buttons and scale
        hbox_brightness = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        min_button = Gtk.Button(label="Min")
        decrease_button = Gtk.Button(label="-")
        brightness_scale = self.new_scale()
        brightness_scale.set_range(0.2, 1.0)
        brightness_scale.set_value(self.brightness)
        increase_button = Gtk.Button(label="+")
        max_button = Gtk.Button(label="Max")

        min_button.connect("clicked", self.set_min_brightness, brightness_scale)
        decrease_button.connect("clicked", self.decrease_brightness, brightness_scale)
        brightness_scale.connect("value-changed", self.scale_value_changed, None)
        increase_button.connect("clicked", self.increase_brightness, brightness_scale)
        max_button.connect("clicked", self.set_max_brightness, brightness_scale)

        hbox_brightness.append(min_button)
        hbox_brightness.append(decrease_button)
        hbox_brightness.append(brightness_scale)
        hbox_brightness.append(increase_button)
        hbox_brightness.append(max_button)
        vbox.append(hbox_brightness)

        # Gamma (contrast) label and scale
        self.gamma_label = self.new_label(f"Contrast (Gamma): {self.gamma:.2f}")
        vbox.append(self.gamma_label)

        # Gamma control with buttons and scale
        hbox_gamma = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        min_gamma_button = Gtk.Button(label="Min")
        decrease_gamma_button = Gtk.Button(label="-")
        gamma_scale = self.new_scale()
        gamma_scale.set_range(0.5, 3.0)  # Gamma range for contrast adjustment
        gamma_scale.set_value(self.gamma)
        increase_gamma_button = Gtk.Button(label="+")
        max_gamma_button = Gtk.Button(label="Max")

        min_gamma_button.connect("clicked", self.set_min_gamma, gamma_scale)
        decrease_gamma_button.connect("clicked", self.decrease_gamma, gamma_scale)
        gamma_scale.connect("value-changed", self.gamma_value_changed)
        increase_gamma_button.connect("clicked", self.increase_gamma, gamma_scale)
        max_gamma_button.connect("clicked", self.set_max_gamma, gamma_scale)

        hbox_gamma.append(min_gamma_button)
        hbox_gamma.append(decrease_gamma_button)
        hbox_gamma.append(gamma_scale)
        hbox_gamma.append(increase_gamma_button)
        hbox_gamma.append(max_gamma_button)
        vbox.append(hbox_gamma)

        window.set_child(vbox)
        window.present()

        # Clean up the temporary CSS file
        os.unlink(css_file_name)

    def detect_video_outputs(self):
        try:
            result = subprocess.run(['xrandr'], capture_output=True, text=True, check=True)
            output_lines = result.stdout.splitlines()

            active_outputs = []
            for line in output_lines:
                if " connected" in line:  # Look for connected outputs
                    output = line.split(" ")[0]
                    active_outputs.append(output)

            return active_outputs

        except subprocess.CalledProcessError as e:
            print("Failed to detect video outputs: {}".format(e))
            return []

    def get_brightness(self):
        if self.video_output:
            try:
                result = subprocess.run(['xrandr', '--verbose', '--output', self.video_output], capture_output=True, text=True, check=True)
                output_lines = result.stdout.splitlines()

                for line in output_lines:
                    if "Brightness:" in line:
                        brightness_str = line.split("Brightness:")[1].strip()
                        brightness = float(brightness_str)
                        return brightness

            except subprocess.CalledProcessError as e:
                print("Failed to get brightness: {}".format(e))

        return None

    def get_gamma(self):
        return self.gamma

    def set_brightness(self, brightness):
        if self.video_output:
            try:
                subprocess.run(['xrandr', '--output', self.video_output, '--brightness', str(brightness)], check=True)
            except subprocess.CalledProcessError as e:
                print("Failed to set brightness: {}".format(e))

    def set_gamma(self, gamma):
        if self.video_output:
            try:
                subprocess.run(['xrandr', '--output', self.video_output, '--gamma', f'{gamma}:{gamma}:{gamma}'], check=True)
            except subprocess.CalledProcessError as e:
                print("Failed to set gamma: {}".format(e))

    def on_output_changed(self, combo, _):
        selected_index = combo.get_selected()
        self.video_output = self.video_outputs[selected_index]
        self.brightness = self.get_brightness() or 0.99
        self.brightness_label.set_text(f"Brightness: {int(self.brightness * 100)}%")

    def scale_value_changed(self, scale, _):
        self.brightness = scale.get_value()
        self.set_brightness(self.brightness)
        self.brightness_label.set_text(f"Brightness: {int(self.brightness * 100)}%")

    def gamma_value_changed(self, scale):
        self.gamma = scale.get_value()
        self.set_gamma(self.gamma)
        self.gamma_label.set_text(f"Contrast (Gamma): {self.gamma:.2f}")

    def decrease_brightness(self, button, scale):
        current_value = scale.get_value()
        new_value = max(0.2, current_value - 0.05)
        scale.set_value(new_value)

    def increase_brightness(self, button, scale):
        current_value = scale.get_value()
        new_value = min(1.0, current_value + 0.05)
        scale.set_value(new_value)

    def set_min_brightness(self, button, scale):
        scale.set_value(0.2)

    def set_max_brightness(self, button, scale):
        scale.set_value(1.0)

    def decrease_gamma(self, button, scale):
        current_value = scale.get_value()
        new_value = max(0.5, current_value - 0.1)
        scale.set_value(new_value)

    def increase_gamma(self, button, scale):
        current_value = scale.get_value()
        new_value = min(3.0, current_value + 0.1)
        scale.set_value(new_value)

    def set_min_gamma(self, button, scale):
        scale.set_value(0.5)

    def set_max_gamma(self, button, scale):
        scale.set_value(3.0)

    def new_window(self, app):
        window = Gtk.ApplicationWindow(application=app)
        return window

    def new_label(self, text):
        label = Gtk.Label(label=text)
        label.set_halign(Gtk.Align.CENTER)
        return label

    def new_scale(self):
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        scale.set_digits(2)
        scale.set_value_pos(Gtk.PositionType.RIGHT)
        return scale

def main():
    app = BrightnessControl()
    app.run()

if __name__ == "__main__":
    main()
