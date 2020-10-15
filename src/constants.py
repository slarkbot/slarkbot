
from enum import Enum

class API_URI_ENDPOINTS(Enum):
    HEALTH_CHECK = 'health'
    MATCHES = 'matches/%s'


well_known_data = {
    'test_match_id': 5657023440,
    'test_user_id': 112955630
}
