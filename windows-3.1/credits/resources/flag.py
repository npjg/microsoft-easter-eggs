#!/usr/bin/python

from PIL import Image
from nefile.resource_table import ResourceType
from io import BytesIO

class Windows31FlagAnimation:
    def __init__(self, shell_dll):
        # GET THE FLAG ANIMATION IMAGE.
        flag_resource = shell_dll.resource_table.resources[ResourceType.RT_BITMAP][9997]
        # The frombuffer and frombytes methods only accept raw pixel data.
        # They do not accept complete image files. For opening complete image files
        # stored in memory, the PIL documentation recommends using a BytesIO object
        # (https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#frombytes).
        flag_bitmap_stream = BytesIO(flag_resource.data)
        # TODO: Add support for RLE 4-bit bitmaps in PILImage.
        flag_image = Image.open(flag_bitmap_stream)

        # SPLIT THE IMAGE INTO ITS CONSTITUENT FRAMES.
        # Each frame is 32 x 33 pixels, and there are 4 images horizontally across.
        frame_width = 32
        frame_height = 33
        self.frame_images = []
        for frame_left_pixel in range(0, flag_image.width, frame_width):
            # CHECK IF THERE ARE MORE FRAMES AVAILABLE.
            # If not, stop iterating.
            if frame_left_pixel + frame_width > flag_image.width:
                break

            # EXTRACT JUST THIS FRAME INTO ITS OWN IMAGE.
            # Since all these frames have the same dimensions,
            # that makes for easy animation and export later.
            frame_top_pixel = 0
            frame_image_bounding_box = (
                frame_left_pixel, 
                frame_top_pixel,
                frame_left_pixel + frame_width, 
                frame_height)
            frame_image = flag_image.crop(box = frame_image_bounding_box)
            self.frame_images.append(frame_image)

    def save_as_animated_gif(self, filepath):
        # CREATE THE ANIMATED GIF.
        first_frame = self.frame_images[0]
        first_frame.save(
            filepath,
            format = 'GIF',
            append_images = self.frame_images[1:],
            save_all = True,
            # TODO: Get the framerate.
            duration = 95,
            # By setting the loop value to 0, indicate we want to loop forever.
            # A positive value would indicate a finite number of loops.
            loop = 0)

    @property
    def transparent_frames(self):
        if self._transparent_frames is not None:
            return self._transparent_frames

        self._transparent_frames = []

        for index, frame_image in enumerate(self.frame_images):
            # SET THE BACKGROUND COLOR TRANSPARENT.
            frame_image = frame_image.convert('RGBA')
            pixdata = frame_image.load()
            width, height = frame_image.size
            for y in range(height):
                for x in range(width):
                    if pixdata[x, y] == (0x00, 0xff, 0xff, 0xff):
                        pixdata[x, y] = (0x00, 0xff, 0xff, 0x00)