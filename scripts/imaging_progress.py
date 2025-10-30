#!/usr/bin/env python3
import re
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def parse_wsclean_log(filepath):
    """Parse WSClean log into separate runs with iteration-flux pairs."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Split into runs by imaging table marker
    runs = re.split("=== IMAGING TABLE ===", content)
    parsed_runs = []

    for r in runs:
        iterations = []
        fluxes = []
        for line in r.splitlines():
            match = re.search(
                r"(?:\(\d+\)\s*)?Iteration\s+(\d+),\s*scale\s*\d+\s*px\s*:\s*([-\d.]+)\s*([µm]?)Jy",
                line, re.IGNORECASE)
            if match:
                iterations.append(int(match.group(1)))
                flux = float(match.group(2))
                unit = match.group(3)
                if unit == r"µ":
                    flux *= 1e-3  # µJy → mJy
                fluxes.append(flux)
        if iterations:
            parsed_runs.append((iterations, fluxes))
    return parsed_runs


def print_terminal_graph(run_id, iterations, fluxes, chunk_size=1):
    """Print ASCII bar graph for each chunk of iterations."""
    if not iterations:
        return

    max_flux = max(abs(f) for f in fluxes)  # scale by absolute value
    print(f"\n=== Run {run_id} ===")

    # iterate in chunks
    for start in range(0, len(iterations), chunk_size):
        end = start + chunk_size
        chunk_iters = iterations[start:end]
        chunk_fluxes = fluxes[start:end]

        # use average or max flux for the chunk
        avg_flux = sum(chunk_fluxes) / len(chunk_fluxes)
        chunk_iter_label = f"{chunk_iters[0]}-{chunk_iters[-1]}"
        
        bar_len = int((abs(avg_flux) / max_flux) * 40)
        bar = "#" * bar_len
        sign = "-" if avg_flux < 0 else " "
        print(f"Iter {chunk_iter_label}: {sign}{bar:<40} {avg_flux:.3e} mJy")

    print()


def plot_runs(runs, max_iter=None, min_iter=None, output_file="wsclean_flux_progress.png"):
    """Plot multiple WSClean runs with legends and color separation."""
    plt.figure(figsize=(8, 6))
    colors = cm.viridis_r
    num_runs = len(runs)
    
    for i, (iterations, fluxes) in enumerate(runs):
        color = colors(i / max(1, num_runs - 1))
        plt.plot(iterations, np.array(fluxes), label=f"Run {i+1}", color=color, linewidth=2)

    plt.xlabel("Iteration", fontsize=12)
    plt.ylabel("Peak Flux (mJy)", fontsize=12)
    plt.title("WSClean Selfcal Flux Convergence", fontsize=13)
    plt.legend()
    plt.xlim(min_iter if min_iter is not None else min(iterations),
             max_iter if max_iter is not None else max(iterations))
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
    print(f"\n✅ Saved plot to: {os.path.abspath(output_file)}")


def main():
    import sys
    if len(sys.argv) <= 1 or len(sys.argv)>3 :
        print("Usage: python plot_wsclean_flux.py <wsclean_log_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    if not os.path.exists(log_file):
        print(f"❌ File not found: {log_file}")
        sys.exit(1)
    max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else None

    runs = parse_wsclean_log(log_file)
    if not runs:
        print("⚠️ No valid iterations found in the log.")
        sys.exit(0)

    for i, (iterations, fluxes) in enumerate(runs):
        print_terminal_graph(i + 1, iterations, fluxes)

    plot_runs(runs, max_iter)


import matplotlib.pyplot as plt

def plot_run_png(run_id, iterations, fluxes, min_iter=None, max_iter=10000, filename=None):
    """Plot iteration vs flux for a run and save PNG."""
    # Apply iteration cut
    if min_iter is not None or max_iter is not None:
        filtered = [(it, fl) for it, fl in zip(iterations, fluxes)
                    if (min_iter is None or it >= min_iter) and (max_iter is None or it <= max_iter)]
        if not filtered:
            print(f"No iterations in range for run {run_id}")
            return
        iterations, fluxes = zip(*filtered)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, fluxes*1000, marker='o', linestyle='-', label=f'Run {run_id}')
    plt.xlabel("Iteration")
    plt.ylabel("Flux [Jy]")
    plt.title(f"WSClean Iterations vs Flux - Run {run_id}")
    plt.grid(True)
    plt.legend()

    if min_iter is not None or max_iter is not None:
        plt.xlim(min_iter if min_iter is not None else min(iterations),
                 max_iter if max_iter is not None else max(iterations))

    if filename is None:
        filename = f"run_{run_id}_iterations.png"
    plt.savefig(filename, dpi=150)
    plt.close()




if __name__ == "__main__":
    main()

