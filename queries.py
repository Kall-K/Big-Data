from pymongo import MongoClient
from bson.json_util import dumps
from bson.json_util import loads

# 1 ===========================================================================
def min_vehicles(start_time, end_time):
    return [ 
        {"$match": {"time": { "$gte": start_time, "$lte": end_time }}},
        {"$group": {"_id": "$link", "totalVehicles": {"$sum": "$num_VEHICLES"}}},
        {"$group": {"_id": "$totalVehicles", "links": {"$push":"$_id"}}},
        {"$sort": { "_id": 1 }},
        {"$limit": 1}
    ]

# 2 ===========================================================================
def max_avg_speed(start_time, end_time):
    return [ 
        {"$match": {"time": { "$gte": start_time, "$lte": end_time }}},
        {"$group": {"_id": "$link", "avgSpeed": {"$max": "$avg_SPEED"}}},
        {"$group": {"_id": "$avgSpeed", "links":{"$push":"$_id"}}},
        {"$sort": { "_id": -1 }},
        {"$limit": 1}
    ]

# 3 ===========================================================================
def max_route(start_time, end_time):
    return [ 
        {"$match": {"time": { "$gte": start_time, "$lte": end_time }}},
        {"$group": {"_id": "$name", "route": {"$push": "$link"}, "distance": {"$sum": "$speed"}}},
        {"$group": {"_id": "$distance", "names":{"$push":"$_id"}, "routes": {"$push": "$route"}}},
        {"$sort": { "_id": -1 }},
        {"$limit": 1}
    ]

def main():
    start_time = input('Give Start Time (YYYY-MM-DD hh:mm:ss): ')
    end_time = input('Give End Time (YYYY-MM-DD hh:mm:ss): ')
    query = input('Select query (1 or 2 or 3): ')
    
    # Set values manually
    # start_time="2024-09-19 15:35:03"
    # end_time="2024-09-08 13:57:04"
    # query=3

    client = MongoClient('localhost', 27017)
    db = client['traffic']
    collection = db['processed_data']

    result = 0
    try:
        # Execute the aggregation
        if int(query) == 1:
            result = collection.aggregate(min_vehicles(start_time, end_time))
            result = loads(dumps(result))
            r = result[0]
            links = ", ".join(r['links'])
            print(f"Minimum Number of Vehicles = {r['_id']}\nLinks = {links}")
        elif int(query) == 2:
            result = collection.aggregate(max_avg_speed(start_time, end_time))
            result = loads(dumps(result))
            r = result[0]
            links = ", ".join(r['links'])
            print(f"Maximum Avg Speed = {r['_id']}\nLinks = {links}")
        elif int(query) == 3:
            collection = db['raw_data']
            result = collection.aggregate(max_route(start_time, end_time))
            result = loads(dumps(result))
            r = result[0]
            cars = [c for c in r['names']]
            routes = [list(dict.fromkeys(x)) for x in r['routes']]
            print(f"Maximum Distance = {r['_id']}")
            for i in range(len(routes)):
                links = ", ".join(routes[i])
                print(f"carID: {cars[i]}   Max Route: {links}")
    except:
        print('No Result Found')

if __name__ == "__main__":
    main()