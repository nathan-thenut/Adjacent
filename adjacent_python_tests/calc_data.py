from pathlib import Path
import pprint
import numpy as np
import matplotlib.pyplot as plt
from core_utils import read_results, Result

FIGURE_PATH = "/home/nathan/Uni-Stuff/CG/Abschlussarbeit/latex/figures/pgf/dataplots/"

SIZE = (9.53, 4.64)


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


def find_not_converged_results(path: Path, remove_files: bool = False):
    """Find results where adjacent didn't converge."""
    not_converged = []
    for file in list(path.glob("*.json")):
        results = read_results(file)
        # if 0 in results["l1_norm"].values():
        #     print(file)
        if 22 in results["steps"].values():
            print(file)
            not_converged.append(file)

    print(f"Found {len(not_converged)} not converged results.")
    if remove_files:
        print("Removing not converged results")
        for file in not_converged:
            file.unlink()


def two_boxplots(paths: list[Path],
                 xticklabels: list[str],
                 key: str,
                 xlabel: str,
                 ylabel: str,
                 filename: str,
                 two_row: bool = True):
    """Creates a two row boxplot."""
    if two_row:
        fig, axes = plt.subplots(2, 1, sharex=True)
    else:
        fig, axes = plt.subplots(1, 2, sharey=True)

    fig.set_tight_layout(True)
    fig.set_size_inches(SIZE, forward=True)
    l1_plots = []
    l2_plots = []
    for path in paths:
        results, avg = get_results_from_dir(path)
        l1_plots.append(results[key]["L1"])
        l2_plots.append(results[key]["L2"])

    l1_ax = axes[0]
    l2_ax = axes[1]
    l1_ax.boxplot(l1_plots)
    l1_ax.set_yscale('log')
    l1_ax.set_title('L1')
    if xticklabels and not two_row:
        l1_ax.set_xticklabels(xticklabels)
    # l1_ax.set_xlabel(xlabel)
    l1_ax.set_ylabel(ylabel)

    l2_ax.boxplot(l2_plots)
    l2_ax.set_yscale('log')
    l2_ax.set_title('L2')
    # if xticklabels:
    #     l2_ax.set_xticklabels(xticklabels)
    l2_ax.set_xlabel(xlabel)
    if two_row:
        l2_ax.set_ylabel(ylabel)
        if xticklabels:
            l2_ax.set_xticks(range(1, len(xticklabels) + 1))
            l2_ax.set_xticklabels(xticklabels)
    plt.savefig(filename, format="pgf")
    plt.show()


def single_boxplot(paths: list[Path], xticklabels: list[str], key: str,
                   result_key: str, xlabel: str, ylabel: str, title: str,
                   filename: str):
    """Creates a single boxplot."""

    fig = plt.figure()
    ax = fig.add_subplot()
    fig.set_tight_layout(True)
    fig.set_size_inches(SIZE, forward=True)
    plots = []
    for path in paths:
        results, avg = get_results_from_dir(path)
        plots.append(results[key][result_key])

    ax.boxplot(plots)
    ax.set_yscale('log')
    ax.set_title(title)
    if xticklabels:
        ax.set_xticklabels(xticklabels)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.savefig(filename, format="pgf")
    plt.show()


def two_row_barplot(path: Path,
                    key: str,
                    xlabel: str,
                    ylabel: str,
                    filename: str,
                    is_printing: bool = False):
    """Create a two-row barplot."""
    results, avg = get_results_from_dir(path)

    l1_data = results[key]["L1"]
    l2_data = results[key]["L2"]
    l1_bins, l1_counts = np.unique(l1_data, return_counts=True)
    l2_bins, l2_counts = np.unique(l2_data, return_counts=True)
    if is_printing:
        l1_str = f"L1 & {np.average(l1_data)} & {l1_bins[l1_counts.argmax()]} & {np.median(l1_data)}\\\\"
        l2_str = f"L2 & {np.average(l2_data)} & {l2_bins[l2_counts.argmax()]} & {np.median(l2_data)}\\\\"
        print(l1_str)
        print(l2_str)

    fig, axes = plt.subplots(2, 1, sharey=True, sharex=True, tight_layout=True)
    fig.set_tight_layout(True)
    fig.set_size_inches(SIZE, forward=True)

    bins = list(l1_bins) + list(l2_bins)
    xticks = list(range(min(bins), max(bins) + 1))
    axes[0].bar(*(l1_bins, l1_counts))
    axes[0].set_title("L1")
    axes[0].set_ylabel(ylabel)
    axes[0].set_xticks(xticks)
    axes[1].bar(*(l2_bins, l2_counts))
    axes[1].set_title("L2")
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel(ylabel)
    axes[1].set_xticks(xticks)

    plt.savefig(filename, format="pgf")
    plt.show()


