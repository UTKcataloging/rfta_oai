import requests


class OAIGenerator:
    """Generates OAI from a UTK IIIF Collection"""
    def __init__(self, collection):
        self.collection = collection
        self.records = self.__read_collection()

    def __read_collection(self):
        r = requests.get(self.collection).json()
        return [record for record in r['items']]


if __name__ == "__main__":
    collection = "https://digital.lib.utk.edu/static/iiif/collections/rfta_completed.json"
    x = OAIGenerator(collection)
