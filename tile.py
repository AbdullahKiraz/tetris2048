import lib.stddraw as stddraw
from lib.color import Color


class Tile:
    # Constants for tile styling
    BOUNDARY_THICKNESS = 0.004
    FONT_FAMILY = "Arial"
    BASE_FONT_SIZE = 14

    # Dictionary defining visual styles for each tile value
    STYLES = {
        2: {
            'background': Color(238, 228, 218),
            'text': Color(119, 110, 101),
            'border': Color(187, 173, 160)
        },
        4: {
            'background': Color(237, 224, 200),
            'text': Color(119, 110, 101),
            'border': Color(187, 173, 160)
        },
        8: {
            'background': Color(242, 177, 121),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        },
        16: {
            'background': Color(245, 149, 99),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        },
        32: {
            'background': Color(246, 124, 95),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        },
        64: {
            'background': Color(246, 94, 59),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        },
        128: {
            'background': Color(237, 207, 114),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        },
        256: {
            'background': Color(237, 204, 97),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        },
        512: {
            'background': Color(237, 200, 80),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        },
        1024: {
            'background': Color(237, 197, 63),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        },
        2048: {
            'background': Color(237, 194, 46),
            'text': Color(249, 246, 242),
            'border': Color(187, 173, 160)
        }
    }

    def __init__(self, number=None):
        self._number = number if number is not None else (2, 4)[hash(str(id(self))) % 2]

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    def _get_style(self):
        #Returns the visual style for the current tile number.
        if self.number in self.STYLES:
            return self.STYLES[self.number]
        else:
            #Uses default style if number isn't in predefined styles.
            return {
                'background': Color(205, 193, 180),
                'text': Color(119, 110, 101),
                'border': Color(187, 173, 160)
            }

    def _calculate_font_size(self):
        #Dynamically calculates font size based on number of digits.
        digits = len(str(self.number))
        return max(8, self.BASE_FONT_SIZE - (digits - 1) * 2)

    def draw(self, position, length=1):

        style = self._get_style()

        # Draw background square
        stddraw.setPenColor(style['background'])
        stddraw.filledSquare(position.x, position.y, length / 2)

        # Draw border
        stddraw.setPenColor(style['border'])
        stddraw.setPenRadius(self.BOUNDARY_THICKNESS)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()  # Return to default weight

        # Draw number text (if not zero)
        if self.number > 0:
            stddraw.setPenColor(style['text'])
            stddraw.setFontFamily(self.FONT_FAMILY)
            stddraw.setFontSize(self._calculate_font_size())
            stddraw.text(position.x, position.y, str(self.number))

    def __str__(self):
        return f"Tile({self.number})"