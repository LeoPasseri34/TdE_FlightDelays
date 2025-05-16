from database.DB_connect import DBConnect
from model.airport import Airport
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nMin, idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.IATA_CODE, count(*) as N
                    from (select a.ID , a.IATA_CODE , f.AIRLINE_ID, count(*) 
                    from airports a, flights f 
                    where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
                    group by a.ID , a.IATA_CODE , f.AIRLINE_ID ) t
                    group by t.ID, t.IATA_CODE
                    having N >= %s
                    order by N asc"""

        cursor.execute(query, (nMin,))

        for row in cursor:
            result.append(idMapAirports[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*)  as N 
                    from flights f  
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    """

        cursor.execute(query,)

        for row in cursor:
            result.append(Arco(idMapAirports[row["ORIGIN_AIRPORT_ID"]],
                               idMapAirports[row["DESTINATION_AIRPORT_ID"]],
                               row["N"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce(t1.n, 0)+coalesce(t2.n, 0) as n
                    from(select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    ) t1
                    left join(select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    ) t2
                    on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID
                    and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID
                    """

        cursor.execute(query, )

        for row in cursor:
            result.append(Arco(idMapAirports[row["ORIGIN_AIRPORT_ID"]],
                               idMapAirports[row["DESTINATION_AIRPORT_ID"]],
                               row["n"]))

        cursor.close()
        conn.close()
        return result