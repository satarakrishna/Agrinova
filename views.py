from unittest import result

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import requests

# ------------------- NORMAL PAGES -------------------
def index(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    return render(request, "Home.html")

def about1(request): return render(request, "cmonsoon.html")
def about2(request): return render(request, "cwinter.html")
def about3(request): return render(request, "csummer.html")
def knowledge(request): return render(request, "knowledge.html")
def weather(request): return render(request, "weather.html")
def soil(request): return render(request, "soil.html")
def chome(request): return render(request, "chome.html")
def cweather(request): return render(request, "cweather.html")
def csoils(request): return render(request, "csoils.html")
def cedu(request): return render(request, "cedu.html")
def cpest(request): return render(request, "cpest.html")
def cmarket(request): return render(request, "cmarket.html")
def cfungal(request): return render(request, "cfungal.html")
def cgrowth(request): return render(request, "cgrowth.html")
def soilmanagement(request): return render(request, "soilmanagement.html")
def irrigationmethods(request): return render(request, "irrigationmethods.html")
def pestcontrol(request): return render(request, "pestcontrol.html")
def governmentschemes(request): return render(request, "governmentschemes.html")
def organicfarming(request): return render(request, "organicfarming.html")
def watermanagement(request): return render(request, "watermanagement.html")
def moderntechniques(request): return render(request, "moderntechniques.html")
def fertilizerguide(request): return render(request, "fertilizerguide.html")
def cropyieldimprovement(request): return render(request, "cropyieldimprovement.html")


def users_list(request):
    users = User.objects.all()  # get all registered users
    return render(request, 'users_list.html', {'users': users})
# ------------------- AUTH -------------------


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("agri")   # your home page
        else:
            return render(request, "login.html", {"error": "Invalid Username or Password"})

    return render(request, "login.html")


def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect("/login/")

    return render(request, "register.html")


def logoutUser(request):
    logout(request)
    return redirect("/login/")

# ------------------- AI CHATBOT USING PHI-3 -------------------
@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message")
            history = data.get("history", [])

            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # Keep last 5 messages only for speed
            history = history[-2:]

            system_instruction = (

                "fertilizers, pest control, seasonal planning, and government schemes. "
                "Always give answers in numbered points, each point on a new line:\n"
                "1. What to do\n"
                "2. How to do it\n"
                "3. When to do it\n"
                "Keep answers simple and farmer-friendly."
            )

            # Combine prompt
            all_messages = [system_instruction] + [h["content"] for h in history] + [user_message]
            prompt = "\n".join(all_messages)

            response = requests.post(
                settings.OLLAMA_API_URL,
                json={"model": "phi3", "prompt": prompt, "max_tokens": 120},
                timeout=15  # shorter timeout for faster response
            )
            response.raise_for_status()

            full_reply = ""
            for line in response.text.splitlines():
                if line.strip():
                    try:
                        chunk = json.loads(line)
                        full_reply += chunk.get("response", "")
                    except json.JSONDecodeError:
                        continue

            if not full_reply:
                full_reply = "Sorry, I couldn't generate a response."

            # Format numbered points on new lines
            formatted_reply = ""
            for part in full_reply.split('. '):
                if part.strip():
                    formatted_reply += part.strip() + ".\n"

            return JsonResponse({"reply": formatted_reply})

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Failed to connect to AI server: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # When page loads, send a welcome message to user
    welcome_message = "Welcome! I am your agricultural assistant. Ask me about crops, soil, irrigation, fertilizers, or government schemes.\n"
    return render(request, "chatbot_widget.html", {"welcome_message": welcome_message})

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)   # change password
            user.save()

            return render(request, "forgot_password.html", {
                "success": "Password changed successfully. You can login now."
            })

        except User.DoesNotExist:
            return render(request, "forgot_password.html", {
                "error": "Username not found"
            })

    return render(request, "forgot_password.html")