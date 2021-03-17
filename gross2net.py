import argparse
import sys
import matplotlib.pyplot as plt
from salary_calculator import Calculator


def print_table(data):
    print(f"GROSS{'':7}NET")
    for d in data:
        print(f"{d[0]:<12.2f}{d[1]:<12.2f}")


def draw_plot(results):
    x_axis = []
    y_axis = []
    for result in sorted(results, key=lambda val: val[1]):
        x_axis.append(result[0])
        y_axis.append(result[1])
    plt.plot(x_axis, y_axis, marker="D")
    _, xlim_size = plt.xlim()
    plt.ylim(top=xlim_size)
    plt.xlabel("GROSS")
    plt.ylabel("NET")
    plt.title("Relationship between Gross and Net")
    plt.grid()
    plt.show()


# validate and returns float value for ppk
def ppk(string):
    try:
        val = float(string)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid float value: '{string}'")
    if not 2 <= val <= 4:
        raise argparse.ArgumentTypeError(f"Value has to be between 2 and 4.")
    return val


def get_arg_parser():
    arg_parser = argparse.ArgumentParser(
        description="This program uses wynagrodzenia.pl to calculate net values from gross values in PLN.")
    arg_parser.add_argument("gross", metavar="GROSS", type=float, nargs="+", help="gross values (max 12).")
    arg_parser.add_argument("-c", "--chart", action="store_true",
                            help="show chart of relationship between given gross and net.")
    arg_parser.add_argument("-u", "--under26", action="store_true",
                            help="calculate net for people under 26 years old.")
    arg_parser.add_argument("-d", "--diff_city", action="store_true",
                            help="calculate net for working in different city.")
    arg_parser.add_argument("-r", "--raw", action="store_true",
                            help="Outputs only calculated net values in format: val val val...")
    arg_parser.add_argument("-p", "--ppk", type=ppk,
                            help="set ppk share (min 2.0 max 4.0).")
    return arg_parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    if len(args.gross) > 12:
        print(f"Too much values to calculate. Max 12 given {len(args.gross)}.")
        sys.exit()
    if args.under26:
        Calculator.set_end26year(False)
    if args.diff_city:
        Calculator.set_the_same_city(False)
    if args.ppk:
        Calculator.set_ppk(args.ppk)

    Calculator.set_values(args.gross)
    results = Calculator.get_results()
    if args.raw:
        print(*[val[1] for val in results])
        sys.exit()

    print_table(results)
    if args.chart:
        draw_plot(results)


if __name__ == '__main__':
    main()
