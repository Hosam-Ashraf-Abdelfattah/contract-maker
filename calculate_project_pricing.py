# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.chrome.options import Options
# # import re
# # import statistics
# # from urllib.parse import quote_plus
# # import time

# # class FreelancePriceScraper:
# #     def __init__(self, headless=True):
# #         """Initialize the scraper with Selenium WebDriver"""
# #         chrome_options = Options()
# #         if headless:
# #             chrome_options.add_argument("--headless")
# #         chrome_options.add_argument("--no-sandbox")
# #         chrome_options.add_argument("--disable-dev-shm-usage")
# #         chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# #         chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
# #         try:
# #             self.driver = webdriver.Chrome(options=chrome_options)
# #             self.wait = WebDriverWait(self.driver, 10)
# #         except Exception as e:
# #             print(f"Error initializing Chrome driver: {e}")
# #             print("\nPlease install ChromeDriver:")
# #             print("1. Download from: https://chromedriver.chromium.org/")
# #             print("2. Or install via: pip install webdriver-manager")
# #             raise
    
# #     def categorize_prices(self, text):
# #         """Categorize prices as hourly rates or fixed project prices"""
# #         hourly_rates = []
# #         fixed_prices = []
        
# #         # Pattern for hourly rates
# #         hourly_patterns = [
# #             r'\$\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:/hr|per hour|hourly|/hour)',
# #             r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:USD|$)\s*(?:/hr|per hour|hourly|/hour)',
# #         ]
        
# #         # Pattern for fixed prices
# #         fixed_patterns = [
# #             r'(?:Fixed|Budget|Price):\s*\$\s*([0-9,]+(?:\.[0-9]{2})?)',
# #             r'\$\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:Fixed|Total|Budget)',
# #         ]
        
# #         # Extract hourly rates
# #         for pattern in hourly_patterns:
# #             matches = re.findall(pattern, text, re.IGNORECASE)
# #             for match in matches:
# #                 try:
# #                     price = float(match.replace(',', ''))
# #                     if 5 <= price <= 500:  # Reasonable hourly rate range
# #                         hourly_rates.append(price)
# #                 except ValueError:
# #                     continue
        
# #         # Extract fixed prices
# #         for pattern in fixed_patterns:
# #             matches = re.findall(pattern, text, re.IGNORECASE)
# #             for match in matches:
# #                 try:
# #                     price = float(match.replace(',', ''))
# #                     if 50 <= price <= 100000:  # Reasonable fixed price range
# #                         fixed_prices.append(price)
# #                 except ValueError:
# #                     continue
        
# #         # If not categorized, try to guess based on context and value
# #         if not hourly_rates and not fixed_prices:
# #             general_pattern = r'\$\s*([0-9,]+(?:\.[0-9]{2})?)'
# #             matches = re.findall(general_pattern, text)
            
# #             for match in matches:
# #                 try:
# #                     price = float(match.replace(',', ''))
# #                     # Heuristic: prices under 200 are likely hourly, above are likely fixed
# #                     if 5 <= price <= 200:
# #                         # Check context for hourly indicators
# #                         match_pos = text.find(f'${match}')
# #                         context = text[max(0, match_pos-50):min(len(text), match_pos+50)].lower()
# #                         if any(word in context for word in ['hour', 'hr', '/hr', 'hourly']):
# #                             hourly_rates.append(price)
# #                         elif price <= 100:  # Small amounts likely hourly
# #                             hourly_rates.append(price)
# #                         else:
# #                             fixed_prices.append(price)
# #                     elif 200 < price <= 100000:
# #                         fixed_prices.append(price)
# #                 except ValueError:
# #                     continue
        
# #         return {
# #             'hourly': list(set(hourly_rates)),
# #             'fixed': list(set(fixed_prices))
# #         }
    
# #     def search_upwork(self, title):
# #         """Search Upwork for projects"""
# #         url = f"https://www.upwork.com/nx/search/jobs/?q={quote_plus(title)}"
# #         print(f"  Accessing: {url}")
        
# #         try:
# #             self.driver.get(url)
# #             time.sleep(4)  # Wait for dynamic content to load
            
# #             page_text = self.driver.page_source
            
# #             # Get all text elements that might contain prices
# #             price_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '$')]")
# #             all_text = " ".join([elem.text for elem in price_elements[:50]])
# #             all_text += " " + page_text
            
# #             categorized = self.categorize_prices(all_text)
            
# #             return {
# #                 'platform': 'Upwork',
# #                 'url': url,
# #                 'hourly_rates': sorted(categorized['hourly'])[:15],
# #                 'fixed_prices': sorted(categorized['fixed'])[:15],
# #                 'hourly_avg': statistics.mean(categorized['hourly']) if categorized['hourly'] else 0,
# #                 'fixed_avg': statistics.mean(categorized['fixed']) if categorized['fixed'] else 0,
# #             }
# #         except Exception as e:
# #             print(f"  Error: {e}")
# #             return {'platform': 'Upwork', 'url': url, 'error': str(e)}
    
# #     def search_freelancer(self, title):
# #         """Search Freelancer.com for projects"""
# #         url = f"https://www.freelancer.com/jobs/?keyword={quote_plus(title)}"
# #         print(f"  Accessing: {url}")
        
# #         try:
# #             self.driver.get(url)
# #             time.sleep(4)
            
# #             page_text = self.driver.page_source
# #             price_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'USD') or contains(text(), '$')]")
# #             all_text = " ".join([elem.text for elem in price_elements[:50]])
# #             all_text += " " + page_text
            
# #             categorized = self.categorize_prices(all_text)
            
# #             return {
# #                 'platform': 'Freelancer',
# #                 'url': url,
# #                 'hourly_rates': sorted(categorized['hourly'])[:15],
# #                 'fixed_prices': sorted(categorized['fixed'])[:15],
# #                 'hourly_avg': statistics.mean(categorized['hourly']) if categorized['hourly'] else 0,
# #                 'fixed_avg': statistics.mean(categorized['fixed']) if categorized['fixed'] else 0,
# #             }
# #         except Exception as e:
# #             print(f"  Error: {e}")
# #             return {'platform': 'Freelancer', 'url': url, 'error': str(e)}
    
# #     def search_fiverr(self, title):
# #         """Search Fiverr for gigs (usually fixed price)"""
# #         url = f"https://www.fiverr.com/search/gigs?query={quote_plus(title)}"
# #         print(f"  Accessing: {url}")
        
# #         try:
# #             self.driver.get(url)
# #             time.sleep(4)
            
# #             page_text = self.driver.page_source
# #             price_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'price') or contains(text(), '$')]")
# #             all_text = " ".join([elem.text for elem in price_elements[:50]])
# #             all_text += " " + page_text
            
# #             categorized = self.categorize_prices(all_text)
            
# #             # Fiverr is mostly fixed-price gigs
# #             return {
# #                 'platform': 'Fiverr',
# #                 'url': url,
# #                 'hourly_rates': sorted(categorized['hourly'])[:15],
# #                 'fixed_prices': sorted(categorized['fixed'])[:15],
# #                 'hourly_avg': statistics.mean(categorized['hourly']) if categorized['hourly'] else 0,
# #                 'fixed_avg': statistics.mean(categorized['fixed']) if categorized['fixed'] else 0,
# #             }
# #         except Exception as e:
# #             print(f"  Error: {e}")
# #             return {'platform': 'Fiverr', 'url': url, 'error': str(e)}
    
# #     def search_all(self, title, show_egp=True):
# #         """Search all platforms"""
# #         print(f"\n{'='*80}")
# #         print(f"Searching for: '{title}'")
# #         print(f"{'='*80}\n")
        
# #         results = []
        
# #         print("Searching Upwork...")
# #         results.append(self.search_upwork(title))
# #         time.sleep(2)
        
# #         print("\nSearching Freelancer...")
# #         results.append(self.search_freelancer(title))
# #         time.sleep(2)
        
# #         print("\nSearching Fiverr...")
# #         results.append(self.search_fiverr(title))
        
# #         # Get exchange rate if needed
# #         exchange_rate = None
# #         if show_egp:
# #             print("\nFetching USD to EGP exchange rate...")
# #             exchange_rate = self.get_usd_to_egp_rate()
        
# #         # Display results with or without EGP
# #         if show_egp and exchange_rate:
# #             self.display_results_with_egp(results, exchange_rate)
# #         else:
# #             # Display results (USD only)
# #             print(f"\n{'='*80}")
# #             print("RESULTS - SEPARATED BY PRICING TYPE")
# #             print(f"{'='*80}\n")
            
