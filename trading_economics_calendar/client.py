"""
Trading Economics Calendar Data Fetcher

This module provides functions to fetch economic calendar events from Trading Economics.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

logger = logging.getLogger(__name__)


class TradingEconomicsClient:
    """Client for fetching data from Trading Economics calendar."""
    
    BASE_URL = "https://tradingeconomics.com"
    CALENDAR_URL = f"{BASE_URL}/calendar"
    
    # Major countries mapping
    MAJOR_COUNTRIES = {
        "united_states": "United States",
        "china": "China", 
        "japan": "Japan",
        "germany": "Germany",
        "united_kingdom": "United Kingdom",
        "france": "France",
        "italy": "Italy",
        "canada": "Canada",
        "australia": "Australia",
        "brazil": "Brazil",
        "india": "India",
        "russia": "Russia",
        "south_korea": "South Korea",
        "spain": "Spain",
        "mexico": "Mexico",
        "netherlands": "Netherlands",
        "switzerland": "Switzerland",
        "belgium": "Belgium",
        "sweden": "Sweden",
        "austria": "Austria"
    }
    
    IMPORTANCE_LEVELS = {
        "low": 1,
        "medium": 2, 
        "high": 3
    }
    
    def __init__(self, session: Optional[requests.Session] = None):
        """Initialize the client with optional session."""
        self.session = session or requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_calendar_events(
        self,
        countries: Optional[List[str]] = None,
        importance: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch economic calendar events.
        
        Args:
            countries: List of country names or codes
            importance: Importance level ('low', 'medium', 'high')
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            category: Event category filter
            
        Returns:
            List of economic events
        """
        try:
            # Build query parameters
            params = {}
            
            if start_date:
                params['from'] = start_date
            if end_date:
                params['to'] = end_date
            if importance and importance.lower() in self.IMPORTANCE_LEVELS:
                params['importance'] = self.IMPORTANCE_LEVELS[importance.lower()]
            if countries:
                # Convert country names to proper format
                country_list = []
                for country in countries:
                    if country.lower().replace(' ', '_') in self.MAJOR_COUNTRIES:
                        country_list.append(self.MAJOR_COUNTRIES[country.lower().replace(' ', '_')])
                    else:
                        country_list.append(country)
                params['countries'] = ','.join(country_list)
            
            # Construct URL
            url = self.CALENDAR_URL
            if params:
                url += f"?{urlencode(params)}"
            
            logger.info(f"Fetching calendar data from: {url}")
            
            # Make request
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            events = self._parse_calendar_events(soup)
            
            # Apply additional filtering if needed
            if countries:
                events = [e for e in events if e.get('country', '').lower() in [c.lower() for c in countries]]
            
            return events
            
        except Exception as e:
            logger.error(f"Error fetching calendar events: {e}")
            raise
    
    def _parse_calendar_events(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Parse economic events from the HTML soup.
        
        Args:
            soup: BeautifulSoup object of the calendar page
            
        Returns:
            List of parsed events
        """
        events = []
        
        try:
            # Look for calendar table or events container
            # This is a simplified parser - the actual structure may vary
            calendar_table = soup.find('table', {'id': 'calendar'}) or soup.find('table', class_='calendar')
            
            if not calendar_table:
                # Try alternative selectors
                event_rows = soup.select('tr[data-event-id]') or soup.select('.calendar-row')
            else:
                event_rows = calendar_table.find_all('tr')[1:]  # Skip header
            
            for row in event_rows:
                try:
                    event = self._parse_event_row(row)
                    if event:
                        events.append(event)
                except Exception as e:
                    logger.warning(f"Error parsing event row: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing calendar events: {e}")
            
        return events
    
    def _parse_event_row(self, row) -> Optional[Dict[str, Any]]:
        """
        Parse a single event row.
        
        Args:
            row: BeautifulSoup element representing an event row
            
        Returns:
            Parsed event data or None
        """
        try:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 5:  # Minimum expected columns
                return None
            
            event = {}
            
            # Extract basic information (this structure may need adjustment based on actual HTML)
            if len(cells) >= 1:
                time_cell = cells[0]
                event['time'] = time_cell.get_text(strip=True) if time_cell else ''
            
            if len(cells) >= 2:
                country_cell = cells[1]
                country_img = country_cell.find('img')
                if country_img:
                    event['country'] = country_img.get('title', '') or country_img.get('alt', '')
                else:
                    event['country'] = country_cell.get_text(strip=True)
            
            if len(cells) >= 3:
                importance_cell = cells[2]
                # Count stars or importance indicators
                stars = len(importance_cell.find_all(['span', 'i'], class_=lambda x: x and 'star' in x.lower())) if importance_cell else 0
                event['importance'] = min(max(stars, 1), 3)  # 1-3 scale
            
            if len(cells) >= 4:
                event_cell = cells[3]
                event['event'] = event_cell.get_text(strip=True) if event_cell else ''
            
            if len(cells) >= 5:
                actual_cell = cells[4]
                event['actual'] = actual_cell.get_text(strip=True) if actual_cell else ''
            
            if len(cells) >= 6:
                forecast_cell = cells[5]
                event['forecast'] = forecast_cell.get_text(strip=True) if forecast_cell else ''
            
            if len(cells) >= 7:
                previous_cell = cells[6]
                event['previous'] = previous_cell.get_text(strip=True) if previous_cell else ''
            
            # Add current date if no date specified
            event['date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Clean up empty values
            event = {k: v for k, v in event.items() if v and v != '-'}
            
            return event if event.get('event') else None
            
        except Exception as e:
            logger.warning(f"Error parsing event row: {e}")
            return None
    
    def get_major_countries(self) -> Dict[str, str]:
        """Get list of major countries."""
        return self.MAJOR_COUNTRIES.copy()
    
    def get_importance_levels(self) -> Dict[str, int]:
        """Get importance level mappings."""
        return self.IMPORTANCE_LEVELS.copy()


async def fetch_calendar_events(
    countries: Optional[List[str]] = None,
    importance: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Async wrapper for fetching calendar events.
    
    Args:
        countries: List of country names
        importance: Importance level
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        category: Event category
        
    Returns:
        List of economic events
    """
    client = TradingEconomicsClient()
    
    # Run in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        client.get_calendar_events,
        countries,
        importance,
        start_date,
        end_date,
        category
    )


def get_today_events(countries: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Get today's economic events."""
    client = TradingEconomicsClient()
    today = datetime.now().strftime('%Y-%m-%d')
    return client.get_calendar_events(
        countries=countries,
        start_date=today,
        end_date=today
    )


def get_week_events(countries: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Get this week's economic events."""
    client = TradingEconomicsClient()
    today = datetime.now()
    week_end = today + timedelta(days=7)
    return client.get_calendar_events(
        countries=countries,
        start_date=today.strftime('%Y-%m-%d'),
        end_date=week_end.strftime('%Y-%m-%d')
    )
