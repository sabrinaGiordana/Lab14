from database.DB_connect import DBConnect
from model.ordine import Ordine

class DAO():
    @staticmethod
    def getArchi(store, diff, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        result = []
        query = """ select distinct o1.order_id, o2.order_id, count(oi2.quantity + oi1.quantity) as Q 
                        from orders o1, orders o2, order_items oi1, order_items oi2 
                        where o1.store_id = %s and o2.store_id = %s
                        and datediff(o1.order_date, o2.order_date) < %s
                        and oi1.order_id = o1.order_id
                        and oi2.order_id =o2.order_id 
                        and o1.order_date > o2.order_date
                        group by o1.order_id, o2.order_id """

        cursor.execute(query, (store, store, diff))
        for row in cursor:
            n1 = idMap[row[0]]
            n2 = idMap[row[1]]
            result.append((n1, n2, row[2]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getVertici(store_id):

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select o.*
                    from orders o 
                    where o.store_id = %s"""

        cursor.execute(query, (store_id,))

        for row in cursor:
            result.append(Ordine(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        result = []

        query = """ select s.store_id 
                    from stores s """
        cursor.execute(query)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result



