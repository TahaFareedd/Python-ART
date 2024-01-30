import random as rd
from enum import Enum
from typing import IO, List, NamedTuple,Tuple

# ENUMS AND TUPLES -- Data Classes
class ShapeKind(str, Enum):
    """Supported shape kinds"""
    CIRCLE = 0
    RECTANGLE = 1
    ELLIPSE = 2

    def __str__(self) -> str:
        return f'{self.value}'

class Irange(NamedTuple):
    """A simple integer range with minimum and maximum values"""
    imin: int
    imax: int

    def __str__(self) -> str:
        return f'{self.imin},{self.imax}'

class Frange(NamedTuple):
    """A simple float range with minimum and maximum values"""
    fmin: float
    fmax: float

    def __str__(self) -> str:
        return f'{self.fmin},{self.fmax}'


class Extent(NamedTuple):
    """Extent definition based on width and height ranges"""
    width: Irange
    height: Irange

    def __str__(self) -> str:
        return f'({self.width},{self.height})'
    
class Color(NamedTuple):
    """RGB color definition based on integer ranges"""
    red: Irange
    green: Irange
    blue: Irange
    opacity: Frange

    def __str__(self) -> str:
        return f'({self.red},{self.green},{self.blue})'

 # STATIC FUNCTIONS
def gen_int(r: Irange) -> int:
    """Generates a random integer"""
    return rd.randint(r.imin, r.imax)

def gen_float(r: Frange) -> float:
    """Generates a random float"""
    return rd.uniform(r.fmin, r.fmax)


# DOMAIN CLASSES
class PyArtConfig:
    """Input configuration to guide the art style (e.g., fall
    colours pointilistic) to be applied to random shapes"""
    pass
                    
class HtmlDocument:
    """An HTML document that allows appending SVG content"""
    TAB: str = "   "  # HTML indentation tab (default: three spaces)

    def __init__(self, file_name: str, win_title: str) -> None:
        self.win_title: str = win_title
        self.__tabs: int = 0
        self.__file: IO = open(file_name + ".html", "w")
        self.__write_head()
        canvas: SvgCanvas = SvgCanvas(self.__file, gen_int(Irange(50,1500)) ,gen_int(Irange(50,1500)))
        self.__write_tail()
        
    def increase_indent(self) -> None:
        """Increases the number of tab characters used for indentation"""
        self.__tabs += 1

    def decrease_indent(self) -> None:
        """Decreases the number of tab characters used for indentation"""
        self.__tabs -= 1

    def append(self, content: str) -> None:
        """Appends the given HTML content to this document"""
        ts: str = HtmlDocument.TAB * self.__tabs
        self.__file.write(f'{ts}{content}\n')

    def __write_head(self) -> None:
        """Appends the HTML preamble to this document"""
        self.append('<html>')
        self.append('<head>')
        self.increase_indent()
        self.append(f'<title>{self.win_title}</title>')
        self.decrease_indent()
        self.append('</head>')
        self.append('<body>')

    def __write_comment(self, comment: str) -> None:
        """Appends an HTML comment to this document"""
        self.append(f'<!--{comment}-->')


    def __write_tail(self) -> None:
        self.append('</body>')
        self.append('</html>')
        
    def gen_art(self):
        """generates circles and rectangles in SVG format"""
        count: int = 1000
        for i in range(count):
            rs: RandomShape = RandomShape(self.width, self.height)
            circle: CircleShape = CircleShape(rs)
            rectangle = RectangleShape = RectangleShape(rs)
            if(rs.sha == circle.sha):
                self.append(circle.as_svg())
            elif(rs.sha == rectangle.sha):
                self.append(rectangle.as_svg())
    
