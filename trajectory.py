import pandas as pd
import matplotlib.pyplot as plt

def plot_trajectory(name):
    df = pd.read_csv(f"data/{name}.csv")
    params = pd.read_csv("data/params.csv")

    top = (params['top_x'][0], params['top_y'][0])
    bottom = (params['bottom_x'][0], params['bottom_y'][0])

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')

    ax.plot([top[0], bottom[0]], [top[1], bottom[1]], color='blue', linewidth=2, label="plane")

    ax.plot(df['center_x'], df['center_y'], 'o', color='gray', markersize=4, label=f"center of the {name}")

    ax.plot(df['tracked_x'], df['tracked_y'], color='orange', linewidth=1.5, label="tracked point")

    ax.plot([df['center_x'].iloc[0], df['tracked_x'].iloc[0]],
            [df['center_y'].iloc[0], df['tracked_y'].iloc[0]],
            color='deepskyblue', linewidth=2)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True)
    ax.set_title(f'{name} rolling down inclined plane')
    ax.legend()
    plt.tight_layout()

    plt.savefig(f"trajectory_{name}.png", dpi=300)
    print("Wykres zapisany jako 'trajektoria_kuli.png'")


def main():
    plot_trajectory("ball")
    plot_trajectory("sphere")


if __name__ == "__main__":
    main()
