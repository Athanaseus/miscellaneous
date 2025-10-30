#!/usr/bin/env python3
import re
import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def parse_wsclean_log(filepath):
    """Parse WSClean log into runs with iteration, flux, and timestamps."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    runs = re.split("=== IMAGING TABLE ===", content)
    parsed_runs = []

    for r in runs:
        iterations, fluxes, times = [], [], []
        for line in r.splitlines():
            match = re.search(
                r"(\d{4}-[A-Za-z]{3}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+).*Iteration\s+(\d+),\s*scale\s*\d+\s*px\s*:\s*([-\d.]+)\s*([µm]?)Jy",
                line)
            if match:
                timestamp_str = match.group(1)
                try:
                    t = datetime.strptime(timestamp_str, "%Y-%b-%d %H:%M:%S.%f")
                except ValueError:
                    continue
                times.append(t)

                iterations.append(int(match.group(2)))
                flux = float(match.group(3))
                unit = match.group(4)
                if unit == "":
                    flux *= 1e-6  # Jy → mJy
                if unit == "µ":
                    flux *= 1e-3  # µJy → mJy
                fluxes.append(flux)
        if iterations:
            parsed_runs.append((iterations, fluxes, times))
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
    """Plot multiple WSClean runs with legends, color separation, and time axis."""
    plt.figure(figsize=(8, 6))
    colors = cm.viridis_r
    num_runs = len(runs)

    for i, (iterations, fluxes, times) in enumerate(runs):
        color = colors(i / max(1, num_runs - 1))
        plt.plot(iterations, fluxes, label=f"Run {i+1}", color=color, linewidth=2)

        # Compute elapsed time in hours for this run
        if times:
            t0 = times[0]
            elapsed_hours = [(t - t0).total_seconds() / 3600 for t in times]
            # store last for axis calibration
            last_elapsed = elapsed_hours[-1]

    plt.axhline(0, color='black', linewidth=2.5, alpha=0.8)
    plt.xlabel("Iteration", fontsize=12)
    plt.ylabel("Peak Flux (mJy)", fontsize=12)
    plt.title("WSClean Selfcal Flux Convergence", fontsize=13)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)

    # Main x-axis limits
    plt.xlim(min_iter if min_iter is not None else min(iterations),
             max_iter if max_iter is not None else max(iterations))

    # === Add top x-axis for elapsed time in hours ===
    ax1 = plt.gca()
    ax2 = ax1.twiny()
    iter_min, iter_max = ax1.get_xlim()
    ax2.set_xlim(0, last_elapsed)
    ax2.set_xlabel("Elapsed Time (hours)", fontsize=12)

    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
    print(f"\n✅ Saved plot to: {os.path.abspath(output_file)}")


def main():
    if len(sys.argv) <= 1:
        print("Usage: python plot_wsclean_flux.py <wsclean_log_file> <max_iter>")
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

    for i, (iterations, fluxes, times) in enumerate(runs):
        print_terminal_graph(i + 1, iterations, fluxes)

    plot_runs(runs, max_iter)

if __name__ == "__main__":
    main()
