import discord
from discord.ext import commands
from typing import List



class TicTacToeButton(discord.ui.Button['TicTacToe']):
        def __init__(self, x: int, y: int):
            super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
            self.x = x
            self.y = y

        #Callback (Nhấn trả về một giá trị)

        async def callback(self, interaction: discord.Interaction):
            assert self.view is not None
            view: TicTacToe = self.view
            state = view.board[self.y][self.x]
            if state in (view.X, view.O):
                return

            if view.current_player == view.X:
                self.style = discord.ButtonStyle.danger
                self.label = 'X'
                self.disabled = True
                view.board[self.y][self.x] = view.X
                view.current_player = view.O
                content = "Lượt của O!"
            else:
                self.style = discord.ButtonStyle.success
                self.label = 'O'
                self.disabled = True
                view.board[self.y][self.x] = view.O
                view.current_player = view.X
                content = 'Lượt của X'

            winner = view.check_board_winner()
            if winner is not None:
                if winner == view.X:
                    content = 'X thắng!'
                elif winner == view.O:
                    content = 'O thắng!'
                else:
                    content = "Hòa rồi!"

                for child in view.children:
                    child.disabled = True

                view.stop()

            await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
        children: List[TicTacToeButton]
        X = -1
        O = 1
        Tie = 2

        def __init__(self):
            super().__init__()
            self.current_player = self.X
            self.board = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]

            for x in range(3):
                for y in range(3):
                    self.add_item(TicTacToeButton(x, y))

        # check xem ai thắng
        def check_board_winner(self):
            for across in self.board:
                value = sum(across)
                if value == 3:
                    return self.O
                elif value == -3:
                    return self.X

            for line in range(3):
                value = self.board[0][line] + self.board[1][line] + self.board[2][line]
                if value == 3:
                    return self.O
                elif value == -3:
                    return self.X

            diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
            if diag == 3:
                return self.O
            elif diag == -3:
                return self.X

            diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
            if diag == 3:
                return self.O
            elif diag == -3:
                return self.X

            if all(i != 0 for row in self.board for i in row):
                return self.Tie

            return None

class TicTacToeGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded cog!')


    @commands.command(name='tic', help='Chơi tic-toc-toe!')
    async def tic(self, ctx: commands.Context):
            """Starts a tic-tac-toe game with yourself."""
            await ctx.send('Tic Tac Toe: X đi trước', view=TicTacToe())
    pass

async def setup(bot):
    await bot.add_cog(TicTacToeGame(bot))
