import json


def bulk_update_json_table(table, primary_key, data):
    col_str = ""
    col_list_str = ""
    column_names = data[0].keys()

    for i, col in enumerate(column_names):
        if col != primary_key:
            print(col)
            if i == len(column_names) - 1:
                col_str += f"{col} = c.{col}"
            else:
                col_str += f"{col} = c.{col}, "
        if i == len(column_names) - 1:
            col_list_str += f"{col}"
        else:
            col_list_str += f"{col}, "

    master_values = ""
    for j, data_json in enumerate(data):
        value_tup = "("
        for ind, key in enumerate(data_json.keys()):
            if type(data_json[key]) == str:
                data_value = f"'{data_json[key]}'"
            else:
                data_value = data_json[key]
            if ind in [1, 2, 3, 4, 5, 6]:
                value_tup += (
                    "'" + json.dumps(data_value).replace("'", "''") + "'" + "::jsonb,"
                )
            else:
                if ind == len(data_json) - 1:
                    value_tup += f"{data_value}"
                else:
                    value_tup += f"{data_value}, "
        value_tup += ")"

        if j == len(data) - 1:
            master_values += value_tup
        else:
            master_values += f"{value_tup}, "

    update_query = f"""update {table} as t set 
    {col_str}
from 
    (values 
        {master_values}
    ) as c({col_list_str})
where 
    c.{primary_key} = t.{primary_key}"""

    return update_query


f = open("share_review_card.json")
data = json.load(f)


bulk_update_query = bulk_update_json_table(
    "app.figma_review_templates", "figma_id", data
)

print(0)
