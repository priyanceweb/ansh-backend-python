from paddleocr import PaddleOCR,draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
# ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
# img_path = './test3.jpg'

# # Perform OCR on the cropped bottom left portion
# result = ocr.ocr(img_path, cls=True)

# # for idx in range(len(result)):
# #     res = result[idx]
# #     for line in res:
# #         print(line)

# parsed_data = result[0]

# # Extract the text values
# text_values = [item[1][0] for item in parsed_data if isinstance(item[1], tuple) and isinstance(item[1][0], str)]

# # Print the result
# # print(text_values)

def search_tracking_and_invoice(data_list):
    result = {
        'tracking_number': None,
        'invoice_id': None
    }

    for item in data_list:
        # Convert item to string in case it's not already
        item_str = str(item).strip()

        # Search for tracking number (starts with 91)
        if item_str.startswith('91') and item_str.isdigit():
            result['tracking_number'] = item_str

        # Search for invoice ID (starts with 00)
        if item_str.startswith('00') and item_str.isdigit():
            result['invoice_id'] = item_str

    return result


# result = search_tracking_and_invoice(text_values)
#     print("Found Tracking Number:", result['tracking_number'])
#     print("Found Invoice ID:", result['invoice_id'])