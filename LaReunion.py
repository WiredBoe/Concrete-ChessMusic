import chess
import chess.pgn
import mido
from chessboard import display
import time
import atexit

# Crear un nuevo tablero de ajedrez
board = chess.Board()

# Inicialización del tablero de ajedrez visual
game_board = display.start()

# Abrir el puerto de salida MIDI (ajusta el nombre del puerto según tu configuración)
outport = mido.open_output('UNITY2 2')

# Función para apagar todas las notas
def turn_off_all_notes():
    for note in current_chord_notes:
        msg = mido.Message('note_off', note=note)
        outport.send(msg)

# Registrar la función para que se llame al salir
atexit.register(turn_off_all_notes)

chord_notes = {

    # Acordes mayores
    'CM': [60, 64, 67],  # Do mayor: Do, Mi, Sol
    'DM': [62, 66, 69],  # Re mayor: Re, Fa#, La
    'EM': [64, 68, 71],  # Mi mayor: Mi, Sol#, Si
    'FM': [65, 69, 72],  # Fa mayor: Fa, La, Do
    'GM': [67, 71, 74],  # Sol mayor: Sol, Si, Re
    'AM': [69, 73, 76],  # La mayor: La, Do#, Mi
    'BM': [71, 75, 78],  # Si mayor: Si, Re#, Fa#

    # Acordes menores
    'Dm': [62, 65, 69],    # Re menor: Re, Fa, La
    'Em': [64, 67, 71],    # Mi menor: Mi, Sol, Si
    'Fm': [65, 68, 72],    # Fa menor: Fa, Lab, Do
    'Gm': [67, 70, 74],    # Sol menor: Sol, Si♭, Re
    'Am': [69, 72, 76],    # La menor: La, Do, Mi
    'Bm': [71, 74, 78],    # Si menor: Si, Re, Fa#

    # Acordes mayores con séptima (maj7)
    'Cmaj7': [60, 64, 67, 71],  # Do maj7: Do, Mi, Sol, Si
    'Dmaj7': [62, 66, 69, 73],  # Re maj7: Re, Fa#, La, Do#
    'Emaj7': [64, 68, 71, 75],  # Mi maj7: Mi, Sol#, Si, Re#
    'Fmaj7': [65, 69, 72, 76],  # Fa maj7: Fa, La, Do, Mi
    'Gmaj7': [67, 71, 74, 78],  # Sol maj7: Sol, Si, Re, Fa#
    'Amaj7': [69, 73, 76, 80],  # La maj7: La, Do#, Mi, Sol#
    'Bmaj7': [71, 75, 78, 82],  # Si maj7: Si, Re#, Fa#, La#

    # Acordes de séptima dominante
    'C7': [60, 64, 67, 70],  # Do7: Do, Mi, Sol, Si♭
    'D7': [62, 66, 69, 72],  # Re7: Re, Fa#, La, Do
    'E7': [64, 68, 71, 74],  # Mi7: Mi, Sol#, Si, Re
    'F7': [65, 69, 72, 75],  # Fa7: Fa, La, Do, Mi♭
    'G7': [67, 71, 74, 77],  # Sol7: Sol, Si, Re, Fa
    'A7': [69, 73, 76, 79],  # La7: La, Do#, Mi, Sol
    'B7': [71, 75, 78, 81],  # Si7: Si, Re#, Fa#, La

    # Acordes de sexta mayor
    'C6': [60, 64, 67, 69],  # Do6: Do, Mi, Sol, La
    'D6': [62, 66, 69, 71],  # Re6: Re, Fa#, La, Si
    'E6': [64, 68, 71, 73],  # Mi6: Mi, Sol#, Si, Re
    'F6': [65, 69, 72, 74],  # Fa6: Fa, La, Do, Re
    'G6': [67, 71, 74, 76],  # Sol6: Sol, Si, Re, Mi
    'A6': [69, 73, 76, 78],  # La6: La, Do#, Mi, Fa#
    'B6': [71, 75, 78, 80],  # Si6: Si, Re#, Fa#, Sol#

    # Acordes aumentados 
    'Caug': [60, 64, 68],  # Do aumentado: Do, Mi, Sol#
    'Daug': [62, 66, 70],  # Re aumentado: Re, Fa#, La
    'Eaug': [64, 68, 72],  # Mi aumentado: Mi, Sol#, Si
    'Faug': [65, 69, 73],  # Fa aumentado: Fa, La, Do#
    'Gaug': [67, 71, 75],  # Sol aumentado: Sol, Si, Re#
    'Aaug': [69, 73, 77],  # La aumentado: La, Do#, Mi
    'Baug': [71, 75, 79],  # Si aumentado: Si, Re#, Fa#

    # Acordes sus4
    'Csus4': [60, 65, 67],  # Do sus4: Do, Fa, Sol
    'Dsus4': [62, 67, 69],  # Re sus4: Re, Sol, La
    'Esus4': [64, 69, 71],  # Mi sus4: Mi, La, Si
    'Fsus4': [65, 70, 72],  # Fa sus4: Fa, Si♭, Do
    'Gsus4': [67, 72, 74],  # Sol sus4: Sol, Do, Re
    'Asus4': [69, 74, 76],  # La sus4: La, Re, Mi
    'Bsus4': [71, 76, 78],  # Si sus4: Si, Mi, Fa#
}

