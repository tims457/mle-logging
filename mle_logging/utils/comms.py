import numpy as np
from typing import Union, List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import datetime
from .._version import __version__


console_width = 100


def print_welcome() -> None:
    """Display header with clock and general logging configurations."""
    welcome_ascii = r"""
 __    __  __      ______  __      ______  ______
/\ "-./  \/\ \    /\  ___\/\ \    /\  __ \/\  ___\
\ \ \-./\ \ \ \___\ \  __\  \ \___\ \ \/\ \ \ \__ \
 \ \_\ \ \_\ \_____\ \_____\ \_____\ \_____\ \_____\
  \/_/  \/_/\/_____/\/_____/\/_____/\/_____/\/_____/
    """.splitlines()
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")
    grid.add_row(
        welcome_ascii[1],
        datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S"),
    )
    grid.add_row(welcome_ascii[2], f"Logger v{__version__} :lock_with_ink_pen:")
    grid.add_row(
        welcome_ascii[3],
        "  [link=https://twitter.com/RobertTLange]@RobertTLange[/link] :bird:",
    )
    grid.add_row(
        welcome_ascii[4],
        "  [link=https://github.com/RobertTLange/mle-logging/blob/main/examples/getting_started.ipynb]MLE-Log"
        " Docs[/link] [not italic]:notebook:[/]",  # noqa: E501
    )
    grid.add_row(
        welcome_ascii[5],
        "  [link=https://github.com/RobertTLange/mle-logging/]MLE-Log"
        " Repo[/link] [not italic]:pencil:[/]",  # noqa: E501
    )
    panel = Panel(grid, style="white on blue", expand=True)
    Console(width=console_width).print(panel)


def print_startup(
    experiment_dir: str,
    config_fname: Union[str, None],
    time_to_track: Union[List[str], None],
    what_to_track: Union[List[str], None],
    model_type: str,
    seed_id: Union[str, int],
    use_tboard: bool,
    reload: bool,
    print_every_k_updates: Union[int, None],
    ckpt_time_to_track: Union[str, None],
    save_every_k_ckpt: Union[int, None],
    save_top_k_ckpt: Union[int, None],
    top_k_metric_name: Union[str, None],
    top_k_minimize_metric: Union[bool, None],
) -> None:
    """Rich print statement at logger startup.

    Args:
        experiment_dir (str): Base experiment directory.
        config_fname (Union[str, None]): Name of job configuration.
        time_to_track (Union[List[str], None]): Time variable names to store.
        what_to_track (Union[List[str], None]): Stats variable names to store.
        model_type (str): Model type to store ("jax", "torch", "tensorflow").
        seed_id (Union[str, int]): Random seed used in experiment
        use_tboard (bool): Whether to also create tensorboard log.
        reload (bool): Whether to use reloaded previous log.
        print_every_k_updates (Union[int, None]): How often to print out log update.
        ckpt_time_to_track (Union[str, None]): Which time var to log with model ckpt.
        save_every_k_ckpt (Union[int, None]): How often to log model ckpt.
        save_top_k_ckpt (Union[int, None]): How many top performing ckpts to store.
        top_k_metric_name (Union[str, None]): Which stats var to use for performance.
        top_k_minimize_metric (Union[bool, None]): Whether to minimize the stats var.
    """
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="left")

    def format_content(title, value):
        if type(value) == list:
            base = f"[b]{title}[/b]: "
            for i, v in enumerate(value):
                base += f"{v}"
                if i < len(value) - 1:
                    base += ", "
            return base
        else:
            return f"[b]{title}[/b]: {value}"

    time_to_print = [
        t for t in time_to_track if t not in ["time", "time_elapsed"]
    ]
    renderables = [
        Panel(format_content(":book: Log Dir", experiment_dir), expand=True),
        Panel(
            format_content(":page_facing_up: Config", config_fname), expand=True
        ),
        Panel(format_content(":watch: Time", time_to_print), expand=True),
        Panel(
            format_content(":chart_with_downwards_trend: Stats", what_to_track),
            expand=True,
        ),
        Panel(format_content(":seedling: Seed ID", seed_id), expand=True),
        Panel(
            format_content(
                ":chart_with_upwards_trend: Tensorboard", use_tboard
            ),
            expand=True,
        ),
        Panel(format_content(":rocket: Model", model_type), expand=True),
        Panel(
            format_content("Tracked ckpt Time", ckpt_time_to_track), expand=True
        ),
        Panel(
            format_content(":clock1130: Every k-th ckpt", save_every_k_ckpt),
            expand=True,
        ),
        Panel(
            format_content(":trident: Top k ckpt", save_top_k_ckpt), expand=True
        ),
        Panel(
            format_content("Top k-th metric", top_k_metric_name), expand=True
        ),
        Panel(
            format_content("Top k-th minimization", top_k_minimize_metric),
            expand=True,
        ),
    ]

    grid.add_row(renderables[0], renderables[1])
    grid.add_row(renderables[2], renderables[3])
    grid.add_row(renderables[4], renderables[6])
    if save_every_k_ckpt is None and save_top_k_ckpt is not None:
        grid.add_row(
            renderables[9],
        )
    elif save_every_k_ckpt is not None and save_top_k_ckpt is None:
        grid.add_row(
            renderables[8],
        )
    elif save_every_k_ckpt is not None and save_top_k_ckpt is not None:
        grid.add_row(renderables[8], renderables[9])
    # grid.add_row(renderables[10], renderables[11])
    panel = Panel(grid, expand=True)
    Console(width=console_width).print(panel)