# #             for result in results:
# #                 print(f"{result['platform']}:")
# #                 print(f"  URL: {result['url']}")
                
# #                 if 'error' in result:
# #                     print(f"  Status: Error occurred")
# #                 else:
# #                     # Hourly rates
# #                     if result.get('hourly_rates'):
# #                         print(f"\n  HOURLY RATES:")
# #                         print(f"    Count: {len(result['hourly_rates'])}")
# #                         print(f"    Average: ${result['hourly_avg']:.2f}/hr")
# #                         print(f"    Range: ${min(result['hourly_rates']):.2f} - ${max(result['hourly_rates']):.2f}/hr")
# #                         print(f"    Samples: {[f'${p:.2f}/hr' for p in result['hourly_rates'][:8]]}")
# #                     else:
# #                         print(f"\n  HOURLY RATES: None detected")
                    
# #                     # Fixed prices
# #                     if result.get('fixed_prices'):
# #                         print(f"\n  FIXED PRICES:")
# #                         print(f"    Count: {len(result['fixed_prices'])}")
# #                         print(f"    Average: ${result['fixed_avg']:.2f}")
# #                         print(f"    Range: ${min(result['fixed_prices']):.2f} - ${max(result['fixed_prices']):.2f}")
# #                         print(f"    Samples: {[f'${p:.2f}' for p in result['fixed_prices'][:8]]}")
# #                     else:
# #                         print(f"\n  FIXED PRICES: None detected")
# #                 print()
            
# #             # Overall summary
# #             all_hourly = []
# #             all_fixed = []
# #             for result in results:
# #                 if 'error' not in result:
# #                     all_hourly.extend(result.get('hourly_rates', []))
# #                     all_fixed.extend(result.get('fixed_prices', []))
            
# #             print(f"{'='*80}")
# #             print("OVERALL SUMMARY")
# #             print(f"{'='*80}")
            
# #             if all_hourly:
# #                 print(f"\nHOURLY RATES ACROSS ALL PLATFORMS:")
# #                 print(f"  Total Found: {len(all_hourly)}")
# #                 print(f"  Average: ${statistics.mean(all_hourly):.2f}/hr")
# #                 print(f"  Median: ${statistics.median(all_hourly):.2f}/hr")
# #                 print(f"  Range: ${min(all_hourly):.2f} - ${max(all_hourly):.2f}/hr")
# #             else:
# #                 print(f"\nHOURLY RATES: None detected")
            
# #             if all_fixed:
# #                 print(f"\nFIXED PRICES ACROSS ALL PLATFORMS:")
# #                 print(f"  Total Found: {len(all_fixed)}")
# #                 print(f"  Average: ${statistics.mean(all_fixed):.2f}")
# #                 print(f"  Median: ${statistics.median(all_fixed):.2f}")
# #                 print(f"  Range: ${min(all_fixed):.2f} - ${max(all_fixed):.2f}")
# #             else:
# #                 print(f"\nFIXED PRICES: None detected")
            
# #             if not all_hourly and not all_fixed:
# #                 print("\nNo prices were detected. This may be due to:")
# #                 print("  - Website structure changes")
# #                 print("  - Anti-scraping measures")
# #                 print("  - No matching projects found")
# #                 print("\nTip: Visit the URLs manually or try different search terms.")
            
# #             print(f"{'='*80}\n")
        
# #         return results
    
# #     def get_usd_to_egp_rate(self):
# #         """Get current USD to EGP exchange rate"""
# #         try:
# #             # Try multiple sources for exchange rate
# #             sources = [
# #                 "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EGP",
# #                 "https://www.google.com/search?q=usd+to+egp",
# #             ]
            
# #             for url in sources:
# #                 try:
# #                     self.driver.get(url)
# #                     time.sleep(2)
                    
# #                     page_text = self.driver.page_source
                    
# #                     # Look for exchange rate patterns
# #                     patterns = [
# #                         r'1\s*USD\s*=\s*([0-9,.]+)\s*EGP',
# #                         r'([0-9,.]+)\s*Egyptian Pound',
# #                         r'([0-9,.]+)\s*EGP',
# #                     ]
                    
# #                     for pattern in patterns:
# #                         matches = re.findall(pattern, page_text, re.IGNORECASE)
# #                         for match in matches:
# #                             try:
# #                                 rate = float(match.replace(',', ''))
# #                                 if 20 <= rate <= 100:  # Reasonable range for USD to EGP
# #                                     print(f"  ✓ Exchange rate found: 1 USD = {rate:.2f} EGP")
# #                                     return rate
# #                             except ValueError:
# #                                 continue
# #                 except:
# #                     continue
            
# #             # Fallback: Use approximate rate if scraping fails
# #             print("  ⚠ Could not fetch live rate, using approximate rate")
# #             return 50.0  # Approximate rate as fallback
            
# #         except Exception as e:
# #             print(f"  Error getting exchange rate: {e}")
# #             return 50.0  # Default fallback rate
    
# #     def convert_usd_to_egp(self, usd_amount, exchange_rate):
# #         """Convert USD amount to EGP"""
# #         return usd_amount * exchange_rate
    
# #     def display_results_with_egp(self, results, exchange_rate):
# #         """Display results with EGP conversion"""
# #         print(f"\n{'='*80}")
# #         print(f"RESULTS WITH EGP CONVERSION (1 USD = {exchange_rate:.2f} EGP)")
# #         print(f"{'='*80}\n")
        
# #         for result in results:
# #             print(f"{result['platform']}:")
# #             print(f"  URL: {result['url']}")
            
# #             if 'error' in result:
# #                 print(f"  Status: Error occurred")
# #             else:
# #                 # Hourly rates with EGP
# #                 if result.get('hourly_rates'):
# #                     print(f"\n  HOURLY RATES:")
# #                     print(f"    Count: {len(result['hourly_rates'])}")
# #                     print(f"    Average: ${result['hourly_avg']:.2f}/hr (EGP {self.convert_usd_to_egp(result['hourly_avg'], exchange_rate):.2f}/hr)")
# #                     min_hourly = min(result['hourly_rates'])
# #                     max_hourly = max(result['hourly_rates'])
# #                     print(f"    Range: ${min_hourly:.2f} - ${max_hourly:.2f}/hr")
# #                     print(f"           (EGP {self.convert_usd_to_egp(min_hourly, exchange_rate):.2f} - {self.convert_usd_to_egp(max_hourly, exchange_rate):.2f}/hr)")
# #                     print(f"    USD Samples: {[f'${p:.2f}/hr' for p in result['hourly_rates'][:5]]}")
# #                     print(f"    EGP Samples: {[f'EGP {self.convert_usd_to_egp(p, exchange_rate):.2f}/hr' for p in result['hourly_rates'][:5]]}")
# #                 else:
# #                     print(f"\n  HOURLY RATES: None detected")
                
# #                 # Fixed prices with EGP
# #                 if result.get('fixed_prices'):
# #                     print(f"\n  FIXED PRICES:")
# #                     print(f"    Count: {len(result['fixed_prices'])}")
# #                     print(f"    Average: ${result['fixed_avg']:.2f} (EGP {self.convert_usd_to_egp(result['fixed_avg'], exchange_rate):.2f})")
# #                     min_fixed = min(result['fixed_prices'])
# #                     max_fixed = max(result['fixed_prices'])
# #                     print(f"    Range: ${min_fixed:.2f} - ${max_fixed:.2f}")
# #                     print(f"           (EGP {self.convert_usd_to_egp(min_fixed, exchange_rate):.2f} - {self.convert_usd_to_egp(max_fixed, exchange_rate):.2f})")
# #                     print(f"    USD Samples: {[f'${p:.2f}' for p in result['fixed_prices'][:5]]}")
# #                     print(f"    EGP Samples: {[f'EGP {self.convert_usd_to_egp(p, exchange_rate):.2f}' for p in result['fixed_prices'][:5]]}")
# #                 else:
# #                     print(f"\n  FIXED PRICES: None detected")
# #             print()
        
# #         # Overall summary with EGP
# #         all_hourly = []
# #         all_fixed = []
# #         for result in results:
# #             if 'error' not in result:
# #                 all_hourly.extend(result.get('hourly_rates', []))
# #                 all_fixed.extend(result.get('fixed_prices', []))
        
