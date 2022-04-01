from whoopbot.actions.add import AddAction
from whoopbot.actions.delete import DeleteAction
from whoopbot.actions.list import ListAction
from whoopbot.actions.lock import LockAction
from whoopbot.actions.release import ReleaseAction

# Map of action to their action classes
ACTION_MAP = {
    'list': ListAction,
    'add': AddAction,
    'delete': DeleteAction,
    'lock': LockAction,
    'release': ReleaseAction
}