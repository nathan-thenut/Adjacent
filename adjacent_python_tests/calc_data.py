from pathlib import Path
import pprint
import numpy as np
import matplotlib.pyplot as plt
from core_utils import read_results, Result


def get_results_from_dir(path: Path) -> (dict[str, dict], dict[str, dict]):
    """gets all results from files in a dir"""
    overall_results = {}

    for file in list(path.glob("*.json")):
        results = read_results(file)
        keys = list(results.keys())
        keys.remove("variables")
        for key in keys:
            if key not in overall_results.keys():
                overall_results[key] = {}
            keyresults = overall_results[key]
            for result_key in results[key].keys():
                if result_key not in keyresults.keys():
                    keyresults[result_key] = []
                keyresults[result_key].append(results[key][result_key])

    # add average and standard variance
    avg_results = {}
    for key in overall_results.keys():
        for result_key in [Result.L1.name, Result.L2.name]:
            value_list = overall_results[key][result_key]
            average = np.average(value_list)
            std_var = np.std(value_list)
            if key not in avg_results.keys():
                avg_results[key] = {}
            if "avg" not in avg_results[key].keys():
                avg_results[key]["avg"] = {}
            if "std_var" not in avg_results[key].keys():
                avg_results[key]["std_var"] = {}
            avg_results[key]["avg"][result_key] = average
            avg_results[key]["std_var"][result_key] = std_var

    return (overall_results, avg_results)


def two_row_boxplot(paths: list[Path], xticklabels: list[str], key: str,
                    xlabel: str, ylabel: str):
    """Creates a two row boxplot."""

    fig, axes = plt.subplots(2, 1)
    l1_plots = []
    l2_plots = []
    for path in paths:
        results, avg = get_results_from_dir(path)
        l1_plots.append(results[key]["L1"])
        l2_plots.append(results[key]["L2"])

    l1_ax = axes[0]
    l2_ax = axes[1]
    l1_ax.boxplot(l1_plots)
    l1_ax.set_title('L1')
    l1_ax.set_xticklabels(xticklabels)
    l1_ax.set_xlabel(xlabel)
    l1_ax.set_ylabel(ylabel)

    l2_ax.boxplot(l2_plots)
    l2_ax.set_title('L2')
    l2_ax.set_xticklabels(xticklabels)
    l2_ax.set_xlabel(xlabel)
    l2_ax.set_ylabel(ylabel)

    plt.show()


def triangle_01_runtime_boxplot():
    """Creates a boxplot for triangle 01 time values."""
    path = Path("/home/nathan/Downloads/Books/triangle-01/")
    results, avg = get_results_from_dir(path)
    # pprint.pprint(results)

    l1_time = results["time"]["L1"]
    l2_time = results["time"]["L2"]

    fig = plt.figure()
    ax = fig.add_subplot(121)
    bp = ax.boxplot(l1_time)
    ax.set_title("L1 runtime")
    plt.semilogy()
    # ax.set_yscale('log')
    # ax.set_xticklabels(['L1 runtime', 'L2 runtime'])
    ax = fig.add_subplot(122)
    bp = ax.boxplot(l2_time)
    ax.set_title("L2 runtime")

    plt.semilogy()
    plt.show()


def triangle_01_norms_boxplot():
    """Creates a boxplot for triangle 01 norm values."""
    path = Path("/home/nathan/Downloads/Books/triangle-01/")
    results, avg = get_results_from_dir(path)
    # pprint.pprint(results)

    l1_l1_norm = results["l1_norm"]["L1"]
    l1_l2_norm = results["l2_norm"]["L1"]

    l2_l1_norm = results["l1_norm"]["L2"]
    l2_l2_norm = results["l2_norm"]["L2"]

    fig = plt.figure()
    ax = fig.add_subplot(121)
    bp = ax.boxplot([l1_l1_norm, l2_l1_norm])
    ax.set_title('$l_1$ norm')
    ax.set_xticklabels(['L1', 'L2'])
    ax = fig.add_subplot(122)
    bp = ax.boxplot([l1_l2_norm, l2_l2_norm])
    ax.set_title('$l_2$ norm')
    ax.set_xticklabels(['L1', 'L2'])

    plt.show()


def triangle_02_boxplots():
    """Creates a boxplot for triangle 02 norm values."""
    main_path = Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/02/")
    paths = [(main_path / "length_05"), (main_path / "length_1"),
             (main_path / "length_2"), (main_path / "length_3"),
             (main_path / "length_4"), (main_path / "length_5")]

    # norm plot settings
    xticklabels = ['0.5', '1', '2', '3', '4', '5']
    two_row_boxplot(paths,
                    xticklabels,
                    key="l1_norm",
                    xlabel="Distance",
                    ylabel='$l_1$ norm')

    # two_row_boxplot(paths,
    #                 xticklabels,
    #                 key="time",
    #                 xlabel="Distance",
    #                 ylabel='Time (s)')


if __name__ == '__main__':
    # results, avg = get_results_from_dir(
    #     Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/02/length_5"))
    # pprint.pprint(avg)
    triangle_02_boxplots()
