from miner.model import Miner

def test_miner_generate():

    miner = Miner()
    g = miner._inference("""
    please provide a json representation of the a tweet from @account with the content "new tweet who dis?"
be sure to use the fields "author" and "content" explicitly. please respond in JSON only. no yapping
    """)
    print(g)
    assert g is not None



test_miner_generate()