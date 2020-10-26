# Import required modules.
from azure.cognitiveservices.search.websearch import WebSearchClient
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.search.entitysearch import EntitySearchClient

# Replace with your subscription key.
subscription_key = "bd29fed378d848988c6503af9ec7655f"
endpoint ="https://riccardo-doyle.cognitiveservices.azure.com/"

# Instantiate the client and replace with your endpoint.
client = WebSearchClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))

# Make a request. Replace Yosemite if you'd like.
web_data = client.web.search(query="assiteca")
print("\r\nSearched for Query# \" assiteca \"")
print(web_data)

'''
Web pages
If the search response contains web pages, the first result's name and url
are printed.
'''

if hasattr(web_data.web_pages, 'value'):
    #print("total search found:" ,web_data.web_pages.value[1])
    print("\r\nWebpage Results#{}".format(len(web_data.web_pages.value)))

    for i in range(len(web_data.web_pages.value)):
        first_web_page = web_data.web_pages.value[i]
        print('#'*30)
        #print(first_web_page)
        
        print("First web page name: {} ".format(first_web_page.name))
        print("First web page URL: {} ".format(first_web_page.url))
        print("first web page description: {}".format(first_web_page.snippet))    
        
else:
    print("Didn't find any web pages...")



'''
News
If the search response contains news, the first result's name and url
are printed.

if hasattr(web_data.news, 'value'):

    print("\r\nNews Results#{}".format(len(web_data.news.value)))

    first_news = web_data.news.value[0]
    print("First News name: {} ".format(first_news.name))
    print("First News URL: {} ".format(first_news.url))

else:
    print("Didn't find any news...")
'''
'''
def dominant_entity_lookup(subscription_key):
    """DominantEntityLookup.
    This will look up a single entity (Satya Nadella) and print out a short description about them.
    """
    client = EntitySearchClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )
    entity_data = client.entities.search(query="Satya Nadella")
    print(entity_data)
    try:
        entity_data = client.entities.search(query="Satya Nadella")
        print(entity_data)

        if entity_data.entities.value:
            # find the entity that represents the dominant one

            main_entities = [entity for entity in entity_data.entities.value
                             if entity.entity_presentation_info.entity_scenario == "DominantEntity"]

            if main_entities:
                print(
                    'Searched for "Satya Nadella" and found a dominant entity with this description:')
                print(main_entities[0].description)
            else:
                print("Couldn't find main entity Satya Nadella!")

        else:
            print("Didn't see any data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    dominant_entity_lookup(subscription_key)'''