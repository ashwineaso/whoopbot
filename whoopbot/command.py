from whoopbot.actions import ACTION_MAP


async def handle_command(command_body) -> str:
    """Parse the command and return the appropriate response."""
    return parse_command(command_body['text'])


def parse_command(command_text: str) -> str:
    """Parse the command text and build a command object."""

    params = command_text.split(" ")

    # part 0 defines the action,
    # if action is not present in the action map
    action_text = params[0]
    if action_text not in ACTION_MAP:
        return f"Invalid action: {action_text} :fire:"

    action = ACTION_MAP[action_text](params[1:])
    return action.process()
