from rusty_iterators import LIter


def validate_report(data: list[int]) -> bool:
    is_incremental = data[1] - data[0] > 0

    def _validate(data: list[int]) -> bool:
        difference = data[1] - data[0]
        is_curr_incremental = difference > 0
        difference = abs(difference)

        return difference >= 1 and difference <= 3 and is_incremental is is_curr_incremental

    return LIter.from_seq(data).moving_window(2).all(_validate)


def main() -> None:
    """An example solution to Advent of Code 2024: day 2, part 1.

    Source:
        - https://adventofcode.com/2024/day/2
    """
    with open("./examples/advent_of_code/input.txt", "r") as file:
        result = (
            LIter.from_it(file)
            .map(
                lambda line: LIter.from_seq(line)
                .filter(lambda char: char.isnumeric())
                .map(lambda char: int(char))
                .collect()
            )
            .filter(validate_report)
            .count()
        )

    assert result == 2  # noqa: S101


if __name__ == "__main__":
    main()
