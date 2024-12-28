#!/usr/bin/env python3


from get_disk import get_disk


def partition_disk(disk: str | None = None) -> None:
    if disk is None:
        disk = get_disk()
    print(f"PD>pd-disk: {disk}")


def main() -> None:
    partition_disk()


if __name__ == "__main__":
    main()

# print(f"PD>pd-disk: {disk}")