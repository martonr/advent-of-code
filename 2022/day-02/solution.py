from __future__ import annotations

import enum
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

_DAY_NUMBER = 2


class RPSMove(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RPSRoundResult(enum.Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


class RPSRound:
    def __init__(self, my_move: RPSMove, opponent_move: RPSMove) -> None:
        self._my_move = my_move
        self._opponent_move = opponent_move
        self._calculate_round_result()

    def _calculate_round_result(self) -> None:
        if self._my_move == self._opponent_move:
            self._round_result = RPSRoundResult.DRAW
        elif self._my_move == RPSMove.ROCK:
            if self._opponent_move == RPSMove.PAPER:
                self._round_result = RPSRoundResult.LOSE
            else:
                self._round_result = RPSRoundResult.WIN
        elif self._my_move == RPSMove.PAPER:
            if self._opponent_move == RPSMove.SCISSORS:
                self._round_result = RPSRoundResult.LOSE
            else:
                self._round_result = RPSRoundResult.WIN
        elif self._my_move == RPSMove.SCISSORS:
            if self._opponent_move == RPSMove.ROCK:
                self._round_result = RPSRoundResult.LOSE
            else:
                self._round_result = RPSRoundResult.WIN

        self._round_score = self._my_move.value + self._round_result.value
        self._opponent_score = self._opponent_move.value + (6 - self._round_result.value)

    @staticmethod
    def find_move_for_outcome(opponent_move: RPSMove, desired_outcome: RPSRoundResult) -> RPSMove:
        if desired_outcome == RPSRoundResult.DRAW:
            return opponent_move
        elif desired_outcome == RPSRoundResult.WIN:
            if opponent_move == RPSMove.ROCK:
                return RPSMove.PAPER
            elif opponent_move == RPSMove.PAPER:
                return RPSMove.SCISSORS
            else:
                return RPSMove.ROCK
        elif desired_outcome == RPSRoundResult.LOSE:
            if opponent_move == RPSMove.ROCK:
                return RPSMove.SCISSORS
            elif opponent_move == RPSMove.PAPER:
                return RPSMove.ROCK
            else:
                return RPSMove.PAPER

    def get_round_result(self) -> RPSRoundResult:
        return self._round_result

    def get_round_score(self) -> int:
        return self._round_score

    def get_opponent_score(self) -> int:
        return self._opponent_score

    def is_a_win(self) -> bool:
        return self._round_result == RPSRoundResult.WIN

    def is_a_loss(self) -> bool:
        return self._round_result == RPSRoundResult.LOSE

    def is_a_draw(self) -> bool:
        return self._round_result == RPSRoundResult.DRAW


class RPSStrategy:
    def __init__(self, filename: str, strategy_type: str = "first") -> None:
        self._input_file = Path(filename).resolve()
        self._strategy_type = strategy_type
        self._opp_moves = {"A": RPSMove.ROCK, "B": RPSMove.PAPER, "C": RPSMove.SCISSORS}
        self._my_moves = {"X": RPSMove.ROCK, "Y": RPSMove.PAPER, "Z": RPSMove.SCISSORS}
        self._my_desired_outcomes = {"X": RPSRoundResult.LOSE, "Y": RPSRoundResult.DRAW, "Z": RPSRoundResult.WIN}
        self._parse_input()

    def _parse_input(self) -> None:
        rps_rounds = dict()
        with self._input_file.open("r", encoding="utf-8") as f:
            round_id = 0
            total_score = 0
            opponent_score = 0
            total_games = 0
            wins = 0
            draws = 0
            losses = 0
            for line in f:
                opp_m, my_m = line.strip().split(" ")
                if self._strategy_type == "first":
                    current_round = RPSRound(self._my_moves[my_m], self._opp_moves[opp_m])
                else:
                    my_chosen_move = RPSRound.find_move_for_outcome(
                        self._opp_moves[opp_m], self._my_desired_outcomes[my_m]
                    )
                    current_round = RPSRound(my_chosen_move, self._opp_moves[opp_m])
                total_score += current_round.get_round_score()
                opponent_score += current_round.get_opponent_score()
                total_games += 1

                if current_round.is_a_win():
                    wins += 1
                elif current_round.is_a_loss():
                    losses += 1
                else:
                    draws += 1

                rps_rounds[round_id] = current_round
                round_id += 1

            self._round = rps_rounds
            self._total_games = total_games
            self._final_score = total_score
            self._final_opponent_score = opponent_score
            self._final_wins = wins
            self._final_losses = losses
            self._final_draws = draws

    def get_strategy_score_result(self) -> int:
        return self._final_score

    def get_strategy_opponent_score_result(self) -> int:
        return self._final_opponent_score

    def get_total_wins(self) -> int:
        return self._final_wins

    def get_total_losses(self) -> int:
        return self._final_losses

    def get_number_of_games(self) -> int:
        return self._total_games


def run_solution() -> int:
    rps = RPSStrategy(f"./2022/day-{_DAY_NUMBER:02}/day_{_DAY_NUMBER:02}.input")
    logger.info(
        (
            "Following the guide my stats would be:\n"
            f"    Total score: {rps.get_strategy_score_result()}\n"
            f"    Wins: {rps.get_total_wins()} out of {rps.get_number_of_games()}\n"
            f"    Opponent wins: {rps.get_total_losses()} out of {rps.get_number_of_games()}\n"
            f"    Opponent score: {rps.get_strategy_opponent_score_result()}"
        )
    )
    rps_a = RPSStrategy(f"./2022/day-{_DAY_NUMBER:02}/day_{_DAY_NUMBER:02}.input", "second")
    logger.info(
        (
            "Following the guide my stats would be:\n"
            f"    Total score: {rps_a.get_strategy_score_result()}\n"
            f"    Wins: {rps_a.get_total_wins()} out of {rps_a.get_number_of_games()}\n"
            f"    Opponent wins: {rps_a.get_total_losses()} out of {rps_a.get_number_of_games()}\n"
            f"    Opponent score: {rps_a.get_strategy_opponent_score_result()}"
        )
    )
    return 0
