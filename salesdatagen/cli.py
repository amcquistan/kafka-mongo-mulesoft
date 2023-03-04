from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('action', choices=['generate'])
    parser.add_argument('--interval', type=int, help='seconds between data generation', default=30)
    parser.add_argument('--intervals', type=int, help='number of intervals', default=-1)

    args = parser.parse_args()


