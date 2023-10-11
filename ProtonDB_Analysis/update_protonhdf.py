import os
import pandas as pd
import glob
import tarfile
import json


def find_distro(string):
    # Find the distro in the string based on string matching
    os_str = string.split(" ")[0]

    distros = ["ubuntu", "manjaro", "arch", "pop!_os", "debian", "fedora", "linux mint", "steamos"]

    if os_str.lower() not in distros and len(string.split(" ")) > 1:
        os_str += " " + string.split(" ")[1]

    manjaro_based = ["manjaro"]
    if any(x in os_str.lower() for x in manjaro_based):
        os_str = "Manjaro"

    arch_based = ["arc", "antergos", "gamer", "ctlos", "artix", "endeavour"]
    if any(x in os_str.lower() for x in arch_based):
        os_str = "Arch"

    ubuntu_based = ["kde", "elementary", "zorin", "ubuntu"]
    if any(x in os_str.lower() for x in ubuntu_based):
        os_str = "Ubuntu"

    mint_based = ["lmde", "mint"]
    if any(x in os_str.lower() for x in mint_based):
        os_str = "Linux Mint"

    pop_based = ["pop"]
    if any(x in os_str.lower() for x in pop_based):
        os_str = "Pop!_OS"

    #     suse_based = ["suse"]
    #     if any(x in os_str.lower() for x in suse_based):
    #         os_str = "OpenSUSE"

    #     flatpack = ["freedesktop"]
    #     if any(x in os_str.lower() for x in flatpack):
    #         os_str = "Flatpak"

    debian_based = [
        "siduction",
        "sparky",
        "devuan",
        "mx",
        "deepin",
        "debian",
    ]
    if any(x in os_str.lower() for x in debian_based):
        os_str = "Debian"

    fedora_based = ["fedora"]
    if any(x in os_str.lower() for x in fedora_based):
        os_str = "Fedora"

    steamos_based = ["steamos"]
    if any(x in os_str.lower() for x in steamos_based):
        os_str = "SteamOS"

    if os_str.lower() not in distros:
        os_str = "Others"

    return os_str


def read_os_from_tar(path):
    with tarfile.open(path, "r") as f:
        data = f.extractfile("reports_piiremoved.json").read()
    data = json.loads(data)
    data = pd.DataFrame(data)

    date_str = os.path.split(path)[1][8:-7]
    month = date_str[:3]
    day = date_str[3]
    year = date_str[5:]
    date_str = pd.to_datetime("-".join([month, day, year]))

    if date_str >= pd.to_datetime("dec-2-2019"):
        df = pd.json_normalize(data["systemInfo"])
    else:
        df = data.dropna(subset=["os"]).copy()

    df["os"] = df["os"].apply(find_distro)
    os_data = df["os"].value_counts()

    os_df = pd.DataFrame(os_data).transpose().reset_index(drop=True)
    os_df["date"] = date_str

    return os_df


df_report = pd.DataFrame(
    read_os_from_tar("protondb-data/reports/reports_dec2_2019.tar.gz")
)

for path in glob.glob("protondb-data/reports/*.gz"):
    date_str = os.path.split(path)[1][8:-7]
    month = date_str[:3]
    day = date_str[3]
    year = date_str[5:]
    date_str = pd.to_datetime("-".join([month, day, year]))
    if date_str not in df_report["date"].to_numpy():
        try:
            df_temp = read_os_from_tar(path)
        except:
            continue
        df_report = pd.concat([df_report, df_temp], ignore_index=True)
df_report = df_report.sort_values(by=["date"])
df_report.to_hdf("proton_db_os.hdf5", "df", mode="w")
