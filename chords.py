import numpy as np

from termcolor import colored, cprint

INTERVALS = ['uni/oct',
             '2nd min',
             '2nd maj',
             '3rd min',
             '3rd maj',
             '4th per',
             '5th dim', #aka 4th aug
             '5th per',
             '5th aug',
             '6th maj',
             '7th min',
             '7th maj']

#whites are of type char
#blacks are of type tuple because they have two names each
NOTES = ['C',
         ('C#','Db'),
         'D',
         ('D#','Eb'),
         'E',
         'F',
         ('F#','Gb'),
         'G',
         ('G#','Ab'),
         'A',
         ('A#','Bb'),
         'B']

MODES = {'maj' : ['uni/oct', '3rd maj', '5th per'],
         'min' : ['uni/oct', '3rd min', '5th per']}

def imposedlenght(message, l) :
    if len(message) >= l :
        return message[0:l]
    else :
        longer = message
        while len(longer) < l :
            longer += ' '
        return longer

def getfonda(key) :
    if key[1] in '#b' :
        return Note(key[0:2])
    else :
        return Note(key[0])

def getmode(key) :
    if key[1] in '#b' :
        return key[2:]
    else :
        return key[1:]

def _initnum(num) :
    label = NOTES[num%12]
    return label

def _initlab(label) :
    try :
        num = NOTES.index(label)
    except ValueError :
        for l in NOTES :
            if label in l :
                num = NOTES.index(l)
    finally :
        return num

    
class Note :
    def __init__(self, arg) :
        if   type(arg) == int :
            self._num, self._label = arg, _initnum(arg) 
        elif type(arg) == str :
            self._label, self._num = arg, _initlab(arg) 
        if type(self._label) == tuple :
            self._color = 'black'
        else :
            self._color = 'white'
            
    def __iadd__(self, N) :
        #n in half tones
        return Note(self._num+N)
        
    def __add__(self, N) :
        new =  Note(self._num)
        new += N
        return new

    def __repr__(self) :
        if self._color == 'black' :
            return self._label[0]
        else :
            return self._label

    def delta(self, note) :
        return (note._num - self._num)

    
class Tuning :
    def __init__(self, seed) :
        if isinstance(seed, Note) :
            self._seed = seed
        elif type(seed) in [int,str] :
            self._seed = Note(seed)
        else :
            raise TypeError
        self._spaces = [0,5,10,15,19,24] #guitar only
        self._notes  = [self._seed + s for s in self._spaces]
        
    def __repr__(self) :
        return ' '.join([imposedlenght((self._seed+n).__repr__(), 3) for n in self._spaces])

    def __iadd__(self, N) :
        #n in half tones
        return Tuning(self._seed+N)

    def __add__(self, N) :
        new =  Tuning(self._seed)
        new += N
        return new


class Scale :
    def __init__(self, seed=Note(4), frets=12) :
        if isinstance(seed, Note) :
            self._seed = seed
        elif type(seed) in [int,str] :
            self._seed = Note(seed)
        else :
            raise TypeError
        self._tuning = Tuning(self._seed)
        self._frets  = frets

    def __repr__(self) :
        return '\n'.join([(self._tuning+n).__repr__() for n in range(self._frets)])
        

class Gamme(Scale) :
    def __init__(self, key='Cmaj') :
        self._fonda = getfonda(key)
        self._mode  = getmode(key)
        Scale.__init__(self, self._fonda)
        self._intervals = MODES[self._mode]
    
    def __repr__(self) :
        clines = []
        for n in range(self._frets) :
            notes  = (self._tuning+n)._notes
            colors = ['red' if INTERVALS[(self._seed.delta(n))%12] in self._intervals else 'white' for n in notes]
            clines.append(' '.join([colored(imposedlenght(n.__repr__(),3),c) for n,c in zip(notes, colors)]))
        return '\n'.join(clines)
            
        
class Chord :
    def __init__(self) :
        pass


# script
# ---------------------------------------
a=Note(5)
print a
print Note('D#')
print Tuning('D#')
print Scale(Note(4))
print Gamme("Cmaj")
print "\n\nBbmin\n"
print Gamme("Bbmin")
