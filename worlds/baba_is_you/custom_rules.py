from rule_builder.rules import Rule, TWorld
from rule_builder.field_resolvers import FieldResolver, resolve_field
from BaseClasses import CollectionState
from typing_extensions import override
import dataclasses
from NetUtils import JSONMessagePart

@dataclasses.dataclass()
class HasBlossoms(Rule[TWorld], game="Baba Is You"):
    count: int | FieldResolver = 0

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        # caching_enabled only needs to be passed in when your world inherits from CachedRuleBuilderWorld
        return self.Resolved(count=resolve_field(self.count, world, int), player=world.player, caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        count: int = 0

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            petals = state.count("Blossom Petal", self.player)
            blossoms = state.count("Blossom", self.player) + (petals // 8)
            return blossoms >= self.count

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            # this function is only required if you have caching enabled
            return {"Blossom": {id(self)}, "Blossom Petal": {id(self)}}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            # this method can be overridden to display custom explanations
            return [
                {"type": "text", "text": "Collect "},
                {"type": "color", "color": "green" if state and self(state) else "salmon", "text": str(self.count)},
                {"type": "text", "text": " Blossoms"},
            ]