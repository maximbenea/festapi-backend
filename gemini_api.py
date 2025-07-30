import os

from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()
client = genai.Client(api_key=os.getenv('API_KEY'))

def gemini_request():
    
    myfile = client.files.upload(file="image.jpg")


    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",

        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            system_instruction=[
                types.Part.from_text(text="""based on the images you will be given and a list of human scents : Fragrant (e.g., florals, perfumes)
    Woody (e.g., pine, fresh cut grass)
    Fruity (non-citrus)
    Chemical (e.g., ammonia, bleach)
    Minty (e.g., eucalyptus, camphor)
    Sweet (e.g., chocolate, vanilla, caramel)
    Popcorn (or toasted/nutty)
    Lemon (or citrus)
    Pungent (e.g., blue cheese, cigar smoke, sweat)
    Decayed (e.g., rotting meat, sour milk), generate a scent characterization of the image, attribute to the image the most accurate smell it will have, if it is an image of a digital interface or any other situation that does not have smell return none of the scents, you are not allowed to mix odors the output should be a single string in lowercase, the response should be as quick as possible but also accurate"""),
            ],
        ),
        contents=myfile,
    )
    return response.text
