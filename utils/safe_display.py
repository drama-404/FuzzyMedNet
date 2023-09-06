"""
Utility functions to help with displaying data_preprocessing in a safer, "blinded" way.
Note: ALWAYS set blinded=True before PUSH
"""

from IPython.display import display
import inspect


def retrieve_name_in_fn(var):
    """
    Parameters
    ----------
    var

    Returns
    -------
    The name of the variable `var` as a string
    """
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    out = [var_name for var_name, var_val in callers_local_vars if var_val is var]
    assert len(out) == 1
    return out[0]


def blind_display(*dfs, blinded=True):
    """
    Parameters
    ----------
    dfs - takes one or more DataFrames as its arguments.
    blinded - safety flag
    -------
    For each DataFrame passed: It prints the shape of the DataFrame.
    Based on the BLINDED flag:
        If BLINDED is True, it displays the DataFrame's header without any rows.
        If BLINDED is False, it displays the top 5 rows of the DataFrame.
    """
    for df in dfs:
        print(f"{retrieve_name_in_fn(df)}.shape: ", df.shape)
        if blinded:
            display(df.head(0))
        else:
            display(df.head())
