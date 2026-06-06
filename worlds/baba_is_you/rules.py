from __future__ import annotations

from typing import TYPE_CHECKING

from worlds.generic.Rules import add_rule, set_rule

from . import items
from .levels import LEVEL_DATA, can_win, can_bonus, can_transform, is_level_winnable, has_any_transform
from .locations import BabaIsYouLocation
from .custom_rules import HasBlossoms
from rule_builder.rules import And, CanReachRegion, Has, HasAny, HasAll, Or, Rule, True_, HasFromList

if TYPE_CHECKING:
    from .world import BabaIsYouWorld


def set_all_rules(world: BabaIsYouWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_goal_rule(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_goal_rule(world: BabaIsYouWorld) -> None:
    # Conditions for ending
    if world.options.goal == 0:
        ending = world.get_location("Goal Reached")
        a_way_out_rule = can_win("Map-Finale", world.options.logic_difficulty)
        world.set_rule(ending, a_way_out_rule & Has("End"))

def set_all_location_rules(world: BabaIsYouWorld) -> None:
    # Set up win, clear, complete, transform, and bonus location logic
    for name in LEVEL_DATA:
        data = LEVEL_DATA[name]
        if data.get("areaAccess", 0) > world.options.area_access or data.get("checkAreaAccess", 0) > world.options.area_access:
            continue # skip non-accessible areas

        parent = data.get("parent") # Get parent of old level
        if world.options.level_shuffle != 0:
            name = world.level_shuffle_dict.get(name, name)
            data = LEVEL_DATA[name]

        # Win rule
        if is_level_winnable(data):
            locationName = data["name"] + ": Win"
            location = world.get_location(locationName)

            rule = can_win(name, world.options.logic_difficulty)
            world.set_rule(location, rule)

            # Create win event with same logic as winning using parent
            if parent is not None:
                region = world.get_region(name)
                region.add_event(location_name = locationName + " Event", item_name = f"{parent} Win", location_type=BabaIsYouLocation, item_type=items.BabaIsYouItem, rule=rule)

        # Bonus rule
        if data.get("bonusLogic") is not None:
            locationName = data["name"] + ": Bonus"
            location = world.get_location(locationName)

            rule = can_bonus(name, world.options.logic_difficulty)
            world.set_rule(location, rule)
        
        # Transform rules
        if has_any_transform(data, world):
            for transform in data["transforms"]:
                locationName = f"{data["name"]}: {transform} Transform"
                rule = can_transform(name, transform, world.options.logic_difficulty)
                
                if world.options.transformsanity and transform.find("+") == -1: # combo transforms are only used for logic
                    location = world.get_location(locationName)
                    world.set_rule(location, rule)
                
                # Create event with same logic
                region = world.get_region(name)
                region.add_event(location_name = locationName + " Event", item_name = f"{data["name"]} -> {transform}", location_type=BabaIsYouLocation, item_type=items.BabaIsYouItem, rule=rule)
        
        # Add clear and completion checks for maps
        if data.get("clearCount") is not None:
            wins = data.get("clearCount")
            locationName = data["name"] + ": Clear"
            itemName = f"{name} Win"
            location = world.get_location(locationName)
            
            world.set_rule(location, Has(itemName, wins))
        if world.options.complete_checks and data.get("completeCount") is not None:
            wins = data.get("completeCount")
            locationName = data["name"] + ": Complete"
            itemName = f"{name} Win"
            location = world.get_location(locationName)
            
            world.set_rule(location, Has(itemName, wins))

# All maps with winnable levels
WIN_NAMES = ("Map Win", "Lake Win", "Island Win", "Ruins Win", "Fall Win",
             "Forest Win", "Space Win", "Garden Win", "Chasm Win", "Cavern Win",
             "Mountain Win", "??? Win", "ABC Win", "Null Win", "Depths Win",
             "Meta Win", "Center Win")

def set_completion_condition(world: BabaIsYouWorld) -> None:
    if world.options.goal <= 4: # end, flower, depths, meta
        world.set_completion_rule(Has("goal_reached"))
    elif world.options.goal == 5: # levels
        world.set_completion_rule(HasFromList(*WIN_NAMES, count=int(world.options.goal_levels)))
    elif world.options.goal == 6: # blossoms
        world.set_completion_rule(HasBlossoms(count=int(world.options.goal_blossoms)))