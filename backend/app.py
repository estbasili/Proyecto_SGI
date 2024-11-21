from api import app
import os

# Para desarrollo:
if __name__ == '__main__':
    app.run(debug=True, host=os.environ.get("HOST", "localhost"), port=int(os.environ.get("PORT", 5001)))

    # Para producción:
# if __name__ == "__main__":
#     app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 5001)))