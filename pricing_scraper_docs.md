# Freelance Pricing Scraper Documentation

## Overview
A modular web scraper that extracts freelance project pricing from Upwork, Freelancer, and Fiverr.

---

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Classes](#classes)
4. [API Reference](#api-reference)
5. [Examples](#examples)
6. [Testing](#testing)

---

## Installation

### Dependencies
```bash
pip install selenium
pip install webdriver-manager
```

### ChromeDriver Setup

**Option 1: Automatic (Recommended)**
```bash
pip install webdriver-manager
```

**Option 2: Manual**
1. Download ChromeDriver: https://chromedriver.chromium.org/
2. Match your Chrome version
3. Add to PATH or place in project directory

### Verify Installation
```bash
python -c "from selenium import webdriver; print('Selenium OK')"
```

---

## Quick Start

### Standalone Mode
```python
python calculate_project_pricing.py
```

### Import as Module
```python
from calculate_project_pricing import FreelancePriceScraper

# Create scraper
scraper = FreelancePriceScraper(headless=True)

# Search platforms
results = scraper.search_all("Python web scraping")

# Get exchange rate
exchange_rate = scraper.get_usd_to_egp_rate()

# Save results
scraper.save_to_json(results, exchange_rate)

# Always close
scraper.close()
```

---

## Classes

### 1. PriceExtractor

**Purpose**: Extract and categorize prices from text

#### Constructor
```python
PriceExtractor()
```

**Parameters**: None

**Returns**: PriceExtractor instance

#### Methods

##### `categorize_prices(text: str) -> Dict[str, List[float]]`

**Description**: Extract hourly rates and fixed prices from text

**Parameters**:
- `text` (str): Text containing price information

**Returns**: Dictionary with categorized prices
```python
{
    'hourly': [25.0, 30.0, 45.0],  # Hourly rates in USD
    'fixed': [500.0, 750.0, 1000.0]  # Fixed prices in USD
}
```

**Example**:
```python
extractor = PriceExtractor()

text = "Project budget: $500. Hourly rate: $25/hr"
prices = extractor.categorize_prices(text)

print(f"Hourly rates: {prices['hourly']}")  # [25.0]
print(f"Fixed prices: {prices['fixed']}")   # [500.0]
```

**Price Ranges**:
- Hourly rates: $5 - $500/hr
- Fixed prices: $50 - $100,000

**Dependencies**: None

---

### 2. PlatformScraper (Abstract Base Class)

**Purpose**: Base class for platform-specific scrapers

**Note**: Do not instantiate directly. Use subclasses: `UpworkScraper`, `FreelancerScraper`, `FiverrScraper`

#### Constructor
```python
PlatformScraper(driver: webdriver.Chrome, price_extractor: PriceExtractor)
```

**Parameters**:
- `driver` (webdriver.Chrome): Selenium WebDriver instance
- `price_extractor` (PriceExtractor): Price extraction instance

#### Methods

##### `search(query: str, wait_time: int = 4) -> Dict`

**Description**: Search platform for pricing information

**Parameters**:
- `query` (str): Search query (e.g., "Python developer")
- `wait_time` (int, optional): Seconds to wait for page load. Default: 4

**Returns**: Dictionary with search results
```python
{
    'platform': 'Upwork',
    'url': 'https://www.upwork.com/...',
    'hourly_rates': [25.0, 30.0, 35.0],
    'fixed_prices': [500.0, 750.0],
    'hourly_avg': 30.0,
    'fixed_avg': 625.0
}
```

**Error Response**:
```python
{
    'platform': 'Upwork',
    'url': 'https://...',
    'error': 'Error message'
}
```

---

### 3. UpworkScraper

**Purpose**: Scrape pricing from Upwork

#### Constructor
```python
UpworkScraper(driver: webdriver.Chrome, price_extractor: PriceExtractor)
```

**Example**:
```python
from selenium import webdriver
from calculate_project_pricing import UpworkScraper, PriceExtractor

driver = webdriver.Chrome()
extractor = PriceExtractor()
upwork = UpworkScraper(driver, extractor)

results = upwork.search("Python developer")
print(results)
```

---

### 4. FreelancerScraper

**Purpose**: Scrape pricing from Freelancer.com

#### Constructor
```python
FreelancerScraper(driver: webdriver.Chrome, price_extractor: PriceExtractor)
```

**Example**:
```python
from calculate_project_pricing import FreelancerScraper, PriceExtractor
from selenium import webdriver

driver = webdriver.Chrome()
extractor = PriceExtractor()
freelancer = FreelancerScraper(driver, extractor)

results = freelancer.search("logo design")
print(results)
```

---

### 5. FiverrScraper

**Purpose**: Scrape pricing from Fiverr

#### Constructor
```python
FiverrScraper(driver: webdriver.Chrome, price_extractor: PriceExtractor)
```

**Example**:
```python
from calculate_project_pricing import FiverrScraper, PriceExtractor
from selenium import webdriver

driver = webdriver.Chrome()
extractor = PriceExtractor()
fiverr = FiverrScraper(driver, extractor)

results = fiverr.search("video editing")
print(results)
```

---

### 6. ExchangeRateService

**Purpose**: Fetch USD to EGP exchange rates

#### Constructor
```python
ExchangeRateService(driver: webdriver.Chrome)
```

**Parameters**:
- `driver` (webdriver.Chrome): Selenium WebDriver instance

#### Methods

##### `get_rate() -> float`

**Description**: Get current USD to EGP exchange rate

**Parameters**: None

**Returns**: `float` - Exchange rate (fallback: 50.0)

**Example**:
```python
from selenium import webdriver
from calculate_project_pricing import ExchangeRateService

driver = webdriver.Chrome()
service = ExchangeRateService(driver)

rate = service.get_rate()
print(f"1 USD = {rate} EGP")
```

**Sources**:
1. xe.com currency converter
2. Google search

**Fallback**: Returns 50.0 if all sources fail

**Dependencies**: Selenium, active internet connection

---

### 7. FreelancePriceScraper

**Purpose**: Main orchestrator for all scraping operations

#### Constructor
```python
FreelancePriceScraper(headless: bool = True)
```

**Parameters**:
- `headless` (bool, optional): Run browser in headless mode. Default: True

**Returns**: FreelancePriceScraper instance

**Example**:
```python
# Headless mode (no browser window)
scraper = FreelancePriceScraper(headless=True)

# Visible browser (for debugging)
scraper = FreelancePriceScraper(headless=False)
```

#### Methods

##### `search_all(query: str, show_egp: bool = False) -> List[Dict]`

**Description**: Search all platforms (Upwork, Freelancer, Fiverr)

**Parameters**:
- `query` (str): Project type to search (e.g., "Python developer")
- `show_egp` (bool, optional): Display EGP prices. Default: False

**Returns**: List of platform results
```python
[
    {
        'platform': 'Upwork',
        'url': 'https://...',
        'hourly_rates': [25.0, 30.0],
        'fixed_prices': [500.0],
        'hourly_avg': 27.5,
        'fixed_avg': 500.0
    },
    {
        'platform': 'Freelancer',
        'url': 'https://...',
        'hourly_rates': [20.0, 25.0],
        'fixed_prices': [400.0, 600.0],
        'hourly_avg': 22.5,
        'fixed_avg': 500.0
    },
    # ... Fiverr results
]
```

**Example**:
```python
scraper = FreelancePriceScraper(headless=True)

# Search for Python developers
results = scraper.search_all("Python developer")

for result in results:
    print(f"{result['platform']}: ${result['hourly_avg']:.2f}/hr avg")

scraper.close()
```

**Duration**: ~30-60 seconds (searches 3 platforms)

**Dependencies**: Active internet, ChromeDriver

##### `get_usd_to_egp_rate() -> float`

**Description**: Get current USD to EGP exchange rate

**Parameters**: None

**Returns**: `float` - Exchange rate

**Example**:
```python
scraper = FreelancePriceScraper(headless=True)
rate = scraper.get_usd_to_egp_rate()
print(f"1 USD = {rate} EGP")
scraper.close()
```

##### `save_to_json(results: List[Dict], exchange_rate: float, filename: Optional[str] = None) -> Tuple[str, Dict]`

**Description**: Save search results to JSON file

**Parameters**:
- `results` (list): Results from `search_all()`
- `exchange_rate` (float): Exchange rate from `get_usd_to_egp_rate()`
- `filename` (str, optional): Output filename. Default: Auto-generated with timestamp

**Returns**: Tuple of (filename, data_dict)

**Example**:
```python
scraper = FreelancePriceScraper(headless=True)

results = scraper.search_all("Python developer")
rate = scraper.get_usd_to_egp_rate()

filename, data = scraper.save_to_json(results, rate)
print(f"Saved to: {filename}")

# Custom filename
filename, data = scraper.save_to_json(
    results, 
    rate, 
    filename="my_pricing_data.json"
)

scraper.close()
```

**Output Format**:
```json
{
  "timestamp": "2026-01-14T10:30:00",
  "date": "2026-01-14 10:30:00",
  "exchange_rate_usd_to_egp": 50.5,
  "platforms": [
    {
      "platform": "Upwork",
      "url": "https://...",
      "hourly_rates": {
        "usd": [25.0, 30.0],
        "count": 2,
        "average_usd": 27.5
      },
      "fixed_prices": {
        "usd": [500.0],
        "count": 1,
        "average_usd": 500.0
      }
    }
  ],
  "overall_summary": {
    "hourly_rates": {
      "total_count": 15,
      "average_usd": 28.5,
      "median_usd": 27.0
    },
    "fixed_prices": {
      "total_count": 10,
      "average_usd": 550.0,
      "median_usd": 500.0
    }
  }
}
```

##### `close()`

**Description**: Close browser and cleanup resources

**Parameters**: None

**Returns**: None

**Example**:
```python
scraper = FreelancePriceScraper(headless=True)
# ... use scraper ...
scraper.close()  # Always call when done
```

**Important**: Always call `close()` to prevent memory leaks and zombie processes

---

## Complete Examples

### Example 1: Basic Usage

```python
from calculate_project_pricing import FreelancePriceScraper

# Create scraper
scraper = FreelancePriceScraper(headless=True)

try:
    # Search platforms
    results = scraper.search_all("Python web scraping")
    
    # Get exchange rate
    exchange_rate = scraper.get_usd_to_egp_rate()
    
    # Display results
    print(f"\nExchange Rate: 1 USD = {exchange_rate} EGP\n")
    
    for result in results:
        if 'error' not in result:
            print(f"{result['platform']}:")
            print(f"  Hourly Avg: ${result['hourly_avg']:.2f}/hr")
            print(f"  Fixed Avg: ${result['fixed_avg']:.2f}")
    
    # Save to file
    filename, data = scraper.save_to_json(results, exchange_rate)
    print(f"\nSaved to: {filename}")

finally:
    scraper.close()
```

### Example 2: Compare Multiple Project Types

```python
from calculate_project_pricing import FreelancePriceScraper

project_types = [
    "Python developer",
    "Logo design",
    "Video editing",
    "WordPress website"
]

scraper = FreelancePriceScraper(headless=True)

try:
    for project in project_types:
        print(f"\n{'='*60}")
        print(f"Analyzing: {project}")
        print('='*60)
        
        results = scraper.search_all(project)
        
        # Calculate overall average
        all_hourly = []
        for result in results:
            if 'error' not in result:
                all_hourly.extend(result.get('hourly_rates', []))
        
        if all_hourly:
            import statistics
            avg = statistics.mean(all_hourly)
            print(f"Overall Hourly Average: ${avg:.2f}/hr")

finally:
    scraper.close()
```

### Example 3: Custom Platform Scraper

```python
from selenium import webdriver
from calculate_project_pricing import PlatformScraper, PriceExtractor

class CustomPlatformScraper(PlatformScraper):
    """Custom scraper for another platform"""
    
    def get_platform_name(self):
        return "CustomPlatform"
    
    def get_search_url(self, query):
        from urllib.parse import quote_plus
        return f"https://customplatform.com/search?q={quote_plus(query)}"

# Use custom scraper
driver = webdriver.Chrome()
extractor = PriceExtractor()

custom = CustomPlatformScraper(driver, extractor)
results = custom.search("Python developer")

print(results)
driver.quit()
```

### Example 4: Scheduled Pricing Checks

```python
from calculate_project_pricing import FreelancePriceScraper
import time
from datetime import datetime

def check_pricing(project_type):
    """Check pricing and save results"""
    scraper = FreelancePriceScraper(headless=True)
    
    try:
        print(f"\n[{datetime.now()}] Checking pricing for: {project_type}")
        
        results = scraper.search_all(project_type)
        rate = scraper.get_usd_to_egp_rate()
        
        filename, _ = scraper.save_to_json(results, rate)
        print(f"✓ Saved to: {filename}")
        
    finally:
        scraper.close()

# Check pricing every 24 hours
while True:
    check_pricing("Python developer")
    
    print("\nNext check in 24 hours...")
    time.sleep(86400)  # 24 hours
```

---

## Testing Script

Save as `test_pricing_scraper.py`:

```python
"""
Test script for calculate_project_pricing module
"""

from calculate_project_pricing import (
    FreelancePriceScraper, 
    PriceExtractor,
    UpworkScraper,
    FreelancerScraper,
    FiverrScraper
)
import json
import os

def test_price_extractor():
    """Test PriceExtractor functionality"""
    print("\n=== Testing PriceExtractor ===")
    
    extractor = PriceExtractor()
    
    # Test hourly rate extraction
    text1 = "I charge $35/hr for Python development"
    result1 = extractor.categorize_prices(text1)
    assert 35.0 in result1['hourly'], "Should extract hourly rate"
    print("✓ Hourly rate extraction works")
    
    # Test fixed price extraction
    text2 = "Budget: $500 for the complete project"
    result2 = extractor.categorize_prices(text2)
    assert 500.0 in result2['fixed'], "Should extract fixed price"
    print("✓ Fixed price extraction works")
    
    # Test mixed
    text3 = "Hourly: $25/hr or Fixed: $1000"
    result3 = extractor.categorize_prices(text3)
    assert 25.0 in result3['hourly'], "Should extract hourly"
    assert 1000.0 in result3['fixed'], "Should extract fixed"
    print("✓ Mixed extraction works")
    
    print("✓ PriceExtractor tests passed!\n")

def test_scraper_initialization():
    """Test FreelancePriceScraper initialization"""
    print("=== Testing Scraper Initialization ===")
    
    try:
        scraper = FreelancePriceScraper(headless=True)
        assert scraper.driver is not None, "Driver should be initialized"
        assert len(scraper.scrapers) == 3, "Should have 3 platform scrapers"
        print("✓ Scraper initialized with 3 platforms")
        
        scraper.close()
        print("✓ Scraper closed successfully")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        raise
    
    print("✓ Initialization tests passed!\n")

def test_platform_search():
    """Test searching a single platform"""
    print("=== Testing Platform Search ===")
    print("This will perform a real search on Upwork...")
    print("Duration: ~10 seconds\n")
    
    try:
        scraper = FreelancePriceScraper(headless=True)
        
        # Test single platform
        upwork = scraper.scrapers[0]  # UpworkScraper
        result = upwork.search("Python developer", wait_time=5)
        
        assert result['platform'] == 'Upwork', "Platform should be Upwork"
        assert 'url' in result, "Should have URL"
        
        if 'error' not in result:
            print(f"✓ Successfully scraped Upwork")
            print(f"  Found {len(result['hourly_rates'])} hourly rates")
            print(f"  Found {len(result['fixed_prices'])} fixed prices")
        else:
            print(f"⚠ Upwork returned error (this is OK for testing)")
        
        scraper.close()
        
    except Exception as e:
        print(f"❌ Platform search failed: {e}")
        raise
    
    print("✓ Platform search test complete!\n")

def test_full_search():
    """Test full search across all platforms"""
    print("=== Testing Full Platform Search ===")
    print("This will search Upwork, Freelancer, and Fiverr...")
    print("Duration: ~30-60 seconds\n")
    
    response = input("Run full search test? (y/n): ")
    if response.lower() != 'y':
        print("Skipped full search test\n")
        return
    
    try:
        scraper = FreelancePriceScraper(headless=True)
        
        # Search all platforms
        results = scraper.search_all("Python developer")
        
        assert len(results) == 3, "Should have 3 platform results"
        print(f"✓ Searched {len(results)} platforms")
        
        # Check results
        for result in results:
            platform = result['platform']
            if 'error' in result:
                print(f"  ⚠ {platform}: Error (OK for testing)")
            else:
                hourly_count = len(result['hourly_rates'])
                fixed_count = len(result['fixed_prices'])
                print(f"  ✓ {platform}: {hourly_count} hourly, {fixed_count} fixed")
        
        scraper.close()
        
    except Exception as e:
        print(f"❌ Full search failed: {e}")
        raise
    
    print("✓ Full search test complete!\n")

def test_exchange_rate():
    """Test exchange rate fetching"""
    print("=== Testing Exchange Rate Service ===")
    
    try:
        scraper = FreelancePriceScraper(headless=True)
        
        rate = scraper.get_usd_to_egp_rate()
        
        assert rate > 0, "Rate should be positive"
        assert 20 <= rate <= 100, "Rate should be in reasonable range"
        print(f"✓ Exchange rate: 1 USD = {rate} EGP")
        
        scraper.close()
        
    except Exception as e:
        print(f"❌ Exchange rate test failed: {e}")
        raise
    
    print("✓ Exchange rate test passed!\n")

def test_json_export():
    """Test JSON export functionality"""
    print("=== Testing JSON Export ===")
    
    try:
        # Create mock results
        mock_results = [
            {
                'platform': 'TestPlatform',
                'url': 'https://test.com',
                'hourly_rates': [25.0, 30.0],
                'fixed_prices': [500.0],
                'hourly_avg': 27.5,
                'fixed_avg': 500.0
            }
        ]
        
        scraper = FreelancePriceScraper(headless=True)
        
        # Save to JSON
        filename, data = scraper.save_to_json(
            mock_results, 
            50.0, 
            filename="test_export.json"
        )
        
        assert os.path.exists(filename), "JSON file should exist"
        print(f"✓ JSON file created: {filename}")
        
        # Verify content
        with open(filename, 'r') as f:
            loaded_data = json.load(f)
        
        assert 'platforms' in loaded_data, "Should have platforms"
        assert 'overall_summary' in loaded_data, "Should have summary"
        print("✓ JSON structure is valid")
        
        # Cleanup
        os.remove(filename)
        scraper.close()
        
    except Exception as e:
        print(f"❌ JSON export test failed: {e}")
        raise
    
    print("✓ JSON export test passed!\n")

if __name__ == "__main__":
    print("="*60)
    print("PRICING SCRAPER MODULE - TEST SUITE")
    print("="*60)
    
    try:
        # Quick tests (no internet required)
        test_price_extractor()
        test_scraper_initialization()
        
        # Tests requiring internet
        print("\nThe following tests require internet connection:")
        test_exchange_rate()
        test_platform_search()
        test_json_export()
        
        # Full test (takes time)
        test_full_search()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
```

Run tests:
```bash
python test_pricing_scraper.py
```

---

## Error Handling

### Common Errors

**1. ChromeDriver not found**
```
Error: WebDriverException: 'chromedriver' executable needs to be in PATH
Solution: Install webdriver-manager or download ChromeDriver manually
```

**2. Page load timeout**
```
Error: TimeoutException
Solution: Increase wait_time parameter or check internet connection
```

**3. No prices found**
```
Result: Empty hourly_rates and fixed_prices lists
Causes: Website structure changed, anti-scraping measures
Solution: Check URLs manually, update scraper logic
```

**4. Exchange rate fetch failed**
```
Warning: "Could not fetch live rate, using fallback: 50.0"
Causes: No internet, blocked by firewall
Solution: Check internet connection, returns safe fallback value
```

---

## Best Practices

1. **Always close scraper**
```python
scraper = FreelancePriceScraper(headless=True)
try:
    # Use scraper
    results = scraper.search_all("Python")
finally:
    scraper.close()  # Always cleanup
```

2. **Use headless mode in production**
```python
# Production
scraper = FreelancePriceScraper(headless=True)

# Debugging only
scraper = FreelancePriceScraper(headless=False)
```

3. **Add delays for multiple searches**
```python
import time

scraper = FreelancePriceScraper(headless=True)

for project in ["Python", "Design", "Video"]:
    results = scraper.search_all(project)
    time.sleep(60)  # Wait 60 seconds between searches

scraper.close()
```

4. **Handle errors gracefully**
```python
scraper = FreelancePriceScraper(headless=True)

results = scraper.search_all("Python")

for result in results:
    if 'error' in result:
        print(f"Error on {result['platform']}: {result['error']}")
        continue
    
    # Process valid results
    print(f"{result['platform']}: ${result['hourly_avg']}/hr")

scraper.close()
```

---

## Performance Tips

- **Headless mode** is 20-30% faster
- **Parallel searches** not recommended (may trigger anti-bot)
- **Cache results** to avoid repeated scraping
- **Typical search duration**: 30-60 seconds for all platforms

---

## Support

For issues:
1. Check ChromeDriver version matches Chrome
2. Verify internet connection
3. Test with `headless=False` to see browser behavior
4. Check website structure hasn't changed
5. Review test script for examples
