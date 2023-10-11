import pandas as pd
import plotly.express as px
import os
import shutil

# import plotly.io as pio
# pio.renderers.default = "iframe"

px.defaults.width = 600
px.defaults.height = 400

# Read the data
df_report = pd.read_hdf("proton_db_os.hdf5", "df")

# Write plots to json
os.makedirs("./analysis", exist_ok=True)


fig = px.line(
    df_report[df_report["date"] > pd.to_datetime("dec-1-2019")],
    x="date",
    y=df_report.columns.drop(["date"]),
    title="ProtonDB user count by Distro",
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="User Count",
    legend_title="Distro",
)
fig.write_json("./analysis/protondb_user_count.json")


fig = px.area(
    df_report[df_report["date"] > pd.to_datetime("dec-1-2019")],
    x="date",
    y=df_report.columns.drop(["date"]),
    groupnorm="percent",
    title="Distro Market Share on ProtonDB",
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Market Share (%)",
    legend_title="Distro",
)
fig.write_json("./analysis/protondb_market_share.json")


arch_based = ["Arch", "Manjaro", "SteamOS"]
debian_based = ["Linux Mint", "Ubuntu", "Pop!_OS", "Debian"]
normalizedDataFrame_combined = df_report.copy()
normalizedDataFrame_combined["Arch-based"] = normalizedDataFrame_combined[
    arch_based
].sum(axis=1)
normalizedDataFrame_combined = normalizedDataFrame_combined.drop(columns=arch_based)
normalizedDataFrame_combined["Debian-based"] = normalizedDataFrame_combined[
    debian_based
].sum(axis=1)
normalizedDataFrame_combined = normalizedDataFrame_combined.drop(columns=debian_based)


fig = px.area(
    normalizedDataFrame_combined[
        normalizedDataFrame_combined["date"] > pd.to_datetime("dec-1-2019")
    ],
    x="date",
    y=normalizedDataFrame_combined.columns.drop(["date"]),
    groupnorm="percent",
    title="Distro-base Market Share on ProtonDB",
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Market Share (%)",
    legend_title="Distro",
)
fig.write_json("./analysis/protondb_market_share_base.json")


fig = px.area(
    df_report[df_report["date"] > pd.to_datetime("jan-1-2022")],
    x="date",
    y=df_report.columns.drop(["date"]),
    groupnorm="percent",
    title="Distro Market Share on ProtonDB from 01/01/2022",
    markers=True,
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Market Share (%)",
    legend_title="Distro",
)
fig.write_json("./analysis/protondb_market_share_steamdeck.json")


fig = px.area(
    normalizedDataFrame_combined[
        normalizedDataFrame_combined["date"] > pd.to_datetime("jan-1-2022")
    ],
    x="date",
    y=normalizedDataFrame_combined.columns.drop(["date"]),
    groupnorm="percent",
    title="Distro-base Market Share on ProtonDB from 01/01/2022",
    markers=True,
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Market Share (%)",
    legend_title="Distro",
)
fig.write_json("./analysis/protondb_market_share_base_steamdeck.json")


df_delta = df_report.sort_values(by="date", ascending=False) - df_report.sort_values(
    by="date", ascending=False
).shift(-1)
df_delta.pop("date")
df_delta["date"] = df_report["date"]
df_delta = df_delta[df_delta["date"] > pd.to_datetime("dec-2-2019")]
fig = px.line(
    df_delta,
    x="date",
    y=df_delta.columns.drop(["date"]),
    title="ProtonDB monthly user count change per Distro",
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="User Count",
    legend_title="Distro",
)
fig.write_json("./analysis/protondb_user_count_delta.json")


normalizedDataFrame_combined = df_delta.copy()
normalizedDataFrame_combined["Arch-based"] = normalizedDataFrame_combined[
    arch_based
].sum(axis=1)
normalizedDataFrame_combined = normalizedDataFrame_combined.drop(columns=arch_based)
normalizedDataFrame_combined["Debian-based"] = normalizedDataFrame_combined[
    debian_based
].sum(axis=1)
normalizedDataFrame_combined = normalizedDataFrame_combined.drop(columns=debian_based)


fig = px.line(
    normalizedDataFrame_combined,
    x="date",
    y=normalizedDataFrame_combined.columns.drop(["date"]),
    title="ProtonDB monthly user count change per Distro-base",
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="User Count",
    legend_title="Distro",
)
fig.write_json("./analysis/protondb_user_count_delta_base.json")


fig = px.line(
    normalizedDataFrame_combined[
        normalizedDataFrame_combined["date"] > pd.to_datetime("01/01/2022")
    ],
    x="date",
    y=normalizedDataFrame_combined.columns.drop(["date"]),
    title="Monthly user count change per Distro-base from 01/01/2022",
    markers=True,
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="User Count",
    legend_title="Distro",
)
fig.write_json("./analysis/protondb_user_count_delta_base_steamdeck.json")

# Copy files to correct path for jekyll
shutil.copytree("analysis", "../../../_includes/protondb_data", dirs_exist_ok=True)
