from psycopg2.extras import execute_values

# ET(L)
def load_data(connection, name_table, data):
    dtypes= data.dtypes
    cols= list(dtypes.index )
    tipos= list(dtypes.values)
    type_map = {'datetime64[ns]': 'TIMESTAMP', 'int64': 'INT','float64': 'FLOAT','object': 'VARCHAR(50)'}
    sql_dtypes = [type_map[str(dtype)] for dtype in tipos]
    column_defs = [f"{name} {data_type}" for name, data_type in zip(cols, sql_dtypes)]
    # ESQUEMA DE LA TABLA EN REDSHIFT
    # CREA LA TABLA
    temp_table_schema = f"""
        CREATE TABLE IF NOT EXISTS temp_data (
          {', '.join(column_defs)}, primary key(date)
        );
        """
    table_schema = f"""
        CREATE TABLE IF NOT EXISTS {name_table} (
          {', '.join(column_defs)}, primary key(date)
        );
        """
    # CURSOR
    cursor = connection.cursor()
    cursor.execute(temp_table_schema)
    cursor.execute(table_schema)
    # VALORES A INSERTAR EN LA TABLA
    values = [tuple(x) for x in data.to_numpy()]
    # EJECUCIÓN PARA CARGAR EN REDSHIFT
    cursor.execute("BEGIN")
    ##
    execute_values(
        cursor,
        f'''
        INSERT INTO temp_data ({', '.join(cols)}) VALUES %s
        ''',
        values,
    )
    cursor.execute(f"""
      DELETE FROM {name_table}
      USING temp_data
      WHERE {name_table}.date = temp_data.date;
    """
    )
    cursor.execute(f"""
      INSERT INTO {name_table}
      SELECT * FROM temp_data;
    """
    )
    cursor.execute("DELETE FROM temp_data;")
    cursor.execute("COMMIT")
    print('Proceso terminado')
    connection.close()