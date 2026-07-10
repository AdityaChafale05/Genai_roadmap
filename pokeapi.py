
from fastapi import FastAPI ,HTTPException      #exception handling
import httpx     # modern form of request library (allows async requests)
from contextlib import asynccontextmanager      # clean startup and shutdown events


@asynccontextmanager
async def lifespan( app: FastAPI):
    app.state.client = httpx.AsyncClient(base_url ="https://pokeapi.co/api/v2/")    #app.state is use to store the client object
    
    yield                                        #everything after yield is shutdown event
    
    await app.state.client.close()


app = FastAPI(title="PokeAPi",lifespan=lifespan)   #Registers our startup/shutdown behavior into the engine.



@app.get("/")
async def root():
    return {'message': "Welcome to pokeapi"}

async def raw_data(client: httpx.AsyncClient, name: str):
    response = await client.get(f"pokemon/{name}")   #get request to pokeapi
    
    if response.status_code == 404:
            raise HTTPException (status_code=404, detail="NOT found")
    return response.json()

@app.get("/pokemon/{name}")
async def get_pokemon(name: str):
    client = app.state.client
    data = await raw_data(client, name )
    
    
    # 2. Return just the basics—no complex loops required!
    return {
        "id": data["id"],
        "name": data["name"],
        "base_experience": data["base_experience"],
        "height": f"{data['height'] / 10} m",
        "weight": f"{data['weight'] / 10} kg",
    }