# #         print(f"{'='*80}")
# #         print("OVERALL SUMMARY (USD & EGP)")
# #         print(f"{'='*80}")
        
# #         if all_hourly:
# #             avg_hourly = statistics.mean(all_hourly)
# #             med_hourly = statistics.median(all_hourly)
# #             min_hourly = min(all_hourly)
# #             max_hourly = max(all_hourly)
            
# #             print(f"\nHOURLY RATES ACROSS ALL PLATFORMS:")
# #             print(f"  Total Found: {len(all_hourly)}")
# #             print(f"  Average: ${avg_hourly:.2f}/hr (EGP {self.convert_usd_to_egp(avg_hourly, exchange_rate):.2f}/hr)")
# #             print(f"  Median: ${med_hourly:.2f}/hr (EGP {self.convert_usd_to_egp(med_hourly, exchange_rate):.2f}/hr)")
# #             print(f"  Range: ${min_hourly:.2f} - ${max_hourly:.2f}/hr")
# #             print(f"         (EGP {self.convert_usd_to_egp(min_hourly, exchange_rate):.2f} - {self.convert_usd_to_egp(max_hourly, exchange_rate):.2f}/hr)")
# #         else:
# #             print(f"\nHOURLY RATES: None detected")
        
# #         if all_fixed:
# #             avg_fixed = statistics.mean(all_fixed)
# #             med_fixed = statistics.median(all_fixed)
# #             min_fixed = min(all_fixed)
# #             max_fixed = max(all_fixed)
            
# #             print(f"\nFIXED PRICES ACROSS ALL PLATFORMS:")
# #             print(f"  Total Found: {len(all_fixed)}")
# #             print(f"  Average: ${avg_fixed:.2f} (EGP {self.convert_usd_to_egp(avg_fixed, exchange_rate):.2f})")
# #             print(f"  Median: ${med_fixed:.2f} (EGP {self.convert_usd_to_egp(med_fixed, exchange_rate):.2f})")
# #             print(f"  Range: ${min_fixed:.2f} - ${max_fixed:.2f}")
# #             print(f"         (EGP {self.convert_usd_to_egp(min_fixed, exchange_rate):.2f} - {self.convert_usd_to_egp(max_fixed, exchange_rate):.2f})")
# #         else:
# #             print(f"\nFIXED PRICES: None detected")
        
# #         print(f"{'='*80}\n")
    
# #     def close(self):
# #         """Close the browser"""
# #         if hasattr(self, 'driver'):
# #             self.driver.quit()


# # # Example usage
# # if __name__ == "__main__":
# #     scraper = None
# #     try:
# #         # Initialize scraper (set headless=False to see the browser)
# #         scraper = FreelancePriceScraper(headless=True)
        
# #         # Search with EGP conversion (default)
# #         scraper.search_all("Python web scraping", show_egp=True)
        
# #         # Search without EGP conversion
# #         # scraper.search_all("logo design", show_egp=False)
        
# #         # Try other searches:
# #         # scraper.search_all("WordPress website", show_egp=True)
# #         # scraper.search_all("mobile app development", show_egp=True)
        
# #     except Exception as e:
# #         print(f"\nFatal error: {e}")
# #     finally:
# #         if scraper:
# #             scraper.close()
# #             print("Browser closed.")


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import re
# import statistics
# from urllib.parse import quote_plus
# import time
# import json
# from datetime import datetime
# import pandas as pd
# import os

# class FreelancePriceScraper:
#     def __init__(self, headless=True):
#         """Initialize the scraper with Selenium WebDriver"""
#         chrome_options = Options()
#         if headless:
#             chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#         chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
#         try:
#             self.driver = webdriver.Chrome(options=chrome_options)
#             self.wait = WebDriverWait(self.driver, 10)
#         except Exception as e:
#             print(f"Error initializing Chrome driver: {e}")
#             print("\nPlease install ChromeDriver:")
#             print("1. Download from: https://chromedriver.chromium.org/")
#             print("2. Or install via: pip install webdriver-manager")
#             raise
    
#     def categorize_prices(self, text):
#         """Categorize prices as hourly rates or fixed project prices"""
#         hourly_rates = []
#         fixed_prices = []
        
#         # Pattern for hourly rates
#         hourly_patterns = [
#             r'\$\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:/hr|per hour|hourly|/hour)',
#             r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:USD|$)\s*(?:/hr|per hour|hourly|/hour)',
#         ]
        
#         # Pattern for fixed prices
#         fixed_patterns = [
#             r'(?:Fixed|Budget|Price):\s*\$\s*([0-9,]+(?:\.[0-9]{2})?)',
#             r'\$\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:Fixed|Total|Budget)',
#         ]
        
#         # Extract hourly rates
#         for pattern in hourly_patterns:
#             matches = re.findall(pattern, text, re.IGNORECASE)
#             for match in matches:
#                 try:
#                     price = float(match.replace(',', ''))
#                     if 5 <= price <= 500:  # Reasonable hourly rate range
#                         hourly_rates.append(price)
#                 except ValueError:
#                     continue
        
#         # Extract fixed prices
#         for pattern in fixed_patterns:
#             matches = re.findall(pattern, text, re.IGNORECASE)
#             for match in matches:
#                 try:
#                     price = float(match.replace(',', ''))
#                     if 50 <= price <= 100000:  # Reasonable fixed price range
#                         fixed_prices.append(price)
#                 except ValueError:
#                     continue
        
#         # If not categorized, try to guess based on context and value
#         if not hourly_rates and not fixed_prices:
#             general_pattern = r'\$\s*([0-9,]+(?:\.[0-9]{2})?)'
#             matches = re.findall(general_pattern, text)
            
#             for match in matches:
#                 try:
#                     price = float(match.replace(',', ''))
#                     # Heuristic: prices under 200 are likely hourly, above are likely fixed
#                     if 5 <= price <= 200:
#                         # Check context for hourly indicators
#                         match_pos = text.find(f'${match}')
#                         context = text[max(0, match_pos-50):min(len(text), match_pos+50)].lower()
#                         if any(word in context for word in ['hour', 'hr', '/hr', 'hourly']):
#                             hourly_rates.append(price)
#                         elif price <= 100:  # Small amounts likely hourly
#                             hourly_rates.append(price)
#                         else:
#                             fixed_prices.append(price)
#                     elif 200 < price <= 100000:
#                         fixed_prices.append(price)
#                 except ValueError:
#                     continue
        
#         return {
#             'hourly': list(set(hourly_rates)),
#             'fixed': list(set(fixed_prices))
#         }
    
#     def search_upwork(self, title):
#         """Search Upwork for projects"""
#         url = f"https://www.upwork.com/nx/search/jobs/?q={quote_plus(title)}"
#         print(f"  Accessing: {url}")
        
#         try:
#             self.driver.get(url)
#             time.sleep(4)  # Wait for dynamic content to load
            
#             page_text = self.driver.page_source
            
#             # Get all text elements that might contain prices
#             price_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '$')]")
#             all_text = " ".join([elem.text for elem in price_elements[:50]])
#             all_text += " " + page_text
            
#             categorized = self.categorize_prices(all_text)
            
#             return {
#                 'platform': 'Upwork',
#                 'url': url,
#                 'hourly_rates': sorted(categorized['hourly'])[:15],
#                 'fixed_prices': sorted(categorized['fixed'])[:15],
#                 'hourly_avg': statistics.mean(categorized['hourly']) if categorized['hourly'] else 0,
#                 'fixed_avg': statistics.mean(categorized['fixed']) if categorized['fixed'] else 0,
#             }
#         except Exception as e:
#             print(f"  Error: {e}")
#             return {'platform': 'Upwork', 'url': url, 'error': str(e)}
    
#     def search_freelancer(self, title):
#         """Search Freelancer.com for projects"""
#         url = f"https://www.freelancer.com/jobs/?keyword={quote_plus(title)}"
#         print(f"  Accessing: {url}")
        
#         try:
#             self.driver.get(url)
#             time.sleep(4)
            
#             page_text = self.driver.page_source
#             price_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'USD') or contains(text(), '$')]")
#             all_text = " ".join([elem.text for elem in price_elements[:50]])
#             all_text += " " + page_text
            
#             categorized = self.categorize_prices(all_text)
            
