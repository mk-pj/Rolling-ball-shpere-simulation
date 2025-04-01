import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

params = pd.read_csv("data/params.csv")
top = params.iloc[0][['top_x', 'top_y']]
bottom = params.iloc[0][['bottom_x', 'bottom_y']]

def animate_system(df_obj, df_circle_obj, output_filename, title):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect('equal')
    ax.set_xlim(df_obj['center_x'].min() - 1, df_obj['center_x'].max() + 1)
    ax.set_ylim(df_obj['center_y'].min() - 1, df_obj['center_y'].max() + 1)
    ax.grid(True)

    tracked_dot, = ax.plot([], [], 'ro', markersize=4)
    center_dot, = ax.plot([], [], 'ko', markersize=3)
    vector_line, = ax.plot([], [], 'r-', lw=1)
    traj_center_line, = ax.plot([], [], 'k--', lw=0.5)
    traj_tracked_line, = ax.plot([], [], 'orange', lw=0.5)
    circle_line, = ax.plot([], [], 'b-', lw=1)

    ax.plot([top['top_x'], bottom['bottom_x']],
            [top['top_y'], bottom['bottom_y']],
            'b-', lw=2)

    traj_center_x, traj_center_y = [], []
    traj_tracked_x, traj_tracked_y = [], []

    def init():
        tracked_dot.set_data([], [])
        center_dot.set_data([], [])
        vector_line.set_data([], [])
        traj_center_line.set_data([], [])
        traj_tracked_line.set_data([], [])
        circle_line.set_data([], [])
        return tracked_dot, center_dot, vector_line, traj_center_line, traj_tracked_line, circle_line

    def update(frame):
        row = df_obj.iloc[frame]
        t = row['t']
        cx, cy = row['center_x'], row['center_y']
        tx, ty = row['tracked_x'], row['tracked_y']

        tracked_dot.set_data([tx], [ty])
        center_dot.set_data([cx], [cy])
        vector_line.set_data([cx, tx], [cy, ty])

        traj_center_x.append(cx)
        traj_center_y.append(cy)
        traj_tracked_x.append(tx)
        traj_tracked_y.append(ty)
        traj_center_line.set_data(traj_center_x, traj_center_y)
        traj_tracked_line.set_data(traj_tracked_x, traj_tracked_y)

        circle_frame = df_circle_obj[df_circle_obj['t'] == t]
        circle_line.set_data(circle_frame['x'], circle_frame['y'])

        return tracked_dot, center_dot, vector_line, traj_center_line, traj_tracked_line, circle_line

    ani = animation.FuncAnimation(fig, update, frames=len(df_obj), init_func=init,
                                  blit=True, interval=40, repeat=False)
    ani.save(output_filename, writer='pillow', fps=25)
    plt.close(fig)


def main():
    df_ball = pd.read_csv("data/ball.csv")
    df_c_ball = pd.read_csv("data/c_ball.csv")
    animate_system(df_ball, df_c_ball, "anim_ball.gif", "Ball")

    df_sphere = pd.read_csv("data/sphere.csv")
    df_c_sphere = pd.read_csv("data/c_sphere.csv")
    animate_system(df_sphere, df_c_sphere, "anim_sphere.gif", "Sphere")


if __name__ == "__main__":
    main()
