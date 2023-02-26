from typing import List, Union


class InlineKeyboard:
    def __init__(self) -> None:
        self.buttons: List[List[dict]] = []
        
    def add_button(self, text: str, url: str = None, callback_data: str = None) -> None:
        button: dict = {
            'text': text,
            'url': url,
            'callback_data': callback_data,
        }
        self.buttons.append([button])
        
    def add_row(self, row_buttons: List[dict]) -> None:
        row: List[dict] = []
        for button in row_buttons:
            row.append({
                'text': button['text'],
                'url': button.get('url'),
                'callback_data': button.get('callback_data'),
            })
        self.buttons.append(row)
        
    def to_dict(self) -> dict:
        return {'inline_keyboard': self.buttons}


""" Examples
keyboard = InlineKeyboard()
keyboard.add_button('Open Google', url='https://www.google.com')
keyboard.add_button('Send callback', callback_data='callback_data')
keyboard.add_row([
    {'text': 'Button 1', 'callback_data': 'button1'},
    {'text': 'Button 2', 'callback_data': 'button2'},
    {'text': 'Button 3', 'callback_data': 'button3'}
])
keyboard_dict = keyboard.to_dict()
"""
