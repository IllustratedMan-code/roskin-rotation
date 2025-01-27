import requests
from importlib import resources
import pandas as pd
import json
from tqdm import tqdm


class ireceptorDown(Exception):
    def __init__(message="Api is down"):
        super().__init__(message)


class Requester:
    URLS = pd.read_csv(
        resources.files("metafetch.data").joinpath("ADC-registry.tsv"), sep="\t"
    )["URL"]

    def __init__(self, table):
        self.table = table
        self.table["repository_url"] = self.table["repository"].apply(
            lambda x: self.study_url(x)
        )

    def study_url(self, study):
        urls = self.URLS.apply(
            lambda x: study.lower()
            .replace("-", "")
            .replace("airr", "")
            .replace(" ", "")
            in x
        )
        d = pd.DataFrame({"urls": self.URLS, "isstudy": urls})
        d = d[d["isstudy"] == True]
        if len(d) > 0:
            d = d["urls"]
            return list(d + "/airr")

    def request(self, f, url, *args, **kwargs):
        r = f(url, *args, **kwargs)
        r.raise_for_status()
        return r

    def get_ok(self, url):
        url = url + "/v1"
        r = self.request(requests.get, url).json()
        if r["result"] != "success":
            raise (ireceptorDown)
        return True

    def post_sequences(self, repertoire_id, url):
        url += "/v1/rearrangement"
        filters = {
            "filters": {
                "op": "=",
                "content": {"field": "repertoire_id", "value": repertoire_id},
            },
            # "fields": ["sequence"],
        }
        print(json.dumps(filters, indent=4))
        r = self.request(requests.post, url, data=json.dumps(filters))
        print(json.dumps(r.json(), indent=4))


if __name__ == "__main__":
    # url = R.study_url("Roche")
    # print(R.get_ok(url))
    # print(R.post_sequences("62d183fab492a282420cde3c", url))

    from .select_control_studies import controlStudies

    c = controlStudies("ireceptor-human-IGH-1-13-2025.tsv")
    R = Requester(c.ireceptor_data)
    print(R.table)

    # d = c.studies_by_subjects.reset_index()
    # print(d.columns)
