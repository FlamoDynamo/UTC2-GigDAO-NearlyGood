from pyteal import *

def approval_program():
    # Define keys for the application
    creator_key = Bytes("creator")

    # On application call
    def on_call():
        return Seq([
            Assert(Txn.application_id() != Int(0)),  # Ensure it's a call to an existing app
            Assert(Txn.sender() == App.globalGet(creator_key)),  # Only creator can call
            Return(Int(1))  # Success
        ])

    # On application creation
    def on_creation():
        return Seq([
            App.globalPut(creator_key, Txn.sender()),  # Store the creator's address
            Return(Int(1))  # Success
        ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation()],  # App creation
        [Txn.application_id() != Int(0), on_call()],  # App call
    )

    return program


def clear_program():
    return Return(Int(1))  # Clear state program, simply returns success


def smart_contract_program():
    # Đây là nơi bạn định nghĩa logic cho smart contract của bạn
    return Seq([
        Return(Int(1))  # Đơn giản chỉ trả về thành công
    ])


if __name__ == "__main__":
    approval = compileTeal(approval_program(), mode=Mode.Application)
    clear = compileTeal(clear_program(), mode=Mode.Application)
    smart_contract = compileTeal(smart_contract_program(), mode=Mode.Application)

    with open("approval.teal", "w") as approval_file:
        approval_file.write(approval)

    with open("clear.teal", "w") as clear_file:
        clear_file.write(clear)
    
    with open("smart_contract.teal", "w") as contract_file:
        contract_file.write(smart_contract)

    print("TEAL files generated: approval.teal, clear.teal, and smart_contract.teal")