from __future__ import annotations

import logging

from pathlib import Path

logger = logging.getLogger(__name__)

_DAY_NUMBER = 1


class Elf:
    def __init__(self, id: int) -> None:
        self._id = id
        self._inventory = list()
        self._calories = 0

    def add_item(self, value: int) -> None:
        self._inventory.append(value)
        self._calories += value

    def get_total_calories(self) -> int:
        return self._calories

    def get_id(self) -> int:
        return self._id

    def __lt__(self, elf: Elf) -> bool:
        if self._calories < elf._calories:
            return True
        return False


class CalorieCatalog:
    def __init__(self, filename: str) -> None:
        self._input_file = Path(filename).resolve()
        self._parse_input()

    def _parse_input(self) -> None:
        elves: dict[int, Elf] = dict()
        with self._input_file.open("r", encoding="utf-8") as f:
            elf_id = 0
            max_calories_value = -1
            current_elf = Elf(elf_id)
            for line in f:
                if line.strip():
                    value = int(line)
                    current_elf.add_item(value)
                else:
                    calories_sum = current_elf.get_total_calories()
                    if calories_sum > max_calories_value:
                        max_calories_value = calories_sum
                        self._current_max_elf = current_elf
                    elves[elf_id] = current_elf
                    elf_id += 1
                    current_elf = Elf(elf_id)

        self._elf_inventories = elves
        self._sorted_elf_list = [v for v in sorted(self._elf_inventories.values(), reverse=True)]

    def get_max_elf(self) -> Elf:
        return self._current_max_elf

    def get_max_calories(self) -> int:
        return self._current_max_elf.get_total_calories()

    def get_sorted_elf_list(self) -> list:
        return self._sorted_elf_list

    def get_top_three_calorie_sum(self) -> int:
        total = 0
        for i in range(3):
            total += self._sorted_elf_list[i].get_total_calories()
        return total


def run_solution() -> int:
    c = CalorieCatalog(f"./2022/day-{_DAY_NUMBER:02}/day_{_DAY_NUMBER:02}.input")
    logger.info(
        (
            f"The max calories are carried by Elf#{c.get_max_elf().get_id()}"
            f" they are carying {c.get_max_calories()} calories worth of food."
        )
    )
    s_l = c.get_sorted_elf_list()
    logger.info(
        (
            f"Top elf list: \n"
            f"    1. {s_l[0].get_total_calories()} - Elf#{s_l[0].get_id()}\n"
            f"    2. {s_l[1].get_total_calories()} - Elf#{s_l[1].get_id()}\n"
            f"    3. {s_l[2].get_total_calories()} - Elf#{s_l[2].get_id()}"
        )
    )
    logger.info(f"The top 3 elves carry a total of {c.get_top_three_calorie_sum()} calories.")
    return 0
