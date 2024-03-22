import flet as ft
import aiohttp
import asyncio

pokemon_actual =0

async def main(page: ft.Page):
    page.window_width = 420
    page.window_height = 1080
    page.window_resizable = False
    page.padding = 0
    page.fonts = {
        "zpix":"https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.9/zpix.ttf"
    }
    page.theme = ft.Theme(font_family="zpix")
    
    async def peticion(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    
    async def evento_get_pokemon(e: ft.ContainerTapEvent):
        global pokemon_actual
        if e.control == flecha_superior:
            pokemon_actual +=1
        else:
            pokemon_actual -=1
            
        numero = (pokemon_actual%150)+1
        resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")
        
        datos = f"Name: {resultado['name']}\n\nAbilities:"
        for elemento in resultado['abilities']:
            habilidad = elemento['ability']['name']
            datos += f"\n{habilidad}"
        datos += f"\n\nHeight:{resultado['height']}"
        texto.value = datos         
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src = sprite_url
        await page.update_async()
    async def blink():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()
    
    luz_azul = ft.Container(width=40, height=40, left=5, top=5, bgcolor=ft.colors.BLUE, border_radius=40)
    boton_azul = ft.Stack([
        ft.Container(width=50, height=50, bgcolor=ft.colors.WHITE, border_radius=40),
        luz_azul,
    ])
    items_superior =[
        ft.Container(boton_azul, width=50, height=50),
        ft.Container(width=30, height=30,bgcolor=ft.colors.RED_200, border_radius=30),
        ft.Container(width=30, height=30, bgcolor=ft.colors.YELLOW, border_radius=30),
        ft.Container(width=30, height=30, bgcolor=ft.colors.GREEN, border_radius=30),
    ]
    
    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png"
    imagen = ft.Image(
        src=sprite_url,
        scale=15,
        width=12,
        height=12,
        top=170/2,
        right=250/2
    )
    stack_central = ft.Stack([
        ft.Container(width=300, height=200, bgcolor=ft.colors.WHITE, border_radius=20),
        ft.Container(width=280, height=180, bgcolor=ft.colors.BLACK, top=10, left=10),
        imagen,   
    ])
    
    triangulo = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(35,0),
            ft.canvas.Path.LineTo(0,40),
            ft.canvas.Path.LineTo(70,40),
        ],
        paint=ft.Paint(
                style=ft.PaintingStyle.FILL,
            ),
        ),
    ],
    width=70,
    height=40                             
    )
    
    flecha_superior = ft.Container(triangulo,width=70, height=50, on_click=evento_get_pokemon)
    flechas= ft.Column(
        [
           flecha_superior,
           ft.Container(triangulo, rotate=ft.Rotate(angle=3.14159),width=70, height=50,on_click=evento_get_pokemon),
        ]
    )
    
    texto = ft.Text(
        value="Hola",
        color=ft.colors.BLACK,
        size=14
    )
    items_inferior =[
        
        ft.Container(texto, padding=10, width=230, height=200, bgcolor=ft.colors.GREEN, border_radius=20),
        ft.Container(flechas, width=80, height=120),
        ft.Container(width=50),
    ]
    
    superior = ft.Container(content=ft.Row(items_superior),width=300, height=50, margin=ft.margin.only(top=40))
    centro = ft.Container(content=stack_central,width=300, height=200, margin=ft.margin.only(top=40),alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior),width=300, height=200, margin=ft.margin.only(top=40))
    
    col = ft.Column(spacing=0, controls=[
        superior,
        centro,
        inferior,
    ])
    contenedor = ft.Container(col, width=420, height=1080, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)
    
    await page.add_async(contenedor)
    await blink()
    
ft.app(target=main)    