#             return {
#                 'platform': 'Freelancer',
#                 'url': url,
#                 'hourly_rates': sorted(categorized['hourly'])[:15],
#                 'fixed_prices': sorted(categorized['fixed'])[:15],
#                 'hourly_avg': statistics.mean(categorized['hourly']) if categorized['hourly'] else 0,
#                 'fixed_avg': statistics.mean(categorized['fixed']) if categorized['fixed'] else 0,
#             }
#         except Exception as e:
#             print(f"  Error: {e}")
#             return {'platform': 'Freelancer', 'url': url, 'error': str(e)}
    
#     def search_fiverr(self, title):
#         """Search Fiverr for gigs (usually fixed price)"""
#         url = f"https://www.fiverr.com/search/gigs?query={quote_plus(title)}"
#         print(f"  Accessing: {url}")
        
#         try:
#             self.driver.get(url)
#             time.sleep(4)
            
#             page_text = self.driver.page_source
#             price_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'price') or contains(text(), '$')]")
#             all_text = " ".join([elem.text for elem in price_elements[:50]])
#             all_text += " " + page_text
            
#             categorized = self.categorize_prices(all_text)
            
#             # Fiverr is mostly fixed-price gigs
#             return {
#                 'platform': 'Fiverr',
#                 'url': url,
#                 'hourly_rates': sorted(categorized['hourly'])[:15],
#                 'fixed_prices': sorted(categorized['fixed'])[:15],
#                 'hourly_avg': statistics.mean(categorized['hourly']) if categorized['hourly'] else 0,
#                 'fixed_avg': statistics.mean(categorized['fixed']) if categorized['fixed'] else 0,
#             }
#         except Exception as e:
#             print(f"  Error: {e}")
#             return {'platform': 'Fiverr', 'url': url, 'error': str(e)}
    
#     def search_all(self, title, show_egp=True):
#         """Search all platforms"""
#         print(f"\n{'='*80}")
#         print(f"Searching for: '{title}'")
#         print(f"{'='*80}\n")
        
#         results = []
        
#         print("Searching Upwork...")
#         results.append(self.search_upwork(title))
#         time.sleep(2)
        
#         print("\nSearching Freelancer...")
#         results.append(self.search_freelancer(title))
#         time.sleep(2)
        
#         print("\nSearching Fiverr...")
#         results.append(self.search_fiverr(title))
        
#         # Get exchange rate if needed
#         exchange_rate = None
#         if show_egp:
#             print("\nFetching USD to EGP exchange rate...")
#             exchange_rate = self.get_usd_to_egp_rate()
        
#         # Display results with or without EGP
#         if show_egp and exchange_rate:
#             self.display_results_with_egp(results, exchange_rate)
#         else:
#             # Display results (USD only)
#             print(f"\n{'='*80}")
#             print("RESULTS - SEPARATED BY PRICING TYPE")
#             print(f"{'='*80}\n")
            
#             for result in results:
#                 print(f"{result['platform']}:")
#                 print(f"  URL: {result['url']}")
                
#                 if 'error' in result:
#                     print(f"  Status: Error occurred")
#                 else:
#                     # Hourly rates
#                     if result.get('hourly_rates'):
#                         print(f"\n  HOURLY RATES:")
#                         print(f"    Count: {len(result['hourly_rates'])}")
#                         print(f"    Average: ${result['hourly_avg']:.2f}/hr")
#                         print(f"    Range: ${min(result['hourly_rates']):.2f} - ${max(result['hourly_rates']):.2f}/hr")
#                         print(f"    Samples: {[f'${p:.2f}/hr' for p in result['hourly_rates'][:8]]}")
#                     else:
#                         print(f"\n  HOURLY RATES: None detected")
                    
#                     # Fixed prices
#                     if result.get('fixed_prices'):
#                         print(f"\n  FIXED PRICES:")
#                         print(f"    Count: {len(result['fixed_prices'])}")
#                         print(f"    Average: ${result['fixed_avg']:.2f}")
#                         print(f"    Range: ${min(result['fixed_prices']):.2f} - ${max(result['fixed_prices']):.2f}")
#                         print(f"    Samples: {[f'${p:.2f}' for p in result['fixed_prices'][:8]]}")
#                     else:
#                         print(f"\n  FIXED PRICES: None detected")
#                 print()
            
#             # Overall summary
#             all_hourly = []
#             all_fixed = []
#             for result in results:
#                 if 'error' not in result:
#                     all_hourly.extend(result.get('hourly_rates', []))
#                     all_fixed.extend(result.get('fixed_prices', []))
            
#             print(f"{'='*80}")
#             print("OVERALL SUMMARY")
#             print(f"{'='*80}")
            
#             if all_hourly:
#                 print(f"\nHOURLY RATES ACROSS ALL PLATFORMS:")
#                 print(f"  Total Found: {len(all_hourly)}")
#                 print(f"  Average: ${statistics.mean(all_hourly):.2f}/hr")
#                 print(f"  Median: ${statistics.median(all_hourly):.2f}/hr")
#                 print(f"  Range: ${min(all_hourly):.2f} - ${max(all_hourly):.2f}/hr")
#             else:
#                 print(f"\nHOURLY RATES: None detected")
            
#             if all_fixed:
#                 print(f"\nFIXED PRICES ACROSS ALL PLATFORMS:")
#                 print(f"  Total Found: {len(all_fixed)}")
#                 print(f"  Average: ${statistics.mean(all_fixed):.2f}")
#                 print(f"  Median: ${statistics.median(all_fixed):.2f}")
#                 print(f"  Range: ${min(all_fixed):.2f} - ${max(all_fixed):.2f}")
#             else:
#                 print(f"\nFIXED PRICES: None detected")
            
#             if not all_hourly and not all_fixed:
#                 print("\nNo prices were detected. This may be due to:")
#                 print("  - Website structure changes")
#                 print("  - Anti-scraping measures")
#                 print("  - No matching projects found")
#                 print("\nTip: Visit the URLs manually or try different search terms.")
            
#             print(f"{'='*80}\n")
        
#         return results
    
#     def get_usd_to_egp_rate(self):
#         """Get current USD to EGP exchange rate"""
#         try:
#             # Try multiple sources for exchange rate
#             sources = [
#                 "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EGP",
#                 "https://www.google.com/search?q=usd+to+egp",
#             ]
            
#             for url in sources:
#                 try:
#                     self.driver.get(url)
#                     time.sleep(2)
                    
#                     page_text = self.driver.page_source
                    
#                     # Look for exchange rate patterns
#                     patterns = [
#                         r'1\s*USD\s*=\s*([0-9,.]+)\s*EGP',
#                         r'([0-9,.]+)\s*Egyptian Pound',
#                         r'([0-9,.]+)\s*EGP',
#                     ]
                    
#                     for pattern in patterns:
#                         matches = re.findall(pattern, page_text, re.IGNORECASE)
#                         for match in matches:
#                             try:
#                                 rate = float(match.replace(',', ''))
#                                 if 20 <= rate <= 100:  # Reasonable range for USD to EGP
#                                     print(f"  ✓ Exchange rate found: 1 USD = {rate:.2f} EGP")
#                                     return rate
#                             except ValueError:
#                                 continue
#                 except:
#                     continue
            
#             # Fallback: Use approximate rate if scraping fails
#             print("  ⚠ Could not fetch live rate, using approximate rate")
#             return 50.0  # Approximate rate as fallback
            
#         except Exception as e:
#             print(f"  Error getting exchange rate: {e}")
#             return 50.0  # Default fallback rate
    
#     def convert_usd_to_egp(self, usd_amount, exchange_rate):
#         """Convert USD amount to EGP"""
#         return usd_amount * exchange_rate
    
#     def display_results_with_egp(self, results, exchange_rate):
#         """Display results with EGP conversion"""
#         print(f"\n{'='*80}")
#         print(f"RESULTS WITH EGP CONVERSION (1 USD = {exchange_rate:.2f} EGP)")
#         print(f"{'='*80}\n")
        
#         for result in results:
#             print(f"{result['platform']}:")
#             print(f"  URL: {result['url']}")
            
