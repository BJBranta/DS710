"""
ec_house_prices.py
------------------
Synthetic Eau Claire, WI house price generator.

Models price as a function of (latitude, longitude) using a Gaussian Mixture
Model (GMM) whose components are anchored at real neighborhood centroids.
Prices are calibrated to 2025 Zillow/Redfin medians (~$290K city-wide).

Two modifiers are layered on top of the GMM signal:
  - Flood/river penalty: proximity to the Chippewa River suppresses price.
  - Highway accessibility bonus: proximity to the Hwy 53 corridor (south side)
    modestly boosts price.

Noise is log-normal so the price distribution is right-skewed, as in reality.

Usage
-----
    python ec_house_prices.py              # sample 100 points, show plots
    python ec_house_prices.py --n 500      # sample 500 points
    python ec_house_prices.py --n 200 --seed 99 --csv out.csv

Functions
---------
    price_at(lat, lon) -> float
        Return the expected (noise-free) price at a single coordinate.

    sample(n, seed) -> pd.DataFrame
        Return a DataFrame of n sampled (lat, lon, price) rows.
"""

import argparse
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ---------------------------------------------------------------------------
# City bounding box (WGS-84)
# ---------------------------------------------------------------------------
LAT_MIN, LAT_MAX = 44.770, 44.840
LON_MIN, LON_MAX = -91.560, -91.450


# ---------------------------------------------------------------------------
# GMM components
# Each entry: (lat, lon, median_price_usd, sigma_lat, sigma_lon, weight)
# Prices grounded in 2025 Redfin/Zillow/NeighborhoodScout data.
# Covariances are isotropic in degree-space; ~0.01 deg ≈ ~1 km in WI.
# Weights are unnormalized — normalised automatically below.
# ---------------------------------------------------------------------------
_COMPONENTS_RAW = [
    # name                  lat       lon      price    s_lat  s_lon  w
    ("South Side/Oakwood",  44.774, -91.497, 355_000, 0.012, 0.016, 1.4),
    ("West Eau Claire",     44.800, -91.540, 295_000, 0.014, 0.014, 1.2),
    ("Downtown/Barstow",    44.812, -91.497, 265_000, 0.008, 0.008, 0.9),
    ("Randall Park/3rd Wd", 44.818, -91.510, 250_000, 0.010, 0.010, 1.0),
    ("Eastside Hill",       44.815, -91.482, 280_000, 0.010, 0.012, 1.0),
    ("North Side",          44.830, -91.500, 272_000, 0.012, 0.014, 0.9),
    ("UWEC / Lower East",   44.806, -91.490, 235_000, 0.008, 0.010, 0.7),
    ("Cannery/River West",  44.808, -91.505, 260_000, 0.007, 0.008, 0.6),
]

# Build arrays for vectorised computation
_N_COMP = len(_COMPONENTS_RAW)
_MU_LAT  = np.array([r[1] for r in _COMPONENTS_RAW])
_MU_LON  = np.array([r[2] for r in _COMPONENTS_RAW])
_PRICES  = np.array([r[3] for r in _COMPONENTS_RAW], dtype=float)
_LOG_P   = np.log(_PRICES)          # work in log-price space
_S_LAT   = np.array([r[4] for r in _COMPONENTS_RAW])
_S_LON   = np.array([r[5] for r in _COMPONENTS_RAW])
_W_RAW   = np.array([r[6] for r in _COMPONENTS_RAW], dtype=float)
_WEIGHTS = _W_RAW / _W_RAW.sum()   # normalise


# ---------------------------------------------------------------------------
# Chippewa River – approximate centerline as a sequence of (lat, lon) waypoints
# ---------------------------------------------------------------------------
_RIVER_WAYPOINTS = np.array([
    [44.778, -91.543],
    [44.790, -91.530],
    [44.800, -91.518],
    [44.810, -91.510],
    [44.815, -91.500],
    [44.818, -91.488],
    [44.820, -91.475],
])

