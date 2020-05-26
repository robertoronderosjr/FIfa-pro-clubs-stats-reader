import glob
import io
import json

import pandas as pd
import pytesseract
from PIL import Image, ImageEnhance
from skimage.exposure import rescale_intensity
from skimage.filters import threshold_yen
from skimage.io import imread, imsave

from getters import *

calculated_stats = []

gamertags = {
    "HAGULIDS": "Hafidguti",
    "Mexyl33t": "mexyl33t",
    "S1lentmx": "S1lentmx",
    "Golda": "mexicanus86",
    "ManuelOS123": "ManuelOS123",
    "Robert": "blackdethbob",
    "Casillas": "jbro435",
    "Chelo": "ElSenorX1276",
    "LC": "LuisCastro92",
    "Andres": "richiandres94",
    "harloco": "harloco"
}

gk_stats = {
    "passing": {
        "l": 1609,
        "t": 436,
        "r": 1673,
        "b": 608,
        "wanted_stats": {
            "Assists": assists,
            "Key Passes": key_passes,
            "Passes Completed": passes_completed,
            "Passes Attempted": passes_attempted,
            "Crosses Completed": crosses_completed,
            "Crosses Attempted": crosses_attempted
        }
    },
    "player_position": {
        "l": 266,
        "t": 357,
        "r": 315,
        "b": 390,
        "wanted_stats": {
            "Position": player_position
        }
    },
    "positioning": {
        "l": 1632,
        "t": 654,
        "r": 1676,
        "b": 716,
        "wanted_stats": {
            "Interceptions": interceptions,
            "Blocks": blocks,
        }
    },
    "ball_retention": {
        "l": 1629,
        "t": 760,
        "r": 1674,
        "b": 864,
        "wanted_stats": {
            "Headers Won": headers_won,
            "Possession Won": possession_won,
            "Possessions Lost": possession_lost,
        }
    },
    "goal_keeper": {
        "l": 878,
        "t": 450,
        "r": 930,
        "b": 587,
        "wanted_stats": {
            "Goals Against": goals_against,
            "GK Saves": gk_saves
        }
    }
}

player_stats = {
    "player_name": {
        "l": 241,
        "t": 224,
        "r": 600,
        "b": 257,
        "wanted_stats": {
            "Player ID": player_id
        }
    },
    "player_position": {
        "l": 266,
        "t": 357,
        "r": 325,
        "b": 390,
        "wanted_stats": {
            "Position": player_position
        }
    },
    "shooting": {
        "l": 860,
        "t": 485,
        "r": 931,
        "b": 550,
        "wanted_stats": {
            "Goals": goals,
            "Shots Attempted": shots,
            "Shots On Target": shots_on_target
        }
    },
    "passing": {
        "l": 860,
        "t": 595,
        "r": 923,
        "b": 765,
        "wanted_stats": {
            "Assists": assists,
            "Key Passes": key_passes,
            "Passes Completed": passes_completed,
            "Passes Attempted": passes_attempted,
            "Crosses Completed": crosses_completed,
            "Crosses Attempted": crosses_attempted
        }
    },
    "tackles": {
        "l": 1620,
        "t": 486,
        "r": 1678,
        "b": 513,
        "wanted_stats": {
            "DEF Tackles": tackles_won,
        }
    },
    "positioning": {
        "l": 1620,
        "t": 631,
        "r": 1678,
        "b": 657,
        "wanted_stats": {
            "Interceptions": interceptions,
            "Blocks": blocks,
        }
    },
    "ball_retention": {
        "l": 1622,
        "t": 736,
        "r": 1690,
        "b": 846,
        "wanted_stats": {
            "Headers Won": headers_won,
            "Possession Won": possession_won,
            "Possessions Lost": possession_lost,
        }
    }
}

match = 'bayervsporto'

f = open(f"team_stats_{match}.txt", "w")
j = open(f"team_stats.json", "w")


def process_image(ss, stats_img_filename, stats, k):
    # enhancer_s = ImageEnhance.Brightness(ss)
    # ss = enhancer_s.enhance(0.4)

    stats_img = ss.crop((stats[k]["l"], stats[k]["t"], stats[k]["r"], stats[k]["b"]))

    stats_img.save(stats_img_filename)

    img = imread(stats_img_filename)
    yen_threshold = threshold_yen(img)
    bright = rescale_intensity(img, (0, yen_threshold), (0, 255))
    imsave(stats_img_filename, bright)

    enhanced_img = Image.open(stats_img_filename)
    enhancer_s = ImageEnhance.Sharpness(enhanced_img)
    out_s = enhancer_s.enhance(5)
    # out_s.save(stats_img_filename)
    enhancer_c = ImageEnhance.Contrast(out_s)
    out_c = enhancer_c.enhance(1)
    out_c.save(stats_img_filename)
    # out_c.show()

    # img_read = cv2.imread(stats_img_filename)
    # # blur the image to remove noise
    # gray = cv2.medianBlur(img_read, 1)
    # cv2.imwrite(stats_img_filename, gray)


def read_image(stats_img_filename, k):
    data = "value\n"
    config = '--psm 6 --oem 0 -c tessedit_char_whitelist="0123456789/"'
    if k == "player_name":
        config = '--psm 6 --oem 0 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"'
    if k == "player_position":
        config = '--psm 6 --oem 0 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ"'

    data += pytesseract.image_to_string(Image.open(stats_img_filename), config=config)
    filtered = "\n".join([ll.rstrip() for ll in data.splitlines() if ll.strip()])
    filtered = filtered.replace(" ", "")
    data_filtered = io.StringIO(filtered)
    df = pd.read_csv(data_filtered, sep=" ")
    # delete auxiliary images
    # os.remove(stats_img_filename)
    return df


def out(stat, val):
    print(f'{stat}: {val}')
    f.write(f'{stat}: {val}\n')


def process_player(stats):
    stat_obj = {}
    gt = ""
    position = ""
    for k, v in stats.items():
        stats_img_filename = f"ss_{k}.png"

        process_image(ss, stats_img_filename, stats, k)
        df = read_image(stats_img_filename, k)

        for stat, func in stats[k]["wanted_stats"].items():
            if stat == "Position":
                position = func(df)
            if position == "PO":
                break
            val = func(df)
            if isinstance(val, str) or val > 0:
                if stat == "Player ID":
                    val = gamertags[func(df)]
                out(stat, val)
                stat_obj[stat] = val
        if position == "PO":
            break
    if position == "PO":
        stat_obj.update(process_gk(gk_stats))
    return stat_obj


def process_gk(stats):
    stat_obj = {}
    for k, v in stats.items():
        stats_img_filename = f"ss_{k}.png"

        process_image(ss, stats_img_filename, stats, k)
        df = read_image(stats_img_filename, k)

        for stat, func in stats[k]["wanted_stats"].items():
            val = func(df)
            if isinstance(val, str) or val > 0:
                out(stat, val)
                stat_obj[stat] = val
    return stat_obj


for ss_filename in glob.glob(f'C:\\Users\\rober\\Videos\\Captures\\{match}\\*.png'):
    ss = Image.open(ss_filename)

    width, height = ss.size
    assert width == 1920
    assert height == 1080

    calculated_stats.append(process_player(player_stats))

    f.write('\n\n')

json.dump(calculated_stats, j)

j.close()
f.close()