#             if 'error' in result:
#                 print(f"  Status: Error occurred")
#             else:
#                 # Hourly rates with EGP
#                 if result.get('hourly_rates'):
#                     print(f"\n  HOURLY RATES:")
#                     print(f"    Count: {len(result['hourly_rates'])}")
#                     print(f"    Average: ${result['hourly_avg']:.2f}/hr (EGP {self.convert_usd_to_egp(result['hourly_avg'], exchange_rate):.2f}/hr)")
#                     min_hourly = min(result['hourly_rates'])
#                     max_hourly = max(result['hourly_rates'])
#                     print(f"    Range: ${min_hourly:.2f} - ${max_hourly:.2f}/hr")
#                     print(f"           (EGP {self.convert_usd_to_egp(min_hourly, exchange_rate):.2f} - {self.convert_usd_to_egp(max_hourly, exchange_rate):.2f}/hr)")
#                     print(f"    USD Samples: {[f'${p:.2f}/hr' for p in result['hourly_rates'][:5]]}")
#                     print(f"    EGP Samples: {[f'EGP {self.convert_usd_to_egp(p, exchange_rate):.2f}/hr' for p in result['hourly_rates'][:5]]}")
#                 else:
#                     print(f"\n  HOURLY RATES: None detected")
                
#                 # Fixed prices with EGP
#                 if result.get('fixed_prices'):
#                     print(f"\n  FIXED PRICES:")
#                     print(f"    Count: {len(result['fixed_prices'])}")
#                     print(f"    Average: ${result['fixed_avg']:.2f} (EGP {self.convert_usd_to_egp(result['fixed_avg'], exchange_rate):.2f})")
#                     min_fixed = min(result['fixed_prices'])
#                     max_fixed = max(result['fixed_prices'])
#                     print(f"    Range: ${min_fixed:.2f} - ${max_fixed:.2f}")
#                     print(f"           (EGP {self.convert_usd_to_egp(min_fixed, exchange_rate):.2f} - {self.convert_usd_to_egp(max_fixed, exchange_rate):.2f})")
#                     print(f"    USD Samples: {[f'${p:.2f}' for p in result['fixed_prices'][:5]]}")
#                     print(f"    EGP Samples: {[f'EGP {self.convert_usd_to_egp(p, exchange_rate):.2f}' for p in result['fixed_prices'][:5]]}")
#                 else:
#                     print(f"\n  FIXED PRICES: None detected")
#             print()
        
#         # Overall summary with EGP
#         all_hourly = []
#         all_fixed = []
#         for result in results:
#             if 'error' not in result:
#                 all_hourly.extend(result.get('hourly_rates', []))
#                 all_fixed.extend(result.get('fixed_prices', []))
        
#         print(f"{'='*80}")
#         print("OVERALL SUMMARY (USD & EGP)")
#         print(f"{'='*80}")
        
#         if all_hourly:
#             avg_hourly = statistics.mean(all_hourly)
#             med_hourly = statistics.median(all_hourly)
#             min_hourly = min(all_hourly)
#             max_hourly = max(all_hourly)
            
#             print(f"\nHOURLY RATES ACROSS ALL PLATFORMS:")
#             print(f"  Total Found: {len(all_hourly)}")
#             print(f"  Average: ${avg_hourly:.2f}/hr (EGP {self.convert_usd_to_egp(avg_hourly, exchange_rate):.2f}/hr)")
#             print(f"  Median: ${med_hourly:.2f}/hr (EGP {self.convert_usd_to_egp(med_hourly, exchange_rate):.2f}/hr)")
#             print(f"  Range: ${min_hourly:.2f} - ${max_hourly:.2f}/hr")
#             print(f"         (EGP {self.convert_usd_to_egp(min_hourly, exchange_rate):.2f} - {self.convert_usd_to_egp(max_hourly, exchange_rate):.2f}/hr)")
#         else:
#             print(f"\nHOURLY RATES: None detected")
        
#         if all_fixed:
#             avg_fixed = statistics.mean(all_fixed)
#             med_fixed = statistics.median(all_fixed)
#             min_fixed = min(all_fixed)
#             max_fixed = max(all_fixed)
            
#             print(f"\nFIXED PRICES ACROSS ALL PLATFORMS:")
#             print(f"  Total Found: {len(all_fixed)}")
#             print(f"  Average: ${avg_fixed:.2f} (EGP {self.convert_usd_to_egp(avg_fixed, exchange_rate):.2f})")
#             print(f"  Median: ${med_fixed:.2f} (EGP {self.convert_usd_to_egp(med_fixed, exchange_rate):.2f})")
#             print(f"  Range: ${min_fixed:.2f} - ${max_fixed:.2f}")
#             print(f"         (EGP {self.convert_usd_to_egp(min_fixed, exchange_rate):.2f} - {self.convert_usd_to_egp(max_fixed, exchange_rate):.2f})")
#         else:
#             print(f"\nFIXED PRICES: None detected")
        
#         print(f"{'='*80}\n")
    
#     def save_to_json(self, results, exchange_rate, filename=None):
#         """Save results to JSON file with timestamp"""
#         if filename is None:
#             timestamp = datetime.now().strftime("%Y%m%d")
#             filename = f"freelance_prices_{timestamp}.json"
        
#         data = {
#             "timestamp": datetime.now().isoformat(),
#             "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "exchange_rate_usd_to_egp": exchange_rate,
#             "platforms": []
#         }
        
#         for result in results:
#             if 'error' not in result:
#                 platform_data = {
#                     "platform": result['platform'],
#                     "url": result['url'],
#                     "hourly_rates": {
#                         "usd": result.get('hourly_rates', []),
#                         "egp": [self.convert_usd_to_egp(p, exchange_rate) for p in result.get('hourly_rates', [])],
#                         "count": len(result.get('hourly_rates', [])),
#                         "average_usd": result.get('hourly_avg', 0),
#                         "average_egp": self.convert_usd_to_egp(result.get('hourly_avg', 0), exchange_rate),
#                         "min_usd": min(result.get('hourly_rates', [0])) if result.get('hourly_rates') else 0,
#                         "max_usd": max(result.get('hourly_rates', [0])) if result.get('hourly_rates') else 0,
#                     },
#                     "fixed_prices": {
#                         "usd": result.get('fixed_prices', []),
#                         "egp": [self.convert_usd_to_egp(p, exchange_rate) for p in result.get('fixed_prices', [])],
#                         "count": len(result.get('fixed_prices', [])),
#                         "average_usd": result.get('fixed_avg', 0),
#                         "average_egp": self.convert_usd_to_egp(result.get('fixed_avg', 0), exchange_rate),
#                         "min_usd": min(result.get('fixed_prices', [0])) if result.get('fixed_prices') else 0,
#                         "max_usd": max(result.get('fixed_prices', [0])) if result.get('fixed_prices') else 0,
#                     }
#                 }
#                 data["platforms"].append(platform_data)
        
#         # Calculate overall statistics
#         all_hourly = []
#         all_fixed = []
#         for result in results:
#             if 'error' not in result:
#                 all_hourly.extend(result.get('hourly_rates', []))
#                 all_fixed.extend(result.get('fixed_prices', []))
        
#         data["overall_summary"] = {
#             "hourly_rates": {
#                 "total_count": len(all_hourly),
#                 "average_usd": statistics.mean(all_hourly) if all_hourly else 0,
#                 "average_egp": self.convert_usd_to_egp(statistics.mean(all_hourly), exchange_rate) if all_hourly else 0,
#                 "median_usd": statistics.median(all_hourly) if all_hourly else 0,
#                 "median_egp": self.convert_usd_to_egp(statistics.median(all_hourly), exchange_rate) if all_hourly else 0,
#                 "min_usd": min(all_hourly) if all_hourly else 0,
#                 "max_usd": max(all_hourly) if all_hourly else 0,
#             },
#             "fixed_prices": {
#                 "total_count": len(all_fixed),
#                 "average_usd": statistics.mean(all_fixed) if all_fixed else 0,
#                 "average_egp": self.convert_usd_to_egp(statistics.mean(all_fixed), exchange_rate) if all_fixed else 0,
#                 "median_usd": statistics.median(all_fixed) if all_fixed else 0,
#                 "median_egp": self.convert_usd_to_egp(statistics.median(all_fixed), exchange_rate) if all_fixed else 0,
#                 "min_usd": min(all_fixed) if all_fixed else 0,
#                 "max_usd": max(all_fixed) if all_fixed else 0,
#             }
#         }
        
#         # Save to file
#         with open(filename, 'w', encoding='utf-8') as f:
#             json.dump(data, f, indent=2, ensure_ascii=False)
        
#         print(f"\n✓ Data saved to: {filename}")
#         return filename, data
    
