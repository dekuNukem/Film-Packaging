import sys, csv
from datetime import datetime, timezone
from collections import defaultdict

def recent_activity_summary(path: str) -> str:
    by_date = defaultdict(set)

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            author = (row.get("author") or "").strip()
            brand = (row.get("brand") or "").strip()
            product = (row.get("product") or "").strip()
            ts_str = (row.get("date_added") or "").strip()

            if not (author and brand and product and ts_str.isdigit()):
                continue

            ts = int(ts_str)
            dt = datetime.fromtimestamp(ts, tz=timezone.utc).date()
            by_date[dt].add((author, brand, product))

    if not by_date:
        return "No activity found."

    latest_days = sorted(by_date.keys(), reverse=True)[:5]

    lines = []
    for day in latest_days:
        lines.append("\n" + day.isoformat())
        entries = sorted(by_date[day], key=lambda x: (x[0].lower(), x[1].lower(), x[2].lower()))
        for author, brand, product in entries:
            lines.append(f"  - {author}: {brand} {product}")

    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_csv>")
        sys.exit(1)

    path = sys.argv[1]
    print(recent_activity_summary(path))


if __name__ == "__main__":
    main()
