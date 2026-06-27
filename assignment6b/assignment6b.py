first_name = "Benjamin"
last_name = "Branta"

# Import Required Packages
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D

# Task 1: Salary Statistics
# Subtask 1.1: Download and read the file
salary_df = pd.read_excel("2021_Salary Statistics by Employee.xlsx")


# Subtask 1.2: Salary vs years in job
# Make a scatterplot of salary (y) vs years in job (x), for the entire dataset.
# Have your code automatically save this figure as LAST_FIRST_assign6b_task1-2.png
#  (as always, replace "LAST_FIRST" with your own last and first name separated by a _).
plt.figure()
sns.scatterplot(salary_df, x="Years in Job", y="Annual Salary")
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task1-2.png", dpi=300, bbox_inches="tight"
)


# Subtask 1.3: Add a third data aspect to a scatterplot
plt.figure()
sns.scatterplot(
    data=salary_df,
    x="Years in Job",
    y="Annual Salary",
    hue="Pay Basis",
    style="Pay Basis",
    palette={
        "A": "#0072B2",  # Blue
        "H": "#E69F00",  # Orange
        "C": "#009E73",  # Bluish Green
    },
    markers={"A": "o", "H": "s", "C": "X"},
    s=40,  # marker size
    alpha=0.6,
)
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task1-3.png", dpi=300, bbox_inches="tight"
)


# Subtask 1.4: Violin plots of salaries
# Subtask 1.4.1
plt.figure()
sns.violinplot(
    data=salary_df,
    x="Pay Basis",
    y="Annual Salary",
    hue="Pay Basis",
    palette={
        "A": "#0072B2",  # Blue
        "H": "#E69F00",  # Orange
        "C": "#009E73",  # Bluish Green
    },
)
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task1-4-1.png", dpi=300, bbox_inches="tight"
)


# Subtask 1.4.2
plt.figure(figsize=(18, 6))  # increase size for plot visibility
# sort by median salary
order = (
    salary_df[salary_df["Empl Class Code"] == "FA"]
    .groupby("Sub Department")["Annual Salary"]
    .median()
    .sort_values(ascending=False)
    .index
)
# create the plot
sns.violinplot(
    data=salary_df[salary_df["Empl Class Code"] == "FA"],
    x="Sub Department",
    y="Annual Salary",
    hue="Sub Department",
    order=order,
    legend=False,
)
# modify plot
plt.xticks(rotation=90)
plt.title("Faculty Salaries by Academic Department")
plt.tight_layout()
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task1-4-2.png", dpi=300, bbox_inches="tight"
)


# Subtask 1.5: Stacked bars
plt.figure()
pay_basis = salary_df.pivot(columns="Pay Basis")
plt.hist(
    [
        pay_basis["Annual Salary"]["A"].dropna(),
        pay_basis["Annual Salary"]["C"].dropna(),
        pay_basis["Annual Salary"]["H"].dropna(),
    ],
    bins=30,
    stacked=True,
    label=["A", "C", "H"],
    color=[
        "#0072B2",  # Blue
        "#009E73",  # Bluish Green
        "#E69F00",  # Orange
    ],
)
plt.xlabel("Annual Salary")
plt.ylabel("Frequency")
plt.legend(title="Pay Basis")
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task1-5.png", dpi=300, bbox_inches="tight"
)


# Subtask 1.6: Claude
"""
Prompt: In the attached data set I am interested in understanding the relationships between "Years in Job", "Pay Basis", and "Annual Salary".
You are an expert in data visualizations using Python, Pandas, Matplotlib, and Seaborn. For this you should use seaborn.
What type of visualization do you suggest to help answer my question?
"""

# --- Load Data ---
# Update this path to wherever your file lives locally
df = pd.read_excel("2021_Salary Statistics by Employee.xlsx")

# --- Prep ---
pay_basis_labels = {"A": "Annual (A)", "C": "Contract (C)", "H": "Hourly (H)"}
df["Pay Basis Label"] = df["Pay Basis"].map(pay_basis_labels)

order = ["Annual (A)", "Contract (C)", "Hourly (H)"]