#     def save_to_dataframe(self, results, exchange_rate):
#         """Convert results to pandas DataFrame"""
#         rows = []
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
#         for result in results:
#             if 'error' not in result:
#                 platform = result['platform']
                
#                 # Add hourly rates
#                 for price_usd in result.get('hourly_rates', []):
#                     rows.append({
#                         'timestamp': timestamp,
#                         'platform': platform,
#                         'price_type': 'hourly',
#                         'price_usd': price_usd,
#                         'price_egp': self.convert_usd_to_egp(price_usd, exchange_rate),
#                         'exchange_rate': exchange_rate,
#                         'url': result['url']
#                     })
                
#                 # Add fixed prices
#                 for price_usd in result.get('fixed_prices', []):
#                     rows.append({
#                         'timestamp': timestamp,
#                         'platform': platform,
#                         'price_type': 'fixed',
#                         'price_usd': price_usd,
#                         'price_egp': self.convert_usd_to_egp(price_usd, exchange_rate),
#                         'exchange_rate': exchange_rate,
#                         'url': result['url']
#                     })
        
#         df = pd.DataFrame(rows)
#         return df
    
#     def save_dataframe_to_csv(self, df, filename=None):
#         """Save DataFrame to CSV file"""
#         if filename is None:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"freelance_prices_{timestamp}.csv"
        
#         df.to_csv(filename, index=False, encoding='utf-8')
#         print(f"✓ DataFrame saved to: {filename}")
#         return filename
    
#     def load_json(self, filename):
#         """Load previously saved JSON data"""
#         with open(filename, 'r', encoding='utf-8') as f:
#             data = json.load(f)
        
#         print(f"\n{'='*80}")
#         print(f"LOADED DATA FROM: {filename}")
#         print(f"{'='*80}")
#         print(f"Saved on: {data['date']}")
#         print(f"Exchange Rate: 1 USD = {data['exchange_rate_usd_to_egp']:.2f} EGP")
#         print(f"\nOverall Summary:")
        
#         hourly = data['overall_summary']['hourly_rates']
#         if hourly['total_count'] > 0:
#             print(f"\n  Hourly Rates:")
#             print(f"    Count: {hourly['total_count']}")
#             print(f"    Average: ${hourly['average_usd']:.2f} (EGP {hourly['average_egp']:.2f})")
#             print(f"    Median: ${hourly['median_usd']:.2f} (EGP {hourly['median_egp']:.2f})")
        
#         fixed = data['overall_summary']['fixed_prices']
#         if fixed['total_count'] > 0:
#             print(f"\n  Fixed Prices:")
#             print(f"    Count: {fixed['total_count']}")
#             print(f"    Average: ${fixed['average_usd']:.2f} (EGP {fixed['average_egp']:.2f})")
#             print(f"    Median: ${fixed['median_usd']:.2f} (EGP {fixed['median_egp']:.2f})")
        
#         print(f"{'='*80}\n")
#         return data
    
#     def load_dataframe(self, filename):
#         """Load previously saved CSV data"""
#         df = pd.read_csv(filename)
        
#         print(f"\n{'='*80}")
#         print(f"LOADED DATAFRAME FROM: {filename}")
#         print(f"{'='*80}")
#         print(f"Total Records: {len(df)}")
#         print(f"Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
#         print(f"\nDataFrame Preview:")
#         print(df.head(10))
#         print(f"\nSummary Statistics:")
#         print(df.groupby(['platform', 'price_type'])['price_usd'].describe())
#         print(f"{'='*80}\n")
        
#         return df
    
#     def compare_historical_data(self, json_files):
#         """Compare multiple JSON files to see price changes over time"""
#         if not json_files:
#             print("No files to compare")
#             return
        
#         print(f"\n{'='*80}")
#         print(f"HISTORICAL PRICE COMPARISON")
#         print(f"{'='*80}\n")
        
#         comparison_data = []
        
#         for filename in json_files:
#             with open(filename, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
                
#                 summary = data['overall_summary']
#                 comparison_data.append({
#                     'date': data['date'],
#                     'exchange_rate': data['exchange_rate_usd_to_egp'],
#                     'hourly_avg_usd': summary['hourly_rates']['average_usd'],
#                     'hourly_avg_egp': summary['hourly_rates']['average_egp'],
#                     'fixed_avg_usd': summary['fixed_prices']['average_usd'],
#                     'fixed_avg_egp': summary['fixed_prices']['average_egp'],
#                 })
        
#         df_comparison = pd.DataFrame(comparison_data)
#         df_comparison = df_comparison.sort_values('date')
        
#         print("Price Trends Over Time:")
#         print(df_comparison.to_string(index=False))
        
#         if len(df_comparison) > 1:
#             print(f"\n{'='*80}")
#             print("PRICE CHANGES:")
#             print(f"{'='*80}")
            
#             first = df_comparison.iloc[0]
#             last = df_comparison.iloc[-1]
            
#             if last['hourly_avg_usd'] > 0:
#                 hourly_change = ((last['hourly_avg_usd'] - first['hourly_avg_usd']) / first['hourly_avg_usd'] * 100) if first['hourly_avg_usd'] > 0 else 0
#                 print(f"\nHourly Rates:")
#                 print(f"  From: ${first['hourly_avg_usd']:.2f} (on {first['date']})")
#                 print(f"  To: ${last['hourly_avg_usd']:.2f} (on {last['date']})")
#                 print(f"  Change: {hourly_change:+.2f}%")
            
#             if last['fixed_avg_usd'] > 0:
#                 fixed_change = ((last['fixed_avg_usd'] - first['fixed_avg_usd']) / first['fixed_avg_usd'] * 100) if first['fixed_avg_usd'] > 0 else 0
#                 print(f"\nFixed Prices:")
#                 print(f"  From: ${first['fixed_avg_usd']:.2f} (on {first['date']})")
#                 print(f"  To: ${last['fixed_avg_usd']:.2f} (on {last['date']})")
#                 print(f"  Change: {fixed_change:+.2f}%")
        
#         print(f"{'='*80}\n")
#         return df_comparison
    
#     def close(self):
#         """Close the browser"""
#         if hasattr(self, 'driver'):
#             self.driver.quit()


# # Example usage
# if __name__ == "__main__":
#     scraper = None
#     try:
#         # Initialize scraper (set headless=False to see the browser)
#         scraper = FreelancePriceScraper(headless=True)
        
#         # Search with EGP conversion
#         results = scraper.search_all("Python web scraping", show_egp=True)
        
#         # Get exchange rate
#         exchange_rate = scraper.get_usd_to_egp_rate()
        
#         # Save to JSON
#         json_file,_ = scraper.save_to_json(results, exchange_rate)
        
#         # Save to DataFrame and CSV
#         # df = scraper.save_to_dataframe(results, exchange_rate)
#         # csv_file = scraper.save_dataframe_to_csv(df)
        
#         print("\n" + "="*80)
#         print("DATA EXPORT SUMMARY")
#         print("="*80)
#         print(f"✓ JSON saved: {json_file}")
#         # print(f"✓ CSV saved: {csv_file}")
#         # print(f"✓ DataFrame shape: {df.shape}")
#         print("="*80)
        
#         # ===== LOAD PREVIOUS DATA EXAMPLES =====
        
#         # Example: Load JSON data
#         # loaded_data = scraper.load_json("freelance_prices_20240113_120000.json")
        
#         # Example: Load CSV data
#         # loaded_df = scraper.load_dataframe("freelance_prices_20240113_120000.csv")
        
#         # Example: Compare historical data
#         # json_files = [
#         #     "freelance_prices_20240101_120000.json",
#         #     "freelance_prices_20240107_120000.json",
#         #     "freelance_prices_20240113_120000.json"
#         # ]
#         # comparison_df = scraper.compare_historical_data(json_files)
        
#     except Exception as e:
#         print(f"\nFatal error: {e}")
#     finally:
#         if scraper:
#             scraper.close()
#             print("\nBrowser closed.")



