import itertools
import pandas as pd
import numpy as np
from pandas.core.arrays.datetimes import generate_regular_range

percents_list = [
    0.4645,
    0.4641,
    0.0194,
    0.0194,
    0.0194,
    0.0082,
    0.0037,
    0.0005,
    0.0005,
]
print(f"summ percents = {sum(percents_list)}")


costs_list = [
    8.45,
    0.01,
    54.73,
    0.01,
    8.29,
    514.36,
    0.01,
    0.01,
    32.52,
]

query_type = [
    "write",
    "write",
    "read",
    "write",
    "read",
    "read",
    "write",
    "write",
    "read",
]


def weighted_average_of_group(values, weights, item):
    return (values * weights).groupby(item).sum() / weights.groupby(item).sum()


df_costs = pd.DataFrame({"type": query_type, "cost": costs_list, "wt": percents_list})

weighted_costs = weighted_average_of_group(
    values=df_costs.cost, weights=df_costs.wt, item=df_costs.type
)

percents = df_costs.groupby("type").wt.sum() * 100

connections = [20, 80, 100, 300, 50]
read_percent = [4.7]
write_percent = [95.3]
# db_mem_coef = [3.694 / 2, 3.694 / 3]
# pgpool_cache_coef = [3.694 / 3, 3.694 / 4]
db_mem_coef = [2 / 3.694, 3 / 3.694]
pgpool_cache_coef = [3 / 3.694, 4 / 3.694]

read_cost = [weighted_costs["read"]]
write_cost = [weighted_costs["write"]]

read_percent = [percents["read"]]
write_percent = [percents["write"]]

gen_template_params_list = list(
    itertools.product(
        connections,
        read_percent,
        write_percent,
        db_mem_coef,
        pgpool_cache_coef,
        read_cost,
        write_cost,
    )
)

client_df = pd.DataFrame(
    data=gen_template_params_list,
    columns=[
        "connections",
        "read_percent",
        "write_percent",
        "db_mem_coef",
        "pgpool_cache_coef",
        "read_cost",
        "write_cost",
    ],
)
print(client_df)

client_df.to_csv("eticum_params2.csv")
client_df.to_excel("eticum_params2.xlsx", index=False)
