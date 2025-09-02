"""Utilities for generating tournament fixtures."""
from __future__ import annotations

from typing import List, Tuple


class FixtureGenerator:
    """Generate fixtures for different tournament formats."""

    def __init__(self, teams: List[str]) -> None:
        self.teams = teams

    def round_robin(self) -> List[List[Tuple[str, str]]]:
        """Generate a round-robin schedule.

        Returns a list of rounds, each containing a list of match tuples
        ``(home, away)``. If the number of teams is odd, a bye is added and
        any matches involving the bye are omitted from the schedule.
        """
        return self.generate_round_robin(self.teams)

    def elimination(self) -> List[List[Tuple[str, str]]]:
        """Generate a single-elimination bracket.

        Returns a list of rounds, each containing match tuples. Subsequent
        rounds reference winners of previous matches using the notation
        ``Winner R{round}M{match}``.
        """
        return self.generate_elimination(self.teams)

    @staticmethod
    def generate_round_robin(teams: List[str]) -> List[List[Tuple[str, str]]]:
        teams = list(teams)
        if len(teams) < 2:
            return []
        if len(teams) % 2 == 1:
            teams.append("BYE")
        n = len(teams)
        rounds: List[List[Tuple[str, str]]] = []
        for _ in range(n - 1):
            round_matches: List[Tuple[str, str]] = []
            for i in range(n // 2):
                home = teams[i]
                away = teams[n - 1 - i]
                if "BYE" not in (home, away):
                    round_matches.append((home, away))
            rounds.append(round_matches)
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        return rounds

    @staticmethod
    def generate_elimination(teams: List[str]) -> List[List[Tuple[str, str]]]:
        teams = list(teams)
        if len(teams) < 2:
            return []
        # Pad with byes to next power of two
        size = 1
        while size < len(teams):
            size *= 2
        teams += ["BYE"] * (size - len(teams))

        rounds: List[List[Tuple[str, str]]] = []
        current_round = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]
        rounds.append(current_round)
        prev_round = current_round
        round_num = 2
        while len(prev_round) > 1:
            winners: List[str] = []
            for i, match in enumerate(prev_round):
                a, b = match
                if a == "BYE" and b == "BYE":
                    winners.append("BYE")
                elif a == "BYE":
                    winners.append(b)
                elif b == "BYE":
                    winners.append(a)
                else:
                    winners.append(f"Winner R{round_num-1}M{i+1}")
            next_round = [(winners[i], winners[i + 1]) for i in range(0, len(winners), 2)]
            rounds.append(next_round)
            prev_round = next_round
            round_num += 1
        return rounds
