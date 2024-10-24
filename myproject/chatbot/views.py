from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot_logic import handle_query as process_query
import json
import pyttsx3


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            print("Request received")
            data = json.loads(request.body.decode('utf-8'))
            print("Data parsed:", data)
            query = data.get('query')
            print("Query received:", query)
            
            if not query:
                print("No query provided")  # Add this line for debugging
                return JsonResponse({'error': 'No query provided'}, status=400)

            # Process the query with the model
            response = process_query(query)
            print("Response generated:", response)
        
            return JsonResponse({'response': response})
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")  # Add this line for debugging
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Exception: {e}")  # Add this line for debugging
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html', {'response': "Hello! I'm Alexander, your personal assistant. How can I help you today?"})
