#!/usr/bin/env python3
"""
Command-line interface for testing the Trading Economics Calendar MCP Server.
"""

import asyncio
import json
import argparse
from datetime import datetime, timedelta

from trading_economics_calendar.client import fetch_calendar_events, TradingEconomicsClient


async def get_events_command(args):
    """Handle get events command."""
    events = await fetch_calendar_events(
        countries=args.countries,
        importance=args.importance,
        start_date=args.start_date,
        end_date=args.end_date
    )
    
    if args.output == 'json':
        print(json.dumps(events, indent=2))
    else:
        print(f"Found {len(events)} events:")
        for event in events:
            country = event.get('country', 'N/A')
            time = event.get('time', 'N/A')
            event_name = event.get('event', 'N/A')
            importance = '★' * event.get('importance', 1)
            print(f"  {country:15} {time:8} {importance:5} {event_name}")


async def get_today_command(args):
    """Handle get today events command."""
    today = datetime.now().strftime('%Y-%m-%d')
    events = await fetch_calendar_events(
        countries=args.countries,
        importance=args.importance,
        start_date=today,
        end_date=today
    )
    
    if args.output == 'json':
        print(json.dumps(events, indent=2))
    else:
        print(f"Today's events ({len(events)} found):")
        for event in events:
            country = event.get('country', 'N/A')
            time = event.get('time', 'N/A')
            event_name = event.get('event', 'N/A')
            importance = '★' * event.get('importance', 1)
            print(f"  {country:15} {time:8} {importance:5} {event_name}")


async def get_week_command(args):
    """Handle get week events command."""
    today = datetime.now()
    week_end = today + timedelta(days=7)
    
    events = await fetch_calendar_events(
        countries=args.countries,
        importance=args.importance,
        start_date=today.strftime('%Y-%m-%d'),
        end_date=week_end.strftime('%Y-%m-%d')
    )
    
    if args.output == 'json':
        print(json.dumps(events, indent=2))
    else:
        print(f"This week's events ({len(events)} found):")
        for event in events:
            country = event.get('country', 'N/A')
            time = event.get('time', 'N/A')
            event_name = event.get('event', 'N/A')
            importance = '★' * event.get('importance', 1)
            print(f"  {country:15} {time:8} {importance:5} {event_name}")


def list_countries_command(args):
    """Handle list countries command."""
    client = TradingEconomicsClient()
    countries = client.get_major_countries()
    
    if args.output == 'json':
        print(json.dumps(countries, indent=2))
    else:
        print("Major countries supported:")
        for code, name in countries.items():
            print(f"  {code:20} -> {name}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Trading Economics Calendar CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s today --countries "United States" "Germany"
  %(prog)s events --start-date 2024-01-01 --end-date 2024-01-31 --importance high
  %(prog)s week --importance high --output json
  %(prog)s countries
        """
    )
    
    parser.add_argument(
        '--output', 
        choices=['table', 'json'], 
        default='table',
        help='Output format (default: table)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Events command
    events_parser = subparsers.add_parser('events', help='Get economic events')
    events_parser.add_argument('--countries', nargs='+', help='Country names')
    events_parser.add_argument('--importance', choices=['low', 'medium', 'high'], help='Importance level')
    events_parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    events_parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    
    # Today command
    today_parser = subparsers.add_parser('today', help="Get today's events")
    today_parser.add_argument('--countries', nargs='+', help='Country names')
    today_parser.add_argument('--importance', choices=['low', 'medium', 'high'], help='Importance level')
    
    # Week command
    week_parser = subparsers.add_parser('week', help="Get this week's events")
    week_parser.add_argument('--countries', nargs='+', help='Country names')
    week_parser.add_argument('--importance', choices=['low', 'medium', 'high'], help='Importance level')
    
    # Countries command
    subparsers.add_parser('countries', help='List supported countries')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'events':
            asyncio.run(get_events_command(args))
        elif args.command == 'today':
            asyncio.run(get_today_command(args))
        elif args.command == 'week':
            asyncio.run(get_week_command(args))
        elif args.command == 'countries':
            list_countries_command(args)
    except KeyboardInterrupt:
        print("\nCancelled by user")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
