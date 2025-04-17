HEB doesn't have documentation on their graphql endpoint - however you can dig through the network logs to find the names/values of common requests done by HEB which are exposed. 

Testing initially to search for stores by address, browsing the inventory of a specific store via a specific category. Hard coded to 'baking goods' currently, and storeId to the one nearest me. 

With these endpoints an agent could go through the checkout flow using only retrieved data from the queries and make the HTTP requests to fulfill the order. Not sure if HEB means to have these exposed,
mostly dug deeper to learn more about this:

https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/graphql.html#discovering-exposed-graphql-structures
