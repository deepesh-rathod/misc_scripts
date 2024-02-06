def generate_trigger_function(sql_query):
    # Extract table name from SQL query
    table_name_start = sql_query.find('CREATE TABLE ') + len('CREATE TABLE ')
    table_name_end = sql_query.find('(', table_name_start)
    table_name_str = sql_query[table_name_start:table_name_end].strip()

    if "." in table_name_str:
        table_name = table_name_str.split(".")[1]
        schema_name = table_name_str.split(".")[0]
    else:
        table_name = table_name_str
        schema_name = 'public'

    # Extract column names and clean them
    columns = []
    parts = sql_query.splitlines()

    for part in parts:
        if part.strip().startswith('"'):
            columns.append(part.split('"')[1])

    table_name=table_name.replace('"',"")

    # Generate trigger function
    trigger_function = f"""CREATE OR REPLACE FUNCTION {schema_name}.{table_name}_logs()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO {schema_name}."{table_name}_logs" ({', '.join(columns)}, operation)
            VALUES({', '.join([f'NEW.{column}' for column in columns])}, 'INSERT');
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO {schema_name}."{table_name}_logs" ({', '.join(columns)}, operation)
            VALUES({', '.join([f'OLD.{column}' for column in columns])}, 'UPDATE');
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO {schema_name}."{table_name}_logs" ({', '.join(columns)}, operation)
            VALUES({', '.join([f'OLD.{column}' for column in columns])}, 'DELETE');
    END IF;
    RETURN NEW;
END;
$function$"""

    return trigger_function

# Sample Input
sql_query = """
CREATE TABLE "campaigns"."app_form" (
    "id" int4 NOT NULL DEFAULT nextval('campaigns.app_form_id_seq'::regclass),
    "uid" uuid,
    "prompt" varchar,
    "flyer" varchar,
    "duration" json,
    "campaign_group_id" uuid,
    "name" varchar,
    "step" varchar DEFAULT 'OFFER_PROMPT_SELECTED'::character varying,
    "clients_added" bool DEFAULT false,
    "campaign_stage" varchar DEFAULT 'USER_CREATION'::character varying,
    "created_at" timestamp DEFAULT now(),
    "all_clients_selected" bool,
    "deleted" bool DEFAULT false,
    "clients_count" int4 DEFAULT 0,
    PRIMARY KEY ("id")
);
"""

# Generate and print the trigger function
trigger_function = generate_trigger_function(sql_query)
print(trigger_function)
