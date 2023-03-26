import random
import os
import glob
import numpy as np
import ffmpeg




class Maze:
    def __init__(self, dims):
        self.dims = dims
        self.walls_all = []
        self.passages_left = []
        self.passages_right = []
        self.maze = np.full(shape=[dims[0], dims[1]], fill_value=3)
        self.start_x = random.randint(0, dims[0] - 1)
        self.start_y = random.randint(0, dims[1] - 1)

        self.maze[self.start_x][self.start_y] = 0
        self.walls_all.append([self.start_x, self.start_y])

    def prims_algorithm(self):
        height = self.dims[0]
        width = self.dims[1]

        # List for temporarily walls
        walls_temp = []
        # Counter for 1's(passageways) around the random wall
        passage_count = 0

        # Get random wall
        current_wall = random.choice(self.walls_all)
        current_wall_height, current_wall_width = current_wall[0], current_wall[1]

        # Checking for passageways under the wall
        if current_wall_height + 1 <= height - 1 and self.maze[current_wall_height + 1][current_wall_width] == 1:
            passage_count += 1
        elif current_wall_height + 1 <= height - 1:
            walls_temp.append([current_wall_height + 1, current_wall_width])

        # Checking for passageways above the wall
        if current_wall_height - 1 >= 0 and self.maze[current_wall_height - 1][current_wall_width] == 1:
            passage_count += 1
        elif current_wall_height - 1 >= 0:
            walls_temp.append([current_wall_height - 1, current_wall_width])

        # Checking for passageways to the right of the wall
        if current_wall_width + 1 <= width - 1 and self.maze[current_wall_height][current_wall_width + 1] == 1:
            passage_count += 1
        elif current_wall_width + 1 <= width - 1:
            walls_temp.append([current_wall_height, current_wall_width + 1])

        # Checking for passageways to the left of the wall
        if current_wall_width - 1 >= 0 and self.maze[current_wall_height][current_wall_width - 1] == 1:
            passage_count += 1
        elif current_wall_width - 1 >= 0:
            walls_temp.append([current_wall_height, current_wall_width - 1])

        # Start if only one of the cells that the wall divides is a passage (stated by algorithm)
        if passage_count == 1 or passage_count == 0:
            self.walls_all.remove(current_wall)
            self.maze[current_wall_height][current_wall_width] = 1

            # Adding passages on the borders to find start and end point later
            if current_wall_width == 0:
                self.passages_left.append(
                    [current_wall_height, current_wall_width])
            elif current_wall_width == width - 1:
                self.passages_right.append(
                    [current_wall_height, current_wall_width])

            # Turn temp walls into actual walls
            for wall in walls_temp:
                self.maze[wall[0]][wall[1]] = 0
                self.walls_all.append(wall)

            self.maze_with_borders = np.pad(self.maze, 1)
            self.maze_with_borders[self.maze_with_borders == 3] = 0
            return self.maze_with_borders
        else:
            self.walls_all.remove(current_wall)
            if len(self.walls_all) == 0:
                starting_cell, end_cell = random.choice(
                    self.passages_left), random.choice(self.passages_right)
                self.maze_with_borders[starting_cell[0] +
                                       1, starting_cell[1]] = 1
                self.maze_with_borders[end_cell[0] + 1, end_cell[1] + 2] = 1
            return self.maze_with_borders

    def depth_first_search_algorithm(self):
       return 


class Visuals:
    def __init__(self):
        # Directory shenanigans
        current_directory = os.getcwd()
        img_folder_name = "images_gif"
        self.path_img_folder = os.path.join(current_directory, img_folder_name)

        # Check if folder for images exists, if not, make one
        if os.path.exists(self.path_img_folder) == False:
            os.mkdir(self.path_img_folder)

    def save_as_pbm(self, maze, rep):
        with open(f"{self.path_img_folder}/" + str(rep).zfill(9) + ".pbm", "wb") as f:
            f.write(bytes(f"P5\n{len(maze[0])} {len(maze)}\n255\n", "utf-8"))
            f.write(np.where(maze != 0, 255, 0).astype(
                np.uint8).tobytes())

    def delete_previous_img(self):
        previous_images = glob.glob(
            self.path_img_folder + "/*.pbm", recursive=True)

        for img in previous_images:
            os.remove(img)

    def generate_gif_ffmpeg(self):
        (
            ffmpeg
            .input(os.path.join(self.path_img_folder, "%09d.pbm"), framerate=25)
            .output('prims_ffmpeg.gif')
            .run()
        )


def main():
    dimensions = (100, 100)
    visuals = Visuals()
    visuals.delete_previous_img()
    maze = Maze(dimensions)
    rep = 1
    while len(maze.walls_all) >= 1:
        maze.prims_algorithm()
        visuals.save_as_pbm(maze.maze_with_borders, rep)
        rep += 1
        print(rep)

    visuals.generate_gif_ffmpeg()


if __name__ == "__main__":
    main()
