"""
Converts a LSDj font to bitfontmaker2 JSON format
"""

# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-locals
# pylint: disable=wrong-import-order
# pylint: disable=import-error
# pylint: disable=line-too-long

import numpy as np
from PIL import Image

import json
from char_codes import CHAR_CODES
from fonts import FONTS


def generate_case_map():
    """ We create a map for all characters that have upper/lower case pairs """

    case_map = {}

    # For all possible characters
    for code in range(0x10000):  # Unicode up to 65535
        try:
            char = chr(code)
            upper = char.upper()
            lower = char.lower()

            # Check that the result is one character
            if len(upper) == 1 and char != upper:
                case_map[code] = ord(upper)
            elif len(lower) == 1 and char != lower:
                case_map[code] = ord(lower)
        except ValueError:
            continue  # skipping invalid characters

    return case_map


def auto_duplicate_case(font_data):
    """ Generate a copy of the font data with additional characters for paired upper/lower case letters. """

    new_data = font_data.copy()
    case_map = generate_case_map()

    for code in font_data:
        paired_code = case_map.get(code)

        if paired_code and paired_code not in font_data:
            new_data[paired_code] = font_data[code]

    return new_data


def pixel_to_bitmask(row):
    """ Converts a 16-bit string to a number. """
    return sum(1 << (15 - i) for i in range(16) if row[i])


def upscale_and_offset_glyph(glyph_8x8, offset_row=0, offset_col=0, scale=1):
    """
    Scales an 8x8 glyph to 16x16, enlarging each pixel by scale x scale,
    and shifts it so that the lower-left corner of the glyph ends up at (offset_row, offset_col).
    """

    # Creating an empty 16x16 matrix
    result = np.zeros((16, 16), dtype=int)

    # Scalable: each pixel -> scale x scale block
    for i in range(8):
        for j in range(8):
            if glyph_8x8[i, j]:  # if the pixel is black
                row_0 = offset_row + 15 - (7 - i) * scale
                col_0 = offset_col + j * scale

                for scale_i in range(scale):
                    for scale_j in range(scale):
                        x_pos = row_0 - scale_i
                        y_pos = 15 - (col_0 + scale_j)

                        if 0 <= x_pos < 16 and 0 <= y_pos < 16:
                            result[x_pos, y_pos] = 1

    return result


def image_to_pixel_font_8x8(
    *,
    image_path,
    output_json_path,
    offset_row=0,
    offset_col=0,
    scale=1,
    letter_space=64,
    name="font",
    copy="Copyright (c) 2025",
):
    """ Converts an image (NxM, multiple of 8) to 16x16 JSON format with scaling and offsetting. """

    img = Image.open(image_path).convert("L")  # grayscale
    img_array = np.array(img)
    height, width = img_array.shape

    if width % 8 != 0 or height % 8 != 0:
        raise ValueError(f"Image dimensions must be multiples of 8, received {width}x{height}")

    # Calculating the number of glyphs
    glyphs_per_row = width // 8
    glyphs_per_col = height // 8
    total_glyphs = glyphs_per_row * glyphs_per_col

    char_codes = CHAR_CODES
    font_data = {}

    # Processing each glyph
    for row_idx in range(glyphs_per_col):
        for col_idx in range(glyphs_per_row):
            idx = row_idx * glyphs_per_row + col_idx

            if idx >= len(char_codes) or idx >= total_glyphs:
                break

            code = char_codes[idx]

            # Cut out 8x8 glyph
            y_start = row_idx * 8
            x_start = col_idx * 8
            glyph_8x8 = img_array[y_start:y_start + 8, x_start:x_start + 8]

            # Binarization: black = 1, white = 0
            glyph_binary = (glyph_8x8 < 128).astype(int)

            # Scale and shift
            glyph_16x16 = upscale_and_offset_glyph(glyph_binary, offset_row, offset_col, scale)

            # Convert to an array of 16 numbers (bit masks)
            row_values = [pixel_to_bitmask(row) for row in glyph_16x16]

            font_data[code] = row_values

    font_data = auto_duplicate_case(font_data)

    font_data["name"] = name
    font_data["copy"] = copy
    font_data["letterspace"] = letter_space
    font_data["basefont_size"] = "512"
    font_data["basefont_left"] = "62"
    font_data["basefont_top"] = "0"
    font_data["basefont"] = "Arial"
    font_data["basefont2"] = ""
    font_data["monospacewidth"] = "8"
    font_data["monospace"] = False

    with open(output_json_path, 'w', encoding='utf-8') as f_handle:
        # noinspection PyTypeChecker
        json.dump(font_data, f_handle, ensure_ascii=False, indent=2)

    print(f"The font has been saved to {output_json_path}")

    return font_data


if __name__ == '__main__':
    for font in FONTS:
        params = font.copy()
        image = f"png/{params.pop('file')}"
        output = f"json/{params.pop('output')}"

        image_to_pixel_font_8x8(image_path=image, output_json_path=output, **params)
