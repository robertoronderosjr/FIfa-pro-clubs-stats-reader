import glob
import io

import cv2
import pandas as pd
import pytesseract
from PIL import Image, ImageEnhance
from skimage.exposure import rescale_intensity
from skimage.filters import threshold_yen
from skimage.io import imread, imsave

from getters import *


stats = {
    "player_name": {
        "l": 241,
        "t": 224,
        "r": 765,
        "b": 257,
        "wanted_stats": {
            "Player ID": player_id
        }
    },
    "shooting": {
        "l": 860,
        "t": 475,
        "r": 931,
        "b": 550,
        "wanted_stats": {
            "Goals": goals,
            "Shots": shots,
            "Shots on Target": shots_on_target
        }
    },
    "passing": {
        "l": 851,
        "t": 595,
        "r": 935,
        "b": 765,
        "wanted_stats": {
            "Assists": assists,
            "Passes Completed": passes_completed,
            "Passes Attempted": passes_attempted,
            "Key Passes": key_passes,
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
            "Tackles Won": tackles_won,
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
            "Possession Won": possession_won,
            "Possession Lost": possession_lost,
            "Headers Won": headers_won
        }
    }
}

f = open("team_stats_p2.txt", "w")

for ss_filename in glob.glob('C:\\Users\\rober\\Videos\\Captures\\p2\\*.png'):
    ss = Image.open(ss_filename)

    width, height = ss.size
    assert width == 1920
    assert height == 1080

    for k, v in stats.items():
        stats_img = ss.crop((stats[k]["l"], stats[k]["t"], stats[k]["r"], stats[k]["b"]))
        stats_img_filename = f"ss_{k}.png"
        stats_img.save(stats_img_filename)

        img = imread(stats_img_filename)
        yen_threshold = threshold_yen(img)
        bright = rescale_intensity(img, (0, yen_threshold), (0, 255))
        imsave(stats_img_filename, bright)

        enhanced_img = Image.open(stats_img_filename)
        enhancer_s = ImageEnhance.Sharpness(enhanced_img)
        out_s = enhancer_s.enhance(2)
        enhancer_c = ImageEnhance.Contrast(out_s)
        out_c = enhancer_c.enhance(2)
        # # out_c.show()
        out_c.save(stats_img_filename)

        img_read = cv2.imread(stats_img_filename)
        # blur the image to remove noise
        gray = cv2.medianBlur(img_read, 3)
        cv2.imwrite(stats_img_filename, gray)

        data = "value\n"
        config = '--psm 6 --oem 0 -c tessedit_char_whitelist=0123456789/'
        if k == "player_name":
            config = '--psm 6'

        data += pytesseract.image_to_string(Image.open(stats_img_filename), config=config)
        filtered = "\n".join([ll.rstrip() for ll in data.splitlines() if ll.strip()])
        filtered = filtered.replace(" ", "")
        data_filtered = io.StringIO(filtered)
        df = pd.read_csv(data_filtered, sep=" ")
        # delete auxiliary images
        # os.remove(stats_img_filename)
        for stat, func in stats[k]["wanted_stats"].items():
            print(f'{stat}: {func(df)}')
            f.write(f'{stat}: {func(df)}\n')
    f.write('\n\n')

f.close()
