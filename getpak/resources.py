import json
import importlib.resources as importlib_resources


def load_s2projgrid():
    # CRS projection information
    path = importlib_resources.files("getpak").joinpath("data/s2_proj_ref.json")
    with path.open("rb") as fp:
        return json.loads(fp.read())

def load_owts_spy_s2_b1_7():
    path = importlib_resources.files("getpak").joinpath("data/means_OWT_Spyrakos_S2A_B1-7.json")
    with path.open("rb") as fp:
        return dict(json.loads(fp.read()))

def load_owts_spy_s2_b2_7():
    path = importlib_resources.files("getpak").joinpath("data/means_OWT_Spyrakos_S2A_B2-7.json")
    with path.open("rb") as fp:
        return dict(json.loads(fp.read()))

def load_owts_spm_s2_b1_8a():
    path = importlib_resources.files("getpak").joinpath("data/Means_OWT_Cordeiro_S2A_SPM.json")
    with path.open("rb") as fp:
        return dict(json.loads(fp.read()))

def load_owts_spm_s2_b2_8a():
    path = importlib_resources.files("getpak").joinpath("data/Means_OWT_Cordeiro_S2A_SPM_B2-8A.json")
    with path.open("rb") as fp:
        return dict(json.loads(fp.read()))