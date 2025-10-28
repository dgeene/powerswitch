import json
import os
import sys
import argparse
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
    proxy_config = switch.get("proxy")
    if switch.get("restapi", False):
        return RestClient(switch["host"], switch["username"], switch["password"], proxy_config)
    else:
        return HTTPClient(switch["host"], switch["username"], switch["password"], proxy_config)


def main():
    """Main CLI function using argparse."""
    parser = argparse.ArgumentParser(
        description="Control Digital Loggers Web Power Switch outlets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s PS7 1 on     # Turn on outlet 1 on switch PS7
  %(prog)s PS7 fan off  # Turn off the 'fan' outlet on switch PS7
  %(prog)s PS5 TV on    # Turn on the 'TV' outlet on switch PS5
        """,
    )

    parser.add_argument("switch", help="Name of the switch to control")
    parser.add_argument("outlet", help="Outlet number or name to control")
    parser.add_argument(
        "action",
        choices=["on", "off"],
        help="Action to perform (on/off)",
        type=str.lower,
    )

    args = parser.parse_args()

    # Load configuration
    switches = load_config()

    # Find the switch
    switch = find_switch_by_name(switches, args.switch)
    if not switch:
        print(f"Error: Switch '{args.switch}' not found in configuration.")
        print("Available switches:")
        for s in switches:
            print(f"  - {s['name']}")
        sys.exit(1)

    # Resolve the outlet
    outlet_id = resolve_outlet(switch, args.outlet)
    if not outlet_id:
        print(f"Error: Outlet '{args.outlet}' not found for switch '{args.switch}'.")
        print("Available outlets:")
        for oid, name in switch["outlets"].items():
            print(f"  - {oid}: {name}")
        sys.exit(1)

    # Create the appropriate client
    try:
        client = create_client(switch)

        # Execute the action
        if args.action == "on":
            client.turn_on(int(outlet_id))
            print(
                f"Turned ON outlet {outlet_id} ({switch['outlets'][outlet_id]}) on switch {args.switch}"
            )
        else:
            client.turn_off(int(outlet_id))
            print(
                f"Turned OFF outlet {outlet_id} ({switch['outlets'][outlet_id]}) on switch {args.switch}"
            )

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
