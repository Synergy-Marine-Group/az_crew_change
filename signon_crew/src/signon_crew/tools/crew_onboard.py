from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel , Field
import snowflake.connector
import os
import pandas as pd

class FetchCrewOnboard(BaseTool):
    name: str = "Crew Data Fetcher"
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
        
        stmt = f""" select 
                        seafarer_id , first_name , last_name , crew_code , nationality_name ,rank_name_se as rank , imo_number , vessel_name , 
                        contract_end_date , tentitive_sign_off_date 
                        from open_analytics_zone.ks_scratchpad.crew_onboards 
                        where imo_number = {imo}"""

        sf_con = snowflake_conn()
        cur = sf_con.cursor()
        sf_stmt = cur.execute(stmt).fetchall()
        hdrs = pd.DataFrame(cur.description)
        result = pd.DataFrame(sf_stmt)
        result.columns = hdrs['name']
        result_json = result.to_json(date_format='iso')
        return result_json
