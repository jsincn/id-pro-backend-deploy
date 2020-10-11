from nanoid import generate
from database import verify_id_not_present
alphabet = "123456789"

def generate_id():
    id = generate(alphabet, 4)
    while not verify_id_not_present(int(id)):
        id = generate(alphabet, 4)
    return int(id)