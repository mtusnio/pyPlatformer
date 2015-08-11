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
    for group in tiled_map.visible_object_groups:
        for obj in tiled_map.layers[group]:
            game_object = engine.GameObject()
            game_object.add_components(components.Transform(position=math.Vector2(obj.x, obj.y)),
                                       engine.components.SpriteRenderer(image=obj.image))
            scene.add_object(game_object)
