from trello import TrelloClient


def get_trello_board(trello_board_name, api_key, token):
    client = TrelloClient(api_key=api_key, token=token)
    all_boards = client.list_boards()
    target_board = None
    for board in all_boards:
        if board.name == trello_board_name:
            target_board = board
            break
    return target_board
