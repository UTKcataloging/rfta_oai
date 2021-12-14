import requests


class OAIGenerator:
    """Generates OAI from a UTK IIIF Collection"""
    def __init__(self, collection):
        self.collection = collection
        self.records = self.__read_collection()
        self.__process()

    def __read_collection(self):
        r = requests.get(self.collection).json()
        return [record['id'] for record in r['items']]

    def __process(self):
        for record in self.records:
            MODS(record)


class MODS:
    """Generates MODS from a UTK IIIF Manifest."""
    def __init__(self, manifest):
        self.manifest = manifest
        self.slug = self.__choose_slug()

    def __choose_slug(self):
        r = requests.get(self.manifest).json()
        label = r['label']['en'][0]
        slugified_label = label.lower().replace('interview with ', '').replace(',','').replace(' ','-')
        return f"https://rfta.lib.utk.edu/interviews/object/{slugified_label}/"

    def __test_slug(self):
        r = requests.get(self.slug)
        if r.status_code != 200:
            print(self.slug)
        return


if __name__ == "__main__":
    collection = "https://digital.lib.utk.edu/static/iiif/collections/rfta_completed.json"
    x = OAIGenerator(collection)
