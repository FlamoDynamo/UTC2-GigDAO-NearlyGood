import pytest
from smart_contracts.contract.contract import GigDAOContract
from algosdk.v2client import algod

class MockAlgodClient:
    def status(self):
        return {"lastRound": 1000, "status": "Online"}

    def account_info(self, address):
        return {"amount": 2000000}  # 2 Algo cho kiểm tra

@pytest.fixture
def gig_dao():
    # Tạo một phiên bản mới của GigDAOContract cho mỗi bài kiểm tra
    mock_algod = MockAlgodClient()
    aes_key = "GByT3lmFRnLg68bm6oq5is6v4j42kxyniHJRg+sqw40="
    return GigDAOContract(mock_algod, aes_key)

@pytest.fixture
def algod_client():
    algod_address = "https://testnet-api.4160.nodely.dev"
    algod_token = ""
    return algod.AlgodClient(algod_token, algod_address)

def test_initialize_dao(gig_dao):
    gig_dao.create_dao("Test DAO", "This is a test DAO.")
    assert gig_dao.is_dao_initialized() is True

def test_add_member(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    assert "user_1" in gig_dao.dao_members

def test_get_account_address(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    account_address = gig_dao.get_account_address("user_1")
    assert account_address == "user_1_address"

def test_get_private_key(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    private_key = gig_dao.get_private_key("user_1")
    assert private_key == "user_1_private_key"

def test_join_dao(gig_dao):
    gig_dao.join_dao("user_1")
    assert "user_1" in gig_dao.dao_members

def test_create_proposal(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.create_proposal("user_1", "Proposal details")
    assert len(gig_dao.proposals) == 1

def test_vote(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.create_proposal("user_1", "Proposal details")
    gig_dao.vote(1, "user_1", "yes")
    assert gig_dao.proposals[1]['votes']['yes'] == 1

def test_finalize_proposal(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.create_proposal("user_1", "Proposal details")
    gig_dao.vote(1, "user_1", "yes")
    gig_dao.finalize_proposal(1)
    assert gig_dao.proposals[1]['status'] == 'passed'

def test_deposit_funds(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.deposit_funds("user_1", 100)
    assert gig_dao.get_fund_balance() == 100

def test_distribute_funds(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.deposit_funds("user_1", 100)
    gig_dao.create_proposal("user_1", "Proposal details")
    gig_dao.vote(1, "user_1", "yes")
    gig_dao.finalize_proposal(1)
    gig_dao.distribute_funds(1, "recipient_address")