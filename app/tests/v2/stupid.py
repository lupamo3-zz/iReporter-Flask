def put(self, id):
        ''' Method that updates a specific order '''
        
        # order = Order().get_by_id(id)
        order = Order().get_by_id(id)
        data = request.get_json(force=True)

        user = get_jwt_identity()

        if not (user[1]):
            return {'message':'You cannot access this route'}, 401

        elif data['status'] not in ["New", "Complete", "Processing", "Cancelled"]:
            return ({'message': 'Status can either be: New, Complete, Processing, Cancelled'}, 400)
        
        if order:
            Order().update_status(data['status'], id)
            order.status = data['status']
            return {"message":order.serialize()},201
        
        return {"Message":"Order not found"},404
''
        self.cursor.execute(''' SELECT * FROM orders WHERE id=%s''',
                            (order_id, ))

        order = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if order:
            return self.objectify(order)
        return None

        def update_status(self, status, order_id):
        self.cursor.execute('''UPDATE orders 
        SET status = %s WHERE id=%s''', (status, order_id))

        self.connection.commit()
        self.cursor.close()