# Cap at 99th percentile to reduce outlier distortion on regression
cap = df["Annual Salary"].quantile(0.99)
df_plot = df[df["Annual Salary"] <= cap].copy()

# --- Plot ---
plt.figure()
sns.set_theme(style="whitegrid", font_scale=1.1)

g = sns.lmplot(
    data=df_plot,
    x="Years in Job",
    y="Annual Salary",
    col="Pay Basis Label",
    col_order=order,
    scatter_kws={"alpha": 0.35, "s": 25},
    line_kws={"color": "crimson", "linewidth": 2},
    ci=95,
    height=5,
    aspect=1.1,
)

g.set_titles(col_template="{col_name}", size=13, fontweight="bold")
g.set_axis_labels("Years in Job", "Annual Salary (USD)")

for ax in g.axes.flat:
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

g.figure.suptitle(
    "Annual Salary vs. Years in Job by Pay Basis\n2021 Employee Salary Data",
    y=1.03,
    fontsize=15,
    fontweight="bold",
)

plt.tight_layout()

# --- Save ---
output_path = f"{last_name}_{first_name}_assign6b_task1-6.png"
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"Figure saved to: {output_path}")


# Task 2: Housing Data
# Subtask 2.1: Load the data
housing_master_df = pd.read_csv("HPI_master.csv")

# Make a new variable housing_df, containing only the records in the set for which
#  the "level" is "MSA", and "hpi_flavor" is "all-transactions".
housing_df = housing_master_df[
    (housing_master_df["level"] == "MSA")
    & (housing_master_df["hpi_flavor"] == "all-transactions")
]


# Subtask 2.2: Plot time series of prices for list of places
def plot_price_for_places(df: pd.DataFrame, places: list) -> tuple:
    matching = df[
        df["place_name"].isin(places)
    ]  # filter dataframe to only places in list
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=matching,
        x=matching["yr"] + 0.25 * matching["period"],
        y="index_nsa",
        hue="place_name",
        ax=ax,
        errorbar=None,
    )
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (HPI)")
    ax.legend(title="Place")
    return (fig, ax)


places = [
    "Eau Claire, WI",
    "Lincoln, NE",
    "Bellingham, WA",
    "Phoenix-Mesa-Chandler, AZ",
]
plot_price_for_places(housing_df, places)
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task2-2-ec-li-bh-pmc.png",
    dpi=300,
    bbox_inches="tight",
)

plot_price_for_places(housing_df, ["Eau Claire, WI", "Madison, WI", "Green Bay, WI"])
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task2-2-WI.png", dpi=300, bbox_inches="tight"
)


# Subtask 2.3
def plot_price_hist(df: pd.DataFrame, t1: tuple, t2: tuple):
    year_1, period_1 = t1
    year_2, period_2 = t2

    # Filter to each time point
    data_t1 = df[(df["yr"] == year_1) & (df["period"] == period_1)][
        "index_nsa"
    ].dropna()
    data_t2 = df[(df["yr"] == year_2) & (df["period"] == period_2)][
        "index_nsa"
    ].dropna()

    # Fixed bin edges: width of 20, spanning 100–450
    bins = np.arange(100, 451, 20)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.hist(data_t1, bins=bins, color="steelblue", edgecolor="white", linewidth=0.4)
    ax1.set_xlabel(f"[thousands of $], {year_1} q{period_1}")
    ax1.set_ylabel("Frequency")

    ax2.hist(data_t2, bins=bins, color="steelblue", edgecolor="white", linewidth=0.4)
    ax2.set_xlabel(f"[thousands of $], {year_2} q{period_2}")
    ax2.set_ylabel("Frequency")

    plt.tight_layout()
    return fig, (ax1, ax2)


plot_price_hist(housing_df, (2010, 1), (2020, 1))
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task2-3.png", dpi=300, bbox_inches="tight"
)


# Subtask 2.4: Choose your own visualization

# 2. Compute Year-over-Year (YoY) growth per MSA
#    Shift within the same quarter (period) to avoid seasonal distortion:
#    e.g. Q1 2020 is compared to Q1 2019, not Q4 2019.
# ---------------------------------------------------------------------------
housing_df_vol = housing_df.sort_values(["place_name", "yr", "period"])