def three_by_two_barplot(paths: list[Path], titles: list[str], key: str,
                         result_key: str, xlabel: str, ylabel: str,
                         filename: str):
    """Three rows and two column barplots"""
    fig, axes = plt.subplots(3, 2, sharey=True, sharex=True, tight_layout=True)
    fig.set_size_inches((9.53, 2 * 4.64), forward=True)
    bins_list = []
    counts_list = []
    for path in paths:
        results, avg = get_results_from_dir(path)

        data = results[key][result_key]
        bins, counts = np.unique(data, return_counts=True)
        bins_list.append(bins)
        counts_list.append(counts)

    bins = np.concatenate(bins_list).ravel().tolist()
    xticks = list(range(min(bins + [0]), max(bins) + 1))
    i = 0
    for row in axes:
        for ax in row:
            if i < len(titles):
                ax.bar(*(bins_list[i], counts_list[i]))
                ax.set_title(titles[i])
                # ax.set_xlim(0.0, 7.74)
                # ax.set_xlim(0.0, 10.74)
                # ax.set_xlim(0.0, 21.30)
                # ax.set_xlim(0.0, 4.54)
                if i % 2 == 0:
                    ax.set_ylabel(ylabel)
                if i == 4 or i == 5 or (i == 3 and len(titles) == 5):
                    ax.set_xlabel(xlabel)
                    # ax.sharex(axes[-1][-1])
                ax.set_xticks(xticks)
                i = i + 1
            else:
                ax.axis('off')

    plt.savefig(filename, format="pgf")
    plt.show()


def triangle_01_runtime_boxplot():
    """Creates a boxplot for triangle 01 time values."""
    path = Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/01")
    results, avg = get_results_from_dir(path)
    # pprint.pprint(results)
    filename = FIGURE_PATH + "triangle_01_timing_boxplot.pgf"
    two_boxplots([path], [],
                 key="time",
                 xlabel="",
                 ylabel='Time (s)',
                 two_row=False,
                 filename=filename)


def triangle_01_norms_boxplot():
    """Creates a boxplot for triangle 01 norm values."""
    filename = FIGURE_PATH + "triangle_01_norms_boxplot.pgf"
    path = Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/01")
    results, avg = get_results_from_dir(path)
    # pprint.pprint(results)

    l1_l1_norm = results["l1_norm"]["L1"]
    l1_l2_norm = results["l2_norm"]["L1"]

    l2_l1_norm = results["l1_norm"]["L2"]
    l2_l2_norm = results["l2_norm"]["L2"]

    fig = plt.figure()
    fig.set_tight_layout(True)
    fig.set_size_inches(SIZE, forward=True)
    ax = fig.add_subplot(121)
    bp = ax.boxplot([l1_l1_norm, l2_l1_norm])
    ax.set_title('$l_1$ norm of offset')
    ax.set_xticklabels(['L1', 'L2'])
    ax = fig.add_subplot(122)
    bp = ax.boxplot([l1_l2_norm, l2_l2_norm])
    ax.set_title('$l_2$ norm of offset')
    ax.set_xticklabels(['L1', 'L2'])

    plt.savefig(filename, format="pgf")
    plt.show()


def triangle_01_barplots():
    """Barplot for triangle 01 data"""
    path = Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/01")
    find_not_converged_results(path)

    # filename = FIGURE_PATH + "triangle_01_steps_barplot.pgf"
    # two_row_barplot(path,
    #                 key="steps",
    #                 xlabel="Newton-Steps",
    #                 ylabel="Frequency",
    #                 filename=filename,
    #                 is_printing=True)

    # filename = FIGURE_PATH + "triangle_01_sparsity_barplot.pgf"
    # two_row_barplot(path,
    #                 key="non_zero_results",
    #                 xlabel="Non-zero results (Sparsity)",
    #                 ylabel="Frequency",
    #                 filename=filename,
    #                 is_printing=True)


def triangle_02_boxplots():
    """Creates boxplots for triangle 02."""
    main_path = Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/02/")
    paths = [(main_path / "length_05"), (main_path / "length_1"),
             (main_path / "length_2"), (main_path / "length_3"),
             (main_path / "length_4"), (main_path / "length_5")]

    # norm plot settings
    xticklabels = ['0.5', '1', '2', '3', '4', '5']
    # filename = FIGURE_PATH + "triangle_02_l1_norm_boxplot.pgf"
    # two_boxplots(paths,
    #              xticklabels,
    #              key="l1_norm",
    #              xlabel="Distance traveled by moved point in length units",
    #              ylabel='$l_1$ norm of offset',
    #              filename=filename)

    # two_boxplots(paths,
    #              xticklabels,
    #              key="time",
    #              xlabel="Distance",
    #              ylabel='Time (s)')

    filename = FIGURE_PATH + "triangle_02_l1_time_boxplot.pgf"
    single_boxplot(paths,
                   xticklabels,
                   key="time",
                   result_key="L1",
                   xlabel="Distance traveled by moved point in length units",
                   ylabel='Time (s)',
                   title='L1 runtime',
                   filename=filename)


