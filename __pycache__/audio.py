import os
import math
import wave
import struct
import random

# Cria a estrutura de pastas 'assets/sons/' caso não exista
os.makedirs("assets/sons", exist_ok=True)


def criar_wav(caminho, duracao, gerador_onda, sample_rate=22050):
    num_samples = int(sample_rate * duracao)
    with wave.open(caminho, "w") as f:
        f.setnchannels(1)       # Mono
        f.setsampwidth(2)        # 16-bit (2 bytes por sample)
        f.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = i / sample_rate
            val = gerador_onda(t, duracao)
            # Normalização para evitar distorção clipping
            val = max(-1.0, min(1.0, val))
            sample = int(val * 32767)
            f.writeframes(struct.pack("<h", sample))


# 1. Som do Tiro (Laser Retro - Glissando Descendente)
def onda_tiro(t, dur):
    freq = 800 - (t / dur) * 600
    env = 1.0 - (t / dur)
    return math.sin(2 * math.pi * freq * t) * env


# 2. Som da Explosão (Ruído Branco + Grave)
def onda_explosao(t, dur):
    env = (1.0 - (t / dur)) ** 2
    ruido = random.uniform(-1.0, 1.0)
    freq = 150 - (t / dur) * 100
    return (ruido * 0.7 + math.sin(2 * math.pi * freq * t) * 0.3) * env


# 3. Som do Item (Power-up / Vida - Glissando Ascendente)
def onda_item(t, dur):
    freq = 400 + (t / dur) * 800
    env = 1.0 - (t / dur)
    return math.sin(2 * math.pi * freq * t) * env


# 4. Trilha de Fundo (Melodia Synthwave 8-bit com Baixo)
def onda_musica(t, dur):
    # Arpejo retro em A menor (A3, C4, E4, G4)
    notas = [220.0, 261.63, 329.63, 392.00, 329.63, 261.63]
    idx = int((t * 6) % len(notas))
    freq = notas[idx]
    
    # Onda quadrada retro + linha de baixo em sub-oitava
    base = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
    baixo = math.sin(2 * math.pi * 110.0 * t)
    
    return (base * 0.15 + baixo * 0.25)


# EJECUÇÃO DO GERADOR
print("Gerando arquivos de áudio retro...")

criar_wav("assets/sons/tiro.wav", 0.15, onda_tiro)
criar_wav("assets/sons/explosao.wav", 0.40, onda_explosao)
criar_wav("assets/sons/item.wav", 0.25, onda_item)
criar_wav("assets/sons/musica.wav", 8.00, onda_musica)

print("Sucesso! Todos os 4 arquivos de áudio (.wav) foram criados em 'assets/sons/'.")