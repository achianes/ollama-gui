import io
import re
import sys
import json
import time
import uuid
import base64
import pprint
import textwrap
import platform
import webbrowser
import urllib.parse
import urllib.request
import re
from threading import Thread
from typing import Optional, List, Generator
import xml.etree.ElementTree as ET
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from ttkthemes.themed_style import ThemedStyle

try:
    import tkinter as tk
    from tkinter import ttk, font, messagebox, filedialog
except (ModuleNotFoundError, ImportError):
    print(
        "Your Python installation does not include the Tk library.\n"
        "Please refer to the original project: https://github.com/chyok/ollama-gui for more information."
    )
    sys.exit(0)

# Icon definitions in base64 format
ICON_REFRESH_B64 = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZ
cwAAFiUAABYlAUlSJPAAAAGHaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49J++7vycgaWQ9J1c1TTBNcENlaGlIenJlU3
pOVGN6a2M5ZCc/Pg0KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyI+PHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9y
Zy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj48cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0idXVpZDpmYWY1YmRkNS1iYTNkLTExZGEtYWQzMS
1kMzNkNzUxODJmMWIiIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIj48dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9y
aWVudGF0aW9uPjwvcmRmOkRlc2NyaXB0aW9uPjwvcmRmOlJERj48L3g6eG1wbWV0YT4NCjw/eHBhY2tldCBlbmQ9J3cnPz4slJgLAAAC9ElEQVRYR9
WWP2vqbBjGLzVQQTo5JVPp1qF1UQkaKFLrULD0Azi4Nm5+B+eudujYb1AoBd1sKXbyA3So0Eb8gxhxiCDXu7x93vZ+GxPbwzmcH2R5ruf2/uVJuE2E
JPEHicqF383fKeB5Ho6Pj1EoFDCbzWS8GfwGi8WChmEQALPZLKfTqdwSmm8JkOR4PGYqlfqxxMaP4O3tDdfX17i4uMD29jYAoNvtolQqYTAYyO3BSC
M/HMfh+fk5E4kEAXx5NZtNWRZIKIFWq0Vd11Ujy7LYaDRYr9cZi8XU2mg0kqWBBAq0221qmkYAzOfz7HQ6JMnhcMiDgwO1Pp/PZWko1go4jsNkMkkA
rFQqXK1WJEnP89SJ5HI5uq4rS2nbNk3T5GQykdEn1gpUq1XV5CPL5ZLlcpnFYvHL5iSZTqcJgLVaTUaf8BXo9/vUNI3RaJS9Xk/Ggdzf3xMA4/E4Hc
eRscJXoNlsEgCPjo5kFBrLsgiAV1dXMlL4zoFutwsAKJVKMgrNyckJAODx8VFGCl+B96Gys7Mjo9Ds7u4CAF5fX2Wk8BWIRCIAgJ98LoT5DV8BwzAA
AM/PzzIKzcvLCwBA13UZKXwFTNMEANze3sooNHd3dwCATCYjo/+Qb+U7juMwHo8TAB8eHmQcSK/XYzQapaZp7Pf7Mlb4CpBkrVYjAKbTaRmRJF3XZb
FYZLlc5nK5/JTl83kCYLVa/bQuWSswmUxomiZt25YRXddlLpcjAOq6Ts/zSJKr1YqVSoUAmEwm1w4hBgn4MZ/P1R3u7+9zOBySJDudjlrXNI3tdluW
/o+NBUajkZpwsViM9XqdjUZDNX4/kVarJUu/ZGOBy8tL1UheiUSCtm0HHvtHIlw3Jb5gMBjg9PQUT09PAADLsnB4eIi9vT0UCgU1P0IjjcIwnU6ZyW
QIgKlUiuPxWG4JzbcE+K9ENpslABqGwcViIbeEYuNH8JHZbIazszNomoabmxtsbW3JLYH8SOBX4Ptf8Lv44wL/AF75rsuoGodUAAAAAElFTkSuQmCC
"""
ICON_SEND_B64 = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAA
GHaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49J++7vycgaWQ9J1c1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCc/Pg0KPHg6
eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyI+PHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi
1zeW50YXgtbnMjIj48cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0idXVpZDpmYWY1YmRkNS1iYTNkLTExZGEtYWQzMS1kMzNkNzUxODJmMWIiIHht
bG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIj48dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPjwvcmRmOk
Rlc2NyaXB0aW9uPjwvcmRmOlJERj48L3g6eG1wbWV0YT4NCjw/eHBhY2tldCBlbmQ9J3cnPz4slJgLAAAD7ElEQVRYR8WXSyh0bxzHv0bDIHc1MiUi
JYupsUBqSuR+yw4LNCliQ7FSVhaywEZuG5SVDWJlSmkKuSZFoYQxuWWOS41L33fzOs3zGP7M6/2/nzqb8/k95/c9l+fpOT4kiX+IRj7xf/PPA/j87V
fgdDqxsrICAMjNzZU1wL/AwcEBR0ZGWFFRwcjISAIgAJaWlvLp6Umo/ZEALpeLNpuNnZ2dTE9PVxu+Henp6TQYDARAq9UqjPU6gMPh4NTUFC0WC+Pi
4oSGoaGhLCsr4+DgIPf390mSJpOJALi4uChc51sBdnZ22NfXx7y8PAYGBgpNk5KS2NTUxNnZWV5fXwvj9vb2CIB6vZ6Pj4+C+zTA/f09rVYr29vbaT
QahYa+vr40m83s6uri6uoqX19f5eEqvb29BMDq6mpZvQ/w8vLCyclJVlZWMjo6Wmiq1+tZWVnJ8fFxHh8fy0M/JCcnhwA4OTkpKzHAzc0NMzMzhaZG
o5FtbW1cWFjg3d2de/mXuLy8ZEBAAP38/Hh+fi5rMUB9fT0BMCEhgf39/dzd3XXXXjE1NUUANJvNsiLdAzw8PDAiIoK+vr7c29sTq/4Du93O1tZWrq
2tyYp1dXUEwO7ublmR7gEURWFQUBC1Wi1vb2/Fqk+w2+1MTk4mALa0tAjO5XKp8397e1twbwivID8/nwBYVFTEjY0Nd+WRs7MztXlqairtdrvgbTYb
ATAxMfHDWSIE2N3dZVRUlPoBZmdnc2JiwuPHJzeX5z5JdnR0EACbm5tlpfJuGh4eHrKhoYFhYWFqEIPBwPb2du7s7JC/V8G35iaTiVdXV/JlSLfVb3
5+XlYq7wK8cXFxwYGBAaalpalBALC4uJgpKSnqnX/U/OjoiD4+PgwNDaXT6ZS1yocB3FlaWqLFYmFwcLAaJCMjw+Njf2NoaIgAWFZWJiuBLwV4w+Fw
0GKxEABrampkLVBaWkoAHB4elpXAtwLwdwitVkt/f3+enJzImiTpdDoZEhJCjUbDo6MjWQt8e0um1+tRUlICl8uFsbExWQMAbDYbFEWByWRCfHy8rA
W+HQAAGhsbAQCjo6N4eXmRNebm5gAARUVFsnqP/Ei+wuvrK5OSkgiAMzMz71xCQgIBcHl5WXCe8CoASfb09BAACwoKhPNbW1vq2iHv/zzhdQCHw0Gd
TkeNRiPsDbq7uwmAtbW1Qv1HeB2AJKuqqgiA5eXlPD095fr6OmNjYwmA09PTcrlH/ijA/v4+Q0JCCIAajUZdpLKysvj8/CyXe+SPApDk5uYmCwsLGR
4ezpiYGDY3N1NRFLnsQ37sz0hRFPj5+UGn08nqU34sgLd4tRD9JL8Ay/HZYj53EEwAAAAASUVORK5CYII=
"""
ICON_STOP_B64 = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAA
LkSURBVFhHxZfLTjoxFMZBRdZsgMACAjvuvhG3J+DicyjwBkbDdSuRiw+hJpoQYUdcAgtFCRzzNWnTKTM4Mn///JImk/br6TczndMzNjowNrXjf7OX
gdfXV7q/v6dOp8MarsfjsSozhWkDj4+PVC6XKZFIkNPpJJvNpmnoS6VSdH5+zrRm+dHAdDqlfD5PDodja1GjdnJyQtlsls39iZ0Gut0u+Xw+TfBQKM
SCX15eUqvVomazSRcXF5ROp9mYrMXc29tbNawGQwPX19d0dHQkgp2dnbHF3t/fVakAY/V6nZLJpJhnt9vp6upKlQp0DfR6PTaRBykWi/T5+anKDFku
l2yO/DTu7u5UGWPLwNvbG7ndbjERj3dfMJfHQUzEVtkykMlkxKRCoaAO/xrE4PEQW0Vj4Pn5mY6Pj5k4FovRarWSh/cCMaLRKIuJ2FhDRmOgVCoJt0
gwKpvNhhaLBc1mM5rP55qGPoxBo9Jut0Vc5BIZYWC9XlMkEmGiYDBIX19fGiHAAvF4nDweD3m9Xk1DH8agUcEGDgQCLDaeBtbiCANIrzzZIPHogTt1
uVzibtSGMWj0QO6ABmtMJhPRLwwMBgMRqFarCYEMguNu1YV5w5iRgUqlInQ4OzjCALIaF+BaDysGGo2G0GFPcIQBeaMg4+lhxQBicp18g7qvoFqtCo
GMFQPyKxgOh6JfGMB5zjdhLpcTApk/3YT4NHjC+MvPEAlO9zMEZhIRTzpyEuJ9lhIReHl5OWwqBigsuFscqVaRj2XsA5UtA+pxjN27L6iaeBzTxzFA
8cAn8vdmpSBBcYMiRw9dAwBllFwVocxCubWrJPv4+NAtyW5ublSpwNAAQEGpV5Rin6DaQXpFVuNFaTgc1mj9fj8rbHex0wBAaY3EhFJbDr6rIdngRL
Vclss8PDywPIHPU+8f4fT0lP204Mfk6elJnW6IaQMcJJrRaET9fp8lGCQsnCOoJ/bh1wb+NQc38A1PQ98GahkXHgAAAABJRU5ErkJggg== 
"""
# Import for Markdown, syntax highlighting and HTML widget
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from tkinterweb import HtmlFrame

__version__ = "1.2.1"

def _system_check(root: tk.Tk) -> Optional[str]:
    """
    Check for system or software incompatibilities.
    """
    def _version_tuple(v):
        filled = []
        for point in v.split("."):
            filled.append(point.zfill(8))
        return tuple(filled)

    if platform.system().lower() == "darwin":
        version = platform.mac_ver()[0]
        if version and 14 <= float(version) < 15:
            tcl_version = root.tk.call("info", "patchlevel")
            if _version_tuple(tcl_version) <= _version_tuple("8.6.12"):
                return (
                    "Warning: Tkinter Responsiveness Issue Detected\n\n"
                    "You may experience unresponsive GUI elements when "
                    "your cursor is inside the window during startup. "
                    "This is a known issue with Tcl/Tk versions 8.6.12 "
                    "and older on macOS Sonoma.\n\nTo resolve this:\n"
                    "Update to Python 3.11.7+ or 3.12+\n"
                    "Or install Tcl/Tk 8.6.13 or newer separately\n\n"
                    "Temporary workaround: Move your cursor out of "
                    "the window and back in if elements become unresponsive.\n\n"
                    "For more information, visit: https://github.com/python/cpython/issues/110218"
                )

def load_icon(base64_data, zoom=1, subsample=1):
    """
    Decode a base64 image, set near-white pixels as transparent and apply scaling.
    """
    image_data = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_data))
    image = image.convert("RGBA")
    datas = image.getdata()
    new_data = []
    for item in datas:
        # If pixel is nearly white, make it transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((item[0], item[1], item[2], 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    # Apply zoom and subsample if needed
    if zoom != 1 or subsample != 1:
        if zoom != 1:
            width, height = image.size
            image = image.resize((width * zoom, height * zoom), Image.NEAREST)
        if subsample != 1:
            width, height = image.size
            image = image.resize((width // subsample, height // subsample), Image.NEAREST)
    return ImageTk.PhotoImage(image)

class OllamaInterface:
    chat_box: HtmlFrame
    user_input: tk.Text
    host_input: ttk.Entry
    progress: ttk.Progressbar
    send_button: ttk.Button
    refresh_button: ttk.Button
    settings_button: ttk.Button
    download_button: ttk.Button
    delete_button: ttk.Button
    model_select: ttk.Combobox
    log_textbox: tk.Text
    models_list: tk.Listbox

    def __init__(self, root: tk.Tk, saved_config: dict):
        self.root: tk.Tk = root
        self.style = ThemedStyle(self.root)
        self.api_url: str = "http://127.0.0.1:11434"
        self.chat_history: List[dict] = []
        self.default_font: str = font.nametofont("TkTextFont").actual()["family"]
        # Set theme and update style configurations
        self.style.set_theme("breeze")
        self.style.configure("TCombobox", fieldbackground=self.style.lookup('TEntry', 'fieldbackground'))
        self.style.configure("Header.TFrame", background=self.style.lookup('TFrame', 'background'))
        self.style.configure("Header.TMenu", background=self.style.lookup('TFrame', 'background'))

        # Load images for the send and stop buttons using load_icon (to ensure transparency)
        self.send_img = load_icon(ICON_SEND_B64)
        self.stop_img = load_icon(ICON_STOP_B64)
        # The refresh icon is loaded with scaling parameters to ensure transparency
        # (instead of using tk.PhotoImage directly)
        # self.refresh_img will be loaded in _header_frame
        style_defs = HtmlFormatter(style='monokai').get_style_defs('.highlight')
        self.initial_html = f"""
        <style>
            {style_defs}

       .user-message {{
            background: #f0f0f0;
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            max-width: 67%;
            margin-left: 33%;
            
        }}
        .copy-link {{
            color: #0078d7;
            text-decoration: underline;
            cursor: pointer;
            margin-left: 5px;           
        }}
        
        /* AI message styles */
        .ai-message {{
            background: #f0f0f0;
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            margin-right: 33%;
            max-width: 67%;
            border: 0px solid black
        }}


        .code-body {{
            padding: 10px;
            color: white;
            font-family: monospace;
            font-size: 14px;          
            border: 0px solid red;

        }}
        
        .code-container {{
            display: flex;
            flex-direction: column;
            border-radius: 8px;
            margin: 15px 40px;
            background: #222;  
            overflow:auto;  
            overflow-y:hide;
            border: 0px solid green;
        }}
        
        .code-header {{
            display: flex;
            align-items: center;
            padding: 5px 10px;
            background-color: #333;
            color: white;
            border-bottom: 1px solid #444;
        }}

        .code-header span {{
            flex-grow: 1;
        }}

        .copy-btn {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 5px 15px;
            cursor: pointer;
            border-bottom-left-radius: 6px;
            margin-left: auto !important;
            
        }}

        /* Think block */
        .think-block {{
            font-style: italic;
            white-space: pre-wrap;
            margin: 5px 40px;
            font-size: 0.9em;
            line-height: 1.2em;
            word-wrap: break-word;
            overflow-wrap: break-word;
            max-width: 100%;
            
        }}

        /* General alignment */
        .chat-container {{
            max-width: 1000px;
            margin: 0 auto;
            
        }}
        .highlight pre {{
            margin: 0;
            padding: 0;
            background: #222;
        }}
        </style>

        <script>
            function copyCode(uniqueId) {{
                const codeBlock = document.getElementById('code-' + uniqueId);
                if (!codeBlock) {{
                    console.log('Failed to find code block.');
                    return;
                }}

                // Crea un link fittizio e ci clicca automaticamente
                let fakeLink = document.createElement('a');
                fakeLink.href = "copy://" + encodeURIComponent(codeBlock.innerText);
                fakeLink.click();
            }}
        </script>
        <div id="chat-content"></div>
        """
        self.html_content = self.initial_html

        self.layout = LayoutManager(self)
        self.layout.init_layout()

        # Prevent automatic link opening
        #self.chat_box.bind("<<LinkClicked>>", lambda e: self.block_link(e))
        self.chat_box.bind("<<LinkClicked>>", self.on_link_clicked)

        self.root.after(200, self.check_system)
        self.refresh_models()
        
        self.saved_host = saved_config.get("host", "http://127.0.0.1:11434")
        self.saved_model = saved_config.get("model", "")
        
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if event.width > 800:
            self.style.configure("TCombobox", font=(self.default_font, 12))
        else:
            self.style.configure("TCombobox", font=(self.default_font, 10))     


    def get_style(self):
        return self.style
        
    def refresh_models(self):
        self.update_host()
        self.model_select.config(foreground="black")
        self.model_select.set("Loading...")
        self.send_button.state(["disabled"])
        self.refresh_button.state(["disabled"])
        
        Thread(target=self.update_model_select, daemon=True).start()

    def update_host(self):
        self.api_url = self.host_input.get()
        
    def handle_key_press(self, event: tk.Event):
        if event.keysym == "Return":
            if event.state & 0x1 == 0x1:  # Shift pressed
                self.user_input.insert("end", "\n")
            elif "disabled" not in self.send_button.state():
                self.on_send_button(event)
            return "break"
            
    def update_model_select(self):
        try:
            models = self.fetch_models()
        except Exception as e:
            models = []
            self.append_log_to_inner_textbox(f"Error loading models: {e}")
        finally:
            self.model_select["values"] = models
            if self.saved_model in models:
                self.model_select.set(self.saved_model)
            elif models:
                self.model_select.set(models[0])
            else:
                self.model_select.set("")
            self.enable_interface()
            
    def on_link_clicked(self, event):
        url = event.url
        if url.startswith("copy://"):
            import urllib.parse
            text_to_copy = urllib.parse.unquote(url[7:])
            text_to_copy = self.remove_line_numbers(text_to_copy)
            self.copy_text(text_to_copy)
            messagebox.showinfo("Copied", "Code copied to clipboard!")
        else:
            messagebox.showinfo("Link", f"Link: {url}\nOpening links is disabled for security reasons.")
        return None

    def remove_line_numbers(self, text):
        lines = text.splitlines()
        cleaned_lines = [re.sub(r'^\s*\d+\s?', '', line) for line in lines]
        return '\n'.join(cleaned_lines).strip()

    def copy_text(self, text: str):
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)

    def copy_all(self):
        self.copy_text(pprint.pformat(self.chat_history))

    @staticmethod
    def open_homepage():
        webbrowser.open("https://github.com/achianes/ollama-gui")

    def show_help(self):
        info = ("Project: Ollama GUI Enhanced\n"
                f"Version: {__version__}\n"
                "Based on the original project by chyok: https://github.com/chyok/ollama-gui\n\n"
                "<Enter>: send message\n"
                "<Shift+Enter>: new line\n")
        messagebox.showinfo("About", info, parent=self.root)

    def check_system(self):
        message = _system_check(self.root)
        if message is not None:
            messagebox.showwarning("Warning", message, parent=self.root)

    def convert_to_html(self, content: str, role: str = "user") -> str:
        prefix = "<strong>User:</strong> " if role == "user" else "<strong>Ollama:</strong> "
        messages = []
        current_code = []
        current_lang = None
        inside_code = False
        current_text = []
        if role == "code":
            return f"""
            <div class="code-container">
                <div class="code-header">
                    Code
                    <span class="copy-link" onclick="window.prompt('Copy:', '{content}')">Copy</span>
                </div>
                <div class="code-body" >{content}</div>
            </div>
            """
        lines = content.split('\n')
        for line in lines:
            if line.startswith('```'):
                if inside_code:
                    messages.append(('code', current_lang, '\n'.join(current_code)))
                    current_code = []
                    current_lang = None
                    inside_code = False
                else:
                    parts = line[3:].strip().split(' ', 1)
                    current_lang = parts[0] if parts else ''
                    inside_code = True
                continue
            if inside_code:
                current_code.append(line)
            else:
                current_text.append(line)
        if current_text:
            messages.append(('text', '\n'.join(current_text)))

        combined = prefix
        for msg in messages:
            if msg[0] == 'text':
                combined += markdown(msg[1])
            elif msg[0] == 'code':
                lang = msg[1]
                code = msg[2]
                try:
                    lexer = get_lexer_by_name(lang) if lang else TextLexer()
                except:
                    lexer = TextLexer()
                formatter = HtmlFormatter(linenos=True, style='monokai')
                highlighted = highlight(code, lexer, formatter)
                unique_id = str(uuid.uuid4()).replace('-', '')
                combined += f"""
                <div class='code-container' id='code-container-{unique_id}'>
                    <div class='code-header'>
                        <span>{lang}</span>
                        <button class='copy-btn' style='margin-left: auto' onclick='py_copy("{urllib.parse.quote(code)}")'>Copy</button>
                    </div>
                    <div class='code-body' id='code-{unique_id}'>{highlighted}</div>
                </div>
                """
        def replace_think(match):
            inner_text = match.group(1).strip()
            if not inner_text:
                return ""
            transformed = "<br>".join(line for line in inner_text.splitlines())
            return f"<div class='think-block'><i>&lt;think&gt;<div style='margin-left:20px;'>{transformed}</div>&lt;/think&gt;</i></div>"

        combined = re.sub(r"<think>(.*?)</think>", replace_think, combined, flags=re.DOTALL)
        div_class = "user-message" if role == "user" else "ai-message"
        return f"<div class='{div_class}'>{combined}</div>"

    def append_html_to_chat(self, content: str, role: str = "user"):
        html_snippet = self.convert_to_html(content, role)
        self.html_content += html_snippet
        self.chat_box.load_html(self.html_content)
        try:
            self.chat_box.yview_moveto(1.0)
        except Exception:
            pass

    def disable_interface(self):
        self.host_input.state(["disabled"])
        self.refresh_button.state(["disabled"])
        self.model_select.state(["disabled"])
        self.user_input.config(state="disabled")
        self.settings_button.state(["disabled"])

        menubar = self.root.nametowidget(self.root["menu"])
        for index in range(menubar.index("end") + 1):
            menu_type = menubar.type(index)
            if menu_type == "cascade":
                submenu = menubar.nametowidget(menubar.entrycget(index, "menu"))
                for i in range(submenu.index("end") + 1):
                    if submenu.entrycget(i, "label") != "Exit":
                        submenu.entryconfig(i, state="disabled")

    def enable_interface(self):
        self.send_button.state(["!disabled"])
        self.host_input.state(["!disabled"])
        self.refresh_button.state(["!disabled"])
        self.model_select.state(["!disabled"])
        self.user_input.config(state="normal")
        self.settings_button.state(["!disabled"])

        menubar = self.root.nametowidget(self.root["menu"])
        for index in range(menubar.index("end") + 1):
            menu_type = menubar.type(index)
            if menu_type == "cascade":
                submenu = menubar.nametowidget(menubar.entrycget(index, "menu"))
                for i in range(submenu.index("end") + 1):
                    submenu.entryconfig(i, state="normal")

    
    def js_copy_to_clipboard(self, text):
        import urllib.parse
        text = urllib.parse.unquote(text)
        text = self.remove_line_numbers(text)
        self.copy_text(text)
        messagebox.showinfo("Copied", "Code copied to clipboard!")    
    
    def on_send_button(self, _=None):
        message = self.user_input.get("1.0", "end-1c")
        if message:
            self.user_input.delete("1.0", "end")
            self.chat_history.append({"role": "user", "content": message})
            self.append_html_to_chat(message, role="user")
            
            self.send_button.config(image=self.stop_img)
            self.disable_interface()
            self.progress.grid()
            self.progress.start(10)
            Thread(target=self.generate_ai_response, daemon=True).start()

    def update_model_list(self):
        if self.models_list.winfo_exists():
            self.models_list.delete(0, tk.END)
            try:
                models = self.fetch_models()
                for model in models:
                    self.models_list.insert(tk.END, model)
            except Exception:
                self.append_log_to_inner_textbox("Error! Please check the Ollama host.")

    def generate_ai_response(self):
        try:
            ai_message = ""
            for i in self.fetch_chat_stream_result():
                ai_message += i
            self.chat_history.append({"role": "assistant", "content": ai_message})
            self.append_html_to_chat(ai_message, role="assistant")
        except Exception:
            error_html = "AI error!"
            self.append_html_to_chat(error_html, role="assistant")
        finally:
            self.progress.stop()
            self.progress.grid_remove()
            self.send_button.config(image=self.send_img)
            self.enable_interface()

    def fetch_models(self) -> List[str]:
        with urllib.request.urlopen(
            urllib.parse.urljoin(self.api_url, "/api/tags")
        ) as response:
            data = json.load(response)
            models = [model["name"] for model in data["models"]]
            return models

    def fetch_chat_stream_result(self) -> Generator:
        request = urllib.request.Request(
            urllib.parse.urljoin(self.api_url, "/api/chat"),
            data=json.dumps({
                    "model": self.model_select.get(),
                    "messages": self.chat_history,
                    "stream": True,
                }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request) as resp:
            for line in resp:
                data = json.loads(line.decode("utf-8"))
                if "message" in data:
                    time.sleep(0.01)
                    yield data["message"]["content"]

    def delete_model(self, model_name: str):
        self.append_log_to_inner_textbox(clear=True)
        if not model_name:
            return
        req = urllib.request.Request(
            urllib.parse.urljoin(self.api_url, "/api/delete"),
            data=json.dumps({"name": model_name}).encode("utf-8"),
            method="DELETE",
        )
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    self.append_log_to_inner_textbox("Model deleted successfully.")
                elif response.status == 404:
                    self.append_log_to_inner_textbox("Model not found.")
        except Exception as e:
            self.append_log_to_inner_textbox(f"Failed to delete model: {e}")
        finally:
            self.update_model_list()
            self.update_model_select()

    def download_model(self, model_name: str, insecure: bool = False):
        self.append_log_to_inner_textbox(clear=True)
        if not model_name:
            return
        self.download_button.state(["disabled"])
        req = urllib.request.Request(
            urllib.parse.urljoin(self.api_url, "/api/pull"),
            data=json.dumps({"name": model_name, "insecure": insecure, "stream": True}).encode("utf-8"),
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as response:
                for line in response:
                    data = json.loads(line.decode("utf-8"))
                    log = data.get("error") or data.get("status") or "No response"
                    if "status" in data:
                        total = data.get("total")
                        completed = data.get("completed", 0)
                        if total:
                            log += f" [{completed}/{total}]"
                    self.append_log_to_inner_textbox(log)
        except Exception as e:
            self.append_log_to_inner_textbox(f"Failed to download model: {e}")
        finally:
            self.update_model_list()
            self.update_model_select()
            if self.download_button.winfo_exists():
                self.download_button.state(["!disabled"])

    def append_log_to_inner_textbox(self, message: Optional[str] = None, clear: bool = False):
        if self.log_textbox.winfo_exists():
            self.log_textbox.config(state=tk.NORMAL)
            if clear:
                self.log_textbox.delete(1.0, tk.END)
            elif message:
                self.log_textbox.insert(tk.END, message + "\n")
            self.log_textbox.config(state=tk.DISABLED)
            self.log_textbox.see(tk.END)
        self.root.update_idletasks()

    def clear_chat(self):
        self.html_content = self.initial_html
        self.chat_box.load_html(self.html_content)
        self.chat_history.clear()

    def show_error(self, text):
        self.model_select.set(text)
        self.model_select.config(foreground="red")
        self.model_select["values"] = []
        self.send_button.state(["disabled"])

    def show_process_bar(self):
        self.progress.grid(row=0, column=0, sticky="nsew")
        self.send_button.grid(row=0, column=1, padx=20)
        self.progress.start(5)

    def hide_process_bar(self):
        self.progress.stop()
        self.send_button.grid_remove()
        self.progress.grid_remove()
     

    def save_as_html(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML file", "*.html")])
        if not file_path:
            return

        # Genera lo stile CSS integrato con Pygments
        pygments_css = HtmlFormatter(style='monokai').get_style_defs('.highlight')
        chat_styles = self.get_chat_styles().replace(pygments_css, "")  # Rimuovi duplicati

        # Genera il markup HTML corretto
        full_html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                {pygments_css}
                {chat_styles}

                .code-body, code-body * {{
                    color: white !important;
                }}
                .copy-btn {{
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    cursor: pointer;
                    margin-left: auto;
                    border-bottom-left-radius: 6px;
                }}
            </style>
            <script>
                document.addEventListener('DOMContentLoaded', () => {{
                    document.querySelectorAll('.copy-btn').forEach(button => {{
                        button.onclick = () => {{
                            const elementId = button.getAttribute('data-code-id');
                            const codeBlock = document.getElementById(elementId);
                            if (codeBlock) {{
                                navigator.clipboard.writeText(codeBlock.textContent).then(() => {{
                                    alert('Code copied!');
                                }});
                            }}
                        }};
                    }});
                }});
            </script>
        </head>
        <body>
            <div class="chat-container">
                {self.html_content}  
            </div>
        </body>
        </html>
        """
        # Salva il file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_html)
            messagebox.showinfo("Success", f"HTML saved at: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))





    def save_as_pdf(self):
        try:
            import pdfkit
        except ImportError:
            messagebox.showerror("Error", "Please install pdfkit and wkhtmltopdf")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF file", "*.pdf")])
        if not file_path:
            return

        # Rigenera correttamente l'HTML con gli snippet elaborati da Pygments
        chat_html_for_pdf = ""
        for msg in self.chat_history:
            content_html = self.convert_to_html_for_pdf(msg['content'], msg['role'])
            chat_html_for_pdf += content_html

        html_content = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                {self.get_chat_styles()}
                pre, .code-body {{
                    color: white !important;
                    white-space: pre-wrap; /* questo abilita il word-wrap */
                    word-break: break-word;
                }}
                .code-container {{
                    max-width: 100%;
                    overflow-x: hidden;
                }}
            </style>
        </head>
        <body>
            <div class="chat-container">
                {chat_html_for_pdf}
            </div>
        </body>
        </html>
        """

        try:
            pdfkit.from_string(html_content, file_path)
            messagebox.showinfo("Success", f"PDF saved at: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save PDF: {str(e)}")

    def convert_to_html_for_pdf(self, content: str, role: str = "user") -> str:
        prefix = "<strong>User:</strong> " if role == "user" else "<strong>Ollama:</strong> "
        messages = []
        current_code = []
        current_lang = None
        inside_code = False
        current_text = []

        lines = content.split('\n')
        for line in lines:
            if line.startswith('```'):
                if inside_code:
                    messages.append(('code', current_lang, '\n'.join(current_code)))
                    current_code = []
                    current_lang = None
                    inside_code = False
                else:
                    current_lang = line[3:].strip()
                    inside_code = True
                continue
            if inside_code:
                current_code.append(line)
            else:
                current_text.append(line)
        if current_text:
            messages.append(('text', '\n'.join(current_text)))

        combined = prefix
        for msg in messages:
            if msg[0] == 'text':
                combined += markdown(msg[1])
            elif msg[0] == 'code':
                lang = msg[1] if msg[1] else "text"
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = HtmlFormatter(noclasses=True, style='monokai')
                highlighted = highlight(msg[2], lexer, formatter)
                combined += f"""
                <div class='code-container'>
                    <div class='code-header'>
                        <span>{lang}</span>
                    </div>
                    <div class='code-body'>{highlighted}</div>
                </div>
                """

        div_class = "user-message" if role == "user" else "ai-message"
        return f"<div class='{div_class}'>{combined}</div>"

            
    def get_chat_styles(self) -> str:
        """Return current chat CSS styles for the PDF, including Pygments Monokai styles."""
        pygments_css = HtmlFormatter(style='monokai').get_style_defs('.highlight')
        return f"""
        {pygments_css}
        /* User message styles */
        .user-message {{
            background: #f0f0f0;
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            max-width: 67%;
            margin-left: 33%;
            
        }}
        .copy-link {{
            color: #0078d7;
            text-decoration: underline;
            cursor: pointer;
            margin-left: 5px;           
        }}
        
        /* AI message styles */
        .ai-message {{
            background: #f0f0f0;
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            margin-right: 33%;
            max-width: 67%;          
        }}

        .code-container {{
            display: flex;
            flex-direction: column;
            border-radius: 8px;
            margin: 15px 40px;
            background: #222;
        }}
        .code-header {{
            display: flex;
            align-items: center;
            padding: 5px 10px;
            background-color: #333;
            color: white;
            border-bottom: 1px solid #444;
        }}

        .code-header span {{
            flex-grow: 1;
        }}

        .code-body {{
            padding: 10px;
            font-family: monospace;
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .copy-btn {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 5px 15px;
            cursor: pointer;
            margin-left: auto;
            border-bottom-left-radius: 6px;
            
        }}

        /* Think block */
        .think-block {{
            font-style: italic;
            white-space: pre-wrap;
            margin: 5px 40px;
            font-size: 0.9em;
            line-height: 1.2em;
            word-wrap: break-word;
            overflow-wrap: break-word;
            max-width: 100%;
            
        }}

        /* General alignment */
        .chat-container {{
            max-width: 1000px;
            margin: 0 auto;
            
        }}
        """

        
class LayoutManager():
    """
    Manages the overall layout of the interface.
    """
    def __init__(self, interface: OllamaInterface):
        self.interface: OllamaInterface = interface
        self.management_window: Optional[tk.Toplevel] = None

    def init_layout(self):
        self.interface.root.grid_columnconfigure(0, weight=1)
        self.interface.root.grid_rowconfigure(1, weight=1)
        self.interface.root.grid_rowconfigure(3, weight=0)
        
        self._header_frame()
        self._chat_container_frame()
        self._processbar_frame()
        self._input_frame()

    def _header_frame(self):
        header_frame = ttk.Frame(self.interface.root, style="Header.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(5, weight=1)
        
        header_frame.grid_columnconfigure(0, weight=1)  # Model Select
        header_frame.grid_columnconfigure(1, weight=0)  # Refresh button
        header_frame.grid_columnconfigure(2, weight=0)  # Settings button
        header_frame.grid_columnconfigure(3, weight=1)  # Spazio vuoto
        header_frame.grid_columnconfigure(4, weight=0)  # Label Host
        header_frame.grid_columnconfigure(5, weight=1)  # Entry Host
        
        self.interface.root.option_add("*Menu.background", self.interface.style.lookup('TFrame', 'background'))
        self.interface.root.option_add("*Menu.foreground", "black")
        self.interface.root.option_add("*Menu.activeBackground", self.interface.style.lookup('TFrame', 'background'))
        self.interface.root.option_add("*Menu.activeForeground", "black")

        model_select = ttk.Combobox(header_frame, state="readonly", width=30)
        model_select.grid(row=0, column=0, padx=(0, 5))

        # Load the refresh icon with transparency fixes via load_icon
        refresh_img = load_icon(ICON_REFRESH_B64, zoom=3, subsample=7)
        refresh_button = ttk.Button(header_frame, image=refresh_img, command=self.interface.refresh_models, width=3)
        refresh_button.image = refresh_img
        refresh_button.grid(row=0, column=1, padx=(0, 5))

        settings_button = ttk.Button(header_frame, text="⚙️", command=self.show_model_management_window, width=3)
        settings_button.grid(row=0, column=2, padx=(0, 10))

        ttk.Label(header_frame, text="Host:").grid(
            row=0, column=4, sticky="e",  
            padx=(0, 5)  # Spaziatura da destra per separare dall'entry
        )

        host_input = ttk.Entry(header_frame, width=24)
        host_input.grid(
            row=0, column=5, sticky="ew",  
            padx=(20, 55)  
        )
        
        host_input.insert(0, self.interface.api_url)

        self.interface.model_select = model_select
        self.interface.refresh_button = refresh_button
        self.interface.settings_button = settings_button
        self.interface.host_input = host_input

    def _chat_container_frame(self):
        chat_frame = ttk.Frame(self.interface.root)
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)

        chat_box = HtmlFrame(chat_frame,  javascript_enabled=True)
        chat_box.grid(row=0, column=0, sticky="nsew")
        chat_box.load_html(self.interface.html_content)
        
        chat_box.register_JS_object("py_copy", self.interface.js_copy_to_clipboard)

        chat_box.bind("<<LinkClicked>>", self.interface.on_link_clicked)
        self.interface.chat_box = chat_box
    
    def _processbar_frame(self):
        pass
        
    def _input_frame(self):
        input_frame = ttk.Frame(self.interface.root)
        input_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 20))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Create the user input text widget with undo enabled
        user_input = tk.Text(
            input_frame,
            bg='white',
            fg=self.interface.style.lookup('TEntry', 'foreground', default='black'),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=self.interface.style.lookup('TEntry', 'bordercolor', default='#4a6984'),
            highlightbackground=self.interface.style.lookup('TEntry', 'fieldbackground', default='white'),
            insertbackground=self.interface.style.lookup('TEntry', 'foreground', default='black'),
            height=4,
            wrap=tk.WORD,
            font=(self.interface.default_font, 12),
            undo=True
        )
        user_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        user_input.bind("<Key>", self.interface.handle_key_press)
        self.interface.user_input = user_input

        # Create a context menu for the user input with cut, copy, paste, undo and redo actions.
        context_menu = tk.Menu(user_input, tearoff=0)
        context_menu.add_command(label="Cut", command=lambda: user_input.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        context_menu.add_command(label="Copy", command=lambda: user_input.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        context_menu.add_command(label="Paste", command=lambda: user_input.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        context_menu.add_command(label="Undo", command=lambda: user_input.event_generate("<<Undo>>"), accelerator="Ctrl+Z")
        context_menu.add_command(label="Redo", command=lambda: user_input.event_generate("<<Redo>>"), accelerator="Ctrl+Y")
        
        def show_context_menu(event):
            context_menu.tk_popup(event.x_root, event.y_root)
        
        user_input.bind("<Button-3>", show_context_menu)
        
        # Pulsante Send/Stop
        send_button = ttk.Button(
            input_frame,
            image=self.interface.send_img,
            command=self.interface.on_send_button
        )
        send_button.grid(row=0, column=1, padx=(5,0))
        send_button.state(["!disabled"])
        self.interface.send_button = send_button
        
        # Progress Bar personalizzata
        style = ttk.Style()
        style.configure(
            "Blue.Horizontal.TProgressbar",
            troughcolor=self.interface.style.lookup('TEntry', 'fieldbackground'),
            background=self.interface.style.lookup('TScrollbar', 'background', default='#0078d7'),
            thickness=8
        )
        
        progress = ttk.Progressbar(
            input_frame,
            mode="indeterminate",
            style="Blue.Horizontal.TProgressbar",
            length=200
        )
        progress.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(8,0))
        progress.grid_remove()
        self.interface.progress = progress 
        
        # Configurazione del menu File e degli altri menù (rimangono invariati)
        menubar = tk.Menu(self.interface.root)
        self.interface.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Model Management", command=self.show_model_management_window)
        file_menu.add_command(label="Exit", command=self.interface.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy All", command=self.interface.copy_all)
        edit_menu.add_command(label="Clear Chat", command=self.interface.clear_chat)
        edit_menu.add_command(label="Save as PDF", command=self.interface.save_as_pdf)
        edit_menu.add_command(label="Save as HTML", command=self.interface.save_as_html)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Source Code", command=self.interface.open_homepage)
        help_menu.add_command(label="Help", command=self.interface.show_help)
        
        settings_button = self.interface.settings_button
        settings_button.grid(row=0, column=2, padx=(5,0))
        settings_button.state(["!disabled"])
        
        input_frame.grid_rowconfigure(1, minsize=30)


    def show_model_management_window(self):
        self.interface.update_host()
        if self.management_window and self.management_window.winfo_exists():
            self.management_window.lift()
            return
        management_window = tk.Toplevel(self.interface.root)
        management_window.title("Model Management")
        screen_width = self.interface.root.winfo_screenwidth()
        screen_height = self.interface.root.winfo_screenheight()
        x = int((screen_width / 2) - (400 / 2))
        y = int((screen_height / 2) - (500 / 2))
        management_window.geometry(f"{400}x{500}+{x}+{y}")
        management_window.grid_columnconfigure(0, weight=1)
        management_window.grid_rowconfigure(3, weight=1)
        frame = ttk.Frame(management_window)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        frame.grid_columnconfigure(0, weight=1)
        model_name_input = ttk.Entry(frame)
        model_name_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        def _download():
            arg = model_name_input.get().strip()
            if arg.startswith("ollama run "):
                arg = arg[11:]
            Thread(target=self.interface.download_model, daemon=True, args=(arg,)).start()
        def _delete():
            arg = models_list.get(tk.ACTIVE).strip()
            Thread(target=self.interface.delete_model, daemon=True, args=(arg,)).start()
        download_button = ttk.Button(frame, text="Download", command=_download)
        download_button.grid(row=0, column=1, sticky="ew")
        tips = tk.Label(frame, text="Find models: https://ollama.com/library", fg="blue", cursor="hand2")
        tips.bind("<Button-1>", lambda e: webbrowser.open("https://ollama.com/library"))
        tips.grid(row=1, column=0, sticky="W", padx=(0, 5), pady=5)
        list_action_frame = ttk.Frame(management_window)
        list_action_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        list_action_frame.grid_columnconfigure(0, weight=1)
        list_action_frame.grid_rowconfigure(0, weight=1)
        models_list = tk.Listbox(list_action_frame)
        models_list.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(list_action_frame, orient="vertical", command=models_list.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        models_list.config(yscrollcommand=scrollbar.set)
        delete_button = ttk.Button(list_action_frame, text="Delete", command=_delete)
        delete_button.grid(row=0, column=2, sticky="ew", padx=(5, 0))
        log_textbox = tk.Text(management_window)
        log_textbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        log_textbox.config(state="disabled")
        self.management_window = management_window
        self.interface.log_textbox = log_textbox
        self.interface.download_button = download_button
        self.interface.delete_button = delete_button
        self.interface.models_list = models_list
        Thread(target=self.interface.update_model_list, daemon=True).start()

if __name__ == "__main__":
    def save_config(host, model):
        try:
            config = ET.Element("config")
            ET.SubElement(config, "host").text = host
            ET.SubElement(config, "model").text = model
            
            tree = ET.ElementTree(config)
            tree.write("config.xml", 
                      encoding="utf-8", 
                      xml_declaration=True)
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def run():
        config = {}
        try:
            tree = ET.parse("config.xml")
            config_root = tree.getroot()
            config = {
                "host": config_root.find("host").text,
                "model": config_root.find("model").text
            }
        except (FileNotFoundError, ET.ParseError):
            print("Configuration not found")
            config = {
                "host": "http://127.0.0.1:11434",
                "model": ""
            }

        root = ThemedTk(theme="arc")
        root.title("Ollama GUI")

        app = OllamaInterface(root, saved_config=config)
        def on_closing(app, root):
            host = app.host_input.get().strip() or "http://127.0.0.1:11434"
            model = app.model_select.get().strip()
            if not model and app.model_select["values"]:
                model = app.model_select["values"][0]
            save_config(host, model)
            root.destroy()        
        app.host_input.delete(0, tk.END)
        app.host_input.insert(0, config["host"])
        
        if config["model"]:
            app.model_select.set(config["model"])

        root.protocol("WM_DELETE_WINDOW", lambda: on_closing(app, root))
        root.mainloop()
        

    run()
