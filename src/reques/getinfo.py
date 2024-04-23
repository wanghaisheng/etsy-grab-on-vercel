from src.reques.product import Product

# https://github.com/v0rkath/EtsyScraperLib

# print(a_product.generate_json())

# ##### Output #####
# {
#     "productName": "Item Title 1",
#     "productDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin velit turpis, vehicula eu interdum eu, dignissim quis risus. Duis ultricies purus a dapibus elementum. Vivamus risus erat, imperdiet vitae urna et, dictum tempus dolor. Aliquam felis eros, feugiat vitae neque in, rhoncus vestibulum libero. Suspendisse quis purus sit amet felis malesuada rhoncus eget vitae nulla. Mauris efficitur nunc in facilisis suscipit. Pellentesque in magna eget velit eleifend ultrices. Maecenas malesuada leo risus, id pellentesque nisl aliquet sit amet.",
#     "productPrice": "$314.99",
#     "productReviews": 0,
#     "media": [
#         "https://i.etsystatic.com/39539439/r/il/455858/5323849019/il_1588xN.5323848888.jpg",
#         "https://i.etsystatic.com/39539439/r/il/26f969/5372017159/il_1588xN.5372018888.jpg",
#         "https://i.etsystatic.com/39539439/r/il/6f0539/5323848409/il_1588xN.5323848888.jpg",
#     ],
# }

from src.utils import *


def getListingsInfo(url, counts):

    a_product = Product("https://www.etsy.com/uk/listing/1479000279/item-title-1")
    a_product.connect()

    a_product.get_all_data()

    # return {"message": f"Hello {keyword}"}
    return a_product.generate_json()


from src.utils import *


def getListingsUrl(url, counts):

    a_product = Product("https://www.etsy.com/uk/listing/1479000279/item-title-1")
    a_product.connect()

    a_product.get_all_data()

    # return {"message": f"Hello {keyword}"}
    return a_product.generate_json()
