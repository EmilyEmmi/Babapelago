from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from . import items
from .levels import LEVEL_DATA
from .locations import BabaIsYouLocation

if TYPE_CHECKING:
    from .world import BabaIsYouWorld


def set_all_rules(world: BabaIsYouWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_up_gates(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_up_gates(world: BabaIsYouWorld) -> None:
    # Set up gates for specific areas
    def check_first_gate(state: CollectionState):
        return get_blossom_count(state, world) >= world.options.first_gate_blossoms

    def check_second_gate(state: CollectionState):
        return get_blossom_count(state, world) >= world.options.second_gate_blossoms
    
    # Gate to A Way Out?
    a_way_out = world.get_region("Map-Finale")
    for entrance in a_way_out.entrances:
        add_rule(entrance, check_first_gate)

    # Gate to Cavern
    cavern = world.get_region("Cavern")
    for entrance in cavern.entrances:
        add_rule(entrance, check_second_gate)

    # Conditions for default ending
    ending = world.get_location("Ending")
    set_rule(ending, lambda state: state.has_all(("Keke", "Is", "Push", "Belt", "Shift", "Rock", "Win", "End"), world.player))


def set_all_location_rules(world: BabaIsYouWorld) -> None:
    # Set up win, clear, complete, and bonus location logic
    for name in LEVEL_DATA:
        data = LEVEL_DATA[name]

        if data.get("map") != True:
            locationName = data["name"] + ": Win"
            location = world.get_location(locationName)

            if data.get("winLogic") != None:
                def can_win(state: CollectionState, words=data["winLogic"]):
                    return state.has_all(words, world.player)
                
                # print(location.name, data["winLogic"])
                set_rule(location, can_win)
            else:
                can_win = None # No rule

            # Get parent based where the level is placed
            parent = data.get("parent")
            if world.options.level_shuffle != 0:
                for oldName in world.level_shuffle_dict:
                    name2 = world.level_shuffle_dict[oldName]
                    if name == name2: # This level got shuffled into the other one, get the old parent
                        parent = LEVEL_DATA[oldName].get("parent")
                        break

            # Create win event with same logic as winning using parent
            if parent != None:
                region = world.get_region(name)
                region.add_event(location_name = locationName + " Event", item_name = f"{parent} Win", location_type=BabaIsYouLocation, item_type=items.BabaIsYouItem, rule=can_win)
        else:
            if data.get("clearCount") != None:
                wins = data.get("clearCount")
                locationName = data["name"] + ": Clear"
                itemName = f"{name} Win"
                location = world.get_location(locationName)
                def can_reach_wins(state: CollectionState, name=itemName, wins=wins):
                    return state.has(name, world.player, wins)
                
                set_rule(location, can_reach_wins)
            if world.options.complete_checks and data.get("completeCount") != None:
                wins = data.get("completeCount")
                locationName = data["name"] + ": Complete"
                itemName = f"{name} Win"
                location = world.get_location(locationName)
                def can_reach_wins(state: CollectionState, name=itemName, wins=wins):
                    return state.has(name, world.player, wins)
                
                set_rule(location, can_reach_wins)

def set_completion_condition(world: BabaIsYouWorld) -> None:
    if world.options.goal == 0: # end
        world.multiworld.completion_condition[world.player] = lambda state: state.has("goal_end", world.player)
    elif world.options.goal == 1: # flower
        world.multiworld.completion_condition[world.player] = lambda state: state.has("goal_flower", world.player)
    elif world.options.goal == 2: # depths
        world.multiworld.completion_condition[world.player] = lambda state: state.has("goal_depths", world.player)
    elif world.options.goal == 3: # meta
        world.multiworld.completion_condition[world.player] = lambda state: state.has("goal_meta", world.player)
    elif world.options.goal == 4: # done
        world.multiworld.completion_condition[world.player] = lambda state: state.has("goal_done", world.player)
    elif world.options.goal == 5: # levels
        world.multiworld.completion_condition[world.player] = lambda state: get_win_count(state, world) >= world.options.goal_levels
    elif world.options.goal == 6: # blossoms
        world.multiworld.completion_condition[world.player] = lambda state: get_blossom_count(state, world) >= world.options.goal_blossoms

# Count blossoms from petals and normal
def get_blossom_count(state: CollectionState, world: BabaIsYouWorld):
    petals = state.count("Blossom Petal", world.player)
    blossoms = state.count("Blossom", world.player) + (petals // 8)
    return blossoms

# Manually count the wins from each map.
# NOTE: Needs to be manually updated when late game is added
def get_win_count(state: CollectionState, world: BabaIsYouWorld):
    wins = state.count("Map Win", world.player)
    wins += state.count("Lake Win", world.player)
    wins += state.count("Island Win", world.player)
    wins += state.count("Ruins Win", world.player)
    wins += state.count("Fall Win", world.player)
    wins += state.count("Forest Win", world.player)
    wins += state.count("Space Win", world.player)
    wins += state.count("Garden Win", world.player)
    wins += state.count("Chasm Win", world.player)
    wins += state.count("Cavern Win", world.player)
    wins += state.count("Mountain Win", world.player)
    return wins