"""
calculate_project_pricing.py - Modular Version
Can run standalone OR be imported as a module
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import re
import random
import time
import statistics
from urllib.parse import quote_plus
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod


class PriceExtractor:
    """Extract and categorize prices from text."""
    
    def categorize_prices(self, text: str) -> Dict[str, List[float]]:
        """Categorize prices as hourly rates or fixed project prices."""
        hourly_rates = []
        fixed_prices = []
        
        # Hourly patterns
        hourly_patterns = [
            r'\$\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:/hr|per hour|hourly|/hour)',
            r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:USD|$)\s*(?:/hr|per hour|hourly|/hour)',
        ]
        
        # Fixed patterns
        fixed_patterns = [
            r'(?:Fixed|Budget|Price):\s*\$\s*([0-9,]+(?:\.[0-9]{2})?)',
            r'\$\s*([0-9,]+(?:\.[0-9]{2})?)\s*(?:Fixed|Total|Budget)',
        ]
        
        # Extract hourly rates
        for pattern in hourly_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                price = self._parse_price(match)
                if price and 5 <= price <= 500:
                    hourly_rates.append(price)
        
        # Extract fixed prices
        for pattern in fixed_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                price = self._parse_price(match)
                if price and 50 <= price <= 100000:
                    fixed_prices.append(price)
        
        # Heuristic categorization if needed
        if not hourly_rates and not fixed_prices:
            hourly_rates, fixed_prices = self._heuristic_categorization(text)
        
        return {
            'hourly': list(set(hourly_rates)),
            'fixed': list(set(fixed_prices))
        }
    
    def _parse_price(self, price_str: str) -> Optional[float]:
        """Parse price string to float."""
        try:
            return float(price_str.replace(',', ''))
        except ValueError:
            return None
    
    def _heuristic_categorization(self, text: str) -> Tuple[List[float], List[float]]:
        """Use heuristics to categorize unlabeled prices."""
        hourly_rates = []
        fixed_prices = []
        
        general_pattern = r'\$\s*([0-9,]+(?:\.[0-9]{2})?)'
        matches = re.findall(general_pattern, text)
        
        for match in matches:
            price = self._parse_price(match)
            if not price:
                continue
            
            if 5 <= price <= 200:
                match_pos = text.find(f'${match}')
                context = text[max(0, match_pos-50):min(len(text), match_pos+50)].lower()
                
                if any(word in context for word in ['hour', 'hr', '/hr', 'hourly']):
                    hourly_rates.append(price)
                elif price <= 100:
                    hourly_rates.append(price)
                else:
                    fixed_prices.append(price)
            elif 200 < price <= 100000:
                fixed_prices.append(price)
        
        return hourly_rates, fixed_prices


class PlatformScraper(ABC):
    """Abstract base class for platform scrapers."""
    
    def __init__(self, driver: webdriver.Chrome, price_extractor: PriceExtractor):
        """Initialize platform scraper."""
        self.driver = driver
        self.price_extractor = price_extractor
    
    @abstractmethod
    def get_search_url(self, query: str) -> str:
        """Get search URL for the platform."""
        pass
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Get platform name."""
        pass
    
    def search(self, query: str, wait_time: int = 4) -> Dict:
        """Search platform for pricing information."""
        url = self.get_search_url(query)
        print(f"  Accessing: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(wait_time)
            
            # Extract text with prices
            page_text = self.driver.page_source
            price_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '$')]")
            all_text = " ".join([elem.text for elem in price_elements[:50]]) + " " + page_text
            
            # Categorize prices
            categorized = self.price_extractor.categorize_prices(all_text)
            
            hourly_rates = sorted(categorized['hourly'])[:15]
            fixed_prices = sorted(categorized['fixed'])[:15]
            
            return {
                'platform': self.get_platform_name(),
                'url': url,
                'hourly_rates': hourly_rates,
                'fixed_prices': fixed_prices,
                'hourly_avg': statistics.mean(hourly_rates) if hourly_rates else 0,
                'fixed_avg': statistics.mean(fixed_prices) if fixed_prices else 0,
            }
            
        except Exception as e:
            print(f"  Error: {e}")
            return {
                'platform': self.get_platform_name(),
                'url': url,
                'error': str(e)
            }


class UpworkScraper(PlatformScraper):
    """Upwork platform scraper."""
    
    def get_platform_name(self) -> str:
        return "Upwork"
    
    def get_search_url(self, query: str) -> str:
        return f"https://www.upwork.com/nx/search/jobs/?q={quote_plus(query)}"


class FreelancerScraper(PlatformScraper):
    """Freelancer.com platform scraper."""
    
    def get_platform_name(self) -> str:
        return "Freelancer"
    
    def get_search_url(self, query: str) -> str:
        return f"https://www.freelancer.com/jobs/?keyword={quote_plus(query)}"


class FiverrScraper(PlatformScraper):
    """Fiverr platform scraper."""
    
    def get_platform_name(self) -> str:
        return "Fiverr"
    
    def get_search_url(self, query: str) -> str:
        return f"https://www.fiverr.com/search/gigs?query={quote_plus(query)}&filter=new"


class ExchangeRateService:
    """Service for fetching USD to EGP exchange rates."""
    
    def __init__(self, driver: webdriver.Chrome):
        """Initialize exchange rate service."""
        self.driver = driver
    
    def get_rate(self) -> float:
        """Get current USD to EGP exchange rate."""
        sources = [
            "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EGP",
            "https://www.google.com/search?q=usd+to+egp",
        ]
        
        patterns = [
            r'1\s*USD\s*=\s*([0-9,.]+)\s*EGP',
            r'([0-9,.]+)\s*Egyptian Pound',
            r'([0-9,.]+)\s*EGP',
            # USD/$ variations (new)
            r'USD\s*/\s*EGP[\s:]*([0-9,.]+)',           # USD/EGP: 30.5
            r'\$\s*1\s*=\s*([0-9,.]+)\s*EGP',           # $1 = 30.5 EGP
            r'1\s*U\.?S\.?\s*D\.?\s*=\s*([0-9,.]+)\s*EGP',  # 1 U.S.D. = 30.5 EGP
            r'([0-9,.]+)\s*EGP\s*per\s*(?:USD|\$)',     # 30.5 EGP per USD/$  
            r'USD\s*to\s*EGP[\s:]*([0-9,.]+)',          # USD to EGP: 30.5
            
            # Bidirectional patterns
            r'([0-9,.]+)\s*EGP\s*=\s*1\s*USD',          # 30.5 EGP = 1 USD
            r'1\s*USD\s*≈\s*([0-9,.]+)\s*EGP',          # 1 USD ≈ 30.5 EGP
            
            # With currency symbols
            r'\$\s*1\s*≈\s*([0-9,.]+)\s*£E',            # $1 ≈ 30.5 £E (Egyptian Pound symbol)
            
            # Range formats  
            r'USD/EGP[\s:]*([0-9,.]+)\s*[-–]\s*([0-9,.]+)',  # USD/EGP: 30.5-31.0
            r'([0-9,.]+)\s*[-–]\s*([0-9,.]+)\s*EGP',         # 30.5-31.0 EGP
            r'\$([0-9,.]+)\s*(?:USD|dollars?)\s*=\s*([0-9,.]+)\s*EGP',  # $1 USD = 30.5 EGP
            r'([0-9,.]+)\s*USD\s*equals?\s*([0-9,.]+)\s*EGP',           # 1 USD equals 30.5 EGP
            r'Exchange rate[:\s]+([0-9,.]+)\s*EGP\s*/\s*USD',           # Exchange rate: 30.5 EGP/USD
            r'Buying rate[:\s]+([0-9,.]+)\s*EGP',                       # Buying rate: 30.5 EGP
            r'Selling rate[:\s]+([0-9,.]+)\s*EGP',                      # Selling rate: 31.0 EGP
            # 1. Fixed price patterns
            r'(?:[Ff]ixed\s*[Pp]rice|[Bb]udget)[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)',  # Fixed price: $2,500.00
            r'[Ee]st\.?\s*[Bb]udget[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)',  # Est. budget: $2,500.00
            
            # 2. Hourly rate patterns
            r'[Hh]ourly[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)\s*-\s*\$?([0-9,]+(?:\.[0-9]{2})?)',  # Hourly: $20.00 - $50.00
            r'([0-9,]+(?:\.[0-9]{2})?)\s*-\s*\$?([0-9,]+(?:\.[0-9]{2})?)',  # $7 - $17 (standalone range)
            
            # 3. Starting from patterns
            r'[Ff]rom\s+\$?([0-9,]+(?:\.[0-9]{2})?)',  # From $250
            r'[Ss]tarting\s+[Aa]t\s+\$?([0-9,]+(?:\.[0-9]{2})?)',  # Starting at $100
            
            # 4. Single price patterns
            r'\$([0-9,]+(?:\.[0-9]{2})?)\s*(?:Avg|Average)?\s*[Bb]id',  # $18 Avg Bid
            r'\$([0-9,]+(?:\.[0-9]{2})?)\s*/\s*(?:hr|hour|hourly)',  # $15 / hr
            
            # 5. Range with Avg patterns
            r'\$([0-9,]+(?:\.[0-9]{2})?)\s*-\s*\$?([0-9,]+(?:\.[0-9]{2})?)\s*(?:Avg|Average)?\s*[Bb]id',  # $7 - $17 Avg Bid
            
            # 6. Direct dollar amounts (most flexible)
            r'\$([0-9,]+(?:\.[0-9]{2})?)',  # Any $ amount (last resort)
            
            # 7. Amounts without $ symbol but in price context
            r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:USD|US\$|\$|dollars?|bucks?)',  # 250 USD, 250 dollars
            
            # 8. Project estimate patterns
            r'[Ee]st\.?\s*(?:[Tt]ime|[Dd]uration)[:\s]*[Ll]ess\s+[Tt]han\s+([0-9]+)\s*(?:month|week|day)',  # Est. time: Less than 1 month
            # For freelancing platforms
            r'[Bb]udget[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)\s*-\s*\$?([0-9,]+(?:\.[0-9]{2})?)',
            r'[Pp]roposed\s+[Aa]mount[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)',
            r'[Bb]id\s+[Rr]ange[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)\s*-\s*\$?([0-9,]+(?:\.[0-9]{2})?)',
            
            # For e-commerce/product listings
            r'[Pp]rice[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)(?:\s*-\s*\$?([0-9,]+(?:\.[0-9]{2})?))?',
            r'[Ss]ale\s+[Pp]rice[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)',
            
            # For service listings
            r'[Ss]ervice\s+[Ff]ee[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)',
            r'[Rr]ate[:\s]*\$?([0-9,]+(?:\.[0-9]{2})?)\s*(?:per|/)\s*(?:hour|hr|day|week|month)',
        ]
        
        for url in sources:
            try:
                self.driver.get(url)
                time.sleep(2)
                
                page_text = self.driver.page_source
                
                for pattern in patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    for match in matches:
                        try:
                            rate = float(match.replace(',', ''))
                            if 20 <= rate <= 100:
                                print(f"  ✓ Exchange rate found: 1 USD = {rate:.2f} EGP")
                                return rate
                        except ValueError:
                            continue
            except:
                continue
        
        print(f"  ⚠ Could not fetch live rate, using fallback: 50.0")
        return 50.0


