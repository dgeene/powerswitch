import json
import os
import sys
from pathlib import Path
from .client import RestClient, HTTPClient


def load_config():
    """Load the switches configuration from the config file."""
    config_paths = [
        Path.home() / ".config" / "switches.json",
        Path.home() / ".config" / "powerswitch" / "switches.json",
        Path(__file__).parent.parent.parent / ".config" / "switches.json",
    ]

    for config_path in config_paths:
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)

    print("Error: No switches.json configuration file found.")
    print("Please create one in one of these locations:")
    for path in config_paths:
        print(f"  - {path}")
    sys.exit(1)


def print_switches(switches):
    """Print available switches with numeric indices."""
    print("\nAvailable switches:")
    for idx, switch in enumerate(switches, 1):
        print(f"{idx}. {switch['name']}")


def print_outlets(outlets):
    """Print available outlets with numeric indices."""
    print("\nAvailable outlets:")
    for outlet_id, outlet_name in outlets.items():
        print(f"{outlet_id}. {outlet_name}")


def get_switch_choice(switches):
    """Get user's switch selection."""
    while True:
        try:
            choice = input("\nSelect switch number (or 'q' to quit): ")
            if choice.lower() == "q":
                return None
            idx = int(choice)
            if 1 <= idx <= len(switches):
                return switches[idx - 1]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number or 'q' to quit.")


def get_outlet_action(outlets):
    """Get user's outlet and action selection."""
    while True:
        try:
            outlet = input("\nSelect outlet number (or 'q' to quit): ")
            if outlet.lower() == "q":
                return None, None

            if outlet not in outlets:
                print("Invalid outlet selection. Please try again.")
                continue

            action = input("Enter action (on/off) or 'q' to quit: ").lower()
            if action == "q":
                return None, None
            if action not in ["on", "off"]:
                print("Invalid action. Please enter 'on' or 'off'.")
                continue

            return outlet, action
        except ValueError:
            print("Please enter a valid outlet number or 'q' to quit.")


def main():
    """Main REPL loop for the power switch controller."""
    switches = load_config()

    while True:
        print_switches(switches)
        switch = get_switch_choice(switches)
        if not switch:
            break

        # Create client based on switch type (defaulting to HTTPClient)
        client = RestClient(switch["host"], switch["username"], switch["password"])

        while True:
            print_outlets(switch["outlets"])
            outlet, action = get_outlet_action(switch["outlets"])
            if not outlet:
                break

            try:
                if action == "on":
                    client.turn_on(int(outlet))
                    print(f"Turned ON outlet {outlet} ({switch['outlets'][outlet]})")
                else:
                    client.turn_off(int(outlet))
                    print(f"Turned OFF outlet {outlet} ({switch['outlets'][outlet]})")
            except Exception as e:
                print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