housing_df_vol["index_lag"] = housing_df_vol.groupby(["place_name", "period"])[
    "index_nsa"
].shift(1)

housing_df_vol["yoy_growth"] = (
    (housing_df_vol["index_nsa"] - housing_df_vol["index_lag"])
    / housing_df_vol["index_lag"]
    * 100
)

# ---------------------------------------------------------------------------
# 3. Per-MSA risk / reward summary
#    - Reward  = mean YoY growth over the full history
#    - Risk    = standard deviation of YoY growth (volatility)
#    Require >= 20 YoY observations so sparse MSAs don't skew results.
# ---------------------------------------------------------------------------
stats = (
    housing_df_vol.groupby("place_name")["yoy_growth"]
    .agg(avg_yoy="mean", std_yoy="std", count="count")
    .dropna()
)
stats = stats[stats["count"] >= 20].copy()

# ---------------------------------------------------------------------------
# 4. Assign each MSA to a quadrant
#    Boundaries are the medians — more robust to outliers than the mean.
#
#    Quadrant layout:
#      HIGH growth / LOW  vol  →  Sweet Spot              (top-left)
#      HIGH growth / HIGH vol  →  High Risk / High Reward (top-right)
#      LOW  growth / LOW  vol  →  Slow & Steady           (bottom-left)
#      LOW  growth / HIGH vol  →  Worst of Both           (bottom-right)
# ---------------------------------------------------------------------------
med_x = stats["std_yoy"].median()  # volatility split
med_y = stats["avg_yoy"].median()  # growth split

quad_map = {
    (True, True): "Sweet Spot",
    (True, False): "High Risk / High Reward",
    (False, True): "Slow & Steady",
    (False, False): "Worst of Both",
}

stats["quadrant"] = stats.apply(
    lambda r: quad_map[(r["avg_yoy"] >= med_y, r["std_yoy"] < med_x)],
    axis=1,
)

# ---------------------------------------------------------------------------
# 5. Visual settings
# ---------------------------------------------------------------------------
quad_palette = {
    "Sweet Spot": "#2ecc71",  # green
    "High Risk / High Reward": "#e67e22",  # orange
    "Slow & Steady": "#3498db",  # blue
    "Worst of Both": "#e74c3c",  # red
}
quad_order = [
    "Sweet Spot",
    "High Risk / High Reward",
    "Slow & Steady",
    "Worst of Both",
]

# ---------------------------------------------------------------------------
# 6. Identify best (★) and worst (▼) MSA per quadrant by avg YoY growth
# ---------------------------------------------------------------------------
label_rows = []
for q, grp in stats.groupby("quadrant"):
    label_rows.append((grp.loc[grp["avg_yoy"].idxmax()], q, "best"))
    label_rows.append((grp.loc[grp["avg_yoy"].idxmin()], q, "worst"))

# ---------------------------------------------------------------------------
# 7. Draw the plot
# ---------------------------------------------------------------------------
sns.set_theme(style="whitegrid", font_scale=1.05)
fig, ax = plt.subplots(figsize=(13, 8))

# -- Scatter: one point per MSA, coloured by quadrant --------------------
sns.scatterplot(
    data=stats,
    x="std_yoy",
    y="avg_yoy",
    hue="quadrant",
    hue_order=quad_order,
    palette=quad_palette,
    alpha=0.55,
    s=45,
    linewidth=0.3,
    edgecolor="white",
    ax=ax,
    legend=False,  # custom legend built below
)

# -- Quadrant divider lines ----------------------------------------------
ax.axvline(med_x, color="#555555", linewidth=1.2, linestyle="--", zorder=2)
ax.axhline(med_y, color="#555555", linewidth=1.2, linestyle="--", zorder=2)

# -- Shaded quadrant backgrounds -----------------------------------------
xmin, xmax = ax.get_xlim()
ymin, ymax = ax.get_ylim()

