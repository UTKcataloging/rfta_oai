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
        self.manifest_id = manifest
        self.manifest = requests.get(self.manifest_id).json()
        self.slug = self.__choose_slug()
        self.pid = self.__get_pid()
        self.mods_path = f"https://digital.lib.utk.edu/collections/islandora/object/{self.pid}/datastream/MODS"
        self.final_mods = self.__get_islandora_mods()

    def __choose_slug(self):
        label = self.manifest['label']['en'][0]
        slugified_label = label.lower().replace('interview with ', '').replace(',','').replace(' ','-')
        return f"https://rfta.lib.utk.edu/interviews/object/{slugified_label}/"

    def __test_slug(self):
        r = requests.get(self.slug)
        if r.status_code != 200:
            print(self.slug)
        return

    def __get_pid(self):
        split_value = self.manifest_id.split('/')
        return(f"{split_value[5]}:{split_value[6]}")

    def __get_islandora_mods(self):
        r = requests.get(self.mods_path)
        original_mods = r.content.decode('utf-8')
        mods_minus_close = original_mods.replace('</mods>\n', '').replace('</mods>', '')
        final_mods = f"{mods_minus_close}\n{self.__add_location_node()}\n</mods>\n"
        return final_mods.replace('\n\n', '\n')

    def __add_location_node(self):
        node = f"""   <location>\n      <physicalLocation>University of Tennessee, Knoxville. Special Collections</physicalLocation>\n      <url access="object in context" usage="primary display">{self.slug}</url>\n      <url access="preview">https://digital.lib.utk.edu/collections/islandora/object/{self.pid}/datastream/TN/view</url>\n   </location>"""
        return node

    def download(self):
        with open(f'output/{self.pid.replace(":", "_")}.xml', 'w') as my_mods:
            my_mods.write(self.final_mods)

if __name__ == "__main__":
    # collection = "https://digital.lib.utk.edu/static/iiif/collections/rfta_completed.json"
    # x = OAIGenerator(collection)
    mods = MODS('https://digital.lib.utk.edu/assemble/manifest/rfta/6')
    mods.download()
