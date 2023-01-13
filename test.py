import pandas as pd
# print(9//2)
# print(9%2)


gameboard_df = pd.read_csv("gameboards/Rushhour12x12_7.csv")

# i = 0
# for vehicle in gameboard_df.iterrows():
#     print(vehicle[0])
    # # make sure car X has always color red
    # if vehicle[1]['car'] == "X":
    #     color_veh = "#FF0000"
    # else:
    #     # retrieve hex value for vehicle color
    #     color_list = list(cnames.items())
    #     color_veh = color_list[i][1]
    #
    #     i += 1
    #     if i >= len(color_list):
    #         i = 0

    # create Vehicle() and add to list
    # self.vehicle_dict[vehicle[1]['car']] = (Vehicles(vehicle[1]['car'], \
    #     vehicle[1]['orientation'], vehicle[1]['col'] - 1, vehicle[1]['row'] - 1, \
    #     vehicle[1]['length'], color_veh))

dict = {"a" : [1, 2, 3], 'b': 2, 'c':3}
print(dict["a"][1])
# for i in dict:
#     print(i)
