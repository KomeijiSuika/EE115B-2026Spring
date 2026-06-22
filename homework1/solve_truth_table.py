from itertools import product
from pathlib import Path


def p0(a: int, b: int, c: int, d: int) -> int:
    return int((not a and b) or (a and not b))


def p1(a: int, b: int, c: int, d: int) -> int:
    return int((not a and not b and c) or (a and b and not c) or (b and c and d))


def p2(a: int, b: int, c: int, d: int) -> int:
    return int((not a) or (not b) or (not c) or (not d))


def p3(a: int, b: int, c: int, d: int) -> int:
    return int(a and (not b) and (not c) and (not d))


def build_rows() -> list[tuple[int, ...]]:
    rows = []
    for a, b, c, d in product([0, 1], repeat=4):
        rows.append((a, b, c, d, p0(a, b, c, d), p1(a, b, c, d), p2(a, b, c, d), p3(a, b, c, d)))
    return rows


def print_markdown_table(rows: list[tuple[int, ...]]) -> None:
    print("| A | B | C | D | P0 | P1 | P2 | P3 |")
    print("|---|---|---|---|----|----|----|----|")
    for row in rows:
        print("| " + " | ".join(str(x) for x in row) + " |")


def write_csv(rows: list[tuple[int, ...]]) -> None:
    output = Path(__file__).with_name("truth_table.csv")
    lines = ["A,B,C,D,P0,P1,P2,P3"]
    lines.extend(",".join(str(x) for x in row) for row in rows)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    table_rows = build_rows()
    print_markdown_table(table_rows)
    write_csv(table_rows)
