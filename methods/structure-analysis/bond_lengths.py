#!/usr/bin/env python3
"""Periodic neighbour-distance distributions and minima for ASE-readable structures."""

import argparse
import csv
import glob
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

import ase
from ase.io import iread
from ase.neighborlist import neighbor_list
import numpy as np


def pair_name(a, b):
    """Put H first for readable interstitial pairs, then sort alphabetically."""
    return "-".join(sorted((a, b), key=lambda x: (x != "H", x)))


def canonical_edge(i, j, shift):
    """One undirected periodic edge: (i,j,S) is equivalent to (j,i,-S)."""
    forward = (int(i), int(j), *(int(x) for x in shift))
    reverse = (int(j), int(i), *(-int(x) for x in shift))
    return min(forward, reverse)


def extract_bonds(atoms, cutoff):
    """Return unique atom/image edges shorter than cutoff (angstrom)."""
    if not math.isfinite(cutoff) or cutoff <= 0:
        raise ValueError("cutoff must be finite and positive")
    if not np.isfinite(atoms.positions).all() or not np.isfinite(atoms.cell).all():
        raise ValueError("nonfinite positions or cell")
    if any(atoms.pbc) and np.linalg.matrix_rank(atoms.cell) < 3:
        raise ValueError("periodic input requires a full-rank cell")
    i, j, distances, shifts = neighbor_list("ijdS", atoms, cutoff, self_interaction=False)
    symbols = atoms.get_chemical_symbols()
    seen = set()
    bonds = []
    for ai, aj, distance, shift in zip(i, j, distances, shifts):
        key = canonical_edge(ai, aj, shift)
        if key in seen:
            continue
        seen.add(key)
        if not math.isfinite(float(distance)) or distance <= 1e-12:
            raise ValueError("overlapping atoms or zero-length neighbour detected")
        ai, aj, sx, sy, sz = key
        a, b = symbols[ai], symbols[aj]
        category = "H-H" if a == b == "H" else (
            "H-metal" if "H" in (a, b) else "metal-metal"
        )
        bonds.append(dict(atom_i=ai, atom_j=aj, element_i=a, element_j=b,
                          shift_x=sx, shift_y=sy, shift_z=sz,
                          pair=pair_name(a, b), category=category,
                          distance_A=float(distance)))
    return sorted(bonds, key=lambda row: (row["distance_A"], row["atom_i"], row["atom_j"],
                                          row["shift_x"], row["shift_y"], row["shift_z"]))


def groups_for(atoms, bonds):
    """Keep empty categories explicit; zero neighbours is not a zero distance."""
    symbols = sorted(set(atoms.get_chemical_symbols()))
    groups = {"all": bonds, "H-metal": [], "metal-metal": []}
    for a, b in itertools.combinations_with_replacement(symbols, 2):
        groups.setdefault(pair_name(a, b), [])
    for bond in bonds:
        if bond["category"] in ("H-metal", "metal-metal"):
            groups[bond["category"]].append(bond)
        # H-H's category and species pair have the same name: append only once.
        groups[bond["pair"]].append(bond)
    return groups


def summary(values):
    distances = np.array([r["distance_A"] for r in values], dtype=float)
    if not len(distances):
        return dict(n_bonds=0, min_A=None, mean_A=None, std_A=None, median_A=None,
                    max_A=None, min_atom_i=None, min_atom_j=None,
                    min_shift_x=None, min_shift_y=None, min_shift_z=None)
    shortest = min(values, key=lambda row: row["distance_A"])
    return dict(n_bonds=len(distances), min_A=float(distances.min()),
                mean_A=float(distances.mean()), std_A=float(distances.std(ddof=0)),
                median_A=float(np.median(distances)), max_A=float(distances.max()),
                min_atom_i=shortest["atom_i"], min_atom_j=shortest["atom_j"],
                min_shift_x=shortest["shift_x"], min_shift_y=shortest["shift_y"],
                min_shift_z=shortest["shift_z"])


def histogram(values, edges):
    counts, _ = np.histogram([r["distance_A"] for r in values], bins=edges)
    density = counts / (len(values) * np.diff(edges)) if values else np.zeros(len(counts))
    return counts, density


def plot_case(groups, edges, title, target):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(8, 7), constrained_layout=True)
    for name in ("all", "H-metal", "metal-metal"):
        if groups[name]:
            _, density = histogram(groups[name], edges)
            axes[0].stairs(density, edges, label=f"{name} (n={len(groups[name])})", linewidth=1.5)
    pair_keys = [name for name in groups if name not in ("all", "H-metal", "metal-metal")]
    h_keys = [name for name in pair_keys if name.startswith("H-") and groups[name]]
    for name in h_keys or [name for name in pair_keys if groups[name]]:
        _, density = histogram(groups[name], edges)
        minimum = min(row["distance_A"] for row in groups[name])
        axes[1].stairs(density, edges, label=f"{name}: min {minimum:.3f} Å", linewidth=1.5)
    axes[0].set_title("All neighbours and broad categories")
    axes[1].set_title("H-containing pairs" if h_keys else "Element pairs")
    for ax in axes:
        ax.set_xlabel("Neighbour distance (Å)")
        ax.set_ylabel("Probability density (Å⁻¹)")
        ax.set_xlim(0, edges[-1])
        ax.grid(alpha=0.2)
        if ax.get_legend_handles_labels()[0]:
            ax.legend(fontsize=8, ncol=2)
    fig.suptitle(title, fontsize=10)
    fig.savefig(target.with_suffix(".png"), dpi=180)
    fig.savefig(target.with_suffix(".pdf"))
    plt.close(fig)


