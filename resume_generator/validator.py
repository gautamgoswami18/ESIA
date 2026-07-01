import pandas as pd


def validate_columns(df, required_columns, file_name):

    missing = []

    for column in required_columns:

        if column not in df.columns:
            missing.append(column)

    if missing:

        raise Exception(
            f"{file_name} is missing columns : {missing}"
        )

    return True