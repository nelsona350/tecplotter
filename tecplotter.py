from pathlib import Path
import re

import numpy as np

ZONE_PATTERN = re.compile(r"\bI\s*=\s*(\d+)\s+J\s*=\s*(\d+)\s+K\s*=\s*(\d+)", re.IGNORECASE)


def _parse_numeric_line(line: str) -> list[float]:
    """Parse one numeric line; supports Fortran D exponents."""
    parsed = np.fromstring(line.replace("D", "E").replace("d", "e"), sep=" ")
    return parsed.tolist()


def parse_zones(path: Path) -> list[tuple[str, int, int, int, np.ndarray, np.ndarray, np.ndarray]]:
    """Parse a Tecplot BLOCK file with multiple ZONE sections.

    Returns tuples of (zone_header, I, J, K, X, Y, Z) with X/Y/Z shaped as (J, I).
    """
    lines = path.read_text().splitlines()
    idx = 0
    zones: list[tuple[str, int, int, int, np.ndarray, np.ndarray, np.ndarray]] = []

    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue

        if not line.upper().startswith("ZONE"):
            idx += 1
            continue

        header = lines[idx].strip()
        m = ZONE_PATTERN.search(header)
        if not m:
            raise ValueError(f"Could not parse zone dimensions from header: {header}")

        i_dim, j_dim, k_dim = map(int, m.groups())
        n_points = i_dim * j_dim * k_dim
        expected = 3 * n_points

        idx += 1
        vals: list[float] = []
        while idx < len(lines):
            nxt = lines[idx].strip()
            if nxt.upper().startswith("ZONE"):
                break
            if nxt:
                vals.extend(_parse_numeric_line(nxt))
            idx += 1

        if len(vals) < expected:
            raise ValueError(
                f"Zone '{header}' has insufficient numeric data "
                f"(expected {expected}, got {len(vals)})"
            )

        nums = np.asarray(vals[:expected], dtype=float)
        x = nums[0:n_points].reshape((j_dim, i_dim))
        y = nums[n_points : 2 * n_points].reshape((j_dim, i_dim))
        z = nums[2 * n_points : 3 * n_points].reshape((j_dim, i_dim))
        zones.append((header, i_dim, j_dim, k_dim, x, y, z))

    return zones


def main() -> None:
    import matplotlib.pyplot as plt

    data_file = Path("for022.dat")
    zones = parse_zones(data_file)

    if len(zones) < 5:
        raise ValueError(f"Expected at least 5 zones (body + 4 fins), found {len(zones)}")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    cmap_cycle = ["viridis", "plasma", "inferno", "magma", "cividis"]

    for idx, (_, _, _, _, x, y, z) in enumerate(zones[:5], start=1):
        ax.plot_surface(
            x,
            y,
            z,
            cmap=cmap_cycle[(idx - 1) % len(cmap_cycle)],
            edgecolor="none",
            alpha=0.9,
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Surface Plot of Body + 4 Fin Datasets from for022.dat")
    plt.show()


if __name__ == "__main__":
    main()
