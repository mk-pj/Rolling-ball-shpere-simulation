import pandas as pd
import matplotlib.pyplot as plt

def plot_energy(csv_path, output_path, title="Energia w czasie"):
    df = pd.read_csv(csv_path)

    if not {'t', 'kinetic', 'potential', 'total'}.issubset(df.columns):
        raise ValueError("Brakuje kolumn: 't', 'kinetic', 'potential', 'total'")

    plt.figure(figsize=(10, 6))
    plt.plot(df["t"], df["kinetic"], label="Energia kinetyczna")
    plt.plot(df["t"], df["potential"], label="Energia potencjalna")
    plt.plot(df["t"], df["total"], label="Energia całkowita", linewidth=2)
    plt.xlabel("Czas [s]")
    plt.ylabel("Energia [J]")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Zapisano wykres do: {output_path}")
def main():
    plot_energy("data/ball.csv", "energy_ball.png", "Energia – kula")
    plot_energy("data/sphere.csv", "energy_sphere.png", "Energia – sfera")


if __name__ == "__main__":
    main()