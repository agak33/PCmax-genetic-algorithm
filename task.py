from typing import Union


class Task:
    """
    Class to draw rectangle on a plot, which represents a single task.
    """
    def __init__(self,
                 x: Union[int, float],
                 y: Union[int, float],
                 width: int,
                 height: int):
        """
        Construct a new object.
        Parameters:
            :param x: x coordinate on the plot
            :param y: y coordinate on the plot
            :param width: width of the rectangle
            :param height: height of the rectangle
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
