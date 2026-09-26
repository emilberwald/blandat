import pandas as pd
from itertools import product
import sympy


def find_harmonic(root_frequency, relative_tolerance=0.01):
    pythagorean_minor = [1, 256 / 243, 32 / 27, 8192 / 6561, 1024 / 729, 128 / 81, 16 / 9]
    pythagorean_major = [1, 9 / 8, 81 / 64, 4 / 3, 3 / 2, 27 / 16, 243 / 128]

    harmonics_data = []

    root_harmonics = get_harmonics(root_frequency)
    for ratio_ix, ratio in enumerate(pythagorean_minor):
        harmonics_data.extend(
            get_harmonics_info("m", root_frequency, relative_tolerance, root_harmonics, ratio_ix, ratio)
        )
    for ratio_ix, ratio in enumerate(pythagorean_major):
        harmonics_data.extend(
            get_harmonics_info("M", root_frequency, relative_tolerance, root_harmonics, ratio_ix, ratio)
        )

    return pd.DataFrame(
        harmonics_data,
        columns=[
            "Note",
            "Note[Hz]",
            "Note Harmonic",
            "Note Harmonic No",
            "Note Harmonic [Hz]",
            "Root Harmonic No",
            "Root Harmonic",
            "Root Harmonic[Hz]",
            "Relative Error",
        ],
    )


def get_harmonics_info(ratio_prefix, root_frequency, relative_tolerance, root_harmonics, ratio_ix, ratio, limit=11):
    base_hertz = root_frequency * ratio
    data = []

    for ratio_harmonic_ix, ratio_harmonic in enumerate(get_harmonics(base_hertz)):
        for root_ix, root_harmonic in enumerate(root_harmonics):
            relative_error = abs(root_harmonic - ratio_harmonic) / root_harmonic
            if relative_error < relative_tolerance:
                ratio_factors = sympy.factorint(ratio_harmonic_ix + 1)
                root_factors = sympy.factorint(root_ix + 1)
                if all((factor <= limit for factor in ratio_factors.keys())) and all(
                    (factor <= limit for factor in root_factors.keys())
                ):
                    data.append(
                        [
                            f"{ratio_prefix}{ratio_ix + 1}",
                            base_hertz,
                            str(ratio_factors),
                            int(ratio_harmonic_ix + 1),
                            int(ratio_harmonic),
                            int(root_ix + 1),
                            str(root_factors),
                            int(root_harmonic),
                            relative_error,
                        ]
                    )

    return data


def get_harmonics(root_frequency):
    return [float(root_frequency * k) for k in range(1, 1 + 2**8)]


if __name__ == "__main__":
    harmonics_df = find_harmonic(220)
    harmonics_df = harmonics_df[~harmonics_df["Note"].str.contains("m1")]
    harmonics_df = harmonics_df[~harmonics_df["Note"].str.contains("M1")]
    harmonics_df = harmonics_df[~harmonics_df["Note"].str.contains("m4")]
    harmonics_df["Note"] = harmonics_df["Note"].str.replace("m5", "d5")
    harmonics_df["Note"] = harmonics_df["Note"].str.replace("M5", "P5")
    harmonics_df["Note"] = harmonics_df["Note"].str.replace("M4", "P4")
    harmonics_df = harmonics_df[harmonics_df["Root Harmonic[Hz]"] <= 20000]

    harmonics_df.to_excel("harmonics_data.xlsx", index=False)
