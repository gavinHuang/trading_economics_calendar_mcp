# Trading Economics Calendar MCP Server

A Model Context Protocol (MCP) server that provides access to economic calendar events from Trading Economics. This server allows you to fetch economic events with various filters including countries, importance levels, and date ranges.

## Features

- 📅 Fetch economic calendar events
- 🌍 Filter by major countries
- 📊 Filter by importance level (low, medium, high)
- 📆 Date range filtering
- 🔍 High-impact events filtering
- 🏛️ Country-specific event queries

## Installation

### From PyPI (when published)
```bash
pip install trading-economics-calendar-mcp
```

### From Source
```bash
git clone <repository-url>
cd trading-economics-calendar-mcp
pip install -e .
```

## Usage

### As MCP Server

Start the server:
```bash
trading-economics-mcp
```

### Available Tools

#### 1. Get Economic Events
```python
get_economic_events(
    countries=["United States", "Germany"],
    importance="high",
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

#### 2. Get Today's Events
```python
get_today_economic_events(
    countries=["United States"],
    importance="medium"
)
```

#### 3. Get This Week's Events
```python
get_week_economic_events(
    countries=["Japan", "United Kingdom"],
    importance="high"
)
```

#### 4. Get Major Countries
```python
get_major_countries()
# Returns: {"united_states": "United States", "germany": "Germany", ...}
```

#### 5. Get Importance Levels
```python
get_importance_levels()
# Returns: {"low": 1, "medium": 2, "high": 3}
```

#### 6. Get High-Impact Events
```python
get_high_impact_events(
    countries=["United States", "China"],
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

#### 7. Get Events by Country
```python
get_events_by_country(
    country="United States",
    start_date="2024-01-01",
    end_date="2024-01-07",
    importance="high"
)
```

## Supported Countries

The server supports filtering by major economies:
- United States
- China
- Japan
- Germany
- United Kingdom
- France
- Italy
- Canada
- Australia
- Brazil
- India
- Russia
- South Korea
- Spain
- Mexico
- Netherlands
- Switzerland
- Belgium
- Sweden
- Austria

## Response Format

Each economic event returns the following structure:
```json
{
    "date": "2024-01-15",
    "time": "08:30",
    "country": "United States",
    "event": "Retail Sales",
    "importance": 3,
    "actual": "0.6%",
    "forecast": "0.4%",
    "previous": "0.3%"
}
```

## Configuration

The server uses the following default settings:
- Base URL: `https://tradingeconomics.com`
- Request timeout: 30 seconds
- User agent: Modern browser string

## Error Handling

The server includes comprehensive error handling:
- Network timeouts
- Invalid response parsing
- Missing data fields
- Rate limiting (when applicable)

## Development

### Setup Development Environment
```bash
git clone <repository-url>
cd trading-economics-calendar-mcp
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
```

### Code Formatting
```bash
black trading_economics_calendar/
flake8 trading_economics_calendar/
mypy trading_economics_calendar/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This tool fetches publicly available data from Trading Economics. Please respect their terms of service and rate limits. This tool is for educational and research purposes.