class SvgCanvas:
    TAB: str = "   "  # HTML indentation tab (default: three spaces)
    def __init__(self, file: IO, width: int, height: int):
        self.file = file
        self.width = width
        self.height = height
        self.__tabs: int = 0
        self.gen_canvas(Extent(Irange(0,width),Irange(0,height)))
        self.gen_art()
        self.close_off()
    
    def increase_indent(self) -> None:
        """Increases the number of tab characters used for indentation"""
        self.__tabs += 1

    def decrease_indent(self) -> None:
        """Decreases the number of tab characters used for indentation"""
        self.__tabs -= 1

    def append(self, content: str) -> None:
        """Appends the given HTML content to this document"""
        ts: str = HtmlDocument.TAB * self.__tabs
        self.file.write(f'{ts}{content}\n')
    
    def __write_comment(self, comment: str) -> None:
        """Appends an SVG comment to this document"""
        self.append(f'<!--{comment}-->')
        
    def gen_canvas(self, dimension:Extent):
        """ writes the <svg> tag with a given width and height"""
        self.increase_indent()
        self.__write_comment('Define SVG drawing box')
        self.append(f'<svg width="{dimension.width.imax}" height="{dimension.height.imax}">')
    
    
    def gen_art(self):
        """generates circles and rectangles in SVG format"""
        count: int = 500
        for i in range(count):
            rs: RandomShape = RandomShape(self.width, self.height)
            circle: CircleShape = CircleShape(rs)
            rectangle: RectangleShape = RectangleShape(rs)
            if(rs.sha == circle.sha):
                self.append(circle.as_svg())
                CircleShape.ccnt +=1
            elif(rs.sha == rectangle.sha):
                self.append(rectangle.as_svg())
                RectangleShape.ccnt +=1
                
            
            
    def close_off(self):
        """closes the SVG tag"""
        return "</svg>"
        

class RandomShape:
    """A shape that can take the form of any type of supported shape"""
    
    count:int = 0
    y:int = 18
    
    
    def __init__(self, width, height) -> None:
        config: PyArtConfig = PyArtConfig(width, height)
        self.x: int = config.rpt[0]
        self.y: int = config.rpt[1]
        self.rad: int = config.rad
        self.red = config.col[0]
        self.green = config.col[1]
        self.blue = config.col[2]
        self.op = config.col[3]
        self.width = config.width
        self.height = config.height
        self.sha = config.sha
    
    def __str__(self):
        return f'{self.count} {self.sha} {self.x} {self.y} {self.rad} {self.width} \
            {self.height} {self.red} {self.green} {self.blue} {round(self.op,1)}'
    
    def as_part2_line(self):
       return f'{self.count} {self.sha} {self.x} {self.y} {self.rad} {self.width} \
            {self.height} {self.red} {self.green} {self.blue} {round(self.op,1)}'

    def as_svg(self):
        return f'<text x="0" y="{RandomShape.y}" fill="black">' \
            f'<tspan x="0" dy="1.2em">{self.count}</tspan>' \
            f'<tspan x="50" dy="0">{self.sha}</tspan>' \
            f'<tspan x="100" dy="0">{self.x}</tspan>' \
            f'<tspan x="150" dy="0">{self.y}</tspan>' \
            f'<tspan x="200" dy="0">{self.rad}</tspan>' \
            f'<tspan x="250" dy="0">{self.width}</tspan>' \
            f'<tspan x="300" dy="0">{self.height}</tspan>' \
            f'<tspan x="350" dy="0">{self.red}</tspan>' \
            f'<tspan x="400" dy="0">{self.green}</tspan>' \
            f'<tspan x="450" dy="0">{self.blue}</tspan>' \
            f'<tspan x="500" dy="0">{round(self.op, 1)}</tspan>' \
            f'</text>'

class CircleShape:
    """A circle shape representing an SVG circle element"""
    ccnt: int = 0  # counting number of circles being constructed

    @classmethod
    def get_circle_count(cls) -> int:
        return CircleShape.ccnt

    def __init__(self, rs: RandomShape) -> None:
        """Initializes a circle"""
        self.sha: int = 0
        self.ctx: int = rs.x
        self.cty: int = rs.y
        self.rad: int = rs.rad
        self.red: int = rs.red
        self.gre: int = rs.green
        self.blu: int = rs.blue
        self.op: float = rs.op

    def as_svg(self) -> str:
        """Produces the SVG code representing this shape"""
        return f'<circle cx="{self.ctx}" cy="{self.cty}" r="{self.rad}" ' \
               f'fill="rgb({self.red},{self.gre},{self.blu})" ' \
               f'fill-opacity="{self.op}"></circle>'

    def __str__(self) -> str:
        """String representation of this shape"""
        return f'\nGenerated random circle\n' \
               f'shape = {self.sha}\n' \
               f'radius = {self.rad}\n' \
               f'(centerx, centery) = ({self.ctx},{self.cty})\n' \
               f'(red, green, blue) = ({self.red},{self.gre},{self.blu})\n' \
               f'opacity = {self.op:.1f}\n'
        
