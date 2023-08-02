from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
# In case I make this work for other gamefront games
game_id = 8

transport = AIOHTTPTransport(url="https://ikora.gamefront.com/graphql")

client = Client(transport=transport, fetch_schema_from_transport=True)

catQuery = gql(
"""
query getGameCategories ($game:ID!) {
	game(id:$game){
		categories(parent:0){
            id
            name
            file_count
        }
	}
}
""")
r = client.execute(catQuery, {"game": game_id})
categories = r["game"]["categories"]
categorydict = {}
for category in categories:
    categorydict[category["name"].lower()] = category
    print(f"Name:\n{category['name']}\nFile Count:\n{category['file_count']}")
print("Choose a category:")
cat = input("- ").lower()
if cat in categorydict.keys():
    print(f"Selected {categorydict[cat]['name']}")
cat = categorydict[cat]
query = gql(
"""
query getFileDetails($id: ID!){
	file_category(id:$id){
        files{
            data{
                title
            }
        }
    }
}
""")
print(client.execute(query, {"id": cat["id"]}))