shade_alpha = 0.06
ax.fill_betweenx(
    [med_y, ymax], xmin, med_x, color=quad_palette["Sweet Spot"], alpha=shade_alpha
)
ax.fill_betweenx(
    [med_y, ymax],
    med_x,
    xmax,
    color=quad_palette["High Risk / High Reward"],
    alpha=shade_alpha,
)
ax.fill_betweenx(
    [ymin, med_y], xmin, med_x, color=quad_palette["Slow & Steady"], alpha=shade_alpha
)
ax.fill_betweenx(
    [ymin, med_y], med_x, xmax, color=quad_palette["Worst of Both"], alpha=shade_alpha
)

# -- Quadrant corner text labels -----------------------------------------
x_pad = (xmax - xmin) * 0.01
y_pad = (ymax - ymin) * 0.02

corner_positions = {
    "Sweet Spot": (xmin + x_pad, med_y + y_pad, "left", "bottom"),
    "High Risk / High Reward": (xmax - x_pad, med_y + y_pad, "right", "bottom"),
    "Slow & Steady": (xmin + x_pad, ymin + y_pad, "left", "bottom"),
    "Worst of Both": (xmax - x_pad, ymin + y_pad, "right", "bottom"),
}
for q, (x, y, ha, va) in corner_positions.items():
    ax.text(
        x,
        y,
        q,
        color=quad_palette[q],
        fontsize=9.5,
        fontweight="bold",
        ha=ha,
        va=va,
        alpha=0.85,
        zorder=4,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", alpha=0.55, ec="none"),
    )

# -- Median crosshair labels ---------------------------------------------
ax.text(
    med_x + 0.07,
    ymin + 0.04,
    f"Median vol\n{med_x:.1f}%",
    fontsize=8,
    color="#555555",
    va="bottom",
)
ax.text(
    xmin + 0.07,
    med_y + 0.04,
    f"Median growth {med_y:.1f}%",
    fontsize=8,
    color="#555555",
    va="bottom",
)

# -- Annotate best & worst MSA per quadrant ------------------------------
already_labeled = set()
for row, q, kind in label_rows:
    name = row.name
    if name in already_labeled:
        continue
    already_labeled.add(name)

    city = name.split(",")[0]
    state = name.split(",")[1].strip().split(" ")[0] if "," in name else ""
    short = city[:20] + "…" if len(city) > 22 else city
    marker = "[+]" if kind == "best" else "[-]"

    ax.annotate(
        f"{marker} {short}, {state}",
        xy=(row["std_yoy"], row["avg_yoy"]),
        xytext=(8, 4),
        textcoords="offset points",
        fontsize=7.5,
        color=quad_palette[q],
        fontweight="bold",
        arrowprops=dict(arrowstyle="-", color=quad_palette[q], lw=0.8),
        zorder=5,
    )

# -- Custom legend -------------------------------------------------------
quad_handles = [mpatches.Patch(color=quad_palette[q], label=q) for q in quad_order]
marker_handles = [
    Line2D(
        [0],
        [0],
        marker="o",
        color="gray",
        markersize=7,
        linestyle="None",
        label="[+] Best in quadrant (highest avg growth)",
    ),
    Line2D(
        [0],
        [0],
        marker="o",
        color="gray",
        markersize=7,
        linestyle="None",
        label="[-] Worst in quadrant (lowest avg growth)",
    ),
]
ax.legend(
    handles=quad_handles + marker_handles,
    loc="upper left",
    fontsize=8.5,
    framealpha=0.85,
)

# -- Axis labels & title -------------------------------------------------
ax.set_xlabel("Volatility — Std. Dev. of Year-over-Year Growth (%)", fontsize=12)
ax.set_ylabel("Reward — Mean Year-over-Year Growth (%)", fontsize=12)
ax.set_title(
    "Housing Risk vs. Reward by MSA (1975–2022)\n"
    "Each point = one Metropolitan Statistical Area",
    fontsize=13,
    fontweight="bold",
    pad=14,
)

ax.grid(True, linestyle=":", alpha=0.4, zorder=1)
plt.tight_layout()

# ---------------------------------------------------------------------------
# 8. Save
# ---------------------------------------------------------------------------
plt.savefig(
    f"{last_name}_{first_name}_assign6b_task2-4.png", dpi=300, bbox_inches="tight"
)
