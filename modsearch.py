from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="https://ikora.gamefront.com/graphql")

client = Client(transport=transport, fetch_schema_from_transport=True)

catQuery = gql(
"""
{
	game(id:8){
		categories(parent:0){
            id
            name
            file_count
        }
	}
}
""")
r = client.execute(catQuery)
#print(r)
categories = r["game"]["categories"]
categorydict = {}
for category in categories:
    categorydict[category["name"].lower()] = category
    print(f"Name:\n{category['name']}\nFile Count:\n{category['file_count']}")
print("Choose a category:")
cat = input("- ")
if cat.lower() in categorydict.keys():
    print(f"Selected {categorydict[cat]['name']}")
cat = categorydict[cat]
query = gql(
"""
{
	file_category(id:%s){
        files{
            data{
                title
            }
        }
    }
}
""" % cat["id"])
print(client.execute(query))