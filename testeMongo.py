from pymongo import MongoClient
def testMongoBTCPersist():
    # Conectar ao MongoDB
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['quotation']
        collection = db['quotation']

        documents = collection.find()
        data = [document['quotation'] for document in documents]
        if data:
            print(data)
        else:
            print('Sem dados')
    except Exception as e:
        print(f"Erro ao conectar no MongoDB: {e}")


testMongoBTCPersist()