def print_update(
    time_to_print: List[str],
    what_to_print: List[str],
    c_tick: Dict[str, Union[str, float]],
    s_tick: Dict[str, float],
    print_header: bool,
) -> None:
    """Rich print statement for logger update.

    Args:
        time_to_print (List[str]): List of time variable names to print.
        what_to_print (List[str]): List of stats variable names to print.
        c_tick (Dict[str, Union[str, float]]): Dict of time variable values.
        s_tick (Dict[str, float]): Dict of stats variable values.
        print_header (bool): Whether to print table header.
    """
    table = Table(
        show_header=print_header,
        row_styles=["none"],
        border_style="white",
        box=box.SIMPLE,
    )
    # Add watch and book emoji
    for i, c_label in enumerate(time_to_print):
        if i == 0:
            table.add_column(
                ":watch: [red]" + c_label + "[/red]",
                style="red",
                width=14,
                justify="left",
            )
        else:
            table.add_column(
                "[red]" + c_label + "[/red]",
                style="red",
                width=12,
                justify="center",
            )
    for i, c_label in enumerate(what_to_print):
        if i == 0:
            table.add_column(
                ":chart_with_downwards_trend: [blue]" + c_label + "[/blue]",
                width=14,
                justify="center",
            )
        else:
            table.add_column(
                "[blue]" + c_label + "[/blue]",
                width=12,
                justify="center",
            )
    row_list_time = []
    for c in time_to_print:
        if c in c_tick.keys():
            row_list_time.append(c_tick[c])
        else:
            row_list_time.append("---")
    row_list_stats = []
    for s in what_to_print:
        if s in s_tick.keys():
            row_list_stats.append(np.round_(s_tick[s], 3))
        else:
            row_list_stats.append("---")
    row_list = row_list_time + row_list_stats
    row_str_list = [str(v) for v in row_list]
    table.add_row(*row_str_list)

    # Print statistics update
    Console(width=console_width).print(table, justify="center")


def print_reload(experiment_dir: str) -> None:
    """Rich print statement for logger reloading.

    Args:
        experiment_dir (str): Base experiment directory.
    """
    Console().log(f"Reloaded log from {experiment_dir}")


def print_storage(
    fig_path: Union[str, None] = None,
    extra_path: Union[str, None] = None,
    init_model_path: Union[str, None] = None,
    final_model_path: Union[str, None] = None,
    every_k_model_path: Union[str, None] = None,
    top_k_model_path: Union[str, None] = None,
    print_first: bool = False,
):
    """Rich print statement for object saving log.

    Args:
        fig_path (Union[str, None], optional):
            Path figure was stored at. Defaults to None.
        extra_path (Union[str, None], optional):
            Path extra object was stored at. Defaults to None.
        init_model_path (Union[str, None], optional):
            Path initial model ckpt was stored at. Defaults to None.
        final_model_path (Union[str, None], optional):
            Path most recent model ckpt was stored at. Defaults to None.
        every_k_model_path (Union[str, None], optional):
            Path last k-th update model ckpt was stored at. Defaults to None.
        top_k_model_path (Union[str, None], optional):
            Path top-k model ckpt was stored at. Defaults to None.
        print_first (bool, optional):
            Whether to always print init/final ckpt path. Defaults to False.
    """
    table = Table(
        show_header=False,
        row_styles=["none"],
        border_style="white",
        box=box.SIMPLE,
    )

    table.add_column(
        "---",
        style="red",
        width=16,
        justify="left",
    )

    table.add_column(
        "---",
        style="red",
        width=64,
        justify="left",
    )

    if fig_path is not None:
        table.add_row(":envelope_with_arrow: - Figure", f"{fig_path}")
    if extra_path is not None:
        table.add_row(":envelope_with_arrow: - Extra", f"{extra_path}")
    if init_model_path is not None and print_first:
        table.add_row(":envelope_with_arrow: - Model", f"{init_model_path}")
    if final_model_path is not None and print_first:
        table.add_row(":envelope_with_arrow: - Model", f"{final_model_path}")
    if every_k_model_path is not None:
        table.add_row(
            ":envelope_with_arrow: - Every-K", f"{every_k_model_path}"
        )
    if top_k_model_path is not None:
        table.add_row(":envelope_with_arrow: - Top-K", f"{top_k_model_path}")

    to_print = (
        (fig_path is not None)
        + (extra_path is not None)
        + (init_model_path is not None and print_first)
        + (final_model_path is not None and print_first)
        + (every_k_model_path is not None)
        + (top_k_model_path is not None)
    ) > 0
    # Print storage update
    if to_print:
        Console(width=console_width).print(table, justify="left")
