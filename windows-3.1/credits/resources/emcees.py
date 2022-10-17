
from PIL import Image
from nefile.resource_table import ResourceType
from io import BytesIO

## Models a two-dimensional point as a pair of left and top coordinates.
class Point:
    def __init__(self, left, top):
        self.left = left
        self.top = top

## The "emcee" for the credits is the character who shows up in the lower-left
## corner of the credits screen and points (statically) to the credits being presented.
## This class contains the information necessary to create the credits area image with
## only this emcee.
class Windows31CreditEmcee:
    def __init__(self, name, source, destination, width, height, image):
        # CREATE A COPY OF THE IMAGE.
        self.image = image.copy()

        # STORE THE METADATA.
        self.name = name
        self.source = source
        self.destination = destination
        self.width = width
        self.height = height

        # CREATE THE GRAPHIC FOR THIS EMCEE.
        # The heads for each of the emcees are stored in the 
        # right corners of the resource bitmap. The information
        # provided can be used to create a graphic with just
        # the desired emcee.
        #
        # GET THE EMCEE'S HEAD.
        emcee_head_source_bounding_box = (
            self.source.left, 
            self.source.top, 
            self.source.left + self.width, 
            self.source.top + self.height)
        emcee_head = self.image.crop(box = emcee_head_source_bounding_box)

        # ERASE THE HEADS.
        all_heads_bounding_box = (
            77,
            6,
            77 + 98,
            6 + 22
        )
        STAGE_BACKGROUND_COLOR = 0x08 # This palette entry corresponds to the color 0xc0c0c0.
        self.image.paste(STAGE_BACKGROUND_COLOR, all_heads_bounding_box)

        # PASTE THIS EMCEE'S HEAD ON THE BODY.
        # The body remains constant for all emcees; only the head changes.
        emcee_head_bounding_box = (
            self.destination.left, 
            self.destination.top, 
            self.destination.left + self.width, 
            self.destination.top + self.height)
        self.image.paste(emcee_head, box = emcee_head_bounding_box)

## Forms a container for all the known emcees in a stock Windows 3.1 credits display.
## There are four known emcees:
##  - Steve Ballmer
##  - Brad Silverberg
##  - Bill Gates
##  - Bear (or T-Bear)
class Windows31CreditEmcees:
    def __init__(self, shell_dll):
        # GET THE CREDITS IMAGE.
        emcees_resource = shell_dll.resource_table.resources[ResourceType.RT_BITMAP][9998]
        # The frombuffer and frombytes methods only accept raw pixel data.
        # They do not accept complete image files. For opening complete image files
        # stored in memory, the PIL documentation recommends using a BytesIO object
        # (https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#frombytes).
        emcees_bitmap_stream = BytesIO(emcees_resource.data)
        emcees_image = Image.open(emcees_bitmap_stream)

        # CREATE THE EMCEES.
        # Each known emcee gets is own entry. The width and height information
        # appears to be hard-coded into SHELL.DLL, so that information is repeated here.
        self.emcees = [
            Windows31CreditEmcee('Steve Ballmer', \
                source = Point(left = 77, top = 7), \
                destination = Point(left = 14, top = 7), \
                width = 23, height = 21, image = emcees_image),
            Windows31CreditEmcee('Brad Silverberg', \
                source = Point(left = 101, top = 7), \
                destination = Point(left = 14, top = 7), \
                width = 23, height = 21, image = emcees_image),
            Windows31CreditEmcee('Bill Gates', \
                source = Point(left = 125, top = 6), \
                destination = Point(left = 14, top = 6), \
                width = 23, height = 22, image = emcees_image),
            Windows31CreditEmcee('Bear', \
                source = Point(left = 150, top = 10), \
                destination = Point(left = 15, top = 10), \
                width = 22, height = 18, image = emcees_image)]
