"""
Trading Economics Calendar MCP Server

This module implements an MCP server that provides access to Trading Economics calendar data.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from .client import TradingEconomicsClient, fetch_calendar_events

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("trading-economics-calendar")


@mcp.tool()
async def get_economic_events(
    countries: Optional[List[str]] = None,
    importance: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Fetch economic calendar events from Trading Economics.
    
    Args:
        countries: List of country names (e.g., ["United States", "Germany"])
        importance: Event importance level ("low", "medium", "high")
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        category: Event category filter
        
    Returns:
        List of economic events with details like country, event name, actual/forecast values
    """
    try:
        events = await fetch_calendar_events(
            countries=countries,
            importance=importance,
            start_date=start_date,
            end_date=end_date,
            category=category
        )
        return events
    except Exception as e:
        logger.error(f"Error fetching economic events: {e}")
        raise


@mcp.tool()
async def get_today_economic_events(
    countries: Optional[List[str]] = None,
    importance: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get today's economic events.
    
    Args:
        countries: List of country names to filter by
        importance: Event importance level ("low", "medium", "high")
        
    Returns:
        List of today's economic events
    """
    try:
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        events = await fetch_calendar_events(
            countries=countries,
            importance=importance,
            start_date=today,
            end_date=today
        )
        return events
    except Exception as e:
        logger.error(f"Error fetching today's events: {e}")
        raise


@mcp.tool()
async def get_week_economic_events(
    countries: Optional[List[str]] = None,
    importance: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get this week's economic events.
    
    Args:
        countries: List of country names to filter by
        importance: Event importance level ("low", "medium", "high")
        
    Returns:
        List of this week's economic events
    """
    try:
        from datetime import datetime, timedelta
        today = datetime.now()
        week_end = today + timedelta(days=7)
        
        events = await fetch_calendar_events(
            countries=countries,
            importance=importance,
            start_date=today.strftime('%Y-%m-%d'),
            end_date=week_end.strftime('%Y-%m-%d')
        )
        return events
    except Exception as e:
        logger.error(f"Error fetching week's events: {e}")
        raise


@mcp.tool()
async def get_major_countries() -> Dict[str, str]:
    """
    Get list of major countries supported by the calendar.
    
    Returns:
        Dictionary mapping country codes to country names
    """
    try:
        client = TradingEconomicsClient()
        return client.get_major_countries()
    except Exception as e:
        logger.error(f"Error getting major countries: {e}")
        raise


@mcp.tool()
async def get_importance_levels() -> Dict[str, int]:
    """
    Get available importance levels for filtering events.
    
    Returns:
        Dictionary mapping importance names to numeric levels
    """
    try:
        client = TradingEconomicsClient()
        return client.get_importance_levels()
    except Exception as e:
        logger.error(f"Error getting importance levels: {e}")
        raise


@mcp.tool()
async def get_high_impact_events(
    countries: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get high-impact economic events only.
    
    Args:
        countries: List of country names to filter by
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        List of high-impact economic events
    """
    try:
        events = await fetch_calendar_events(
            countries=countries,
            importance="high",
            start_date=start_date,
            end_date=end_date
        )
        return events
    except Exception as e:
        logger.error(f"Error fetching high-impact events: {e}")
        raise


@mcp.tool()
async def get_events_by_country(
    country: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    importance: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get economic events for a specific country.
    
    Args:
        country: Country name (e.g., "United States", "Germany")
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        importance: Event importance level ("low", "medium", "high")
        
    Returns:
        List of economic events for the specified country
    """
    try:
        events = await fetch_calendar_events(
            countries=[country],
            importance=importance,
            start_date=start_date,
            end_date=end_date
        )
        return events
    except Exception as e:
        logger.error(f"Error fetching events for {country}: {e}")
        raise


def main():
    """Main entry point for the MCP server."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Trading Economics Calendar MCP Server")
        print("Usage: trading-economics-mcp")
        print("\nAvailable tools:")
        print("- get_economic_events: Fetch economic calendar events")
        print("- get_today_economic_events: Get today's events")
        print("- get_week_economic_events: Get this week's events")
        print("- get_major_countries: List supported countries")
        print("- get_importance_levels: List importance levels")
        print("- get_high_impact_events: Get high-impact events only")
        print("- get_events_by_country: Get events for specific country")
        return
    
    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
