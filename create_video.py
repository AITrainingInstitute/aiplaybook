#!/usr/bin/env python3
"""
AI Playbook für Digitales Marketing - Professionelles Werbevideo Generator
============================================================================
Erstellt ein hochprofessionelles Werbevideo mit:
- Deutscher Sprachausgabe (gTTS oder ElevenLabs)
- Dynamischen Textanimationen
- Professioneller Hintergrundmusik
- Cinematischen Übergängen
"""

import os
import sys
import math
import tempfile
from pathlib import Path

# Video/Audio Libraries
from moviepy import *
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, FadeIn, FadeOut
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Text-to-Speech
from gtts import gTTS

# ============================================================================
# KONFIGURATION
# ============================================================================

VIDEO_CONFIG = {
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "output_file": "ai_playbook_werbevideo.mp4"
}

# Farbpalette (Modern & Professional)
COLORS = {
    "primary": "#0066FF",      # Brillantes Blau
    "secondary": "#00D4AA",    # Türkis/Mint
    "accent": "#FF6B35",       # Orange Akzent
    "dark": "#0A1628",         # Dunkles Navy
    "light": "#FFFFFF",        # Weiß
    "gradient_start": "#667eea",
    "gradient_end": "#764ba2"
}

# ============================================================================
# SKRIPT FÜR DAS VIDEO
# ============================================================================

SCRIPT_SECTIONS = [
    {
        "id": "hook",
        "text": "Die Zukunft des Marketings ist hier. Und sie wird von künstlicher Intelligenz angetrieben.",
        "duration": 5,
        "visual": "opening",
        "title": None
    },
    {
        "id": "problem",
        "text": "Jeden Tag kämpfen Marketing-Teams mit den gleichen Herausforderungen: Zu viele Kanäle, zu wenig Zeit, und der ständige Druck, mehr Ergebnisse zu liefern.",
        "duration": 7,
        "visual": "problem",
        "title": "DAS PROBLEM"
    },
    {
        "id": "solution_intro",
        "text": "Doch was wäre, wenn es einen besseren Weg gäbe? Einen Weg, der Ihre Produktivität verdreifacht und Ihre Ergebnisse revolutioniert?",
        "duration": 6,
        "visual": "transition",
        "title": None
    },
    {
        "id": "product",
        "text": "Willkommen beim AI Playbook für Digitales Marketing. Ihr ultimativer Leitfaden, um KI in Ihre Marketing-Strategie zu integrieren.",
        "duration": 7,
        "visual": "product_reveal",
        "title": "AI PLAYBOOK"
    },
    {
        "id": "feature1",
        "text": "Lernen Sie, wie Sie KI-Tools wie ChatGPT, Midjourney und Claude nutzen, um in Minuten Content zu erstellen, der sonst Stunden dauern würde.",
        "duration": 7,
        "visual": "feature",
        "title": "CONTENT CREATION"
    },
    {
        "id": "feature2",
        "text": "Entdecken Sie automatisierte Kampagnen-Optimierung, die Ihre Werbeausgaben um bis zu 40 Prozent effizienter macht.",
        "duration": 6,
        "visual": "feature",
        "title": "KAMPAGNEN"
    },
    {
        "id": "feature3",
        "text": "Nutzen Sie prädiktive Analysen, um Trends vorherzusagen, bevor sie passieren, und Ihren Wettbewerbern immer einen Schritt voraus zu sein.",
        "duration": 7,
        "visual": "feature",
        "title": "ANALYTICS"
    },
    {
        "id": "benefits",
        "text": "Das Ergebnis? Mehr Zeit für Strategie, bessere Ergebnisse, und ein Marketing-Team, das die Zukunft gestaltet.",
        "duration": 6,
        "visual": "benefits",
        "title": "IHR VORTEIL"
    },
    {
        "id": "cta",
        "text": "AI Playbook für Digitales Marketing. Transformieren Sie Ihr Marketing. Heute.",
        "duration": 5,
        "visual": "cta",
        "title": None
    }
]