class FreelancePriceScraper:
    """Main scraper orchestrator for freelance pricing."""
    
    def __init__(self, headless: bool = True):
        """Initialize the scraper."""
        self.driver = self._initialize_driver(headless)
        self.price_extractor = PriceExtractor()
        self.exchange_service = ExchangeRateService(self.driver)
        
        # Initialize platform scrapers
        self.scrapers = [
            UpworkScraper(self.driver, self.price_extractor),
            FreelancerScraper(self.driver, self.price_extractor),
            FiverrScraper(self.driver, self.price_extractor),
        ]
    
    # def _initialize_driver(self, headless: bool) -> webdriver.Chrome:
    #     """Initialize Chrome WebDriver."""
    #     chrome_options = Options()
    #     if headless:
    #         chrome_options.add_argument("--headless")
    #     chrome_options.add_argument("--no-sandbox")
    #     chrome_options.add_argument("--disable-dev-shm-usage")
    #     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    #     chrome_options.add_argument(
    #         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    #     )
        
    #     try:
    #         return webdriver.Chrome(options=chrome_options)
    #     except Exception as e:
    #         print(f"Error initializing Chrome driver: {e}")
    #         print("\nPlease install ChromeDriver")
    #         raise

    def _initialize_driver(self, headless: bool, user_agent: str = None):
        """Initialize Chrome WebDriver with enhanced stealth features."""
        
        try:
            # List of realistic user agents
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            ]
            
            # Use provided user agent or pick random
            if not user_agent:
                user_agent = random.choice(user_agents)
            
            # Initialize with user agent
            driver = uc.Chrome(
                headless=headless,
                version_main=None,
                use_subprocess=True,
            )
            
            # Apply multiple stealth techniques
            stealth_scripts = [
                # Hide webdriver property
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                
                # Override languages
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
                
                # Override platform
                "Object.defineProperty(navigator, 'platform', {get: () => 'Win32'})",
                
                # Override plugins
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
            ]
            
            # Execute all stealth scripts
            for script in stealth_scripts:
                driver.execute_script(script)
            
            # Set user agent via CDP
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": user_agent
            })
            
            # Set viewport for consistency
            driver.set_window_size(1920, 1080)
            
            return driver
            
        except Exception as e:
            print(f"Error initializing enhanced driver: {e}")
            
            # Try basic version as fallback
            return self._initialize_driver_basic(headless)

    def _initialize_driver_basic(self, headless: bool):
        """Basic driver initialization as fallback."""
        
        try:
            # Very simple initialization
            driver = uc.Chrome(headless=headless)
            return driver
        except Exception as e:
            print(f"Basic initialization failed: {e}")
            
            # Last resort: try with just headless flag
            try:
                driver = uc.Chrome()
                if headless:
                    print("Warning: Headless mode not available, using visible browser")
                return driver
            except Exception as final_error:
                print(f"All driver initialization attempts failed: {final_error}")
                raise RuntimeError("Failed to initialize Chrome driver. Please check Chrome installation.")





    def search_all(self, query: str, show_egp: bool = False) -> List[Dict]:
        """Search all platforms for pricing."""
        print(f"\n{'='*80}")
        print(f"Searching for: '{query}'")
        print(f"{'='*80}\n")
        
        results = []
        
        for scraper in self.scrapers:
            print(f"Searching {scraper.get_platform_name()}...")
            result = scraper.search(query)
            results.append(result)
            time.sleep(2)
        
        return results
    
    def get_usd_to_egp_rate(self) -> float:
        """Get current USD to EGP exchange rate."""
        print("\nFetching USD to EGP exchange rate...")
        return self.exchange_service.get_rate()
    
    def save_to_json(self, results: List[Dict], exchange_rate: float,
                     filename: Optional[str] = None) -> Tuple[str, Dict]:
        """Save results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"freelance_prices_{timestamp}.json"
        
        # Build data structure
        all_hourly = []
        all_fixed = []
        
        platforms_data = []
        for result in results:
            if 'error' not in result:
                platforms_data.append({
                    "platform": result['platform'],
                    "url": result['url'],
                    "hourly_rates": {
                        "usd": result.get('hourly_rates', []),
                        "count": len(result.get('hourly_rates', [])),
                        "average_usd": result.get('hourly_avg', 0),
                    },
                    "fixed_prices": {
                        "usd": result.get('fixed_prices', []),
                        "count": len(result.get('fixed_prices', [])),
                        "average_usd": result.get('fixed_avg', 0),
                    }
                })
                
                all_hourly.extend(result.get('hourly_rates', []))
                all_fixed.extend(result.get('fixed_prices', []))
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "exchange_rate_usd_to_egp": exchange_rate,
            "platforms": platforms_data,
            "overall_summary": {
                "hourly_rates": {
                    "total_count": len(all_hourly),
                    "average_usd": statistics.mean(all_hourly) if all_hourly else 0,
                    "median_usd": statistics.median(all_hourly) if all_hourly else 0,
                },
                "fixed_prices": {
                    "total_count": len(all_fixed),
                    "average_usd": statistics.mean(all_fixed) if all_fixed else 0,
                    "median_usd": statistics.median(all_fixed) if all_fixed else 0,
                }
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Data saved to: {filename}")
        return filename, data
    
    def close(self):
        """Close the browser."""
        if hasattr(self, 'driver'):
            self.driver.quit()


# ============ STANDALONE MODE ============

if __name__ == "__main__":
    scraper = None
    try:
        scraper = FreelancePriceScraper(headless=True)
        
        results = scraper.search_all("Python web scraping")
        exchange_rate = scraper.get_usd_to_egp_rate()
        
        json_file, _ = scraper.save_to_json(results, exchange_rate)
        
        print(f"\n{'='*80}")
        print("DATA EXPORT SUMMARY")
        print(f"{'='*80}")
        print(f"✓ JSON saved: {json_file}")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"\nFatal error: {e}")
    finally:
        if scraper:
            scraper.close()
            print("\nBrowser closed.")