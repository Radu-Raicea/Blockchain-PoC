
import hashlib


def generate_new_proof(previous_proof):
    """
    Finds the next proof that, when concatenated to and hashed with the previous_proof, returns a hash with 4 leading zeroes.

    :param int previous_proof: Proof of the previous block
    :return int: Proof of the next block
    """

    proof = 0

    while validate_proof(previous_proof, proof) is False:
        proof += 1

    return proof


def validate_proof(previous_proof, proof):
    """
    Validates the new proof.

    :param int previous_proof: Proof of the previous block
    :param int proof: Potential proof of the next block
    :return bool: True if the new proof is valid, False if not
    """

    attempt = f'{previous_proof}{proof}'.encode()
    hashed_attempt = hashlib.sha256(attempt).hexdigest()

    return hashed_attempt[:4] == '0000'
