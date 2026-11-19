"""Plotting utilities for manuscript-ready figures."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def save_composite_indicator_figure(df: pd.DataFrame, path: Path) -> None:
    """Create Figure 1: selected composite indicators with Wilson CIs."""
    label_map = {
        "hukuki_bilgi_dogru": "Legal item keyed response",
        "hukuki_guvensizlik": "Legal insecurity",
        "hukuki_risk_ana_engel": "Legal risk as main barrier",
        "hukuki_prosedurel_cozum": "Legal/procedural solution preference",
    }
    fig_df = df[df["gosterge"].isin(label_map)].copy()
    fig_df["label"] = fig_df.apply(lambda r: f"{label_map[r['gosterge']]} ({int(r['n_pozitif'])}/{int(r['payda'])})", axis=1)
    fig_df = fig_df.set_index("gosterge").loc[list(label_map.keys())].reset_index()

    y = np.arange(len(fig_df))
    x = fig_df["yuzde"].to_numpy()
    xerr = np.vstack([x - fig_df["wilson95_alt"].to_numpy(), fig_df["wilson95_ust"].to_numpy() - x])

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.barh(y, x, color="#B9CDE5", zorder=2)
    ax.errorbar(x, y, xerr=xerr, fmt="o", color="#8B1A1A", ecolor="#8B1A1A", capsize=5, linewidth=1.7, zorder=4)
    ax.set_yticks(y, fig_df["label"])
    ax.set_xlabel("Percentage (%)")
    ax.set_xlim(0, 100)
    ax.set_title("Survey indicators with Wilson 95% CIs")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=600, bbox_inches="tight")
    plt.close(fig)


def save_solution_preferences_figure(df: pd.DataFrame, path: Path) -> None:
    """Create Figure 2: system-level solution preferences."""
    label_map = {
        "yasal_duzenleme_talebi": "Legal regulation",
        "dnr_protokol_talebi": "Written DNR/protocol form",
        "q6_C_etik_kurul_danismanlik": "Ethics consultation",
        "q6_D_hekim_egitimi": "Physician training",
        "q6_E_palyatif_bakim": "Palliative care strengthening",
    }
    rows = []
    for col, label in label_map.items():
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            rows.append({"label": label, "percent": (s.eq(1).sum() / len(s) * 100) if len(s) else np.nan})
    fig_df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.barh(np.arange(len(fig_df)), fig_df["percent"])
    ax.set_yticks(np.arange(len(fig_df)), fig_df["label"])
    ax.set_xlabel("Selected by participants (%)")
    ax.set_xlim(0, 100)
    ax.set_title("System-level solution preferences")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=600, bbox_inches="tight")
    plt.close(fig)


def save_legal_risk_solution_figure(df: pd.DataFrame, path: Path) -> None:
    """Create Figure 3: legal/procedural solution demand by legal risk barrier."""
    tmp = df[["hukuki_risk_ana_engel", "hukuki_prosedurel_cozum"]].dropna().copy()
    grouped = tmp.groupby("hukuki_risk_ana_engel")["hukuki_prosedurel_cozum"].mean().reindex([0, 1]) * 100
    counts = tmp.groupby("hukuki_risk_ana_engel")["hukuki_prosedurel_cozum"].agg(["sum", "count"]).reindex([0, 1])
    labels = [f"Legal risk not main barrier\n(n={int(counts.loc[0, 'count'])})", f"Legal risk main barrier\n(n={int(counts.loc[1, 'count'])})"]

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.bar(labels, grouped.values)
    ax.set_ylabel("Legal/procedural solution preference (%)")
    ax.set_ylim(0, 110)
    ax.set_title("Solution preference by perceived legal risk barrier")
    ax.grid(axis="y", alpha=0.25)
    for i, v in enumerate(grouped.values):
        if pd.notna(v):
            ax.text(i, v + 2, f"{int(counts.iloc[i]['sum'])}/{int(counts.iloc[i]['count'])} ({v:.1f}%)", ha="center", va="bottom")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=600, bbox_inches="tight")
    plt.close(fig)

