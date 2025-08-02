import yaml

LOC_FILE = 'sunapse-bot/data/locations.yaml'
DROP_FILE = 'sunapse-bot/data/drops.yaml'

def test_all_locations_have_mine_entries():
    locations = yaml.safe_load(open(LOC_FILE))['locations']
    mine = yaml.safe_load(open(DROP_FILE))['mine']
    ids = [loc['id'] for loc in locations]
    for loc_id in ids:
        assert loc_id in mine, f"{loc_id} missing from mine drop table"
        assert mine[loc_id], f"{loc_id} has no drops"
