#!/usr/bin/env python3
import requests
import json
from typing import Dict, Any, Optional

class HEBGraphQLClient:
    """
    Client for making GraphQL requests to the HEB API
    """
    
    def __init__(self):
        self.url = "https://www.heb.com/graphql"
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "RapidAPI/4.2.8 (Macintosh; OS X/14.2.1) GCDHTTPRequest",
            "Connection": "close",
            # Cookies are included in the header for authentication
            "Cookie": "sst=hs:sst:7ZDTNKeQy1SDERnnhcxXY; sst.sig=sxZSKSOcDblaxwi9h7aOC87RuLvQhDvLieDzmy4nhf4; visid_incap_2302070=lhatO8YlSKGrANNSQa010x5nAWgAAAAAQUIPAAAAAAD3Ffp2x0iIedeesNHV8uHq; incap_ses_468_2302070=yNyePMH7uXEO+7IG56t+BqWKAWgAAAAAMpPsAwzRwUW7aNDOFlBIOw=="
        }
    
    def search_stores_by_address(self, 
                                address: str = "1803 West Bronze St, Pharr, TX", 
                                radius_miles: int = 25, 
                                fulfillment_channels: list = None) -> Dict[str, Any]:
        """
        Make a GraphQL request to search for stores near an address
        
        Args:
            address: The address to search near
            radius_miles: The search radius in miles
            fulfillment_channels: List of fulfillment channels to filter by
            
        Returns:
            Dictionary containing the API response
        """
        if fulfillment_channels is None:
            fulfillment_channels = []
            
        # Define the GraphQL query
        query = """
        query StoreSearch {
          searchStoresByAddress(
            address: "%s"
            radiusMiles: %d
            fulfillmentChannels: %s
          ) {
            stores {
              distanceMiles
              nextAvailableTimeslot {
                timeslot
              }
              store {
                address {
                  locality
                  postalCode
                  region
                  streetAddress
                }
                name
                storeNumber
                __typename
              }
              __typename
            }
            __typename
          }
        }
        """ % (address, radius_miles, json.dumps(fulfillment_channels))
        
        # Remove whitespace for the actual request
        compact_query = " ".join(query.split())
        
        # Prepare the payload
        payload = {
            "query": compact_query,
            "variables": {}
        }
        
        # Make the request
        response = requests.post(self.url, headers=self.headers, json=payload)
        
        # Check for successful response
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    
    def process_stores(self, data: Dict[str, Any]) -> None:
        """
        Process and display store information from the API response
        
        Args:
            data: The API response data
        """
        if 'data' not in data:
            print("No data found in the response")
            return
            
        stores_data = data['data']['searchStoresByAddress']['stores']
        print(f"Found {len(stores_data)} stores:")
        
        for store_info in stores_data:
            print(f"\n{'-' * 50}")
            store = store_info['store']
            print(f"Store: {store['name']} (#{store['storeNumber']})")
            
            address = store['address']
            print(f"Address: {address['streetAddress']}, {address['locality']}, {address['region']} {address['postalCode']}")
            
            print(f"Distance: {store_info['distanceMiles']} miles")
            
            if store_info['nextAvailableTimeslot'] and store_info['nextAvailableTimeslot']['timeslot']:
                print(f"Next Available Timeslot: {store_info['nextAvailableTimeslot']['timeslot']}")
            else:
                print("Next Available Timeslot: None")
    
    def browse_category(self, 
                        category_id: str = "490113", 
                        store_id: int = 590, 
                        shopping_context: str = "CURBSIDE_PICKUP", 
                        limit: int = 15) -> Dict[str, Any]:
        """
        Make a GraphQL request to browse a specific category of products
        
        Args:
            category_id: The category ID to browse
            store_id: The store ID to check
            shopping_context: The shopping context (CURBSIDE_PICKUP, etc.)
            limit: Maximum number of products to return
            
        Returns:
            Dictionary containing the API response
        """
        # Define the GraphQL query
        query = """
        query {
          browseCategory(
            categoryId: "%s"
            storeId: %d
            shoppingContext: %s
            limit: %d
          ) {
            pageTitle
            records {
              id
              displayName
              minimumOrderQuantity
              maximumOrderQuantity
              productImageUrls {
                size
                url
              }
              bestAvailable
              onAd
              isNew
              isComboLoco
              deal
              pricedByWeight
              brand {
                name
                isOwnBrand
              }
              SKUs {
                id
                contextPrices {
                  context
                  isOnSale
                  unitListPrice {
                    unit
                    formattedAmount
                  }
                  priceType
                  listPrice {
                    unit
                    formattedAmount
                  }
                  salePrice {
                    formattedAmount
                  }
                }
                productAvailability
                skuPrice {
                  listPrice {
                    displayName
                  }
                }
              }
            }
            total
            hasMoreRecords
            nextCursor
            previousCursor
          }
        }
        """ % (category_id, store_id, shopping_context, limit)
        
        # Remove whitespace for the actual request
        compact_query = " ".join(query.split())
        
        # Prepare the payload
        payload = {
            "query": compact_query,
            "variables": {}
        }
        
        # Make the request
        response = requests.post(self.url, headers=self.headers, json=payload)
        
        # Check for successful response
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    
    def process_products(self, data: Dict[str, Any]) -> None:
        """
        Process and display product information from the API response
        
        Args:
            data: The API response data
        """
        if 'data' not in data:
            print("No data found in the response")
            return
            
        category_data = data['data']['browseCategory']
        print(f"Category: {category_data['pageTitle']}")
        print(f"Total products: {category_data['total']}")
        print(f"Has more records: {category_data['hasMoreRecords']}")
        print("\nProducts:")
        
        for product in category_data['records']:
            print(f"\n{'-' * 50}")
            print(f"Name: {product['displayName']}")
            print(f"Brand: {product['brand']['name']}")
            print(f"ID: {product['id']}")
            
            # Print the first SKU price info if available
            if product['SKUs'] and len(product['SKUs']) > 0:
                sku = product['SKUs'][0]
                if 'contextPrices' in sku and len(sku['contextPrices']) > 0:
                    price_info = sku['contextPrices'][0]
                    if 'listPrice' in price_info:
                        print(f"Price: {price_info['listPrice']['formattedAmount']}")
                    if price_info.get('isOnSale') and 'salePrice' in price_info:
                        print(f"Sale Price: {price_info['salePrice']['formattedAmount']}")
            
            # Print the first image URL if available
            if 'productImageUrls' in product and len(product['productImageUrls']) > 0:
                print(f"Image URL: {product['productImageUrls'][0]['url']}")
                
            print(f"On Ad: {product['onAd']}")
            print(f"New: {product['isNew']}")

def main():
    """
    Main function to demonstrate the HEB GraphQL client
    """
    client = HEBGraphQLClient()
    
    try:
        # Demonstrate category browsing
        print("\n===== BROWSING CATEGORY =====")
        print("Fetching category products...")
        category_response = client.browse_category()
        
        # Process and display products
        client.process_products(category_response)
        
        # Save raw JSON response to a file
        with open('heb_category_response.json', 'w') as f:
            json.dump(category_response, f, indent=2)
        print("\nRaw category response saved to heb_category_response.json")
        
        # Demonstrate store search
        print("\n\n===== SEARCHING STORES =====")
        print("Searching for stores near '1803 West Bronze St, Pharr, TX'...")
        store_response = client.search_stores_by_address()
        
        # Process and display stores
        client.process_stores(store_response)
        
        # Save raw JSON response to a file
        with open('heb_stores_response.json', 'w') as f:
            json.dump(store_response, f, indent=2)
        print("\nRaw stores response saved to heb_stores_response.json")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
