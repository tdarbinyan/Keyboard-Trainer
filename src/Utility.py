import os

class Utility:
  
  # -------------------- utility for easy access to files --------------------
  def get_file(path):
      script_dir = os.path.dirname(os.path.abspath(__file__))
      file_path = os.path.join(script_dir, path)
      return file_path

  # -------------------- constants --------------------
  keyboard_layout = "1234567890qwertyuiopasdfghjklzxcvbnm"

  positions = {
              "1": 0,
              "2": 1,
              "3": 2,
              "4": 3,
              "5": 4,
              "6": 5,
              "7": 6,
              "8": 7,
              "9": 8,
              "0": 9,
              "q": 10,
              "w": 11,
              "e": 12,
              "r": 13,
              "t": 14,
              "y": 15,
              "u": 16,
              "i": 17,
              "o": 18,
              "p": 19,
              "a": 20,
              "s": 21,
              "d": 22,
              "f": 23,
              "g": 24,
              "h": 25,
              "j": 26,
              "k": 27,
              "l": 28,
              "z": 31,
              "x": 32,
              "c": 33,
              "v": 34,
              "b": 35,
              "n": 36,
              "m": 37,
          }