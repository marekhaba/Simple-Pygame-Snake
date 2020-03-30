"""
Very simple pygame GUI solution
"""
import pygame

class Menu:
    """
    Creates a Menu that contains various widgets\n
     - screen: pygame display
     - theme: Theme that is defaulty used for all widgets
     - Menu.update() needs to be called every frame 
    """
    def __init__(self, screen, theme=None, color_bg=(150,150,150), frame_rate=60):
        self.screen = screen
        self.theme = Theme() if theme is None else theme
        self.color_bg = color_bg
        self.widgets = []
        self.clock = pygame.time.Clock()
        self.frame_rate = frame_rate

    def update(self):
        """
        Updates all the widgets.
        """
        #Handle events and responses
        events = pygame.event.get()
        result = "self"
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
        for widget in self.widgets:
            result_ = widget.update(events)
            if result_ != "self":
                result = result_
        #Draw stuff
        self.screen.fill(self.color_bg)
        for widget in self.widgets:
            draw_func = getattr(widget, "draw", None)
            if draw_func is not None:
                widget.draw()
        pygame.display.update()
        return result
            
    def _assign_widget(self, widget):
        """
        Function used by other widgets to assign themeself to this Menu.
        Tou don't need to worry about this function
        """
        self.widgets.append(widget)

class GenericWidget:
    """
    Preset for a widget
    """
    def __init__(self, parent, x, y, theme):
        self.parent = parent
        if isinstance(parent, pygame.Surface):
            self.screen = parent
        else:
            self.screen = parent.screen
            theme = parent.theme if theme is None else theme
            parent._assign_widget(self)
        self.x = x
        self.y = y
        self.theme = Theme() if theme is None else theme

    def draw(self):
        pass

    def update(self, events=None):
        return "self"

class Theme:
    """
    Container with all the infor about colors and dizajn of 'widgets'
    Mainly used so you can mantain an uniform style across multiple widgets
    text_size is in characters
    """
    def __init__(self, color_normal=(30, 30, 30), color_hover=(50, 50, 50), color_clicked=(100, 100, 100), text_color=(200, 200, 200), text_size=20, text_font="Verdana", text_bold=False, text_italic=False):
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_clicked = color_clicked
        self.text_color = text_color
        self.text_size = text_size
        self.text_font_name = text_font
        self.text_bold = text_bold
        self.text_italic = text_italic

        self.text_font = pygame.font.SysFont(self.text_font_name, self.text_size, self.text_bold, self.text_italic)


class Button(GenericWidget):
    """
    You click this it runs command\n
     - parent can be set to a Menu object if you want this under a Menu otherwise used to define pygame screen
     - command can be either a function that will be called, or a string that will be returned in update method
     - for theme create a Theme object
     - contionus: if the command should trigger on MOUSEBUTTONDOWN(True) or on MOUSEBUTTONUP(False)
    """
    #ADD ANCHOR
    def __init__(self, parent, x, y, width, height, command, text=":)", theme=None, continous=False):
        super().__init__(parent, x, y, theme)
        self.y = y
        self.width = width
        self.height = height
        self.command = command
        self.text = text
        self.text_rendered = self.theme.text_font.render(text, True, self.theme.text_color)
        self.continous = continous
        self.state = "normal" #can be normal, hover, pressed or (disabled(this needs to be added))

    def draw(self):
        color = self.theme.color_normal
        if self.state == "hover":
            color = self.theme.color_hover
        elif self.state == "pressed":
            color = self.theme.color_clicked
        pygame.draw.rect(self.screen, color, (self.x, self.y, self.width, self.height))
        text_width, text_height = self.theme.text_font.size(self.text)
        cords = (self.x + self.width//2 - text_width//2, self.y + self.height//2 - text_height//2, text_width, text_height)
        self.screen.blit(self.text_rendered, cords)

    def update(self, events=None):
        events = pygame.event.get() if events is None else events
        result = "self"
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
                    self.state = "hover"
                elif self.state == "hover":
                    self.state = "normal"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
                    self.state = "pressed"
                    if self.continous:
                        if isinstance(self.command, str):
                            result = self.command
                        else:
                            self.command()
                elif self.state == "pressed":
                    self.state = "normal"
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
                    if self.continous is False:
                        if isinstance(self.command, str):
                            result = self.command
                        else:
                            self.command()
                if self.state == "pressed":
                    self.state = "normal"
        return result

    def change_text(self, text):
        self.text = text
        self.text_rendered = self.theme.text_font.render(text, True, self.theme.text_color)

class Label(GenericWidget):
    """
    Used to display text
     - text_allign: how to allign text around x,y. Centre(C), North (N), South East (SE)...
     - text_size overrides the text size that is in theme
     - to change text use Label().change_text()
    """
    def __init__(self, parent, x, y, text, text_anchor="C", theme=None, text_size=None):
        super().__init__(parent, x, y, theme)
        self.text = text
        self.text_anchor = text_anchor
        self.text_size = text_size
        if self.text_size is not None:
            self.font = pygame.font.SysFont(self.theme.text_font_name, self.text_size, self.theme.text_bold, self.theme.text_italic)
        else:
            self.font = self.theme.text_font
        self.text_rendered = self.font.render(self.text, True, self.theme.text_color)
        self._anchor()

    def change_text(self, text, anchor=False):
        """
        Changes text\n
         - anchor: if text is supoused to be again alligned to anchor
        """
        self.text = text
        self.text_rendered = self.font.render(self.text, True, self.theme.text_color)
        if anchor:
            self._anchor()

    def _anchor(self):
        """
        Allgins the text to text_anchor needs to be called each time the size, font, etc. is changed.
        """
        width, height = self.font.size(self.text)
        self.cords = [self.x - width//2, self.y - height//2, width, height]
        if self.text_anchor == "C":
            return
        if "N" in self.text_anchor:
            self.cords[1] += height//2
        if "S" in self.text_anchor:
            self.cords[1] -= height//2
        if "W" in self.text_anchor:
            self.cords[0] += width//2
        if "E" in self.text_anchor:
            self.cords[0] -= width//2

    def draw(self):
        self.screen.blit(self.text_rendered, self.cords)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    test_screen = pygame.display.set_mode((500,500))
    done = False
    test = Menu(test_screen)
    btn = Button(test, 50, 150, 100, 50, lambda: print("Test"), text="click")
    label = Label(test, 250, 75, "Test Menu", text_size=75)
    while not done:
        result = test.update()
        #pygame.display.update()
        if result == 'quit':
            done = True
    pygame.quit()