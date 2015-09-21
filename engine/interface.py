from pygame import image
from .math import Vector2
from collections import OrderedDict
import pygame
import pygame.transform
from functools import reduce


class UIElement(object):
    """
    :type name: str
    :type parent: engine.interface.UIElement
    :type children: OrderedDict
    :type position: engine.math.Vector2
    :type width: int
    :type height: int
    :type event_listeners: dict
    """
    def __init__(self, name, position=None, width=0, height=0):
        self.name = name
        self.parent = None
        self.children = OrderedDict()
        if position is  None:
            position = (0, 0)
        position = Vector2(position[0], position[1])
        self.position = position
        self.width = width
        self.height = height

        self.event_listeners = {}

    def add_child(self, element):
        """
        Adds a new element as a child, child with the same name cannot already exist. Does not allow addition
        if already has a parent

        :param UIElement element: Element to add
        """
        if element.parent is not None:
            raise ValueError("Element is already part of an interface")

        if element.name is None or len(element.name) == 0:
            raise ValueError("Element name cannot be empty or null")

        if element.name in self.children or element in self.children.values():
            raise IndexError

        self.children[element.name] = element
        element.parent = self

    def remove_child(self, element_name):
        """
        Removes a child from the element

        :param str element_name: Name fo the element to remove
        :return: Returns element removed, None if it wasn't found
        """
        if element_name is None or len(element_name) == 0:
            raise ValueError("Element name cannot be empty or null")

        if element_name not in self.children:
            return None

        element = self.children[element_name]
        del self.children[element_name]
        element.parent = None
        return element

    def find_child(self, child_name):
        """
        Finds a child object as defined by given name.

        :param str child_name: Name of the element we are looking for. By default this will check only direct children.
                                Use "child1/child3/child4" syntax for traversing the tree further down.
        :return: None if cannot find the element, otherwise UIElement is returned
        """
        all_elements = child_name.split("/")
        parent = self
        for element_name in all_elements:
            if element_name not in parent.children:
                return None
            parent = parent.chilren[element_name]

        return parent

    def process_event(self, event):
        name = event["name"]
        if name in self.event_listeners:
            self.event_listeners[name](self, event)

    def listen_for_event(self, event_name, callback):
        if callback is None:
            raise ValueError("Event callback cannot be None")

        self.event_listeners[event_name] = callback

    def stop_listening_for_event(self, event_name):
        if event_name in self.event_listeners:
            del self.event_listeners[event_name]

    def update(self):
        pass

    def get_children(self, direct=False):
        """
        Yields all children of this element (unless direct is set to true) in a breadth-first search

        :param bool direct: If False, will return all nested children, if True will return only direct
        :rtype: engine.interface.UIElement
        """
        children = list(self.children.values())
        for element in children:
            if not direct:
                children.extend(list(element.children.values()))
            yield element


class Canvas(UIElement):
    """
    Base UI element which encompasses the entire screen, is responsible for handling all its children for events etc.
    purposes

    :type scene: engine.scene.Scene
    :type screen: pygame.Surface
    """
    def __init__(self, scene):
        """
        :param engine.scene.Scene scene: Scene we are being attached to
        """
        if scene is None:
            raise ValueError("Canvas cannot exist without a scene")
        self.scene = scene
        self.screen = scene.game.renderer.screen
        super(Canvas, self).__init__("canvas", (0, 0), self.screen.get_width(), self.screen.get_height())

    def update(self):
        for child in self.get_children():
            child.update()

    def process_event(self, event):
        for child in self.get_children():
            if event["name"] in child.event_listeners:
                child.process_event(event)


class SpriteElement(UIElement):
    """
    Displays specified sprite scaled to width/height

    :type sprite: pygame.Surface
    """
    def __init__(self, name, sprite_path, position=None, width=0, height=0):
        self.sprite = None
        if sprite_path is not None:
            self.sprite = image.load(sprite_path)
            if self.sprite is not None:
                width = self.sprite.get_width() if width == 0 else width
                height = self.sprite.get_height() if height == 0 else height

        super(SpriteElement, self).__init__(name, position, width, height)


class SpriteGroup(SpriteElement):
    """
    Displays multiple sprites in a row or column.
    Remember to call rebuild_sprite after values have been changed!

    :type horizontal: bool
    :type spacing: int
    :type visible_count: int
    """
    def __init__(self, name, sprites, position=None, spacing=0, horizontal=True):
        """
        :param str name: Name of the object
        :param engine.math.Vecto2 position: Position of the container
        :param list sprites: List of tuples describing sprites: sprite name, width, height
        :param int spacing: Spacing between sprites
        :param bool horizontal: If True, will render sprites horizontally, otherwise vertically
        """
        super(SpriteGroup, self).__init__(name, None, position)
        self.horizontal = horizontal
        self.spacing = spacing
        self.visible_count = len(sprites)

        self._images = []
        for sprite in sprites:
            self._images.append((image.load(sprite[0]), sprite[1], sprite[2]))

        self.rebuild_sprite()

    def rebuild_sprite(self):
        """
        Rebuilds the sprites after its properties have changed
        """
        self._construct_sprite()

        x = 0
        y = 0
        for i, info in enumerate(self._images):
            if i >= self.visible_count:
                break

            if self.horizontal:
                if i > 0:
                    x += self.spacing
                    x += self._images[i - 1][1]
                self.height = max(y, info[2])
                self.width = x + info[1]
            else:
                if i > 0:
                    y += self.spacing
                    y += self._images[i - 1][2]

                self.width = max(x, info[1])
                self.height = y + info[2]

            self.sprite.blit(pygame.transform.scale(info[0], (info[1], info[2])), (x, y))

    def _construct_sprite(self):
        if self.visible_count == 0:
            self.sprite = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
            return

        visible = self._images[:self.visible_count]
        spacing_size = max((len(visible) - 1) * self.spacing, 0)
        if self.horizontal:
            width = reduce(lambda x, y: x + y[1], visible, 0) + spacing_size
            height = max([x[2] for x in visible])
        else:
            height = reduce(lambda x, y: x + y[2], visible, 0) + spacing_size
            width = max([x[1] for x in visible])

        self.sprite = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.sprite = self.sprite.convert_alpha()


