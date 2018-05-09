
import sphinxapi

if __name__ == "__main__":
    client = sphinxapi.SphinxClient()
    client.SetServer('localhost', 9312)
    client.SetMatchMode(sphinxapi.SPH_MATCH_ALL)
    print(client.Query('Washington', 'news1gb'))
    print(client.RunQueries())
