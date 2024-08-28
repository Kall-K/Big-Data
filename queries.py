from pymongo import MongoClient

# 1 ===========================================================================
def min_vehicles(start_time, end_time):
    return [ 
        {"$match": {"t": { "$gte": start_time, "$lte": end_time }}},
        {"$group": {"_id": "$link", "totalVehicles": {"$sum": "$num_VEHICLES"}}},
        {"$group": {"_id": "$totalVehicles", "links": {"$push":"$_id"}}},
        {"$sort": { "_id": 1 }},
        {"$limit": 1}
    ]

# 2 ===========================================================================
def max_avg_speed(start_time, end_time):
    return [ 
        {"$match": {"t": { "$gte": start_time, "$lte": end_time }}},
        {"$group": {"_id": "$link", "avgSpeed": {"$max": "$avg_SPEED"}}},
        {"$group": {"_id": "$avgSpeed", "links":{"$push":"$_id"}}},
        {"$sort": { "_id": -1 }},
        {"$limit": 1}
    ]

# 3 ===========================================================================
def max_route(start_time, end_time):
    return [ 
        {"$match": {"t": { "$gte": start_time, "$lte": end_time }}},
        {"$group": {"_id": "$name", "route": {"$push": "$link"}, "distance": {"$sum": "$x"}}},
        {"$sort": { "count": -1 }}
    ]

def main():
    start_time = input('Give Start Time (YYYY-MM-DD hh:mm:ss): ')
    end_time = input('Give End Time (YYYY-MM-DD hh:mm:ss): ')
    query = input('Select query (1 or 2 or 3): ')

    # start_time="2024-08-18 19:59:06"
    # end_time="2024-08-18 19:59:11"
    # query=3

    client = MongoClient('localhost', 27017)
    db = client['traffic_data']
    collection = db['processed_data']

    result = 0

    # Execute the aggregation
    if int(query) == 1:
        result = collection.aggregate(min_vehicles(start_time, end_time))
    elif int(query) == 2:
        result = collection.aggregate(max_avg_speed(start_time, end_time))
    elif int(query) == 3:
        collection = db['raw_data']
        result = collection.aggregate(max_route(start_time, end_time))

    # Print the result
    for res in result:
        print(res)

if __name__ == "__main__":
    main()