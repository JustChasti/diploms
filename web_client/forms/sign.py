from fastapi import APIRouter, Request, Form


class LoginForm:
    def __init__(self, request: Request) -> None:
        self.requst = request
        self.login = None
        self.password = None

    async def load_data(self):
        data = await self.requst.form()
        self.login = data.get('login')
        self.password = data.get('password')
