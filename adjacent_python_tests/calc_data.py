from pathlib import Path
import pprint
import numpy as np
import matplotlib.pyplot as plt
from core_utils import read_results, Result


def get_results_from_dir(path: Path) -> dict[str, dict]:
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
    for key in overall_results.keys():
        for result_key in [Result.L1.name, Result.L2.name]:
            value_list = overall_results[key][result_key]
            average = np.average(value_list)
            std_var = np.std(value_list)
            if "avg" not in overall_results[key].keys():
                overall_results[key]["avg"] = {}
            if "std_var" not in overall_results[key].keys():
                overall_results[key]["std_var"] = {}
            overall_results[key]["avg"][result_key] = average
            overall_results[key]["std_var"][result_key] = std_var

    return overall_results


def triangle_01_runtime_boxplot():
    """Creates a boxplot for triangle 01 time values."""
    path = Path("/home/nathan/Downloads/Books/triangle-01/")
    results = get_results_from_dir(path)
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
    results = get_results_from_dir(path)
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


if __name__ == '__main__':
    triangle_01_norms_boxplot()