def expand_inputs(patterns):
    paths = []
    seen = set()
    for pattern in patterns:
        matches = sorted(glob.glob(pattern, recursive=True))
        if not matches:
            raise ValueError(f"input pattern matched no files: {pattern}")
        for name in matches:
            path = Path(name).absolute()
            if not path.is_file():
                raise ValueError(f"input is not a file: {path}")
            # The same physical structure reached through an alias is not a new case.
            identity = path.resolve()
            if identity not in seen:
                seen.add(identity)
                paths.append(path)
    return paths


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="files or quoted glob patterns")
    parser.add_argument("--cutoff", required=True, type=float, help="neighbour cutoff in angstrom")
    parser.add_argument("--bin-width", type=float, default=0.02, help="histogram bin width in angstrom")
    parser.add_argument("--frames", choices=("last", "all"), default="last")
    parser.add_argument("--format", help="explicit ASE format, e.g. vasp or lammps-dump-text")
    parser.add_argument("--out", required=True, type=Path, help="new output directory; must not exist")
    parser.add_argument("--no-plots", action="store_true", help="write CSV/JSON only")
    args = parser.parse_args(argv)
    if not math.isfinite(args.cutoff) or args.cutoff <= 0:
        parser.error("--cutoff must be finite and positive")
    if not math.isfinite(args.bin_width) or args.bin_width <= 0:
        parser.error("--bin-width must be finite and positive")
    n_bins = max(1, math.ceil(args.cutoff / args.bin_width))
    if n_bins > 1_000_000:
        parser.error("too many histogram bins; increase --bin-width")
    try:
        paths = expand_inputs(args.inputs)
    except ValueError as exc:
        parser.error(str(exc))
    if args.out.exists():
        parser.error("output directory already exists; use a new --out path")
    if not args.no_plots:
        # Fail before creating partial outputs if plotting is unavailable.
        import matplotlib  # noqa: F401
    args.out.mkdir(parents=True)
    metadata = dict(status="running", units="angstrom", cutoff_A=args.cutoff,
                    bin_width_requested_A=args.bin_width, frames=args.frames,
                    frame_index_convention="-1 means last frame; all uses zero-based indices",
                    counting="undirected periodic atom/image edges; reverse edges counted once",
                    index_base=0, std_definition="population SD (ddof=0)",
                    note="Geometric cutoff neighbours, not electronic bonds or an RDF."
                         " Non-H atoms in this alloy tool are labelled metal.",
                    ase_version=ase.__version__, numpy_version=np.__version__,
                    script_sha256=sha256(Path(__file__)), inputs=[], cases=0)
    meta_path = args.out / "metadata.json"
    def save_metadata():
        meta_path.write_text(json.dumps(metadata, indent=2, allow_nan=False) + "\n")
    save_metadata()
    edges = np.linspace(0.0, args.cutoff, n_bins + 1)
    metadata["bin_width_actual_A"] = float(edges[1] - edges[0])
    common = ["case_id", "source", "frame_index"]
    bond_fields = ["atom_i", "atom_j", "element_i", "element_j", "shift_x", "shift_y", "shift_z",
                   "pair", "category", "distance_A"]
    summary_fields = list(summary([]))
    plots = args.out / "plots"
    if not args.no_plots:
        plots.mkdir()
    try:
        with (args.out / "bonds.csv").open("w", newline="") as bf, \
             (args.out / "summary.csv").open("w", newline="") as sf, \
             (args.out / "histograms.csv").open("w", newline="") as hf:
            bw = csv.DictWriter(bf, common + bond_fields)
            sw = csv.DictWriter(sf, common + ["group"] + summary_fields)
            hw = csv.DictWriter(hf, common + ["group", "left_A", "right_A", "count", "density_per_A"])
            for writer in (bw, sw, hw):
                writer.writeheader()
            for number, path in enumerate(paths):
                file_hash = sha256(path)
                entry = dict(source=str(path), sha256=file_hash, selected_frames=0)
                metadata["inputs"].append(entry)
                for frame, atoms in enumerate(iread(str(path), index="-1" if args.frames == "last" else ":",
                                                    format=args.format)):
                    frame_index = -1 if args.frames == "last" else frame
                    case_id = f"{number:04d}_{path.stem}_frame{frame_index}"
                    identity = dict(case_id=case_id, source=str(path), frame_index=frame_index)
                    bonds = extract_bonds(atoms, args.cutoff)
                    groups = groups_for(atoms, bonds)
                    for row in bonds:
                        bw.writerow(identity | row)
                    for name, values in groups.items():
                        sw.writerow(identity | {"group": name} | summary(values))
                        counts, density = histogram(values, edges)
                        for left, right, count, value in zip(edges[:-1], edges[1:], counts, density):
                            hw.writerow(identity | dict(group=name, left_A=left, right_A=right,
                                                         count=int(count), density_per_A=float(value)))
                    if not args.no_plots:
                        plot_case(groups, edges, f"{path.name}, frame {frame_index}; cutoff {args.cutoff:g} Å",
                                  plots / case_id)
                    entry["selected_frames"] += 1
                    metadata["cases"] += 1
                if entry["selected_frames"] == 0:
                    raise ValueError(f"no frames read from {path}")
                if sha256(path) != file_hash:
                    raise ValueError(f"input changed during analysis: {path}")
                save_metadata()
        metadata["status"] = "complete"
        save_metadata()
    except Exception as exc:
        metadata["status"] = "failed"
        metadata["error"] = str(exc)
        save_metadata()
        raise
    print(f"Analysed {metadata['cases']} cases. Outputs: {args.out.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"Analysis failed: {exc}", file=sys.stderr)
        sys.exit(1)
