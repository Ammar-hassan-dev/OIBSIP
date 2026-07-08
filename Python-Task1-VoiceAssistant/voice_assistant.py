"""
Voice Assistant (GUI Version)
Oasis Infobyte - Python Programming Internship
Task 3: Voice Assistant
"""

import ctypes
import sys
import datetime
import threading
import webbrowser
import tkinter as tk
from tkinter import scrolledtext, messagebox

import speech_recognition as sr
import pyttsx3
import wikipedia

# Windows high-DPI screens par blurry/pixelated rendering fix karta hai
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# ---------- TTS Engine ----------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 175)


class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant | Oasis Infobyte")
        self.root.configure(bg="#eef2f7")
        self.root.minsize(480, 620)
        self.root.geometry("560x700")

        self.is_listening = False
        self.recognizer = sr.Recognizer()

        self.build_ui()
        self.after_greeting()

    def build_ui(self):
        # ---------- Header Banner ----------
        header = tk.Frame(self.root, bg="#2c3e50")
        header.pack(fill="x")

        tk.Label(
            header, text="🎙️  Voice Assistant", font=("Segoe UI", 22, "bold"),
            bg="#2c3e50", fg="white"
        ).pack(pady=(20, 0))

        tk.Label(
            header, text="Speak a command and I'll take care of it",
            font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7"
        ).pack(pady=(0, 20))

        # ---------- Card (flexible layout, resizes with window) ----------
        outer_pad = tk.Frame(self.root, bg="#eef2f7")
        outer_pad.pack(fill="both", expand=True, padx=25, pady=25)

        card = tk.Frame(
            outer_pad, bg="white", highlightbackground="#d0d7e2",
            highlightthickness=1, bd=0
        )
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="both", expand=True, padx=30, pady=30)

        # Status label
        tk.Label(
            inner, text="STATUS", font=("Segoe UI", 9, "bold"),
            bg="white", fg="#7f8c8d"
        ).pack(anchor="w", pady=(0, 5))

        self.status_label = tk.Label(
            inner, text="Idle", font=("Segoe UI", 13, "bold"),
            bg="white", fg="#2c3e50", anchor="w"
        )
        self.status_label.pack(fill="x", pady=(0, 18))

        # Conversation log
        tk.Label(
            inner, text="CONVERSATION", font=("Segoe UI", 9, "bold"),
            bg="white", fg="#7f8c8d"
        ).pack(anchor="w", pady=(0, 5))

        # Buttons row - pinned to the bottom FIRST so it's always visible,
        # no matter how large the window/log area grows
        btn_row = tk.Frame(inner, bg="white")
        btn_row.pack(side="bottom", fill="x", pady=(20, 0))

        log_frame = tk.Frame(inner, bg="#f4f6f8", highlightbackground="#dcdde1", highlightthickness=1)
        log_frame.pack(fill="both", expand=True)

        self.log_box = scrolledtext.ScrolledText(
            log_frame, font=("Segoe UI", 10), bg="#f4f6f8", fg="#2c3e50",
            relief="flat", wrap="word", borderwidth=0
        )
        self.log_box.pack(fill="both", expand=True, padx=8, pady=8)
        self.log_box.configure(state="disabled")

        self.log_box.tag_config("user", foreground="#27ae60", font=("Segoe UI", 10, "bold"))
        self.log_box.tag_config("assistant", foreground="#2980b9", font=("Segoe UI", 10, "bold"))
        self.log_box.tag_config("system", foreground="#95a5a6", font=("Segoe UI", 9, "italic"))

        self.listen_btn = tk.Button(
            btn_row, text="🎤  Listen", font=("Segoe UI", 11, "bold"),
            bg="#2980b9", fg="white", activebackground="#3498db",
            activeforeground="white", relief="flat", cursor="hand2",
            command=self.on_listen_click
        )
        self.listen_btn.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))

        clear_btn = tk.Button(
            btn_row, text="Clear Log", font=("Segoe UI", 11, "bold"),
            bg="#ecf0f1", fg="#2c3e50", activebackground="#dcdde1",
            relief="flat", cursor="hand2", command=self.clear_log
        )
        clear_btn.pack(side="left", ipady=10, padx=(8, 0))

    # ---------- LOGGING HELPERS ----------
    def log(self, text, tag="system"):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n", tag)
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def set_status(self, text, color="#2c3e50"):
        self.status_label.config(text=text, fg=color)

    # ---------- SPEECH ----------
    def speak(self, text):
        self.log(f"Assistant: {text}", "assistant")
        engine.say(text)
        engine.runAndWait()

    def after_greeting(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 17:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        self.log(greeting + " I am your voice assistant. Click Listen to talk to me.", "assistant")

    def on_listen_click(self):
        if self.is_listening:
            return
        self.is_listening = True
        self.listen_btn.config(state="disabled", text="Listening...")
        self.set_status("Listening...", "#f39c12")
        threading.Thread(target=self.listen_and_process, daemon=True).start()

    def listen_and_process(self):
        query = self.listen()
        self.root.after(0, lambda: self.finish_listen(query))

    def finish_listen(self, query):
        self.listen_btn.config(state="normal", text="🎤  Listen")
        self.set_status("Idle")
        if query:
            self.log(f"You said: {query}", "user")
            self.process_command(query)
        self.is_listening = False

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.pause_threshold = 1
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                return ""

        try:
            query = self.recognizer.recognize_google(audio, language='en-in')
            return query.lower()
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.speak("Sorry, I didn't catch that. Could you please repeat?"))
            return ""
        except sr.RequestError:
            self.root.after(0, lambda: self.speak(
                "Speech service is unavailable right now. Please check your internet connection."))
            return ""

    # ---------- COMMAND PROCESSING ----------
    def process_command(self, query):
        if "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")

        elif "date" in query:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today's date is {today}")

        elif "wikipedia" in query:
            self.speak("Searching Wikipedia...")
            search_term = query.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(search_term, sentences=2)
                self.speak("According to Wikipedia:")
                self.speak(result)
            except Exception:
                self.speak("Sorry, I couldn't find anything on Wikipedia for that.")

        elif "open youtube" in query:
            self.speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in query:
            self.speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "search for" in query:
            search_term = query.replace("search for", "").strip()
            self.speak(f"Searching Google for {search_term}")
            webbrowser.open(f"https://www.google.com/search?q={search_term}")

        elif "who are you" in query or "what is your name" in query:
            self.speak("I am a voice assistant, built as part of the Oasis Infobyte Python internship.")

        elif "thank you" in query:
            self.speak("You're welcome! Happy to help.")

        elif "stop" in query or "exit" in query or "quit" in query or "goodbye" in query:
            self.speak("Goodbye! Have a great day.")
            self.root.after(1000, self.root.destroy)

        else:
            self.speak("I'm not sure how to help with that yet. You can ask me about the time, "
                        "date, search Wikipedia, or open YouTube and Google.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()