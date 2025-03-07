## **CONFMON - Monitor Configuration Utility**

**Description:**

CONFMON is a monitor configuration tool for Linux-based operating systems. It allows you to detect connected monitors, configure resolutions and refresh rates, and save and load configurations.

**Features:**

* Detects connected monitors and displays information about them
* Configures resolutions and refresh rates for each monitor
* Saves configurations to a JSON file
* Loads configurations from a JSON file
* Intuitive and easy-to-use user interface

**Requirements:**

* Linux-based operating system
* xrandr installed and configured correctly

**Usage:**

1. Clone the repository: `git clone https://github.com/Rip70022/CONFMON.git`
2. Change to the project directory: `cd CONFMON`
3. Run the script: `python3 confmon.py`

**Command Line Options:**

* `--load`: Loads the saved configuration from the `monitor_config.json` file on startup
* `--save`: Saves the current configuration to the specified file and exits the program
* `--detect`: Detects connected monitors and displays information about them, without starting the user interface

**Examples:**

* `python3 confmon.py --load`: Loads the saved configuration and applies it on startup
* `python3 confmon.py --save config.json`: Saves the current configuration to the `config.json` file and exits the program
* `python3 confmon.py --detect`: Detects connected monitors and displays information about them

**AUTHOR:**

* Created by: Rip70022/craxterpy
* GitHub repository: https://github.com/Rip70022/CONFMON
