from strategies.strategy import Strategy, StrategyStep


# **,**% winrate
class FlagStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_next_player_steps(self) -> StrategyStep | None:
        strategy_step = None
        return strategy_step
