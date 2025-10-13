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


def find_switch_by_name(switches, switch_name):
    """Find a switch configuration by name."""
    for switch in switches:
        if switch["name"] == switch_name:
            return switch
    return None


def resolve_outlet(switch, outlet_input):
    """Resolve outlet by number or name, return outlet number as string."""
    outlets = switch["outlets"]

    # Try as direct outlet number
    if outlet_input in outlets:
        return outlet_input

    # Try as outlet name (case-insensitive)
    for outlet_id, outlet_name in outlets.items():
        if outlet_name.lower() == outlet_input.lower():
            return outlet_id

    return None


def create_client(switch):
    """Create appropriate client based on switch configuration."""
    if switch.get("restapi", False):
        return RestClient(switch["host"], switch["username"], switch["password"])
    else:
        return HTTPClient(switch["host"], switch["username"], switch["password"])


def print_usage():
    """Print usage information."""
    print("Usage: cli.py <switch_name> <outlet_number_or_name> <on|off>")
    print("\nExample:")
    print("  cli.py PS7 1 on")
    print("  cli.py PS7 fan off")
    print("  cli.py PS5 TV on")


def main():
    """Main CLI function with positional arguments."""
    if len(sys.argv) != 4:
        print("Error: Invalid number of arguments.")
        print_usage()
        sys.exit(1)

    switch_name = sys.argv[1]
    outlet_input = sys.argv[2]
    action = sys.argv[3].lower()

    # Validate action
    if action not in ["on", "off"]:
        print(f"Error: Invalid action '{sys.argv[3]}'. Must be 'on' or 'off'.")
        sys.exit(1)

    # Load configuration
    switches = load_config()

    # Find the switch
    switch = find_switch_by_name(switches, switch_name)
    if not switch:
        print(f"Error: Switch '{switch_name}' not found in configuration.")
        print("Available switches:")
        for s in switches:
            print(f"  - {s['name']}")
        sys.exit(1)

    # Resolve the outlet
    outlet_id = resolve_outlet(switch, outlet_input)
    if not outlet_id:
        print(f"Error: Outlet '{outlet_input}' not found for switch '{switch_name}'.")
        print("Available outlets:")
        for oid, name in switch["outlets"].items():
            print(f"  - {oid}: {name}")
        sys.exit(1)

    # Create the appropriate client
    try:
        client = create_client(switch)

        # Execute the action
        if action == "on":
            client.turn_on(int(outlet_id))
            print(
                f"Turned ON outlet {outlet_id} ({switch['outlets'][outlet_id]}) on switch {switch_name}"
            )
        else:
            client.turn_off(int(outlet_id))
            print(
                f"Turned OFF outlet {outlet_id} ({switch['outlets'][outlet_id]}) on switch {switch_name}"
            )

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
