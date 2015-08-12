__author__ = 'Maverick'

from pytmx.util_pygame import load_pygame as load
from pytmx import TiledMap
import engine, components, math


def fill_scene_with_objects(scene, tiled_map):
    """
    Creates GameObjects based on objects supplied by tiled_map and adds them to scene
    :type scene: engine.Scene
    :type tiled_map: TiledMap
    """
    import game.components as game_components

    for group in tiled_map.visible_object_groups:
        for obj in tiled_map.layers[group]:
            game_object = engine.GameObject()
            obj_position = math.Vector2(obj.x, obj.y)
            game_object.add_components(components.Transform(position=obj_position),
                                       engine.components.SpriteRenderer(image=obj.image))
            obj_components = obj.properties.get("components", "")
            for component_name in obj_components.split(";"):
                component_class = None
                if hasattr(engine.components, component_name):
                    component_class = getattr(components, component_name, None)
                elif hasattr(game_components, component_name):
                    component_class = getattr(game_components, component_name)

                if component_class is not None:
                    game_object.add_components(component_class())
            scene.add_object(game_object)
