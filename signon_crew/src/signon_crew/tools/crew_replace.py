from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel , Field
import snowflake.connector
import os
import pandas as pd

class FetchCrewRep (BaseTool):
    name: str = "Crew replacement Fetcher"
    description: str = "Fetches  data, comments, and activity from a Snowflake"
    
    def _run(self, role :str) -> dict:
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
        
        stmt = f""" select first_name , last_name , crew_code , nationality_name ,rank_name_se ,country ,  
                        vessel_category_name ,
                       rank_category , rank_level
                        from open_analytics_zone.ks_scratchpad.crew_full_df
                        where current_status ='Sign Off'
                        and profile_status ='Active Seafarer'
                        and availability_date < current_date +7
                        and sign_off_reason ='End of Contract'
                        and rank_name_se ='{role}';
                        """

        sf_con = snowflake_conn()
        cur = sf_con.cursor()
        sf_stmt = cur.execute(stmt).fetchall()
        hdrs = pd.DataFrame(cur.description)
        result = pd.DataFrame(sf_stmt)
        result.columns = hdrs['name']
        result_dict =result.to_dict
        return result_dict