# ============================================================================
# HILFSFUNKTIONEN
# ============================================================================

def hex_to_rgb(hex_color):
    """Konvertiert Hex-Farbe zu RGB-Tupel"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_frame(width, height, color1, color2, direction='diagonal'):
    """Erstellt einen Gradient-Hintergrund"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)

    for y in range(height):
        for x in range(width):
            if direction == 'diagonal':
                ratio = (x + y) / (width + height)
            elif direction == 'horizontal':
                ratio = x / width
            else:  # vertical
                ratio = y / height

            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)

            draw.point((x, y), fill=(r, g, b))

    return np.array(img)

def create_text_image(text, width, height, font_size=60, color="white",
                      bg_color=None, align="center", y_position=0.5):
    """Erstellt ein Bild mit Text"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Versuche verschiedene Schriftarten
    font = None
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, font_size)
                break
            except:
                continue

    if font is None:
        font = ImageFont.load_default()

    # Text-Wrapping
    words = text.split()
    lines = []
    current_line = []
    max_width = width - 200

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    # Berechne Gesamthöhe
    line_height = font_size + 10
    total_height = len(lines) * line_height

    # Zeichne Text
    y = int(height * y_position) - total_height // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]

        if align == "center":
            x = (width - text_width) // 2
        elif align == "left":
            x = 100
        else:
            x = width - text_width - 100

        # Schatten für bessere Lesbarkeit
        draw.text((x+3, y+3), line, font=font, fill=(0, 0, 0, 180))
        draw.text((x, y), line, font=font, fill=color)

        y += line_height

    return np.array(img)

def create_animated_background(duration, fps, width, height):
    """Erstellt einen animierten Gradient-Hintergrund"""

    def make_frame(t):
        # Animierter Gradient mit Pulsieren
        phase = math.sin(t * 0.5) * 0.1 + 0.5

        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Basis-Farben
        r1, g1, b1 = hex_to_rgb(COLORS["dark"])
        r2, g2, b2 = hex_to_rgb(COLORS["primary"])

        for y in range(height):
            ratio = y / height
            ratio = ratio * (1 - phase) + phase * (1 - ratio)

            r = int(r1 + (r2 - r1) * ratio * 0.3)
            g = int(g1 + (g2 - g1) * ratio * 0.3)
            b = int(b1 + (b2 - b1) * ratio * 0.5)

            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Füge subtile Partikel/Glühen hinzu
        num_particles = 20
        for i in range(num_particles):
            px = int((math.sin(t * 0.3 + i * 0.5) * 0.5 + 0.5) * width)
            py = int((math.cos(t * 0.2 + i * 0.7) * 0.5 + 0.5) * height)
            size = int(5 + math.sin(t + i) * 3)

            for dx in range(-size, size+1):
                for dy in range(-size, size+1):
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist <= size and 0 <= px+dx < width and 0 <= py+dy < height:
                        alpha = (1 - dist/size) * 0.3
                        x, y = px+dx, py+dy
                        old = img.getpixel((x, y))
                        new_r = min(255, int(old[0] + 100 * alpha))
                        new_g = min(255, int(old[1] + 150 * alpha))
                        new_b = min(255, int(old[2] + 255 * alpha))
                        draw.point((x, y), fill=(new_r, new_g, new_b))

        return np.array(img)

    return VideoClip(make_frame, duration=duration).with_fps(fps)

def create_title_card(title, subtitle=None, duration=3, width=1920, height=1080):
    """Erstellt eine animierte Titelkarte"""

    def make_frame(t):
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Fade-in Effekt
        alpha = min(1, t * 2) * 255

        # Lade Schriftart
        font = None
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]

        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, 80)
                    font_small = ImageFont.truetype(path, 40)
                    break
                except:
                    continue

        if font is None:
            font = ImageFont.load_default()
            font_small = font

        # Animierter Einflug von links
        slide_offset = max(0, (1 - t * 3)) * 200

        # Titel
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2 - int(slide_offset)
        y = height // 2 - 50

        # Glow-Effekt
        for offset in range(5, 0, -1):
            glow_alpha = int(alpha * 0.1)
            color = (hex_to_rgb(COLORS["primary"])[0],
                    hex_to_rgb(COLORS["primary"])[1],
                    hex_to_rgb(COLORS["primary"])[2],
                    glow_alpha)
            draw.text((x+offset, y+offset), title, font=font, fill=color)

        draw.text((x, y), title, font=font, fill=(255, 255, 255, int(alpha)))

        # Untertitel
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=font_small)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2 + int(slide_offset * 0.5)
            y = height // 2 + 60

            color_rgb = hex_to_rgb(COLORS["secondary"])
            draw.text((x, y), subtitle, font=font_small,
                     fill=(color_rgb[0], color_rgb[1], color_rgb[2], int(alpha * 0.9)))

        # Dekorative Linie
        line_width = int(min(text_width + 100, (t * 500)))
        line_x = (width - line_width) // 2
        line_y = height // 2 + 30

        color_rgb = hex_to_rgb(COLORS["accent"])
        draw.rectangle([line_x, line_y, line_x + line_width, line_y + 4],
                      fill=(color_rgb[0], color_rgb[1], color_rgb[2], int(alpha)))

        return np.array(img)

    return VideoClip(make_frame, duration=duration).with_fps(30)

def create_feature_icon(icon_type, size=200):
    """Erstellt ein animiertes Feature-Icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2
    color = hex_to_rgb(COLORS["secondary"])

    if icon_type == "content":
        # Dokument-Icon
        draw.rectangle([size//4, size//6, size*3//4, size*5//6],
                      outline=(*color, 255), width=4)
        for i in range(3):
            y = size//3 + i * (size//6)
            draw.line([size//3, y, size*2//3, y], fill=(*color, 200), width=2)

    elif icon_type == "campaign":
        # Rakete/Pfeil Icon
        points = [
            (center, size//6),
            (size*3//4, size*2//3),
            (center, size//2),
            (size//4, size*2//3)
        ]
        draw.polygon(points, outline=(*color, 255), width=3)
        draw.line([center, size//2, center, size*5//6], fill=(*color, 255), width=4)

    elif icon_type == "analytics":
        # Chart Icon
        points = [
            (size//6, size*3//4),
            (size//3, size//2),
            (size//2, size*2//3),
            (size*2//3, size//4),
            (size*5//6, size//3)
        ]
        draw.line(points, fill=(*color, 255), width=4)
        for p in points:
            draw.ellipse([p[0]-8, p[1]-8, p[0]+8, p[1]+8], fill=(*color, 255))

    return np.array(img)

# ============================================================================
# AUDIO-FUNKTIONEN
# ============================================================================

def create_voiceover(sections, output_dir):
    """Erstellt die Sprachausgabe für alle Sektionen"""
    audio_files = []

    print("🎙️  Erstelle Sprachausgabe...")

    for i, section in enumerate(sections):
        filename = os.path.join(output_dir, f"voice_{i:02d}_{section['id']}.mp3")

        print(f"   Generiere: {section['id']}")

        # Google Text-to-Speech (kostenlos)
        tts = gTTS(text=section['text'], lang='de', slow=False)
        tts.save(filename)

        audio_files.append({
            "file": filename,
            "section": section
        })

    return audio_files

def create_background_music(duration, output_file, sample_rate=44100):
    """
    Erstellt eine einfache, professionelle Ambient-Hintergrundmusik
    mit sanften Synthesizer-Tönen
    """
    print("🎵 Erstelle Hintergrundmusik...")

    # Erzeuge eine sanfte, inspirierende Melodie
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Basis-Frequenzen (D-Dur Akkord-Progression)
    frequencies = [
        (146.83, 0.3),   # D3
        (220.00, 0.2),   # A3
        (293.66, 0.25),  # D4
        (369.99, 0.15),  # F#4
    ]

    music = np.zeros_like(t)

    for freq, amp in frequencies:
        # Leicht verstimmte Oszillatoren für Wärme
        wave1 = np.sin(2 * np.pi * freq * t) * amp
        wave2 = np.sin(2 * np.pi * freq * 1.003 * t) * amp * 0.5
        wave3 = np.sin(2 * np.pi * freq * 0.997 * t) * amp * 0.5

        music += wave1 + wave2 + wave3

    # Füge subtile Modulation hinzu
    lfo = np.sin(2 * np.pi * 0.1 * t) * 0.1 + 1
    music = music * lfo

    # Soft Attack/Release Envelope
    attack_samples = int(3 * sample_rate)
    release_samples = int(3 * sample_rate)

    envelope = np.ones_like(t)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    envelope[-release_samples:] = np.linspace(1, 0, release_samples)

    music = music * envelope

    # Normalisieren und auf niedrige Lautstärke setzen (für Hintergrund)
    music = music / np.max(np.abs(music)) * 0.15

    # Konvertiere zu Audio
    from moviepy import AudioClip

    def make_frame(t_arr):
        indices = (np.array(t_arr) * sample_rate).astype(int)
        indices = np.clip(indices, 0, len(music) - 1)
        return music[indices].reshape(-1, 1)

    audio = AudioClip(make_frame, duration=duration, fps=sample_rate)
    audio.write_audiofile(output_file, fps=sample_rate, logger=None)

    return output_file

# ============================================================================
# HAUPTVIDEO-ERSTELLUNG
# ============================================================================

def create_section_clip(section, voice_audio, width, height, fps):
    """Erstellt einen Video-Clip für eine Sektion"""

    # Hole die tatsächliche Dauer vom Audio
    audio_clip = AudioFileClip(voice_audio)
    duration = audio_clip.duration + 1.0  # +1 Sekunde Puffer

    # Erstelle Hintergrund
    bg = create_animated_background(duration, fps, width, height)

    clips = [bg]

    # Titel-Overlay (falls vorhanden)
    if section.get('title'):
        title_overlay = create_title_card(
            section['title'],
            duration=duration,
            width=width,
            height=height
        ).with_position(('center', 150))
        clips.append(title_overlay)

    # Text-Overlay mit dem gesprochenen Text
    text_img = create_text_image(
        section['text'],
        width, height,
        font_size=50,
        color="white",
        y_position=0.65
    )

    # Animierter Text-Einblendung
    def text_frame(t):
        alpha = min(1, t * 2)  # Fade in
        if t > duration - 0.5:
            alpha = max(0, (duration - t) * 2)  # Fade out

        result = text_img.copy()
        result[:, :, 3] = (result[:, :, 3] * alpha).astype(np.uint8)
        return result

    text_clip = VideoClip(text_frame, duration=duration).with_fps(fps)
    clips.append(text_clip)

    # Kombiniere Clips
    video = CompositeVideoClip(clips, size=(width, height))

    # Füge Audio hinzu
    video = video.with_audio(audio_clip)

    return video

def create_intro_clip(width, height, fps, duration=3):
    """Erstellt einen dramatischen Intro-Clip"""

    def make_frame(t):
        img = Image.new('RGB', (width, height), hex_to_rgb(COLORS["dark"]))
        draw = ImageDraw.Draw(img)

        # Animierter Kreis, der sich ausbreitet
        radius = int(t / duration * max(width, height))
        center = (width // 2, height // 2)

        # Gradient im Kreis
        for r in range(radius, max(0, radius - 100), -1):
            alpha = (radius - r) / 100
            color_rgb = hex_to_rgb(COLORS["primary"])
            color = (
                int(color_rgb[0] * alpha * 0.3),
                int(color_rgb[1] * alpha * 0.3),
                int(color_rgb[2] * alpha * 0.5)
            )
            draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r],
                        outline=color, width=2)

        # Logo/Text Einblendung
        if t > 1:
            font = None
            for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
                if os.path.exists(path):
                    try:
                        font = ImageFont.truetype(path, 100)
                        break
                    except:
                        continue

            if font:
                text = "AI PLAYBOOK"
                alpha = min(1, (t - 1) * 2)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                y = height // 2 - 50

                color_rgb = hex_to_rgb(COLORS["light"])
                draw.text((x, y), text, font=font,
                         fill=(int(color_rgb[0]*alpha),
                               int(color_rgb[1]*alpha),
                               int(color_rgb[2]*alpha)))

        return np.array(img)

    return VideoClip(make_frame, duration=duration).with_fps(fps)

def create_outro_clip(width, height, fps, duration=4):
    """Erstellt einen professionellen Outro-Clip mit Call-to-Action"""

    def make_frame(t):
        img = Image.new('RGB', (width, height), hex_to_rgb(COLORS["dark"]))
        draw = ImageDraw.Draw(img)

        # Gradient-Overlay
        for y in range(height):
            ratio = y / height
            r, g, b = hex_to_rgb(COLORS["primary"])
            color = (
                int(r * ratio * 0.3),
                int(g * ratio * 0.3),
                int(b * ratio * 0.5)
            )
            draw.line([(0, y), (width, y)], fill=color)

        # Lade Schriftarten
        font_large = None
        font_medium = None
        for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
            if os.path.exists(path):
                try:
                    font_large = ImageFont.truetype(path, 80)
                    font_medium = ImageFont.truetype(path, 40)
                    break
                except:
                    continue

        alpha = min(1, t * 2)

        # Haupttext
        if font_large:
            text = "AI PLAYBOOK"
            bbox = draw.textbbox((0, 0), text, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height // 3

            draw.text((x, y), text, font=font_large,
                     fill=(int(255*alpha), int(255*alpha), int(255*alpha)))

        if font_medium:
            # Untertitel
            subtitle = "für Digitales Marketing"
            bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height // 3 + 100

            color_rgb = hex_to_rgb(COLORS["secondary"])
            draw.text((x, y), subtitle, font=font_medium,
                     fill=(int(color_rgb[0]*alpha),
                           int(color_rgb[1]*alpha),
                           int(color_rgb[2]*alpha)))

            # CTA
            if t > 1.5:
                cta_alpha = min(1, (t - 1.5) * 2)
                cta = "Jetzt starten →"
                bbox = draw.textbbox((0, 0), cta, font=font_medium)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                y = height * 2 // 3

                # Button-Hintergrund
                padding = 30
                btn_rect = [x - padding, y - padding//2,
                           x + text_width + padding, y + 50 + padding//2]

                color_rgb = hex_to_rgb(COLORS["accent"])
                draw.rounded_rectangle(btn_rect, radius=10,
                    fill=(int(color_rgb[0]*cta_alpha),
                          int(color_rgb[1]*cta_alpha),
                          int(color_rgb[2]*cta_alpha)))

                draw.text((x, y), cta, font=font_medium,
                         fill=(int(255*cta_alpha), int(255*cta_alpha), int(255*cta_alpha)))

        return np.array(img)

    return VideoClip(make_frame, duration=duration).with_fps(fps)

def main():
    """Hauptfunktion - Erstellt das komplette Werbevideo"""

    print("=" * 60)
    print("🎬 AI PLAYBOOK - WERBEVIDEO GENERATOR")
    print("=" * 60)

    # Erstelle temporäres Verzeichnis
    work_dir = Path(tempfile.mkdtemp(prefix="ai_playbook_video_"))
    output_dir = Path("/home/user/aiplaybook")

    print(f"\n📁 Arbeitsverzeichnis: {work_dir}")
    print(f"📁 Ausgabeverzeichnis: {output_dir}")

    width = VIDEO_CONFIG["width"]
    height = VIDEO_CONFIG["height"]
    fps = VIDEO_CONFIG["fps"]

    # Schritt 1: Erstelle Sprachausgabe
    print("\n" + "=" * 40)
    print("SCHRITT 1: Sprachausgabe erstellen")
    print("=" * 40)

    audio_files = create_voiceover(SCRIPT_SECTIONS, str(work_dir))

    # Schritt 2: Erstelle Hintergrundmusik
    print("\n" + "=" * 40)
    print("SCHRITT 2: Hintergrundmusik erstellen")
    print("=" * 40)

    # Berechne Gesamtdauer
    total_duration = 3  # Intro
    for af in audio_files:
        clip = AudioFileClip(af["file"])
        total_duration += clip.duration + 1.5
        clip.close()
    total_duration += 4  # Outro

    music_file = str(work_dir / "background_music.mp3")
    create_background_music(total_duration, music_file)

    # Schritt 3: Erstelle Video-Clips
    print("\n" + "=" * 40)
    print("SCHRITT 3: Video-Clips erstellen")
    print("=" * 40)

    clips = []

    # Intro
    print("   Erstelle Intro...")
    intro = create_intro_clip(width, height, fps, duration=3)
    clips.append(intro)

    # Haupt-Sektionen
    for i, af in enumerate(audio_files):
        print(f"   Erstelle Sektion {i+1}/{len(audio_files)}: {af['section']['id']}")
        clip = create_section_clip(
            af['section'],
            af['file'],
            width, height, fps
        )
        clips.append(clip)

    # Outro
    print("   Erstelle Outro...")
    outro = create_outro_clip(width, height, fps, duration=4)
    clips.append(outro)

    # Schritt 4: Kombiniere alles
    print("\n" + "=" * 40)
    print("SCHRITT 4: Video zusammenstellen")
    print("=" * 40)

    print("   Füge Clips zusammen...")
    final_video = concatenate_videoclips(clips, method="compose")

    # Füge Hintergrundmusik hinzu
    print("   Füge Hintergrundmusik hinzu...")
    bg_music = AudioFileClip(music_file).with_effects([
        afx.AudioFadeIn(2),
        afx.AudioFadeOut(3)
    ])

    # Mische Audio
    if final_video.audio:
        final_audio = CompositeAudioClip([
            bg_music.with_volume_scaled(0.3),
            final_video.audio.with_volume_scaled(1.0)
        ])
        final_video = final_video.with_audio(final_audio)
    else:
        final_video = final_video.with_audio(bg_music)

    # Schritt 5: Rendere finales Video
    print("\n" + "=" * 40)
    print("SCHRITT 5: Video rendern")
    print("=" * 40)

    output_file = str(output_dir / VIDEO_CONFIG["output_file"])

    print(f"   Ausgabedatei: {output_file}")
    print("   Rendering läuft... (Dies kann einige Minuten dauern)")

    final_video.write_videofile(
        output_file,
        fps=fps,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile=str(work_dir / "temp_audio.m4a"),
        remove_temp=True,
        threads=4,
        preset='medium',
        bitrate='8000k',
        logger='bar'
    )

    # Aufräumen
    final_video.close()
    for clip in clips:
        clip.close()

    print("\n" + "=" * 60)
    print("✅ VIDEO ERFOLGREICH ERSTELLT!")
    print("=" * 60)
    print(f"\n📹 Ausgabedatei: {output_file}")
    print(f"⏱️  Dauer: ~{int(total_duration)} Sekunden")
    print(f"📐 Auflösung: {width}x{height}")
    print(f"🎞️  FPS: {fps}")

    return output_file

if __name__ == "__main__":
    main()