class RectangleShape:
    """A rectangle shape that can be drawn as an SVG rect element"""
    ccnt: int = 0  # counting number of circles being constructed
    
    @classmethod
    def get_rect_count(cls) -> int:
        return RectangleShape.ccnt
    
    def __init__(self, rs: RandomShape):
        """initializies the rectangle"""
        self.sha: int = 1
        self.tlx: int = rs.x
        self.tly: int = rs.y
        self.width: int = rs.width
        self.height: int = rs.height
        self.red: int = rs.red
        self.gre: int = rs.green
        self.blu: int = rs.blue
        self.op: float = rs.op
    
    def as_svg(self) -> str:
        """Produces the SVG code representing this shape"""
        return f'<rect x ="{self.tlx}" y = "{self.tly}" width = "{self.width}" \
            height = "{self.height}" fill = "rgb({self.red},{self.gre},{self.blu})" \
                fill-opacity = "{self.op}"/>'


class PyArtConfig:
    """Input config to determine artstyle (fall, winter, spring)"""
    
    theme:str = "autumn"
    
    def __init__(self, width, height) -> None:
        if (PyArtConfig.theme == "autumn"):
            self.sha:int = gen_int(Irange(0,1))
            self.rpt: List[int] = [gen_int(Irange(10,width)), gen_int(Irange(10,height))]
            self.rad: int = gen_int(Irange(0,100))
            self.col: List[int] = [gen_int(Irange(156,255)),gen_int(Irange(81,210)), gen_int(Irange(0,98)),gen_float(Frange(0,1.0))]
            self.width = gen_int(Irange(10,100))
            self.height = gen_int(Irange(10,100))
            
        elif(PyArtConfig.theme == "winter"):
            self.sha:int = gen_int(Irange(0,1))
            self.rpt: List[int] = [gen_int(Irange(10,width)), gen_int(Irange(10,height))]
            self.rad: int = gen_int(Irange(0,100))
            self.col: List[int] = [gen_int(Irange(66,203)),gen_int(Irange(104,218)),gen_int(Irange(113,241)),gen_float(Frange(0,1.0))]
            self.width = gen_int(Irange(10,100))
            self.height = gen_int(Irange(10,100))
            
        elif(PyArtConfig.theme == "spring"):
            self.sha:int = gen_int(Irange(0,1))
            self.rpt: List[int] = [gen_int(Irange(10,width)), gen_int(Irange(10,height))]
            self.rad: int = gen_int(Irange(0,100))
            self.col: List[int] = [gen_int(Irange(94,246)),gen_int(Irange(111,215)),gen_int(Irange(60,185)),gen_float(Frange(0,1.0))]
            self.width = gen_int(Irange(10,100))
            self.height = gen_int(Irange(10,100))
            
        elif(PyArtConfig.theme == "summer"):
            self.sha:int = gen_int(Irange(0,1))
            self.rpt: List[int] = [gen_int(Irange(10,width)), gen_int(Irange(10,height))]
            self.rad: int = gen_int(Irange(0,100))
            self.col: List[int] = [gen_int(Irange(21,255)),gen_int(Irange(89,215)),gen_int(Irange(0,211)),gen_float(Frange(0,1.0))]
            self.width = gen_int(Irange(10,100))
            self.height = gen_int(Irange(10,100))
            
        else:
            self.rpt: List[int] = [gen_int(Irange(0,width)), gen_int(Irange(0,height))]
            self.rad: int = gen_int(Irange(0,100))
            self.col: List[int] = [gen_int(Irange(0,255)),gen_int(Irange(0,255)),gen_int(Irange(0,255)),gen_float(Frange(0,1.0))]
            self.width = gen_int(Irange(10,100))
            self.height = gen_int(Irange(10,100))
            


def create_html_file() -> None:
    fileName1: str = "a431"
    fileName2: str = "a432"
    fileName3: str = "a433"
    winTitle: str = "TAHA FAREED ART"
    art1: HtmlDocument = HtmlDocument(fileName1, winTitle)
    art2: HtmlDocument = HtmlDocument(fileName2, winTitle)
    art3: HtmlDocument = HtmlDocument(fileName3, winTitle)


def main() -> None:
    create_html_file()
    print(f'Circles generated: {CircleShape.ccnt}')
    print(f'Rectangles generated: {RectangleShape.ccnt}')
    
main()