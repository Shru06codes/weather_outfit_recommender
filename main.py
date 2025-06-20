import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os

# Replace with your actual API key
API_KEY = "4d41719d282e1158499ed8ee5d330d69"

# Main weather + outfit logic
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        messagebox.showerror("City Error", f"City not found: {city}")
        return

    temp = data["main"]["temp"]
    weather_desc = data["weather"][0]["description"]

    suggestion, image_file = get_outfit_suggestion(temp, weather_desc)
    show_result(temp, weather_desc, suggestion, image_file)

# Suggestion logic
def get_outfit_suggestion(temp, weather_desc):
    weather_desc = weather_desc.lower()
    if "rain" in weather_desc:
        return "Carry an umbrella and wear waterproof shoes!", r"D:/Python_shit/weather_outfit_recommender/outfit_images/rainy.png"
    elif temp >= 30:
        return "Wear light cotton clothes and sunglasses!", r"D:/Python_shit/weather_outfit_recommender/outfit_images/hot.png"
    elif temp <= 15:
        return "Wear warm clothes and a jacket!", r"D:/Python_shit/weather_outfit_recommender/outfit_images/cold.png"
    else:
        return "Wear comfortable clothes!", r"D:/Python_shit/weather_outfit_recommender/outfit_images/hot.png"

# Display the result
def show_result(temp, weather_desc, suggestion, image_path):
    result_label.config(text=f"Temperature: {temp}°C\nCondition: {weather_desc}\n\nSuggestion: {suggestion}")
    try:
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.Resampling.LANCZOS)

        outfit_photo = ImageTk.PhotoImage(image)
        image_label.config(image=outfit_photo)
        image_label.image = outfit_photo
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve image.\n{str(e)}")

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Weather-Based Outfit Recommender")
root.geometry("420x480")
root.configure(bg="#e0f7fa")  # light cyan background

header = tk.Label(root, text="Weather-Based Outfit Recommender", font=("Helvetica", 16, "bold"), bg="#e0f7fa", fg="#00796b")
header.pack(pady=15)

input_frame = tk.Frame(root, bg="#e0f7fa")
input_frame.pack(pady=10)

city_label = tk.Label(input_frame, text="Enter City Name:", font=("Arial", 12), bg="#e0f7fa")
city_label.grid(row=0, column=0, padx=5, pady=5)

city_entry = tk.Entry(input_frame, font=("Arial", 12), width=20, bd=2, relief=tk.GROOVE)
city_entry.grid(row=0, column=1, padx=5)

get_btn = tk.Button(root, text="Get Weather", font=("Arial", 12, "bold"), bg="#0288d1", fg="white", bd=0, padx=20, pady=8, command=get_weather)
get_btn.pack(pady=15)

image_label = tk.Label(root, bg="#e0f7fa")
image_label.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), bg="#e0f7fa", justify="center", wraplength=350)
result_label.pack(pady=10)

root.mainloop()
