import psycopg2
import random
import time
from environment import PG_CONNECT


# productkey = 100
# customerkey = round(random.uniform(100, 10000), 0)
# salesterritorykey = round(random.uniform(100, 1000), 0)
# salesordernumber = "SO" + str(round(random.uniform(100, 10000), 0))
# totalproductcost = "100"
# salesamount = round(random.uniform(200, 1000), 1)
# id = datetime.now()
# created_at = datetime.now().replace(tzinfo=None)

import psycopg2

def insert_sale(amount):
    """ Insert a new vendor into the vendors table """

    sql = """INSERT INTO sales(salesamount,created_at)
             VALUES(%s,current_timestamp) RETURNING id;"""
    
    id = None

    try:
        with  psycopg2.connect(PG_CONNECT) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (amount,))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    vendor_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return id


if __name__ == '__main__':
    while True:
        insert_sale(round(random.uniform(200, 1000), 2))
        time.sleep(1.5)
        