def get_df_col_val(df, index):
    return df.iloc(0)[index].value


def get_val(v: str):
    return int(v) if str(v).isnumeric() else 0


def goals(df):
    return get_val(get_df_col_val(df, 0))


def shots(df):
    shots_split = get_df_col_val(df, 1).split("/")
    return get_val(shots_split[0]) + get_val(shots_split[1])


def shots_on_target(df):
    shots_split = get_df_col_val(df, 1).split("/")
    return get_val(shots_split[0])


def assists(df):
    return get_val(get_df_col_val(df, 0))


def passes_completed(df):
    passes_split = get_df_col_val(df, 1).split("/")
    return get_val(passes_split[0]) + get_val(passes_split[1]) + get_val(passes_split[2])


def passes_attempted(df):
    passes_split = get_df_col_val(df, 2).split("/")
    return passes_completed(df) + get_val(passes_split[0]) + get_val(passes_split[1]) + get_val(passes_split[2])


def key_passes(df):
    return get_val(get_df_col_val(df, 3))


def crosses_completed(df):
    crosses_split = get_df_col_val(df, 4).split("/")
    return get_val(crosses_split[0])


def crosses_attempted(df):
    crosses_split = get_df_col_val(df, 4).split("/")
    return crosses_completed(df) + get_val(crosses_split[1])


def player_id(df):
    return get_df_col_val(df, 0)


def tackles_won(df):
    return get_val(get_df_col_val(df, 0))


def interceptions(df):
    interceptions_split = get_df_col_val(df, 0).split("/")
    return get_val(interceptions_split[0])


def blocks(df):
    interceptions_split = get_df_col_val(df, 0).split("/")
    return get_val(interceptions_split[1])


def possession_won(df):
    possession_split = get_df_col_val(df, 0).split("/")
    return get_val(possession_split[0])


def possession_lost(df):
    possession_split = get_df_col_val(df, 0).split("/")
    return get_val(possession_split[1])


def headers_won(df):
    possession_split = get_df_col_val(df, 2).split("/")
    return get_val(possession_split[0])
