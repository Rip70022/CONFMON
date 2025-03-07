#!/usr/bin/env python3
# hell nah
import os
import sys
import time
import subprocess
import random
import json
import argparse
from typing import List, Dict, Tuple, Optional

CREATOR_GITHUB = "https://www.github.com/Rip70022"

ASCII_LOGO = r"""
 ██████╗ ██████╗ ███╗   ██╗███████╗███╗   ███╗ ██████╗ ███╗   ██╗
██╔════╝██╔═══██╗████╗  ██║██╔════╝████╗ ████║██╔═══██╗████╗  ██║
██║     ██║   ██║██╔██╗ ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
██║     ██║   ██║██║╚██╗██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
╚██████╗╚██████╔╝██║ ╚████║██║     ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                  CONFMON - MONITOR CONFIGURATION
                  Created by: Rip70022/craxterpy
                  https://www.github.com/Rip70022
"""

ASCII_MONITOR = r"""
      ╔═══════════════════════════════════════════╗
      ║                                           ║
      ║     ╭───────────────────────────────╮     ║
      ║     │                               │     ║
      ║     │                               │     ║
      ║     │                               │     ║
      ║     │                               │     ║
      ║     │                               │     ║
      ║     │                               │     ║
      ║     ╰───────────────────────────────╯     ║
      ║                                           ║
      ║                   ▬▬▬                     ║
      ╚═══════════════════════════════════════════╝
                           ╲╱
                   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

ASCII_LOADING = [
    "[    ]",
    "[=   ]",
    "[==  ]",
    "[=== ]",
    "[====]",
    "[ ===]",
    "[  ==]",
    "[   =]",
    "[    ]",
    "[   =]",
    "[  ==]",
    "[ ===]",
    "[====]",
    "[=== ]",
    "[==  ]",
    "[=   ]"
]

ASCII_SUCCESS = r"""
          ╭────────────────────────────╮
          │                            │
          │         SUCCESS!           │
          │                            │
          ╰────────────────────────────╯
"""

ASCII_ERROR = r"""
          ╭────────────────────────────╮
          │                            │
          │          ERROR!            │
          │                            │
          ╰────────────────────────────╯
