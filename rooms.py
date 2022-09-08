from email.policy import default
import random


room_attributes = {"width": 0, "height": 0, "is_spawn": False,
                   "is_end": False, "palette": "blue"}


def to_map(plan, **attr):
    m = {}
    for k, v in room_attributes.items():
        m[k] = v
    m["width"] = min(list(map(lambda r: len(r), plan)))
    m["height"] = len(plan)
    height = m["height"]
    for a, v in attr.items():
        m[a] = v
    for y in range(m["height"]):
        for x in range(m["width"]):
            t = plan[y][x]
            if t == "-":
                continue
            else:
                g = m.get(t, [])
                g.append((x, height - 1 - y))
                m[t] = g
    return m


spawn_room = to_map(
    ["--1--",
     "-----",
     "-----",
     "-----",
     "-----"],
    is_spawn=True,
    palette="blue")
general_room_ = to_map(
    ["-----",
     "-----",
     "-----",
     "-----",
     "-----"],
    palette="blue")

general_room_1 = to_map(
    ["--1--",
     "--n--",
     "3n0-7",
     "---n-",
     "--5--"],
    palette="blue")
general_room_2 = to_map(
    ["--1--",
     "-nW--",
     "3WWW7",
     "--W--",
     "--5n-"],
    palette="stone")
general_room_3 = to_map(
    ["-W1--",
     "--W-W",
     "3-0n7",
     "WnW--",
     "--5W-"],
    palette="stone")
general_room_4 = to_map(
    ["11111",
     "-n---",
     "WWSWW",
     "---n-",
     "55555"],
    palette="stone")
general_room_5 = to_map(
    ["2-1-8",
     "n-S--",
     "3SSS7",
     "--S-n",
     "4-5-6"],
    palette="slime")
general_room_6 = to_map(
    ["-11--",
     "--W-7",
     "3-S-7",
     "3-W--",
     "--56-"],
    palette="blue")
general_room_7 = to_map(
    ["-n---",
     "-W0W7",
     "3W0W7",
     "3W0W-",
     "---n-"],
    palette="stone")
general_room_8 = to_map(
    ["--1--",
     "--n--",
     "3mWm7",
     "--n--",
     "--5--"],
    palette="blue")
general_room_9 = to_map(
    ["--1--",
     "-WsW-",
     "3-s-7",
     "-WsW-",
     "--5--"],
    palette="blue")
general_room_10 = to_map(
    ["111",
     "---",
     "-W-",
     "sss",
     "-W-",
     "---",
     "555"],
    palette="blue")

treasury_room_1 = to_map(
    ["mmmmm",
     "m---m",
     "m-0-m",
     "m---m",
     "mmmmm"],
    palette="gold")


end_room_0 = to_map(
    ["-----",
     "-----",
     "--0--",
     "-----",
     "-----"],
    is_end=True,
    palette="stone")
end_room_1 = to_map(
    ["--1--",
     "-----",
     "-----",
     "-----",
     "-----"],
    is_end=True,
    palette="stone")
end_room_2 = to_map(
    ["2----",
     "-----",
     "-----",
     "-----",
     "-----"],
    is_end=True,
    palette="stone")
end_room_3 = to_map(
    ["-----",
     "-----",
     "3----",
     "-----",
     "-----"],
    is_end=True,
    palette="stone")
end_room_4 = to_map(
    ["-----",
     "-----",
     "-----",
     "-----",
     "4----"],
    is_end=True,
    palette="stone")
end_room_5 = to_map(
    ["-----",
     "-----",
     "-----",
     "-----",
     "--5--"],
    is_end=True,
    palette="stone")
end_room_6 = to_map(
    ["-----",
     "-----",
     "-----",
     "-----",
     "----6"],
    is_end=True,
    palette="stone")
end_room_7 = to_map(
    ["-----",
     "-----",
     "----7",
     "-----",
     "-----"],
    is_end=True,
    palette="stone")
end_room_8 = to_map(
    ["----8",
     "-----",
     "-----",
     "-----",
     "-----"],
    is_end=True,
    palette="stone")
end_room_9 = to_map(
    ["-----",
     "-----",
     "--9--",
     "-----",
     "-----"],
    is_end=True,
    palette="stone")

END_ROOMS = [end_room_0, end_room_1, end_room_2,
             end_room_3, end_room_4, end_room_5,
             end_room_6, end_room_7, end_room_8,
             end_room_9]
TREASURY_ROOMS = [treasury_room_1]
GENERAL_ROOMS = [general_room_1, general_room_2, general_room_3,
                 general_room_4, general_room_5, general_room_7,
                 general_room_8, general_room_9, general_room_10] + TREASURY_ROOMS


def find_room_with_door(l, door_number):
    while True:
        p = l[random.randint(0, len(l) - 1)]
        if str(door_number) in p.keys():
            return p