# Asignar acordes a las casillas del tablero
square_chords_mapping = {
    chess.A8: 'G7',
    chess.B8: 'A7',
    chess.C8: 'B7',
    chess.D8: 'C7',
    chess.E8: 'D7',
    chess.F8: 'E7',
    chess.G8: 'F7',
    chess.H8: 'G/',
    chess.A7: 'Dm',
    chess.B7: 'Em',
    chess.C7: 'Fm',
    chess.D7: 'Gm',
    chess.E7: 'Am',
    chess.F7: 'Bm',
    chess.G7: 'Cm',
    chess.H7: 'Dm',
    chess.A6: 'F6',
    chess.B6: 'G6',
    chess.C6: 'A6',
    chess.D6: 'B6',
    chess.E6: 'C6',
    chess.F6: 'D6',
    chess.G6: 'E6',
    chess.H6: 'F6',
    chess.A5: 'Cmaj7',
    chess.B5: 'Dmaj7',
    chess.C5: 'Emaj7',
    chess.D5: 'Fmaj7',
    chess.E5: 'Gmaj7',
    chess.F5: 'Amaj7',
    chess.G5: 'Bmaj7',
    chess.H5: 'Cmaj7',
    chess.A4: 'CM',
    chess.B4: 'DM',
    chess.C4: 'EM',
    chess.D4: 'FM',
    chess.E4: 'GM',
    chess.F4: 'AM',
    chess.G4: 'BM',
    chess.H4: 'CM',
    chess.A3: 'Fsus4',
    chess.B3: 'Gsus4',
    chess.C3: 'Asus4',
    chess.D3: 'Bsus4',
    chess.E3: 'Csus4',
    chess.F3: 'Esus4',
    chess.G3: 'Fsus4',
    chess.H3: 'Gsus4',
    chess.A2: 'Dm',
    chess.B2: 'Em',
    chess.C2: 'Fm',
    chess.D2: 'Gm',
    chess.E2: 'Am',
    chess.F2: 'Bm',
    chess.G2: 'Cm',
    chess.H2: 'Dm',
    chess.A1: 'Gaug',
    chess.B1: 'Aaug',
    chess.C1: 'Baug',
    chess.D1: 'Caug',
    chess.E1: 'Daug',
    chess.F1: 'Faug',
    chess.G1: 'Gaug',
    chess.H1: 'Aaug',
}

# Mantén un registro del acorde actual
current_chord_notes = []

def send_midi_on_move(move):
    global current_chord_notes

    # Apagar las notas del acorde actual
    for note in current_chord_notes:
        msg = mido.Message('note_off', note=note)
        outport.send(msg)

    # Limpiar la lista de notas del acorde actual
    current_chord_notes.clear()

    dest_square = move.to_square
    chord_name = square_chords_mapping.get(dest_square, 'CMaj')  # Acorde predeterminado si no se encuentra la casilla

    # Obtener las notas MIDI del acorde
    chord_notes_list = chord_notes.get(chord_name, [])

    # Enviar un mensaje MIDI para cada nota del acorde
    for note in chord_notes_list:
        msg = mido.Message('note_on', note=note)
        outport.send(msg)

        # Agregar la nota al acorde actual
        current_chord_notes.append(note)

# Cargar un archivo PGN (ajusta la ruta del archivo según su ubicación)
pgn_file = 'morphy_duke_karl_count_isouard_1858.pgn'
with open(pgn_file) as pgn:
    game = chess.pgn.read_game(pgn)
    moves = list(game.mainline_moves())

# Jugar los movimientos desde el archivo PGN
for move in moves:
    # Verificar si el movimiento es legal
    if move in board.legal_moves:
        board.push(move)

        # Enviar un mensaje MIDI
        send_midi_on_move(move)
        print(f"Enviando acorde MIDI para el movimiento: {move}")

        # Actualizar la posición del tablero visual
        display.update(board.fen(), game_board)

        # Esperar 5 segundos
        time.sleep(2)