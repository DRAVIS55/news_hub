from django.shortcuts import render,redirect
from.models import News
from django.shortcuts import render, get_object_or_404
# Create your views here.
# views.py
import os
import json
import openai
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import News

# ✅ Load API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY") 
# -------------------------------
# Home Page / News Listing
# -------------------------------
def index(request):
    category = request.GET.get('category')
    search_query = request.GET.get('q', '')

    news = News.objects.all()

    # Filtering
    if category:
        news = news.filter(news_type=category)
    if search_query:
        news = news.filter(description__icontains=search_query) | news.filter(
            heading__icontains=search_query
        )

    # Detect file types for frontend rendering
    for new in news:
        if new.file:
            ext = os.path.splitext(new.file.url)[1].lower()
            if ext in ['.mp4', '.webm', '.ogg']:
                new.file_type = 'video'
                new.video_ext = ext[1:]
            else:
                new.file_type = 'image'
        else:
            new.file_type = None

    return render(
        request,
        "index.html",
        {
            'news': news,
            'selected_category': category,
            'search_query': search_query,
        },
    )

def get_chat_history(request):
    # Delete old chats before returning
    thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
    ChatHistory.objects.filter(created_at__lt=thirty_minutes_ago).delete()

    chats = ChatHistory.objects.order_by('created_at')
    data = [
        {"user": c.user_message, "ai": c.ai_response, "time": c.created_at.strftime("%H:%M")}
        for c in chats
    ]
    return JsonResponse({"chats": data})

# -------------------------------
# AI Chat Endpoint
# -------------------------------
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from openai import OpenAI
from .models import ChatHistory, News

# ✅ Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@csrf_exempt
def chat_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            category_filter = data.get('category')
                        # fetch relevant news
            from rapidfuzz import process

            news_qs = News.objects.all()
            # Optional category filter
            if category_filter:
                news_qs = news_qs.filter(news_type=category_filter)

            # Convert queryset to list
            all_news = list(news_qs)

            # Build choices (for fuzzy search)
            choices = [f"{n.heading} {n.description}" for n in all_news]

            # Fuzzy match top 10 results for the user query
            matches = process.extract(user_message, choices, limit=10, score_cutoff=60)

            # Map back to News objects
            matched_news = [all_news[i] for _, _, i in matches]

            # Build the final string for AI input
            news_text = "\n".join([f"{n.heading}: {n.description}" for n in matched_news])
            prompt = f"""
You are a news assistant AI. Use the following news to answer user questions:
{news_text}
User Question: {user_message}
Provide a concise, clear answer. Summarize if necessary.
"""
            # ✅ Use correct model
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful news assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )

            # ✅ Extract the AI’s reply
            answer = response.choices[0].message.content.strip()
            print(f'==================================================\n{answer}')
            print('working==============================')
            print(user_message)

            # ✅ Save conversation to DB
            ChatHistory.objects.create(
                user_message=user_message,
                ai_response=answer,
                category=category_filter
            )

            # ✅ Delete expired chats (older than 30 mins)
            thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
            ChatHistory.objects.filter(created_at__lt=thirty_minutes_ago).delete()

            return JsonResponse({'reply': answer})

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'reply': f"Error: {str(e)}"})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def admin_panel(request):
    if request.method=='POST':
        Author=request.POST.get('author')
        title=request.POST.get('title')
        Description=request.POST.get('description')
        NewsFile=request.FILES.get('file')
        News.objects.create(
            author=Author,
            heading =title,
    description = Description,
    file =NewsFile
        )
        return redirect('admin-panel')
    news=News.objects.all()
    return render(request,"admin_panel.html",{'news':news})

from django.shortcuts import render
from .scrape_news import scrape_method

def scrape_news_manually(request):
    headings, content_map = scrape_method()
    contents = [(head, content_map[head]) for head in headings]
    
    context = {
        'heading_s': headings,  # list of headings
        'contents': contents,   # list of (heading, body) tuples
    }
    return render(request, "scrape_news.html", context)


def scrape_news_(request):
    return render(request, "scrape_news.html")


def news_detail(request, pk):
    highlighted_news = get_object_or_404(News, pk=pk)
    other_news = News.objects.exclude(pk=pk)  # All except highlighted
    return render(request, 'news_details.html', {
        'highlighted_news': highlighted_news,
        'other_news': other_news
    })


from .models import ContactInfo

def contact_list(request):
    contacts = ContactInfo.objects.all().order_by('-created_at')
    context = {
        'contacts': contacts
    }
    return render(request, "contact_list.html", context)

from django.shortcuts import render
from django.http import HttpResponse
from .models import ContactInfo

def submit_contact(request):
    if request.method == "POST":
        ContactInfo.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )

        # Instead of redirect, return a success message
        return HttpResponse("""
        <html>
        <head>
            <title>Message Sent</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                }
                .container {
                    text-align: center;
                    padding: 40px;
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-radius: 12px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                button {
                    margin-top: 20px;
                    padding: 12px 25px;
                    font-size: 16px;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }
                button:hover {
                    background-color: #218838;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Thank you! Your message has been submitted successfully.</h2>
                <button onclick="window.location.href='/'">Return Home</button>
            </div>
        </body>
        </html>
        """)

    return render(request, "contact_form.html")

from .models import ChatHistory
def api_responses(request):
    chats=ChatHistory.objects.all()

    return render(request,'api_responses.html',{'chats':chats})