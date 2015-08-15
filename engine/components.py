__author__ = 'Maverick'
import pygame
from engine.math import Vector2
import tiledmap


class BaseComponent(object):
    """
    :type game_object: engine.GameObject
    """
    def __init__(self, **kwargs):
        self.game_object = None

    def update(self):
        """
        Runs once per frame before rendering
        """
        pass


class Camera(BaseComponent):
    """
    :type fov: float
    """
    def __init__(self, **kwargs):
        super(Camera, self).__init__(**kwargs)
        self.fov = kwargs.get("fov", 80)


class Renderable(BaseComponent):
    """
    :type should_render: bool
    """
    def __init__(self, **kwargs):
        super(Renderable, self).__init__(**kwargs)
        self.should_render = True


class SpriteRenderer(Renderable):
    """
    :type image_path: str
    :type image: pygame.Surface
    """
    def __init__(self, **kwargs):
        super(SpriteRenderer, self).__init__(**kwargs)
        if "image" not in kwargs:
            image_path = kwargs.get("path", None)
            self.image = pygame.image.load(image_path) if image_path is not None else None
        else:
            self.image = kwargs.get("image", None)


class Transform(BaseComponent):
    """
    :type position: Vector2
    :type rotation: float
    :type scale: float
    """
    def __init__(self, **kwargs):
        super(Transform, self).__init__(**kwargs)
        self._position = kwargs.get("position", Vector2(0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.scale = kwargs.get("scale", 1)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position.x = value.x
        self._position.y = value.y
        self._position.epsilon = value.epsilon


class BoundingRectangle(BaseComponent):
    """
    Base class for all bounding rectangles that we need to calculate
    """
    def __init__(self, **kwargs):
        super(BoundingRectangle, self).__init__(**kwargs)

    @property
    def rectangle(self):
        raise NotImplementedError()


class SpriteBoundingRectangle(BoundingRectangle):
    """
    Bounding rectangle calculated using the sprite image
    """
    def __init__(self, **kwargs):
        super(SpriteBoundingRectangle, self).__init__(**kwargs)

    @property
    def rectangle(self):
        return self.game_object.get_component(SpriteRenderer).image.get_rect(center=self.game_object.transform.position)


class TiledMap(Renderable):
    """
    :type map_path: str
    :type map: tiledmap.TiledMap
    """
    def __init__(self, **kwargs):
        super(TiledMap, self).__init__(**kwargs)
        map_path = kwargs.get("path", None)
        self.map = tiledmap.load(map_path) if map_path is not None else None

    def is_position_in_map(self, position):
        """
        Checks if the supplied world position is within map's bounds
        :param Vector2 position: World position
        :return: True if position is within map's bounds, False otherwise
        """
        relative_pos = position - self.game_object.transform.position
        if position[0] < 0 or position[1] < 0:
            return False

        if position[0] > self.map.tilewidth * self.map.width:
            return False

        if position[1] > self.map.tileheight * self.map.height:
            return False

        return True

    def get_tile_for_position(self, position, extrapolate = False):
        """
        Returns x/y tile coordinates for specified world position
        :param Vector2 position: World position
        :param bool extrapolate: If set to True it will return return potential out of bound tiles
        :return: Tuple containing x/y coordinates
        """
        if extrapolate is not True and not self.is_position_in_map(position):
            raise ValueError("Position is out of map")

        relative_position = position - self.game_object.transform.position
        return relative_position[0] // self.map.tilewidth, relative_position[1] // self.map.tileheight

    def fill_scene_with_objects(self):
        """
        Fills this object's scene with objects as described by tiled_map
        """
        import game.components as game_components
        from engine import GameObject

        tiled_map = self.map
        scene = self.game_object.scene
        for group in tiled_map.visible_object_groups:
            for obj in tiled_map.layers[group]:
                game_object = GameObject()
                obj_position = Vector2(obj.x + obj.image.get_width()/2, obj.y + obj.image.get_height()/2)
                game_object.add_components(Transform(position=obj_position))
                if obj.image is not None:
                    game_object.add_components(SpriteRenderer(image=obj.image), SpriteBoundingRectangle())

                obj_components = obj.properties.get("components", "")
                for component_name in obj_components.split(";"):
                    component_class = None
                    if hasattr(self.__module__, component_name):
                        component_class = getattr(self.__module__, component_name, None)
                    elif hasattr(game_components, component_name):
                        component_class = getattr(game_components, component_name)

                    if component_class is not None:
                        game_object.add_components(component_class())
                scene.add_object(game_object)