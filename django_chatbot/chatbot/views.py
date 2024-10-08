from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from .ai_agent import agent_executor
import asyncio
import aiohttp
import requests
import time


def chatbot(request):
    if request.user.is_anonymous:
        return redirect("login")

    chats = Chat.objects.filter(user=request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        response = agent_executor.invoke(
            {"input": message + ". Answer in less than 10 words."}
        )  # could probably add chats to the input so LLM can have memory of previous conversations

        chat = Chat(
            user=request.user,
            message=message,
            response=response["output"],
            created_at=timezone.now(),
        )
        chat.save()
        return JsonResponse({"message": message, "response": response["output"]})
    return render(request, "chatbot.html", {"chats": chats})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)  # gives client a sessionid cookie
            return redirect("chatbot")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                # in settings.py, we have 'django.contrib.auth.middleware.AuthenticationMiddleware' which is why we can use auth.login
                auth.login(request, user)
                return redirect("chatbot")
            except:
                error_message = "Error creating account"
                return render(
                    request, "register.html", {"error_message": error_message}
                )
        else:
            error_message = "Password dont match"
            return render(request, "register.html", {"error_message": error_message})
    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("login")

# # synchronous version takes around 10 seconds
# def employee(request):
#     def fetch_json(url):
#         response = requests.get(url)
#         time.sleep(5) # simulate slow network
#         return response.json()

#     albums = fetch_json("https://jsonplaceholder.typicode.com/albums")
#     users = fetch_json("https://jsonplaceholder.typicode.com/users")

#     for user in users:
#         user["albums"] = [album for album in albums if album["userId"] == user["id"]]

#     return JsonResponse({"users": users})

# async version takes around 5 seconds
def employee(request):
    async def fetch_json(session, url):
        async with session.get(url) as response:
            await asyncio.sleep(5) # simulate slow network
            return await response.json()

    async def fetch_and_gather():
        async with aiohttp.ClientSession() as session:
            albums_task = fetch_json(
                session, "https://jsonplaceholder.typicode.com/albums"
            )
            users_task = fetch_json(
                session, "https://jsonplaceholder.typicode.com/users"
            )

            albums, users = await asyncio.gather(albums_task, users_task) # instead of gather, can use asyncio.create_task and it'll run both fetches at the same time. OR with TaskGroup which has different error handling

            for user in users:
                user["albums"] = [
                    album for album in albums if album["userId"] == user["id"]
                ]

            return users

    users = asyncio.run(fetch_and_gather())
    return JsonResponse({"users": users})

