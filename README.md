# Shogi-in-Python

Through python's pygame library, I create my first big game project centred around the Japanese chess board game called Shogi. At the moment the game is just focused on playing between 2 players locally on the same machine.

![shogi_game](https://user-images.githubusercontent.com/90066802/177181791-6f085957-187f-4026-953c-068a45ac52cc.gif)


## Installation Requirements

- Have python version 3.10.X or higher
- Have pygame installed
- Install all fonts within the font folder

To install pygame enter the following in your terminal or command line: 
```bash
  pip3 install pygame
```

If the above command failed try:
```bash
  python3 -m pip install pygame
``` 

## Known Bugs

- Very rare bug in which the game crashes when selecting a piece
- Selected captured pieces in a player's komadai isnt deselected when an active piece is selected instead from the board
- Timer countdown isnt constant and so speed of decrementation slighty can vary
- When the King piece is in check, it can still capture pieces in a square that keeps the King in check


## License

[MIT](https://choosealicense.com/licenses/mit/)

NOT FOR COMMERCIAL USE If you intened to use any of my code for commercial use please contact me and get my permission. If you intend to make money using any of my code please ask my permission.


## Authors

- [@aspherr](https://www.github.com/octokatherine)