# Hwy 53 corridor (north–south, west side of city)
_HWY53_WAYPOINTS = np.array([
    [44.771, -91.502],
    [44.790, -91.500],
    [44.810, -91.498],
    [44.830, -91.496],
])


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _haversine_km(lat1, lon1, lat2, lon2):
    """Vectorised haversine distance in km. Inputs may be scalars or arrays."""
    R = 6371.0
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + (
        np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    )
    return R * 2 * np.arcsin(np.sqrt(a))


def _min_dist_to_polyline_km(lat, lon, waypoints):
    """
    Minimum haversine distance (km) from point (lat, lon) to a polyline
    defined by waypoints (N x 2 array of [lat, lon]).
    Approximates each segment as a point-to-point minimum.
    """
    dists = _haversine_km(lat, lon, waypoints[:, 0], waypoints[:, 1])
    return float(np.min(dists))


# ---------------------------------------------------------------------------
# GMM posterior responsibilities at a point
# ---------------------------------------------------------------------------

def _responsibilities(lat, lon):
    """
    Return the GMM posterior weight vector w_k(lat, lon).
    Shape: (_N_COMP,)
    """
    z_lat = (lat - _MU_LAT) / _S_LAT
    z_lon = (lon - _MU_LON) / _S_LON
    log_gauss = -0.5 * (z_lat ** 2 + z_lon ** 2)
    log_gauss -= np.log(2 * np.pi * _S_LAT * _S_LON)   # normalisation
    log_resp = np.log(_WEIGHTS) + log_gauss
    # Softmax-style normalisation in log space for numerical stability
    log_resp -= log_resp.max()
    resp = np.exp(log_resp)
    return resp / resp.sum()


# ---------------------------------------------------------------------------
# Price modifiers
# ---------------------------------------------------------------------------

def _river_modifier(lat, lon):
    """
    Log-price penalty for proximity to the Chippewa River.
    Within 0.5 km: up to -8% penalty. Tapers to 0 at 3 km.
    """
    d_km = _min_dist_to_polyline_km(lat, lon, _RIVER_WAYPOINTS)
    penalty = -0.08 * np.exp(-d_km / 1.5)   # ~-8% at river's edge
    return penalty                            # in log-price units


def _highway_modifier(lat, lon):
    """
    Log-price bonus for accessibility to Hwy 53 (south-side corridor).
    Bonus peaks within ~1 km, fades beyond 4 km.
    Only applies south of lat 44.800 to avoid boosting north neighbourhoods.
    """
    if lat > 44.800:
        return 0.0
    d_km = _min_dist_to_polyline_km(lat, lon, _HWY53_WAYPOINTS)
    bonus = 0.04 * np.exp(-d_km / 2.0)      # up to +4% near corridor
    return bonus


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def price_at(lat, lon):
    """
    Return the expected (noise-free) house price at (lat, lon).

    Parameters
    ----------
    lat : float  – WGS-84 latitude  (44.77 – 44.84 for Eau Claire)
    lon : float  – WGS-84 longitude (-91.56 – -91.45 for Eau Claire)

    Returns
    -------
    float – predicted price in USD
    """
    resp = _responsibilities(lat, lon)
    log_price_gmm = float(np.dot(resp, _LOG_P))
    log_price = log_price_gmm + _river_modifier(lat, lon) + _highway_modifier(lat, lon)
    return float(np.exp(log_price))


def sample(n=100, seed=42):
    """
    Sample n (lat, lon, price) observations from the model.

    Locations are drawn uniformly within the Eau Claire bounding box.
    Prices are the GMM+modifier mean corrupted by log-normal noise
    (sigma = 0.18 in log space ≈ ±18% on a log scale, ~$50K at median).

    Parameters
    ----------
    n    : int – number of samples
    seed : int – random seed for reproducibility

    Returns
    -------
    pd.DataFrame with columns ['lat', 'lon', 'price']
    """
    rng = np.random.default_rng(seed)
    lats = rng.uniform(LAT_MIN, LAT_MAX, size=n)
    lons = rng.uniform(LON_MIN, LON_MAX, size=n)

    log_sigma = 0.18   # noise in log-price space
    prices = np.array([
        np.exp(np.log(price_at(la, lo)) + rng.normal(0, log_sigma))
        for la, lo in zip(lats, lons)
    ])

    return pd.DataFrame({"lat": lats, "lon": lons, "price": prices})


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------

