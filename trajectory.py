import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("data/sphere.csv")
    params = pd.read_csv("data/params.csv")

    top = (params['top_x'][0], params['top_y'][0])
    bottom = (params['bottom_x'][0], params['bottom_y'][0])

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')

    ax.plot([top[0], bottom[0]], [top[1], bottom[1]], color='blue', linewidth=2, label="równia")

    ax.plot(df['center_x'], df['center_y'], 'o', color='gray', markersize=4, label="środek kuli")

    ax.plot(df['tracked_x'], df['tracked_y'], color='orange', linewidth=1.5, label="punkt śledzony")

    ax.plot([df['center_x'].iloc[0], df['tracked_x'].iloc[0]],
            [df['center_y'].iloc[0], df['tracked_y'].iloc[0]],
            color='deepskyblue', linewidth=2)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True)
    ax.set_title('Toczenie się kuli po równi – trajektorie')
    ax.legend()
    plt.tight_layout()

    plt.savefig("trajektoria_kuli.png", dpi=300)
    print("Wykres zapisany jako 'trajektoria_kuli.png'")


if __name__ == "__main__":
    main()
