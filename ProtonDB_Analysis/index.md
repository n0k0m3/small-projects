---
excerpt_separator: "<!--more-->"
categories:
  - Projects
tags:
  - ProtonDB
  - Jupyter
  - Plotly
  - Steam Deck
  - SteamOS
title: Analysis of ProtonDB Linux Distribution
last_modified_at: 2023-10-11
plotly: true
---

### Data Preprocessing

[Notebook link](https://github.com/n0k0m3/Personal-Setup/blob/main/ProtonDB_Analysis/analysis.ipynb)


### Cumulative Results


**Note:** On Dec 2nd 2019, ProtonDB contribute workflow changed to a questionnaire, subsequently changed the data structures. All data prior to this date are for reference only and should NOT be inferred.


#### Raw user counts per distro
{{< plotly json="protondb_data/protondb_user_count.json">}}
#### Normalized distro market share on ProtonDB
{{< plotly json="protondb_data/protondb_market_share.json">}}
#### Normalized distro market share on ProtonDB (Merged distro base)
{{< plotly json="protondb_data/protondb_market_share_base.json">}}
Arch Linux and Arch-based distro is on the rise, while Debian-based (Ubuntu) distros are on the decline.


### Steam Deck/SteamOS effect on ProtonDB market share analysis

Is there a shift due to Steam Deck and SteamOS? We'll filter from Jan 1st 2022 till now to see if there is a shift in the market share.
{{< plotly json="protondb_data/protondb_market_share_steamdeck.json">}}

Let's group the distro by their bases.
{{< plotly json="protondb_data/protondb_market_share_base_steamdeck.json">}}

As we can see, the market share graph doesn't show that there's any effect of Steam Deck release on ProtonDB user base. Let's check monthly increased user counts to see if there's any change.


#### Monthly delta of user counts

{{< plotly json="protondb_data/protondb_user_count_delta.json">}}
Debian and Fedora experienced a spike in new user count. More analysis on the market is needed.


{{< plotly json="protondb_data/protondb_user_count_delta_base.json">}}



Debian-based new installation is on a constant decline, while arch and "other" distros are on a rise. As the market share of "other" distros is not as significant as Debian or Arch derivatives, we won't go deeper into this category.


{{< plotly json="protondb_data/protondb_user_count_delta_base_steamdeck.json">}}


New install of both Arch and Debian-based distros is on plateau. So for now, the release of Steam Deck is not that big of a disruption. Interestingly, by the end of March there is a spike in installation of Fedora due to a beta release of Fedora 36.
