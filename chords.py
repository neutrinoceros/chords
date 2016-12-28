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


def imposedlenght(message, l) :
    if len(message) >= l :
        return message[0:l]
    else :
        longer = message
        while len(longer) < l :
            longer += ' '
        return longer
        
class Note :
    def __init__(self, num=0) :
        self._num   = num
        self._label = NOTES[num%12]
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
    def __init__(self, seed=Note(4)) :
        self._seed   = seed
        self._spaces = [0,5,10,15,19,24]
        self._notes  = [seed + s for s in self._spaces]
        
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
        self._seed   = seed
        self._tuning = Tuning(seed)
        self._frets  = frets

    def __repr__(self) :
        return '\n'.join([(self._tuning+n).__repr__() for n in range(self._frets)])
        

class Gamme(Scale) : #only major
    def __init__(self, seed=Note(4), frets=12, intervals=['uni/oct']) :
        Scale.__init__(self, seed,frets)
        self._intervals = intervals
        
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

majeure = Gamme(seed=Note(0),intervals=['uni/oct', '3rd maj', '5th per'])
print majeure
