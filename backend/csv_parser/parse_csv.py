#!/usr/bin/python

import csv
import json
import pprint
import re
import sys


def replace_if_not_empty(dict, key, value):
    if key not in dict or not dict[key]:
        dict[key] = value


def to_float_or_none(value):
    # lmao lazy
    try:
        return float(value)
    except ValueError:
        return None


def replace_slashes(str):
    return str.replace("/", "\\") if str else None


def strip_or_none(str):
    try:
        return str.strip() if str.strip() else None
    except:
        return None


def write_json(dic, file_name):
    print(f"saving {file_name}")
    with open(file=file_name, mode="w") as f:
        json.dump(dic, f, indent=2)
        f.write("\n")


def main(tsv_name: str):
    print(f"reading {tsv_name}")

    with open(file=tsv_name) as tsv_file:
        # skip first 2 lines
        tsv_file.readline()
        tsv_file.readline()

        # convert file to array of dicts
        # not efficient but good for reuse
        rows = list(csv.DictReader(tsv_file, delimiter="\t"))

        extract_keyboards(rows)
        extract_mousepads(rows)
        extract_mice(rows)
        extract_users(rows)


def extract_keyboards(rows):
    kbs = {}
    for row in rows:
        kb_model = replace_slashes(strip_or_none(row["Keyboard Model"]))
        if not kb_model:
            continue

        if kb_model not in kbs or not kbs[kb_model]:
            kb = {}
        else:
            kb = kbs[kb_model]

        # set keyboard switch
        replace_if_not_empty(kb, "switch", strip_or_none(row["Key Switch"]))
        kbs[kb_model] = kb

    # pprint.PrettyPrinter().pprint(kbs)
    write_json(kbs, "keyboards.json")


def extract_mousepads(rows):
    mps = {}
    for row in rows:
        mp = replace_slashes(strip_or_none(row["Mousepad"]))
        if not mp:
            continue
        if mp not in mps or not mps[mp]:
            mps[mp] = {}

    # pprint.PrettyPrinter().pprint(mps)
    write_json(mps, "mousepads.json")


def extract_mice(rows):
    mice = {}

    # iterate through rows
    for row in rows:
        mm = replace_slashes(strip_or_none(row["Mouse Model"]))
        # skip row
        if not mm:
            continue

        # get mouse model
        if mm not in mice or not mice[mm]:
            mouse = {}
        else:
            mouse = mice[mm]

        # update mouse model
        # using split because sometimes there is a range of values
        # im lazy so i just take first value
        replace_if_not_empty(
            mouse, "sensor", row["Sensor"] if row["Sensor"] else None)
        replace_if_not_empty(mouse, "weight", to_float_or_none(
            row["Weight"].split("g")[0]))
        replace_if_not_empty(mouse, "length", to_float_or_none(
            row["Length"].split("m")[0]))
        replace_if_not_empty(mouse, "width", to_float_or_none(
            row["Width"].split("m")[0]))
        replace_if_not_empty(mouse, "height", to_float_or_none(
            row["Height"].split("m")[0]))
        replace_if_not_empty(
            mouse, "switch", row["Mouse Switch"] if row["Mouse Switch"] else None)

        # set mouse model
        mice[mm] = mouse

    # pprint.PrettyPrinter().pprint(mice)
    write_json(mice, "mice.json")


def extract_users(rows):
    status = "Mouse"
    users = {}

    # iterate through rows
    for row in rows:
        if row["Rank"].startswith("Notable"):
            status = "Notable"
        elif row["Rank"].startswith("Traitors"):
            status = "Traitors"
        elif row["Rank"].startswith("Banned"):
            break

        # skip notable mentions
        if status == "Notable":
            continue

        # skip row if username is not well-formatted
        pattern = "=HYPERLINK\\(\"https:\\/\\/osu\\.ppy\\.sh\\/u\\/(\\d+)\",\"(\\w+)\"\\)"
        result = re.search(pattern, row["Name"])
        if not result or not result.group(1) or not result.group(2):
            continue

        # extract user info
        userID = result.group(1)
        userName = result.group(2)
        is_traitor = status == "Trators"

        # win settings, very safe way
        win_settings = row['=HYPERLINK("http://puu.sh/nJtmY/e2a5589f67.png","OS")'].split()
        if win_settings:
            win_sensitivity = to_float_or_none(win_settings[0].split("/")[0])
            if len(win_settings) >= 2:
                accl_setting = win_settings[1].strip().lower()
                if accl_setting.startswith("off"):
                    win_acceleration = False
                elif accl_setting.startswith("on"):
                    win_acceleration = True
            else:
                win_acceleration = None

        # osu settings, again it is focused on safe
        osu_multiplyer = to_float_or_none(
            row["Multiplier"].strip().split("~")[0].rstrip("xX"))
        if row["Raw"].strip().lower().startswith("on"):
            osu_raw = True
        elif row["Raw"].strip().lower().startswith("off"):
            osu_raw = False
        else:
            osu_raw = None

        # hardware setup info
        screen_resolution = row["Resolution"].strip().split("~")[0].split("x")
        if len(screen_resolution) >= 2:
            screen_width = to_float_or_none(screen_resolution[0])
            screen_height = to_float_or_none(screen_resolution[1])
        else:
            screen_width = None
            screen_height = None

        mousepad = strip_or_none(row["Mousepad"])
        keyboard = strip_or_none(row["Keyboard Model"])

        # mouse playstyle info
        playstyle = strip_or_none(row["Playstyle"])
        mouse = strip_or_none(row["Mouse Model"])
        dpi = to_float_or_none(row["DPI"].strip().rstrip("dpi"))
        polling = to_float_or_none(row["Polling"].lower().rstrip("hz"))

        # possibly calculate mouse area
        if win_sensitivity and osu_multiplyer and dpi and screen_width and screen_height:
            m = [0.00625, 0.0125, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
            win_multi = m[int(win_sensitivity - 1)]

            # get play area
            if (screen_width / screen_height) >= (4 / 3):
                play_height = screen_height
                play_width = screen_height * (4 / 3)
            else:
                play_width = screen_width
                play_height = screen_width / (4 / 3)

            # get area
            effective_ppi = dpi * win_multi * osu_multiplyer
            area_width = round(25.4 * play_width / effective_ppi)
            area_height = round(25.4 * play_height / effective_ppi)
        else:
            area_width = None
            area_height = None

        # create new user
        users[userID] = {
            "name": userName,  # dont really need username tho
            "rank": None,
            "pp": None,
            "is_banned": False,
            "is_traitor": is_traitor,
            "windows_sensitivity": win_sensitivity,
            "windows_acceleration": win_acceleration,
            "osu_multiplyer": osu_multiplyer,
            "osu_raw": osu_raw,
            "screen_width": screen_width,
            "screen_height": screen_height,
            "playstyle": playstyle,
            "dpi": dpi,
            "polling": polling,
            "area_width": area_width,
            "area_height": area_height,
            "mouse": mouse,
            "mousepad": mousepad,
            "keyboard": keyboard,
        }

    # pprint.PrettyPrinter().pprint(users)
    write_json(users, "users.json")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: python ./parse_tsv 'tsv/file/path'")
