from flask import Flask, render_template, request, send_file, url_for
from pytube import YouTube
import os
import uuid

app = Flask(__name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'downloads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Downloader</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100 h-screen flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg shadow-md w-96">
            <h1 class="text-2xl font-bold mb-6 text-center">YouTube Downloader</h1>
            <form action="/download" method="post" class="space-y-4">
                <div>
                    <label for="url" class="block text-sm font-medium text-gray-700">YouTube URL</label>
                    <input type="url" name="url" id="url" required 
                           class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
                </div>
                <div>
                    <label for="format" class="block text-sm font-medium text-gray-700">Format</label>
                    <select name="format" id="format" 
                            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
                        <option value="mp4">MP4 (Video)</option>
                        <option value="mp3">MP3 (Audio)</option>
                    </select>
                </div>
                <button type="submit" 
                        class="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 transition-colors">
                    Download
                </button>
            </form>
            {% if error %}
            <p class="mt-4 text-red-500 text-center">{{ error }}</p>
            {% endif %}
        </div>
    </body>
    </html>
    ''')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        format_type = request.form['format']
        
        yt = YouTube(url)
        filename = f"{uuid.uuid4().hex[:10]}_{yt.title}"
        
        if format_type == 'mp4':
            stream = yt.streams.get_highest_resolution()
            file_path = os.path.join(UPLOAD_FOLDER, f"{filename}.mp4")
            stream.download(output_path=UPLOAD_FOLDER, filename=f"{filename}.mp4")
        else:  # mp3
            stream = yt.streams.filter(only_audio=True).first()
            file_path = os.path.join(UPLOAD_FOLDER, f"{filename}.mp3")
            stream.download(output_path=UPLOAD_FOLDER, filename=f"{filename}.mp3")
        
        return send_file(file_path, as_attachment=True)
    
    except Exception as e:
        return render_template_string(
            index_template, 
            error=f"An error occurred: {str(e)}"
        )

if __name__ == '__main__':
    app.run(debug=True)
