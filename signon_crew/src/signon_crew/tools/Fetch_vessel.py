from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel , Field
import snowflake.connector
import os
import pandas as pd

class FetchVesselPosition(BaseTool):
    name: str = "Vessel Data Fetcher"
    description: str = "Fetches  data, comments, and activity from a Snowflake"
    
    def _run(self, imo: str) ->dict:
        # Your tool's logic here
        def snowflake_conn():
            con = snowflake.connector.connect(
            user='AGENTIC_AI',
            password=os.getenv("SNOWFLAKE_CREDS"),
            role='AGENTIC_AI_ROLE',
            account='ew45124.central-india.azure',
            database='OPEN_ANALYTICS_ZONE',
            schema='KS_SCRATCHPAD',
            warehouse='AGENTIC_AI_WH'
            )
            return con
        
        stmt = f"""   select imo , lat, lon , market , shipname , ship_class , type_name ,current_port , next_port_country , next_port_unlocode , eta_calc ,speed , avg_speed , distance_to_go
          from OPEN_ANALYTICS_ZONE.KS_SCRATCHPAD.vessel_position
            where imo ={imo}
            qualify row_number() over (PARTITION BY IMO ORDER BY TIMESTAMP DESC) =1 """

        sf_con = snowflake_conn()
        cur = sf_con.cursor()
        sf_stmt = cur.execute(stmt).fetchall()
        hdrs = pd.DataFrame(cur.description)
        result = pd.DataFrame(sf_stmt)
        result.columns = hdrs['name']
        result_json = result.to_json(date_format='iso')
        return result_json
