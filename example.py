#!/usr/bin/env python3
"""
Example usage of the Trading Economics Calendar MCP Server.
"""

import asyncio
import json
from datetime import datetime, timedelta

from trading_economics_calendar.client import TradingEconomicsClient, fetch_calendar_events


async def main():
    """Main example function."""
    print("Trading Economics Calendar MCP Server - Examples")
    print("=" * 50)
    
    # Example 1: Get today's events for major countries
    print("\n1. Today's events for US and Germany:")
    try:
        today_events = await fetch_calendar_events(
            countries=["United States", "Germany"],
            start_date=datetime.now().strftime('%Y-%m-%d'),
            end_date=datetime.now().strftime('%Y-%m-%d')
        )
        print(f"Found {len(today_events)} events")
        for event in today_events[:3]:  # Show first 3
            print(f"  - {event.get('country', 'N/A')}: {event.get('event', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Get high-impact events for this week
    print("\n2. High-impact events for this week:")
    try:
        today = datetime.now()
        week_end = today + timedelta(days=7)
        
        high_impact_events = await fetch_calendar_events(
            importance="high",
            start_date=today.strftime('%Y-%m-%d'),
            end_date=week_end.strftime('%Y-%m-%d')
        )
        print(f"Found {len(high_impact_events)} high-impact events")
        for event in high_impact_events[:3]:  # Show first 3
            print(f"  - {event.get('country', 'N/A')}: {event.get('event', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Get available countries and importance levels
    print("\n3. Available countries and importance levels:")
    try:
        client = TradingEconomicsClient()
        countries = client.get_major_countries()
        importance_levels = client.get_importance_levels()
        
        print(f"Major countries: {list(countries.values())[:5]}...")  # Show first 5
        print(f"Importance levels: {importance_levels}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Get events for specific country
    print("\n4. Events for United States (next 3 days):")
    try:
        today = datetime.now()
        three_days = today + timedelta(days=3)
        
        us_events = await fetch_calendar_events(
            countries=["United States"],
            start_date=today.strftime('%Y-%m-%d'),
            end_date=three_days.strftime('%Y-%m-%d')
        )
        print(f"Found {len(us_events)} US events")
        for event in us_events[:3]:  # Show first 3
            print(f"  - {event.get('time', 'N/A')} {event.get('event', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("Examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
