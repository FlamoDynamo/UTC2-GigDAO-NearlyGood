# config.py

# Algorand network configuration
ALGOD_ADDRESS = "https://testnet-api.4160.nodely.dev/"
ALGOD_TOKEN = ""  # Thường là chuỗi rỗng cho public nodes
INDEXER_ADDRESS = "https://testnet-idx.4160.nodely.dev"
INDEXER_TOKEN = ""  # Thường là chuỗi rỗng cho public nodes

# Smart contract IDs
GIG_DAO_CONTRACT_ID = None  # Cập nhật sau khi triển khai
NFT_MINTING_CONTRACT_ID = None  # Cập nhật sau khi triển khai

# Các cấu hình khác của dự án (nếu có)
AES_KEY = "GByT3lmFRnLg68bm6oq5is6v4j42kxyniHJRg+sqw40="
QUORUM_THRESHOLD = 0.5  # Tỷ lệ quorum cho các đề xuất

# Asset ID của NFT mà bạn đã opt-in
NFT_ASSET_ID = 45629201

# Thêm dòng này vào cuối file config.py
contracts = {}  # hoặc bất kỳ giá trị mặc định nào phù hợp với dự án của bạn