"""

ASCII_DIVIDER = "═" * 80

def print_color(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def print_green(text):
    print_color(text, "92")

def print_cyan(text):
    print_color(text, "96")

def print_yellow(text):
    print_color(text, "93")

def print_red(text):
    print_color(text, "91")

def print_magenta(text):
    print_color(text, "95")

def print_blue(text):
    print_color(text, "94")

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_centered(text, width=80):
    lines = text.split('\n')
    for line in lines:
        if line:
            padding = (width - len(line)) // 2
            print(' ' * padding + line)
        else:
            print()

def show_loading_animation(message, duration=2):
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        clear_screen()
        print("\n\n\n")
        print_centered(f"{message} {ASCII_LOADING[i]}")
        i = (i + 1) % len(ASCII_LOADING)
        time.sleep(0.1)

def show_success(message):
    clear_screen()
    print_green(ASCII_SUCCESS)
    print_centered(message)
    print("\n\n")
    time.sleep(1.5)

def show_error(message):
    clear_screen()
    print_red(ASCII_ERROR)
    print_centered(message)
    print("\n\n")
    time.sleep(1.5)

class MonitorConfig:
    def __init__(self):
        self.monitors = []
        self.current_config = {}
        self.available_resolutions = []
        self.available_refresh_rates = []
    
    def detect_monitors(self) -> List[str]:
        show_loading_animation("Detecting monitors")
        
        result = subprocess.run(['xrandr', '--query'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')
        
        self.monitors = []
        for line in lines:
            if " connected " in line:
                monitor_name = line.split()[0]
                self.monitors.append(monitor_name)
        
        return self.monitors
    
    def get_monitor_info(self, monitor: str) -> Dict:
        result = subprocess.run(['xrandr', '--query'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')
        
        monitor_info = {"name": monitor, "resolutions": []}
        capture_mode = False
        
        for line in lines:
            if monitor in line and " connected " in line:
                capture_mode = True
                continue
            elif capture_mode and "disconnected" in line:
                break
            elif capture_mode and line.startswith("   "):
                resolution_info = line.strip().split()
                resolution = resolution_info[0]
                refresh_rates = []
                
                for item in resolution_info[1:]:
                    if "Hz" in item:
                        rate = item.replace("*", "").replace("+", "").replace("Hz", "")
                        refresh_rates.append(float(rate))
                
                if refresh_rates:
                    monitor_info["resolutions"].append({
                        "resolution": resolution,
                        "refresh_rates": refresh_rates
                    })
        
        return monitor_info
    
    def set_resolution(self, monitor: str, resolution: str) -> bool:
        show_loading_animation(f"Setting resolution to {resolution}")
        
        try:
            subprocess.run(['xrandr', '--output', monitor, '--mode', resolution], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def set_refresh_rate(self, monitor: str, resolution: str, refresh_rate: float) -> bool:
        show_loading_animation(f"Setting refresh rate to {refresh_rate} Hz")
        
        rate_str = f"{refresh_rate:.2f}"
        try:
            subprocess.run(['xrandr', '--output', monitor, '--mode', resolution, '--rate', rate_str], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def set_position(self, monitor: str, position: str, reference_monitor: Optional[str] = None) -> bool:
        position_display = position
        if reference_monitor:
            position_display = f"{position} {reference_monitor}"
        
        show_loading_animation(f"Setting monitor position to {position_display}")
        
        try:
            if position == "primary":
                subprocess.run(['xrandr', '--output', monitor, '--primary'], check=True)
                return True
            elif reference_monitor and position in ["left-of", "right-of", "above", "below"]:
                subprocess.run(['xrandr', '--output', monitor, f'--{position}', reference_monitor], check=True)
                return True
            return False
        except subprocess.CalledProcessError:
            return False
    
    def save_config(self, filename: str) -> bool:
        show_loading_animation(f"Saving configuration to {filename}")
        
        config = {}
        for monitor in self.monitors:
            info = self.get_monitor_info(monitor)
            active_res = None
            active_rate = None
            
            result = subprocess.run(['xrandr', '--query'], stdout=subprocess.PIPE, text=True)
            lines = result.stdout.strip().split('\n')
            
            for line in lines:
                if monitor in line and " connected " in line:
                    continue
                elif line.startswith("   "):
                    if "*" in line:
                        parts = line.strip().split()
                        active_res = parts[0]
                        for part in parts:
                            if "*" in part and "Hz" in part:
                                active_rate = float(part.replace("*", "").replace("+", "").replace("Hz", ""))
            
            if active_res and active_rate:
                config[monitor] = {
                    "resolution": active_res,
                    "refresh_rate": active_rate
                }
                
                position_result = subprocess.run(['xrandr', '--query'], stdout=subprocess.PIPE, text=True)
                for line in position_result.stdout.strip().split('\n'):
                    if monitor in line and " connected " in line:
                        if "primary" in line:
                            config[monitor]["position"] = "primary"
                        else:
                            for pos in ["left", "right", "above", "below"]:
                                if f"{pos} " in line:
                                    ref_monitor = line.split(f"{pos} ")[1].split()[0]
                                    config[monitor]["position"] = f"{pos}-of"
                                    config[monitor]["reference"] = ref_monitor
        
        try:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_config(self, filename: str) -> bool:
        show_loading_animation(f"Loading configuration from {filename}")
        
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
            
            for monitor, settings in config.items():
                if monitor in self.monitors:
                    self.set_resolution(monitor, settings["resolution"])
                    self.set_refresh_rate(monitor, settings["resolution"], settings["refresh_rate"])
                    
                    if "position" in settings:
                        if settings["position"] == "primary":
                            self.set_position(monitor, "primary")
                        elif "reference" in settings:
                            self.set_position(monitor, settings["position"], settings["reference"])
            
            return True
        except Exception:
            return False

class FuturisticUI:
    def __init__(self):
        self.monitor_config = MonitorConfig()
    
    def display_main_menu(self):
        clear_screen()
        print_cyan(ASCII_LOGO)
        print_yellow(ASCII_DIVIDER)
        print_green("\n\n")
        
        print_centered("MAIN MENU")
        print("\n")
        print_cyan("  [1] Detect Monitors")
        print_cyan("  [2] Configure Monitor")
        print_cyan("  [3] Save Configuration")
        print_cyan("  [4] Load Configuration")
        print_cyan("  [0] Exit")
        print("\n\n")
        print_yellow(ASCII_DIVIDER)
        
        choice = input("\nEnter your choice (0-4): ")
        
        if choice == "1":
            self.detect_monitors()
        elif choice == "2":
            self.select_monitor()
        elif choice == "3":
            self.save_configuration()
        elif choice == "4":
            self.load_configuration()
        elif choice == "0":
            self.exit_program()
        else:
            show_error("Invalid choice. Please try again.")
            self.display_main_menu()
    
    def detect_monitors(self):
        monitors = self.monitor_config.detect_monitors()
        
        clear_screen()
        print_cyan(ASCII_MONITOR)
        print_yellow(ASCII_DIVIDER)
        
        if monitors:
            print_green(f"\nDetected {len(monitors)} monitors:")
            for i, monitor in enumerate(monitors, 1):
                print_cyan(f"  {i}. {monitor}")
            print("\n")
        else:
            print_red("\nNo monitors detected!")
            print("\n")
        
        print_yellow(ASCII_DIVIDER)
        input("\nPress Enter to continue...")
        self.display_main_menu()
    
    def select_monitor(self):
        monitors = self.monitor_config.detect_monitors()
        
        if not monitors:
            show_error("No monitors detected!")
            self.display_main_menu()
            return
        
        clear_screen()
        print_cyan(ASCII_MONITOR)
        print_yellow(ASCII_DIVIDER)
        
        print_green("\nSelect a monitor to configure:")
        for i, monitor in enumerate(monitors, 1):
            print_cyan(f"  {i}. {monitor}")
        print_cyan(f"  0. Back to Main Menu")
        print("\n")
        
        print_yellow(ASCII_DIVIDER)
        
        try:
            choice = int(input("\nEnter your choice (0-" + str(len(monitors)) + "): "))
            if choice == 0:
                self.display_main_menu()
            elif 1 <= choice <= len(monitors):
                selected_monitor = monitors[choice - 1]
                self.configure_monitor(selected_monitor)
            else:
                show_error("Invalid choice. Please try again.")
                self.select_monitor()
        except ValueError:
            show_error("Invalid input. Please enter a number.")
            self.select_monitor()
    
    def configure_monitor(self, monitor):
        monitor_info = self.monitor_config.get_monitor_info(monitor)
        
        clear_screen()
        print_cyan(ASCII_MONITOR)
        print_yellow(ASCII_DIVIDER)
        
        print_green(f"\nConfiguring monitor: {monitor}")
        print_cyan("\nWhat would you like to configure?")
        print_cyan("  [1] Resolution")
        print_cyan("  [2] Position")
        print_cyan("  [0] Back")
        print("\n")
        
        print_yellow(ASCII_DIVIDER)
        
        choice = input("\nEnter your choice (0-2): ")
        
        if choice == "1":
            self.select_resolution(monitor, monitor_info)
        elif choice == "2":
            self.select_position(monitor)
        elif choice == "0":
            self.select_monitor()
        else:
            show_error("Invalid choice. Please try again.")
            self.configure_monitor(monitor)
    
    def select_resolution(self, monitor, monitor_info):
        clear_screen()
        print_cyan(ASCII_MONITOR)
        print_yellow(ASCII_DIVIDER)
        
        print_green(f"\nSelect resolution for {monitor}:")
        
        resolutions = [res_info["resolution"] for res_info in monitor_info["resolutions"]]
        
        for i, resolution in enumerate(resolutions, 1):
            print_cyan(f"  {i}. {resolution}")
        print_cyan(f"  0. Back")
        print("\n")
        
        print_yellow(ASCII_DIVIDER)
        
        try:
            choice = int(input("\nEnter your choice (0-" + str(len(resolutions)) + "): "))
            if choice == 0:
                self.configure_monitor(monitor)
            elif 1 <= choice <= len(resolutions):
                selected_resolution = resolutions[choice - 1]
                if self.monitor_config.set_resolution(monitor, selected_resolution):
                    show_success(f"Resolution set to {selected_resolution}")
                    self.select_refresh_rate(monitor, monitor_info, selected_resolution)
                else:
                    show_error(f"Failed to set resolution to {selected_resolution}")
                    self.select_resolution(monitor, monitor_info)
            else:
                show_error("Invalid choice. Please try again.")
                self.select_resolution(monitor, monitor_info)
        except ValueError:
            show_error("Invalid input. Please enter a number.")
            self.select_resolution(monitor, monitor_info)
    
    def select_refresh_rate(self, monitor, monitor_info, selected_resolution):
        refresh_rates = []
        
        for res_info in monitor_info["resolutions"]:
            if res_info["resolution"] == selected_resolution:
                refresh_rates = res_info["refresh_rates"]
                break
        
        clear_screen()
        print_cyan(ASCII_MONITOR)
        print_yellow(ASCII_DIVIDER)
        
        print_green(f"\nSelect refresh rate for {monitor} @ {selected_resolution}:")
        
        for i, rate in enumerate(refresh_rates, 1):
            print_cyan(f"  {i}. {rate} Hz")
        print_cyan(f"  0. Skip (Keep current)")
        print("\n")
        
        print_yellow(ASCII_DIVIDER)
        
        try:
            choice = int(input("\nEnter your choice (0-" + str(len(refresh_rates)) + "): "))
            if choice == 0:
                self.configure_monitor(monitor)
            elif 1 <= choice <= len(refresh_rates):
                selected_rate = refresh_rates[choice - 1]
                if self.monitor_config.set_refresh_rate(monitor, selected_resolution, selected_rate):
                    show_success(f"Refresh rate set to {selected_rate} Hz")
                    self.configure_monitor(monitor)
                else:
                    show_error(f"Failed to set refresh rate to {selected_rate} Hz")
                    self.select_refresh_rate(monitor, monitor_info, selected_resolution)
            else:
                show_error("Invalid choice. Please try again.")
                self.select_refresh_rate(monitor, monitor_info, selected_resolution)
        except ValueError:
            show_error("Invalid input. Please enter a number.")
            self.select_refresh_rate(monitor, monitor_info, selected_resolution)
    
    def select_position(self, monitor):
        clear_screen()
        print_cyan(ASCII_MONITOR)
        print_yellow(ASCII_DIVIDER)
        
        print_green(f"\nSet position for {monitor}:")
        print_cyan("  [1] Set as Primary")
        print_cyan("  [2] Position Left of Another Monitor")
        print_cyan("  [3] Position Right of Another Monitor")
        print_cyan("  [4] Position Above Another Monitor")
        print_cyan("  [5] Position Below Another Monitor")
        print_cyan("  [0] Back")
        print("\n")
        
        print_yellow(ASCII_DIVIDER)
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == "1":
            if self.monitor_config.set_position(monitor, "primary"):
                show_success(f"Set {monitor} as primary")
                self.configure_monitor(monitor)
            else:
                show_error("Failed to set primary monitor")
                self.select_position(monitor)
        elif choice in ["2", "3", "4", "5"]:
            positions = ["left-of", "right-of", "above", "below"]
            selected_position = positions[int(choice) - 2]
            self.select_reference_monitor(monitor, selected_position)
        elif choice == "0":
            self.configure_monitor(monitor)
        else:
            show_error("Invalid choice. Please try again.")
            self.select_position(monitor)
    
    def select_reference_monitor(self, monitor, position):
        monitors = self.monitor_config.detect_monitors()
        reference_monitors = [m for m in monitors if m != monitor]
        
        if not reference_monitors:
            show_error("No other monitors to reference")
            self.select_position(monitor)
            return
        
        clear_screen()
        print_cyan(ASCII_MONITOR)
        print_yellow(ASCII_DIVIDER)
        
        position_names = {
            "left-of": "to the left of",
            "right-of": "to the right of",
            "above": "above",
            "below": "below"
        }
        
        print_green(f"\nSelect reference monitor to position {monitor} {position_names[position]}:")
        
        for i, ref_monitor in enumerate(reference_monitors, 1):
            print_cyan(f"  {i}. {ref_monitor}")
        print_cyan(f"  0. Back")
        print("\n")
        
        print_yellow(ASCII_DIVIDER)
        
        try:
            choice = int(input("\nEnter your choice (0-" + str(len(reference_monitors)) + "): "))
            if choice == 0:
                self.select_position(monitor)
            elif 1 <= choice <= len(reference_monitors):
                reference_monitor = reference_monitors[choice - 1]
                if self.monitor_config.set_position(monitor, position, reference_monitor):
                    show_success(f"Positioned {monitor} {position_names[position]} {reference_monitor}")
                    self.configure_monitor(monitor)
                else:
                    show_error(f"Failed to position monitor")
                    self.select_reference_monitor(monitor, position)
            else:
                show_error("Invalid choice. Please try again.")
                self.select_reference_monitor(monitor, position)
        except ValueError:
            show_error("Invalid input. Please enter a number.")
            self.select_reference_monitor(monitor, position)
    
    def save_configuration(self):
        filename = "monitor_config.json"
        
        if self.monitor_config.save_config(filename):
            show_success(f"Configuration saved to {filename}")
        else:
            show_error("Failed to save configuration")
        
        self.display_main_menu()
    
    def load_configuration(self):
        filename = "monitor_config.json"
        
        if not os.path.exists(filename):
            show_error(f"Configuration file {filename} not found")
            self.display_main_menu()
            return
        
        if self.monitor_config.load_config(filename):
            show_success(f"Configuration loaded from {filename}")
        else:
            show_error("Failed to load configuration")
        
        self.display_main_menu()
    
    def exit_program(self):
        clear_screen()
        print_magenta(ASCII_LOGO)
        print_yellow(ASCII_DIVIDER)
        print_green("\n\nThank you for using CONFMON!\n")
        print_cyan(f"Created by: {CREATOR_GITHUB}")
        print("\n\n")
        print_yellow(ASCII_DIVIDER)
        time.sleep(1)
        clear_screen()
        sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser(description="CONFMON - Monitor Configuration Utility")
    parser.add_argument('--load', action='store_true', help='Load saved configuration on startup')
    parser.add_argument('--save', type=str, help='Save configuration to specified file and exit')
    parser.add_argument('--detect', action='store_true', help='Detect monitors and print information')
    return parser.parse_args()

def main():
    args = parse_args()
    monitor_config = MonitorConfig()
    
    if args.detect:
        monitors = monitor_config.detect_monitors()
        print(f"Detected {len(monitors)} monitors:")
        for monitor in monitors:
            print(f"- {monitor}")
            info = monitor_config.get_monitor_info(monitor)
            for res_info in info["resolutions"]:
                print(f"  {res_info['resolution']}: {', '.join([str(r) + ' Hz' for r in res_info['refresh_rates']])}")
        return
    
    if args.save:
        if monitor_config.save_config(args.save):
            print(f"Configuration saved to {args.save}")
        else:
            print("Error saving configuration")
        return
    
    ui = FuturisticUI()
    
    if args.load:
        if os.path.exists("monitor_config.json"):
            if monitor_config.load_config("monitor_config.json"):
                print("Configuration loaded successfully")
            else:
                print("Error loading configuration")
    
    try:
        clear_screen()
        print_magenta(ASCII_LOGO)
        time.sleep(1.5)
        ui.display_main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print("Program terminated by user")

if __name__ == "__main__":
    main()
