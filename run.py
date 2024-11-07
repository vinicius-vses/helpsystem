from app import create_app
import traceback

app = create_app()

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()