def triangle_02_barplots():
    """Create triangle 02 barplots."""
    main_path = Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/02/")
    paths = [(main_path / "length_05"), (main_path / "length_1"),
             (main_path / "length_2"), (main_path / "length_3"),
             (main_path / "length_4"), (main_path / "length_5")]

    # counter = 1
    # for path in paths:
    #     filename = FIGURE_PATH + f"triangle_02_sparsity_barplot-{counter}.pgf"
    #     two_row_barplot(path,
    #                     key="non_zero_results",
    #                     xlabel="Non-zero results (Sparsity)",
    #                     ylabel="Frequency",
    #                     filename=filename)
    #     counter = counter + 1

    # filename = FIGURE_PATH + "triangle_02_l2_sparsity_barplot.pgf"
    titles = ["0.5", "1", "2", "3", "4", "5"]
    for i in range(len(titles)):
        titles[i] = "Distance of " + titles[i]
    # three_by_two_barplot(paths,
    #                      titles=titles,
    #                      key="non_zero_results",
    #                      result_key="L2",
    #                      xlabel="Non-zero results (Sparsity)",
    #                      ylabel="Frequency",
    #                      filename=filename)

    filename = FIGURE_PATH + "triangle_02_l2_steps_barplot.pgf"
    three_by_two_barplot(paths,
                         titles=titles,
                         key="steps",
                         result_key="L2",
                         xlabel="Newton-Steps",
                         ylabel="Frequency",
                         filename=filename)


def pentagon_01_boxplots():
    """Creates boxplots for pentagon 01."""
    main_path = Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/pentagon/01/")
    paths = [(main_path / "angle_1"), (main_path / "angle_2"),
             (main_path / "angle_3"), (main_path / "angle_4"),
             (main_path / "angle_5")]

    # norm plot settings
    xticklabels = ['1', '2', '3', '4', '5']
    # filename = FIGURE_PATH + "pentagon_01_l1_norm_boxplot.pgf"
    # two_boxplots(paths,
    #              xticklabels,
    #              key="l1_norm",
    #              xlabel="Number of angle constraints",
    #              ylabel='$l_1$ norm',
    #              filename=filename)

    filename = FIGURE_PATH + "pentagon_01_l1_time_boxplot.pgf"
    # two_boxplots(paths,
    #              xticklabels,
    #              key="time",
    #              xlabel="Number of angle constraints",
    #              ylabel='Time (s)',
    #              filename=filename)

    single_boxplot(paths,
                   xticklabels,
                   key="time",
                   result_key="L1",
                   xlabel="Number of angle constraints",
                   ylabel='Time (s)',
                   title='L1 runtime',
                   filename=filename)


def pentagon_01_barplots():
    """Creates barplots for pentagon 01."""
    main_path = Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/pentagon/01/")
    paths = [(main_path / "angle_1"), (main_path / "angle_2"),
             (main_path / "angle_3"), (main_path / "angle_4"),
             (main_path / "angle_5")]

    titles = ['1', '2', '3', '4', '5']
    for i in range(len(titles)):
        titles[i] = titles[i] + " angle constraint(s)"

    # filename = FIGURE_PATH + "pentagon_01_l2_sparsity_barplot.pgf"
    # three_by_two_barplot(paths,
    #                      titles=titles,
    #                      key="non_zero_results",
    #                      result_key="L2",
    #                      xlabel="Non-zero results (Sparsity)",
    #                      ylabel="Frequency",
    #                      filename=filename)

    filename = FIGURE_PATH + "pentagon_01_l2_steps_barplot.pgf"
    three_by_two_barplot(paths,
                         titles=titles,
                         key="steps",
                         result_key="L2",
                         xlabel="Newton-Steps",
                         ylabel="Frequency",
                         filename=filename)


if __name__ == '__main__':
    # results, avg = get_results_from_dir(
    #     Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/02/length_5"))
    # pprint.pprint(avg)
    # find_not_converged_results(Path("/home/nathan/Downloads/Books/"), True)
    # triangle_01_runtime_boxplot()
    # triangle_01_norms_boxplot()
    # triangle_01_barplots()
    # triangle_02_boxplots()
    # triangle_02_barplots()
    pentagon_01_boxplots()
    # pentagon_01_barplots()