def _build_surface(grid_res=40):
    """Return lat grid, lon grid, and price surface arrays for plotting."""
    lats = np.linspace(LAT_MIN, LAT_MAX, grid_res)
    lons = np.linspace(LON_MIN, LON_MAX, grid_res)
    lon_grid, lat_grid = np.meshgrid(lons, lats)   # shape (grid_res, grid_res)
    price_grid = np.vectorize(price_at)(lat_grid, lon_grid)
    return lat_grid, lon_grid, price_grid


def plot_3d(df, show=True):
    """
    Render two Plotly 3D traces on a shared figure:
      1. Smooth GMM surface  (expected price, no noise)
      2. Sampled scatter     (noisy observations)

    Parameters
    ----------
    df   : pd.DataFrame from sample()
    show : bool – call fig.show() if True; always returns the figure object

    Returns
    -------
    plotly.graph_objects.Figure
    """
    lat_g, lon_g, price_g = _build_surface()

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "scene"}, {"type": "scene"}]],
        subplot_titles=["GMM Price Surface (expected)", "Sampled Observations"],
    )

    # --- Surface ---
    surface = go.Surface(
        x=lon_g,
        y=lat_g,
        z=price_g,
        colorscale="RdYlGn",
        colorbar=dict(title="Price (USD)", x=0.45, len=0.8),
        opacity=0.85,
        name="Expected price",
        showscale=True,
        scene="scene1",
    )

    # --- Scatter ---
    scatter = go.Scatter3d(
        x=df["lon"],
        y=df["lat"],
        z=df["price"],
        mode="markers",
        marker=dict(
            size=4,
            color=df["price"],
            colorscale="RdYlGn",
            colorbar=dict(title="Price (USD)", x=1.02, len=0.8),
            showscale=True,
            opacity=0.85,
        ),
        name="Sampled prices",
        scene="scene2",
    )

    fig.add_trace(surface, row=1, col=1)
    fig.add_trace(scatter, row=1, col=2)

    axis_style = dict(
        backgroundcolor="rgb(230,230,230)",
        gridcolor="white",
        showbackground=True,
        zerolinecolor="white",
    )

    fig.update_layout(
        title=dict(
            text="Synthetic Eau Claire, WI House Prices",
            font=dict(size=18),
            x=0.5,
        ),
        scene1=dict(
            xaxis=dict(title="Longitude", **axis_style),
            yaxis=dict(title="Latitude",  **axis_style),
            zaxis=dict(title="Price (USD)", **axis_style),
        ),
        scene2=dict(
            xaxis=dict(title="Longitude", **axis_style),
            yaxis=dict(title="Latitude",  **axis_style),
            zaxis=dict(title="Price (USD)", **axis_style),
        ),
        height=650,
        margin=dict(l=0, r=0, t=60, b=0),
    )

    if show:
        fig.show()
    return fig


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args():
    parser = argparse.ArgumentParser(
        description="Generate synthetic Eau Claire house price data."
    )
    parser.add_argument(
        "--n", type=int, default=100,
        help="Number of samples to generate (default: 100)."
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility (default: 42)."
    )
    parser.add_argument(
        "--csv", type=str, default=None,
        help="Optional path to save samples as a CSV file."
    )
    parser.add_argument(
        "--no-plot", action="store_true",
        help="Skip the Plotly visualisation."
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    print(f"Sampling {args.n} observations (seed={args.seed}) ...")
    df = sample(n=args.n, seed=args.seed)

    print(df.describe().to_string())
    print(f"\nMedian price: ${df['price'].median():,.0f}")

    if args.csv:
        df.to_csv(args.csv, index=False)
        print(f"Saved {len(df)} rows to {args.csv}")

    if not args.no_plot:
        plot_3d(df, show=True)


if __name__ == "__main__":
    main()

# %%
