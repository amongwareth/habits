import time
import numpy as np
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class BaseMemoryObject:
    '''
    base class that fixes some of the interface
    ===========================================
        - binary numbers
        - regular numbers
        - faces
        - poems
        - texts
        - cards
        - new palace memory
        - numbers with meaning (physical / eco / geo etc)
        - dates
        - words foreign language

        Abstractions :
        object of memory containing an iterable to remember, a way to test the memory, a way to present the iterable for memory
        a type, to code for the fact that the order matters or not
        a way to build the iterable that is deterministic yet random

        store in db the seed of the object in order to avoid storing the proper object
        MongoDB?
    '''

    def __init__(self):
        '''
        Attributes :
        -----------
        _components : the iterable containing the actual data to be remebered
        _stride : an integer controlling how many items are shown at the same time
        _length : fixes how long is the iterable when the builder method is called
        _order : boolean storing whether the order matters (long sequence of numbers) or not (faces)
        '''
        self._components = None
        self._stride = None
        self._order = None
        self._length = None

    def store_in_db(self):
        '''
        method used to store in db the seed for recreating the object
        '''
        raise NotImplementedError

    def iterable_builder(self):
        '''
        method used to generate one iterable for this particular instance
        '''
        raise NotImplementedError

    def learning_generator(self):
        '''
        method used to present the information during the learning phase
        '''
        raise NotImplementedError

    def testing_generator(self):
        '''
        method used to present partial information to test the user
        '''
        raise NotImplementedError

    def test_evaluation(self):
        '''
        method used to compared the answer of the user and return a True/False + good answer of False
        '''
        raise NotImplementedError


class SequencePutBack(BaseMemoryObject):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._position < self._length:
            ret = self._components[self._position:self._position + self._stride]
        else:
            raise StopIteration()
        self._position = self._position + self._stride
        return ret

    def test_evaluation(self, myiterable):
        match_seq = []
        dif_seq = []
        for ref, proposed in zip(self._components, myiterable):
            if ref == proposed:
                match_seq.append(ref)
                dif_seq.append('_')
            else:
                match_seq.append('_')
                dif_seq.append(proposed)
        return ''.join(match_seq), ''.join(dif_seq)


class IntegerSequence(SequencePutBack):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._length = kwargs.get('length', 10)
        self._stride = kwargs.get('stride', 4)
        self._components = self.iterable_builder()

    def iterable_builder(self):
        temp = np.random.randint(0, 10, self._length)
        return ''.join([str(el) for el in temp])

    def store_in_db(self):
        pass


class BinarySequence(SequencePutBack):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._length = kwargs.get('length', 10)
        self._stride = kwargs.get('stride', 4)
        self._components = self.iterable_builder()

    def iterable_builder(self):
        temp = np.random.randint(0, 2, self._length)
        return ''.join([str(el) for el in temp])

    def store_in_db(self):
        pass


class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):
        self._cards[position] = value

    def __delitem__(self, position):
        del self._cards[position]

    def insert(self, position, value):
        self._cards.insert(position, value)
