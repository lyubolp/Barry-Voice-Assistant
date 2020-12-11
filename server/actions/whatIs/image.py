"""
:version: 1.0
:author Lyuboslav Karev

    Contains the Image class, which is used to represent image based content
"""


class Image:
    """
    The image class is used in the Content class, when the WikiAPI returns an image.
    It has three fields - src, width and height which are representing an image.
    """
    def __init__(self, src: str = None, width: str = None, height: str = None):
        self.src: str = ""
        self.width: str = ""
        self.height: str = ""

        if src is not None:
            self.src = src
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
