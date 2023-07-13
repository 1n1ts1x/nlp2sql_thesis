class Query:
    def __init__(self):
        pass

    def prepare_query(self, where='', table='', flag=False, flag_good_bad=False):
        if flag:
            return f'''
                SELECT id, Date_n_Time, 'Temperature' AS param, Temperature AS pvalue
                FROM {table}
                WHERE Temperature {"<" if flag_good_bad else ">="} (SELECT opt_temp_from FROM ideal_parameters)
                    OR Temperature {">" if flag_good_bad else "<="} (SELECT opt_temp_to FROM ideal_parameters)
                UNION
                SELECT id, Date_n_Time, 'Humidity' AS param, Humidity AS pvalue
                FROM {table}
                WHERE Humidity {"<" if flag_good_bad else ">="} (SELECT opt_humid_from FROM ideal_parameters)
                    OR Humidity {">" if flag_good_bad else "<="} (SELECT opt_humid_to FROM ideal_parameters)
                UNION
                SELECT id, Date_n_Time, 'Soil_Moisture' AS param, Soil_Moisture AS pvalue
                FROM {table}
                WHERE Soil_Moisture {"<" if flag_good_bad else ">="} (SELECT opt_soil_from FROM ideal_parameters)
                    OR Soil_Moisture {">" if flag_good_bad else "<="} (SELECT opt_soil_to FROM ideal_parameters)
                UNION
                SELECT id, Date_n_Time, 'Air_Quality' AS param, Air_Quality AS pvalue
                FROM {table}
                WHERE Air_Quality {"<" if flag_good_bad else ">="} (SELECT opt_air_from FROM ideal_parameters)
                    OR Air_Quality {">" if flag_good_bad else "<="} (SELECT opt_air_to FROM ideal_parameters)
                UNION
                SELECT id, Date_n_Time, 'Light_Intensity' AS param, Light_Intensity AS pvalue
                FROM {table}
                WHERE Light_Intensity {"<" if flag_good_bad else ">="} (SELECT opt_light_from FROM ideal_parameters)
                    OR Light_Intensity {">" if flag_good_bad else "<="} (SELECT opt_light_to FROM ideal_parameters);
            '''
        else:
            return f'''
                SELECT 
                    SUM(CASE WHEN p = 'TRUE' THEN 1 ELSE 0 END) AS count_temperature,
                    SUM(CASE WHEN p2 = 'TRUE' THEN 1 ELSE 0 END) AS count_humidity,
                    SUM(CASE WHEN p3 = 'TRUE' THEN 1 ELSE 0 END) AS count_soil,
                    SUM(CASE WHEN p4 = 'TRUE' THEN 1 ELSE 0 END) AS count_air,
                    SUM(CASE WHEN p5 = 'TRUE' THEN 1 ELSE 0 END) AS count_light
                FROM 
                    (SELECT
                        CASE WHEN EXISTS (
                                SELECT Temperature 
                                FROM {table} 
                                WHERE Temperature >= (SELECT opt_temp_from FROM ideal_parameters) 
                                AND Temperature <= (SELECT opt_temp_to FROM ideal_parameters) {'AND '  + where if len(where) > 0 else ''} 
                            ) THEN 'TRUE' ELSE 'FALSE' 
                        END AS p,
                        CASE WHEN EXISTS (
                                SELECT Humidity 
                                FROM {table} 
                                WHERE Humidity >= (SELECT opt_humid_from FROM ideal_parameters) 
                                AND Humidity <= (SELECT opt_humid_to FROM ideal_parameters) {'AND ' + where if len(where) > 0 else ''} 
                            ) THEN 'TRUE' ELSE 'FALSE' 
                        END AS p2,
                        CASE WHEN EXISTS (
                                SELECT Soil_Moisture 
                                FROM {table} 
                                WHERE Soil_Moisture >= (SELECT opt_soil_from FROM ideal_parameters) 
                                AND Soil_Moisture <= (SELECT opt_soil_to FROM ideal_parameters) {'AND ' + where if len(where) > 0 else ''} 
                            ) THEN 'TRUE' ELSE 'FALSE' 
                        END AS p3,
                        CASE WHEN EXISTS (
                                SELECT Air_Quality 
                                FROM {table} 
                                WHERE Air_Quality >= (SELECT opt_air_from FROM ideal_parameters) 
                                AND Air_Quality <= (SELECT opt_air_to FROM ideal_parameters) {'AND ' + where if len(where) > 0 else ''} 
                            ) THEN 'TRUE' ELSE 'FALSE' 
                        END AS p4,
                        CASE WHEN EXISTS (
                                SELECT Light_Intensity 
                                FROM {table} 
                                WHERE Light_Intensity >= (SELECT opt_light_from FROM ideal_parameters) 
                                AND Light_Intensity <= (SELECT opt_light_to FROM ideal_parameters) {'AND ' + where if len(where) > 0 else ''} 
                            ) THEN 'TRUE' ELSE 'FALSE' 
                        END AS p5
                    ) AS params;
            '''
